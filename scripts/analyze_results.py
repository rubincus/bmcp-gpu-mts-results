from pathlib import Path
import json, math, statistics, hashlib
import numpy as np
from scipy.stats import friedmanchisquare, rankdata
R=Path(__file__).resolve().parents[1]; W=R/'runs/analysis'; W.mkdir(parents=True,exist_ok=True)
old=json.loads((R/'data/comparison/previous_comparison.json').read_text(encoding='utf-8'))
raw=[json.loads(l) for l in (R/'data/historical/results.jsonl').read_text().splitlines()]
rows=old['rows']; assert len(rows)==90
alg=['plts','vdls','ihs','anrma','gpu']; groups=['I','II_medium','II_large']
for r in rows:
    rr=[z for z in raw if z['instance'].replace('.txt','').replace(chr(92),'/').split('/')[-1]==r['name']]
    assert len(rr)==10 and len({z['seed'] for z in rr})==10
    assert all(z['feasible'] and z['instance_sha256']==r['sha256'] for z in rr)
    values=[z['profit'] for z in rr]
    assert min(values)==max(values)==r['gpu_best']
    r.update(gpu_mean=statistics.mean(values),gpu_sd=statistics.stdev(values),gpu_tavg=statistics.mean(z['time_to_best_seconds'] for z in rr),gpu_tstd=statistics.stdev(z['time_to_best_seconds'] for z in rr))
    r['reference_old']=r['reference_best']
    r['reference_best']=max(r['reference_old'],r['gpu_best'])

def holm(values):
    answer=[0.]*len(values);prev=0.
    for j,k in enumerate(sorted(range(len(values)),key=lambda k:values[k])):
        prev=max(prev,min(1.,(len(values)-j)*values[k]));answer[k]=prev
    return answer
stats=[];rng=np.random.default_rng(20260920)
for a in alg[:-1]:
    diff=np.array([100*(r['gpu_mean']-r[a+'_mean'])/r['reference_best'] for r in rows]);nz=diff[diff!=0];n=len(nz)
    assert all(nz>0)
    boot=diff[rng.integers(0,len(rows),(20000,len(rows)))].mean(axis=1)
    stats.append(dict(algorithm=a,wins=int(sum(diff>0)),ties=int(sum(diff==0)),losses=int(sum(diff<0)),n_nonzero=n,sign_p=2.**(1-n) if n else 1.,wilcoxon_exact_sign_randomization_p=2.**(1-n) if n else 1.,mean_advantage_pp=float(diff.mean()),ci95=np.quantile(boot,[.025,.975]).tolist(),rank_biserial_nonzero=1. if n else None))
for s,p in zip(stats,holm([s['sign_p'] for s in stats])):s['holm_p']=p
fried=[]
for g in ['all']+groups:
    rr=rows if g=='all' else [r for r in rows if r['cohort']==g]
    a=np.array([[r[k+'_mean'] for k in alg] for r in rr]);res=friedmanchisquare(*a.T)
    ranks=np.array([rankdata(-v,method='average') for v in a]).mean(axis=0)
    fried.append(dict(group=g,n=len(rr),statistic=float(res.statistic),p=float(res.pvalue),ranks=dict(zip(alg,ranks.tolist()))))
for f,p in zip(fried,holm([f['p'] for f in fried])):f['holm_p_4_omnibus']=p
summary=[]
for g in groups:
    rr=[r for r in rows if r['cohort']==g]
    for a in alg:
        gaps=[100*(r['reference_best']-r[a+'_mean'])/r['reference_best'] for r in rr]
        summary.append(dict(group=g,algorithm=a,mean_gap_pct=statistics.mean(gaps),best_wins_gpu=sum(r['gpu_best']>r[a+'_best'] for r in rr),mean_wins_gpu=sum(r['gpu_mean']>r[a+'_mean'] for r in rr)))
byname={r['name']:r for r in rows};curves=[];early=[]
for g in groups:
    runs=[r for r in raw if byname[r['instance'].replace('.txt','').replace('\\','/').split('/')[-1]]['cohort']==g];assert len(runs)==300
    times=[r['time_to_best_seconds'] for r in runs]
    curves.append(dict(group=g,n=300,times=sorted(times),mean=statistics.mean(times),median=statistics.median(times),max=max(times)))
    for sec in [1,5,10,30,60,90]:
        values={};gaps=[];hits=0
        for r in runs:
            name=r['instance'].replace('.txt','').replace('\\','/').split('/')[-1];ref=byname[name]['reference_best']
            value=max([0]+[t['profit'] for t in r['trace'] if t['seconds']<=min(sec,r['seconds'])])
            hits+=value>=ref;gaps.append(100*(ref-value)/ref);values.setdefault(name,[]).append(value)
        early.append(dict(group=g,seconds=sec,hits=hits,n=300,mean_gap_pct=statistics.mean(gaps),instances_with_nonzero_sd=sum(len(set(v))>1 for v in values.values())))
out=dict(rows=rows,algorithms=alg,group_summary=summary,tests=stats,friedman=fried,attainment=curves,early=early,
    source_note='900 archived GPU runs; published PLTS, VDLS, IHS and ANRMA values from Wei et al. (2026), Tables C.1-C.2, doi:10.1016/j.swevo.2026.102289; competitor run-level records unavailable.',bootstrap=dict(seed=20260920,samples=20000,unit='instance',scope='descriptive individual confidence intervals'))
(W/'analysis.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'instances':len(rows),'runs':len(raw),'improved_published_BKV':sum(r['gpu_best']>r['reference_old'] for r in rows),'output':str(W/'analysis.json')},indent=2))
