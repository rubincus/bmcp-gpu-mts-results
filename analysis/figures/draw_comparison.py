"""Rebuild the five-method comparison with Wei et al. (2026); archived solver runs are not modified."""
from pathlib import Path
import json, statistics, os
from decimal import Decimal
import numpy as np
from scipy.stats import friedmanchisquare, rankdata

HERE=Path(__file__).resolve().parent
OUT=Path(os.environ.get('BMCP_FIGURE_OUT',str(HERE.parent)))
os.environ['MPLCONFIGDIR']=str(HERE/'mplcache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
A=json.loads((HERE/'analysis.json').read_text(encoding='utf-8'))
rows=A['rows'];alg=['plts','vdls','ihs','anrma','gpu']
names=dict(zip(alg,['PLTS','VDLS','IHS','ANRMA','GPU-MTS']))
groups=[('I','I: pequeñas'),('II_medium','II: medianas'),('II_large','II: grandes')]

def holm(values):
    result=[0.]*len(values);previous=0.
    for j,k in enumerate(sorted(range(len(values)),key=lambda k:values[k])):
        previous=max(previous,min(1.,(len(values)-j)*values[k]));result[k]=previous
    return result

for s,p in zip(A['tests'],holm([s['sign_p'] for s in A['tests']])):s['holm_p']=p
fried=[]
for g in ['all']+[g for g,_ in groups]:
    rr=rows if g=='all' else [r for r in rows if r['cohort']==g]
    a=np.array([[r[k+'_mean'] for k in alg] for r in rr])
    res=friedmanchisquare(*a.T)
    ranks=np.array([rankdata(-v,method='average') for v in a]).mean(axis=0)
    fried.append(dict(group=g,n=len(rr),statistic=float(res.statistic),p=float(res.pvalue),ranks=dict(zip(alg,ranks.tolist()))))
for f,p in zip(fried,holm([f['p'] for f in fried])):f['holm_p_4_omnibus']=p
A['friedman']=fried
A['comparison_scope']=dict(source='Wei et al. (2026), Tables C.1-C.2, doi:10.1016/j.swevo.2026.102289',methods=alg,posthoc_family_size=4,reference_definition='R=max(BKV, GPU best)',claim_scope='improvements over the values reported by Wei et al. (2026)')
(OUT/'comparison_analysis.json').write_text(json.dumps(A,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def w(name,s):(OUT/name).write_text(s,encoding='utf-8')
def esc(s):return s.replace('_',r'\_')
def blue(s):return str(s)
def row(v):return ' & '.join(map(str,v))+r'\\'+'\n'
def num(x):return format(Decimal(f'{x:.2e}'),'f') if x else '0'
def sci(x):return num(x)
def pval(x):return '$<0.001$' if x<.001 else num(x)
def table(name,caption,label,columns,header,data,note=''):
    s=r'\begin{table}[tbp]\centering\small'+'\n'
    s+=r'\caption{'+caption+'}\n'+r'\label{'+label+'}\n'+r'\begin{tabular}{'+columns+'}\n'+r'\toprule'+'\n'+row(header)+r'\midrule'+'\n'
    s+=''.join(row(v) for v in data)+r'\bottomrule\end{tabular}'+'\n'
    if note:s+=r'\par\smallskip\parbox{.97\linewidth}{\footnotesize '+note+'}\n'
    w(name,s+r'\end{table}'+'\n')

table('table_cohorts.tex','Cobertura del banco y balance respecto de los valores bibliográficos. Diez corridas por instancia; best = media = peor y desviación final nula.','tab:cohort-results','lrrrr',
      ['Grupo','Instancias','$H_i$: 180/90 s',r'Mejora/empate $\mathrm{BKV}_i$',r'$\mathrm{std}(f)$'],
      [[label,30,'0/30' if g=='I' else '26/4' if g=='II_medium' else '30/0','4/26' if g=='II_large' else '0/30',0] for g,label in groups])
im=[r for r in rows if r['gpu_best']>r['reference_old']]
assert len(im)==4 and sum(r['gpu_best']==r['reference_old'] for r in rows)==86
table('table_improvements.tex',r'Cuatro mejoras respecto de los valores reportados por Wei et al.~\cite{Wei2026ANRMA}. Best y Media corresponden a GPU-MTS, que obtiene cada valor en 10/10 ejecuciones. Tiempo es la media de alcance en segundos.','tab:reference-improvements','lrrrrr',
      ['Instancia','BKV','Best','Media','Ganancia','Tiempo (s)'],
      [[esc(r['name'][5:]),r['reference_old'],r'\textbf{'+str(r['gpu_best'])+'}',r'\textbf{'+str(int(r['gpu_mean']))+'}',r['gpu_best']-r['reference_old'],num(r['gpu_tavg'])] for r in im])
for c,g,label in [('small','I','pequeñas (conjunto I)'),('medium','II_medium','medianas (conjunto II)'),('large','II_large','grandes (conjunto II)')]:
    rr=[r for r in rows if r['cohort']==g];data=[]
    means={a:{k:statistics.mean(r[a+'_'+k] for r in rr) for k in ['best','mean']} for a in alg}
    maxima={k:max(means[a][k] for a in alg) for k in ['best','mean']}
    for a in alg:
        def gep(k):
            d=[r['gpu_'+k]-r[a+'_'+k] for r in rr]
            return '/'.join(str(sum(f(x) for x in d)) for f in [lambda x:x>0,lambda x:x==0,lambda x:x<0])
        gap=statistics.mean(100*(r['reference_best']-r[a+'_mean'])/r['reference_best'] for r in rr)
        summary=[]
        for k in ['best','mean']:
            v=f'{means[a][k]:.2f}'
            if means[a][k]==maxima[k]:v=r'\textbf{'+v+'}'
            summary.append(v)
        data.append([names[a]]+summary+[gep('best') if a!='gpu' else '--',gep('mean') if a!='gpu' else '--',sci(gap) if gap else '0'])
    table(f'table_benchmark_{c}.tex',f'Calidad en las {len(rr)} instancias {label}. Promedios aritméticos de los mejores valores (Best) y de las medias por instancia (Media). Negrita: mayor promedio de cada métrica, incluidos empates.',f'tab:benchmark-{c}','lrrrrr',
          ['Método','Best','Media','Best: G/E/P','Media: G/E/P',r'Brecha (\%)'],data,
          r'G/E/P cuenta victorias, empates y pérdidas de GPU-MTS frente a cada método. La brecha media utiliza $R_i=\max\{\mathrm{BKV}_i,f^{\mathrm{best}}_{i,\rm GPU}\}$; BKV identifica el valor bibliográfico de Wei et al.~\cite{Wei2026ANRMA}.')
table('table_friedman.tex','Rangos medios de calidad (menor es mejor). Cinco métodos; Friedman con empates y Holm sobre los cuatro contrastes ómnibus.','tab:friedman','lrrrrrrr',
      ['Grupo']+[names[a] for a in alg]+['$Q$',r'$p_{\rm H}$'],
      [[dict(all='Todas',I='I',II_medium='II medianas',II_large='II grandes')[f['group']]]+[f'{f["ranks"][a]:.2f}' for a in alg]+[f'{f["statistic"]:.1f}',pval(f['holm_p_4_omnibus'])] for f in fried], 'Los valores p inferiores a 0.001 se muestran mediante ese umbral; el archivo de análisis conserva la precisión completa.')
table('table_statistical.tex',r'Comparaciones de media por instancia frente a GPU-MTS. Ventaja normalizada en puntos porcentuales; intervalo bootstrap descriptivo del 95\%. Signos bilateral y Holm para cuatro comparaciones.','tab:statistical','lrrrr',
      ['Método','G/E/P','Efecto medio',r'Intervalo 95\%',r'$p_{\rm H}$'],
      [[names[s['algorithm']],f'{s["wins"]}/{s["ties"]}/{s["losses"]}',sci(s['mean_advantage_pp']),f'[{sci(s["ci95"][0])}, {sci(s["ci95"][1])}]',pval(s['holm_p'])] for s in A['tests']], 'Los valores p inferiores a 0.001 se muestran mediante ese umbral; el archivo de análisis conserva la precisión completa.')
data=[];timing_summary=[]
for g,group_name in groups:
    rr=[r for r in rows if r['cohort']==g]
    comparison_alg=['plts','ihs','anrma','gpu'] if g=='I' else ['anrma','gpu']
    for a in comparison_alg:
        if a in ('plts','ihs'):
            tt=statistics.mean(r['original_c1_timing'][a+'_tavg'] for r in rr)
            sd=statistics.mean(r['original_c1_timing'][a+'_sd'] for r in rr)
        else:
            tt=statistics.mean(r[a+'_tavg'] for r in rr)
            sd=statistics.mean(r[a+'_sd'] for r in rr)
        budget=('90' if g=='I' else '90/180' if g=='II_medium' else '180') if a=='gpu' else ('600' if g=='I' else '1800')
        n=10 if a=='gpu' else 30
        data.append([group_name,names[a],n,budget,num(sd),num(tt)])
        timing_summary.append(dict(group=g,algorithm=a,instances=30,runs_per_instance=n,budget_seconds_display=budget,mean_objective_std=sd,mean_time_seconds=tt))
table('table_literature_timing.tex',r'Contexto temporal por grupo. Tiempo es el promedio de los 30 tiempos medios por instancia hasta el resultado final de cada método; $\mathrm{std}(f)$ corresponde a calidad. Equipos y protocolos distintos.','tab:literature-timing','llrrrr',
      ['Grupo','Método','$n$','Límite (s)',r'Media de $\mathrm{std}(f)$','Tiempo (s)'],data,
      r'GPU-MTS: cuatro medianas con 90 s y 26 con 180 s. Su reloj incluye búsqueda y observación, y excluye preparación. Los datos bibliográficos proceden de Wei y Hao~\cite{Wei2023IHS} (PLTS e IHS en pequeñas) y Wei et al.~\cite{Wei2026ANRMA} (ANRMA).')
A['timing_summary_by_group']=timing_summary
(OUT/'comparison_analysis.json').write_text(json.dumps(A,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

out=r'''\begin{landscape}
\setlength{\LTcapwidth}{\linewidth}
\section{Comparación completa por instancia}
\label{app:full-results}
{BKV y los resultados bibliográficos proceden de Wei et al.~\cite{Wei2026ANRMA}. Best es el mejor valor y Media el promedio por instancia; en GPU-MTS coinciden en sus diez ejecuciones, con $\mathrm{std}(f)=0$. La negrita identifica el mayor Best y la mayor Media, incluidos empates. Promedio resume las 30 instancias del grupo.}
'''
display_alg=['gpu','plts','vdls','ihs','anrma']
for group,caption,lab in [('I','I: 30 pequeñas','tab:full-c1'),('II_medium','II: 30 medianas','tab:full-c2'),('II_large','II: 30 grandes','tab:full-c2-large')]:
    rr=sorted([r for r in rows if r['cohort']==group],key=lambda r:tuple(float(x) for x in r['name'][5:].split('_')))
    header=row(['Instancia',blue('BKV')]+[r'\multicolumn{2}{c}{'+names[a]+'}' for a in display_alg])+row(['','',blue('Best'),blue('Media')]+['Best','Media']*4)
    out+=r'\begingroup\footnotesize\setlength{\tabcolsep}{2.5pt}\renewcommand{\arraystretch}{.88}'+'\n'+r'\begin{longtable}{lrrrrrrrrrrr}'+'\n'+r'\caption{{Calidad del conjunto '+caption+r'. Best y Media por método; negrita para los mejores resultados.}}\label{'+lab+r'}\\'+'\n'+r'\toprule'+'\n'+header+r'\midrule\endfirsthead'+'\n'+header+r'\midrule\endhead'+'\n'+r'\bottomrule\endlastfoot'+'\n'
    for r in rr:
        maxima={k:max(r[a+'_'+k] for a in display_alg) for k in ['best','mean']}
        values=[esc(r['name'][5:]),str(r['reference_old'])]
        for a in display_alg:
            for k in ['best','mean']:
                v=str(int(r[a+'_'+k]))
                if r[a+'_'+k]==maxima[k]:v=blue(r'\textbf{'+v+'}')
                elif a=='gpu':v=blue(v)
                values.append(v)
        out+=row(values)
    avgs={a:{k:statistics.mean(r[a+'_'+k] for r in rr) for k in ['best','mean']} for a in display_alg}
    maxima={k:max(avgs[a][k] for a in display_alg) for k in ['best','mean']}
    values=[blue('Promedio'),blue(f'{statistics.mean(r["reference_old"] for r in rr):.2f}')]
    for a in display_alg:
        for k in ['best','mean']:
            v=f'{avgs[a][k]:.2f}'
            if avgs[a][k]==maxima[k]:v=r'\textbf{'+v+'}'
            values.append(blue(v))
    out+=r'\midrule'+'\n'+row(values)
    out+=r'\end{longtable}\endgroup\clearpage'+'\n'
out+=r'''\section{{Comparación temporal por instancia}}
\label{app:full-times}
{Los datos bibliográficos proceden de Wei y Hao~\cite{Wei2023IHS} (PLTS e IHS) y Wei et al.~\cite{Wei2026ANRMA} (ANRMA). VDLS no aporta tiempos comparables. GPU-MTS utiliza diez ejecuciones por instancia. Los tiempos se redondean a tres cifras significativas. Promedio resume los 30 valores de cada columna; promediar desviaciones no equivale a calcular una desviación conjunta.}

'''
for group,caption in groups:
    rr=sorted([r for r in rows if r['cohort']==group],key=lambda r:tuple(float(x) for x in r['name'][5:].split('_')))
    aa=['plts','ihs','anrma'] if group=='I' else ['anrma'];ncols=1+2*len(aa)+3
    header=row(['Instancia']+[r'\multicolumn{2}{c}{'+names[a]+'}' for a in aa]+[r'\multicolumn{3}{c}{GPU-MTS}'])+row(['']+[r'$\mathrm{std}(f)$','Tiempo (s)']*len(aa)+['$H_i$ (s)','Tiempo (s)',r'$\mathrm{std}(t)$ (s)'])
    out+=r'\footnotesize\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{.88}'+'\n'+r'\begin{longtable}{l'+'r'*(ncols-1)+'}\n'+r'\caption{Dispersión y tiempos: '+caption+r'. Tiempo: media al resultado final; $\mathrm{std}(f)$ y $\mathrm{std}(t)$: desviaciones estándar de objetivo y tiempo; $H_i$: presupuesto (s). GPU-MTS: $\mathrm{std}(f)=0$, $n=10$.}\\'+'\n'+r'\toprule'+'\n'+header+r'\midrule\endfirsthead'+'\n'+header+r'\midrule\endhead'+'\n'+r'\bottomrule\endlastfoot'+'\n'
    for r in rr:
        v=[esc(r['name'][5:])]
        for a in aa:
            if a in ('plts','ihs'):v += [num(r['original_c1_timing'][a+'_sd']),num(r['original_c1_timing'][a+'_tavg'])]
            else:v += [num(r[a+'_sd']),num(r[a+'_tavg'])]
        out+=row(v+[int(r['budget']),num(r['gpu_tavg']),num(r['gpu_tstd'])])
    v=['Promedio']
    for a in aa:
        if a in ('plts','ihs'):
            v += [num(statistics.mean(r['original_c1_timing'][a+'_sd'] for r in rr)),num(statistics.mean(r['original_c1_timing'][a+'_tavg'] for r in rr))]
        else:v += [num(statistics.mean(r[a+'_sd'] for r in rr)),num(statistics.mean(r[a+'_tavg'] for r in rr))]
    v += ['--',num(statistics.mean(r['gpu_tavg'] for r in rr)),num(statistics.mean(r['gpu_tstd'] for r in rr))]
    out+=r'\midrule'+'\n'+row(v)
    out+=r'\end{longtable}\clearpage'+'\n'
out+=r'\end{landscape}'+'\n';w('appendix_results.tex',out)

BLUE='#000000'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(1,3,figsize=(7.2,4.6),sharey=True)
for ax,(g,title) in zip(axes,groups):
    rr=sorted([r for r in rows if r['cohort']==g],key=lambda r:r['name']);vals=[]
    for i,a in enumerate(alg):
        vals.append([100*(r['reference_best']-r[a+'_mean'])/r['reference_best'] for r in rr])
        jitter=np.random.default_rng(19+i).uniform(-.18,.18,30)
        ax.scatter(vals[-1],i+1+jitter,s=13,c=BLUE if a=='gpu' else '#546A7B',alpha=.75,zorder=3,linewidths=.2,edgecolor='white')
    ax.boxplot(vals,vert=False,positions=range(1,6),widths=.5,patch_artist=True,showfliers=False,medianprops={'color':'#172B3A'},boxprops={'facecolor':'#EAF0F5','edgecolor':'#526C89'})
    ax.set_xscale('symlog',linthresh=.01,linscale=.9);ax.set_xlim(-.0015,12);ax.set_xticks([0,.01,.1,1,10]);ax.set_xticklabels(['0','.01','.1','1','10'],fontsize=8)
    ax.axvline(0,color='#888888',lw=.7,ls=':');ax.grid(axis='x',alpha=.18);ax.set_title(title+'\n30 instancias',fontsize=10)
    ax.set_xlabel('Brecha al mejor del banco (%)',color=BLUE,fontsize=8)
    ax.set_yticks(range(1,6));ax.set_yticklabels([names[a] for a in alg]);ax.set_ylim(5.6,.4)
fig.suptitle('¿Cómo se compara la calidad con los métodos de referencia?',fontsize=11,color=BLUE,x=.06,ha='left')
fig.text(.06,.90,'R = máximo entre referencia bibliográfica y mejor resultado de GPU-MTS.',fontsize=8.5,color=BLUE)
fig.subplots_adjust(top=.79,bottom=.18,left=.085,right=.99,wspace=.15)
fig.savefig(OUT/'fig_benchmark_gaps.pdf',bbox_inches='tight')
fig.savefig(HERE/'fig_benchmark_gaps.png',dpi=170,bbox_inches='tight');plt.close(fig)
print(json.dumps({'improvements_over_published_reference':len(im),'ties':86,'friedman':fried,'holm':[s['holm_p'] for s in A['tests']]},indent=2))
