"""Rebuild the work/time and CPU/GPU figures from archived observations; no searches."""
from pathlib import Path
import json, math, os
ROOT=Path(__file__).resolve().parent
OUT=Path(os.environ['BMCP_FIGURE_OUT']);OUT.mkdir(parents=True,exist_ok=True)
os.environ['MPLCONFIGDIR']=str(OUT/'mplcache')
METHODS=('base','outgoing_2')
LABELS={'base':'Original (K = 4)','outgoing_2':'K = 2'}
COLORS={'base':'#0072B2','outgoing_2':'#D55E00'}
MARKERS={'base':'o','outgoing_2':'s'}
FIGURE='fig_work_time'
def draw(data, output):
    os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'work/bmcp_experiments/mplconfig_focused_a'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.ticker import LogLocator, NullFormatter, FuncFormatter
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10.5, 'axes.titlesize': 11,
        'axes.labelsize': 10.5, 'xtick.labelsize': 9.8, 'ytick.labelsize': 10,
        'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none', 'axes.spines.top': False,
        'axes.spines.right': False})
    fig, axs = plt.subplots(2, 3, figsize=(9.6, 6.7), sharey=True)
    fig.subplots_adjust(left=.085, right=.985, top=.785, bottom=.155, hspace=.52, wspace=.24)
    fig.suptitle('Does reducing K preserve attainment per step and per second?', x=.52, y=.976, fontsize=14, weight='bold')
    fig.text(.52, .925, '10 paired runs per method · n = 10 at each point · Fixed own targets', ha='center', fontsize=10.2)
    handles = [Line2D([0], [0], color=COLORS[m], marker=MARKERS[m], markerfacecolor='white' if m == 'base' else COLORS[m],
        markersize=6, linewidth=1.8, linestyle='-' if m == 'base' else '--', label=LABELS[m]) for m in METHODS]
    fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(.52, .90), frameon=False, ncol=2, columnspacing=3)
    for col, case in enumerate(data['cases']):
        top, bottom = axs[:, col]
        top.set_title(f"{case['display_title']}\nTarget {case['target']:,} · H = {case['horizon_seconds']} s", pad=10)
        for method in METHODS:
            grid = case['plotted_checkpoints']
            top.scatter([g['step'] for g in grid], [g['methods'][method]['hit_fraction'] for g in grid],
                s=48 if method == 'base' else 22, marker=MARKERS[method],
                edgecolors=COLORS[method], facecolors='white' if method == 'base' else COLORS[method], linewidths=1.3,
                zorder=3 if method == 'base' else 4)
            events = sorted(case['observed_target_times'][method], key=lambda t: (t['observed_seconds'], t['seed']))
            event_times = [r['observed_seconds'] for r in events]
            fractions = [(i + 1) / 10 for i in range(10)]
            bottom.plot(event_times, fractions, drawstyle='steps-post', color=COLORS[method],
                        linestyle='-' if method == 'base' else '--', linewidth=1.65, zorder=2)
            bottom.scatter(event_times, fractions, marker=MARKERS[method], s=25,
                           facecolors='white' if method == 'base' else COLORS[method], edgecolors=COLORS[method],
                           linewidths=1.0, zorder=4)
        top.set_xscale('log', base=2)
        max_step = case['display_stops_at_first_all_hit_checkpoint']
        top.set_xlim(.75, max_step * 1.32)
        exponent = int(math.log2(max_step))
        ticks = sorted({2 ** round(exponent * k / 3) for k in range(4)})
        top.set_xticks(ticks, [f'{x:,}' for x in ticks])
        top.xaxis.set_minor_formatter(NullFormatter())
        top.set_xlabel('Steps per trajectory (log scale)', fontsize=8.4)
        all_times = [r['observed_seconds'] for m in METHODS for r in case['observed_target_times'][m]]
        lo, hi = min(all_times) / 1.3, max(all_times) * 1.25
        bottom.set_xscale('log'); bottom.set_xlim(lo, hi)
        # Extend the empirical CDF outside its extrema, without inventing new
        # objective observations or additional experimental replicates.
        for method in METHODS:
            ts = sorted(r['observed_seconds'] for r in case['observed_target_times'][method])
            style = '-' if method == 'base' else '--'
            bottom.plot([lo, ts[0]], [0, 0], color=COLORS[method], linestyle=style, linewidth=1.65)
            bottom.plot([ts[0], ts[0]], [0, .1], color=COLORS[method], linestyle=style, linewidth=1.65)
            bottom.plot([ts[-1], hi], [1, 1], color=COLORS[method], linestyle=style, linewidth=1.65)
        visible_ticks = ([2, 5, 10, 20, 50], [.02, .1, 1, 10], [.005, .01, .02, .05, .1, .2])[col]
        visible_ticks = [x for x in visible_ticks if lo <= x <= hi]
        bottom.set_xticks(visible_ticks, [f'{x:g}' for x in visible_ticks])
        bottom.xaxis.set_minor_formatter(NullFormatter())
        bottom.set_xlabel('Time to target (s; log scale)', fontsize=8.4)
        for ax in (top, bottom):
            ax.set_ylim(-.045, 1.08)
            ax.set_yticks([0, .5, 1], ['0/10', '5/10', '10/10'])
            ax.grid(axis='y', color='#DDDDDD', linewidth=.65)
            ax.set_axisbelow(True)
    axs[0, 0].set_ylabel('At equal work\nCumulative hits')
    axs[1, 0].set_ylabel('By observed time\nCumulative hits')
    fig.text(.52, .074, 'Top: exact nominal work checkpoints. Bottom: empirical distribution of batch-observed times.', ha='center', fontsize=9.4)
    fig.text(.52, .04, 'Axes differ by case. Both methods finish at 10/10; subsecond differences require cautious interpretation.', ha='center', fontsize=9.3)
    for ext in ('png', 'pdf', 'svg'):
        fig.savefig(output / f'{FIGURE}.{ext}', dpi=240, facecolor='white', bbox_inches='tight')
    plt.close(fig)


def draw_platform():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    data=json.loads((ROOT/'platform_analysis.json').read_text(encoding='utf-8'))
    observations=json.loads((ROOT/'platform_observations.json').read_text(encoding='utf-8'))
    assert len(observations)==90
    rows=[dict(instance_uid=r['instance_uid'],platform=r['platform'],seed=r['seed'],
               common_work=dict(first_observed_seconds=r['seconds'],hit=True)) for r in observations]
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':10,'axes.labelsize':9,
        'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
    fig, axes=plt.subplots(1,3,figsize=(10.8,4.4))
    fig.subplots_adjust(left=.12,right=.99,top=.75,bottom=.27,wspace=.22)
    colors=['#0072B2','#D55E00','#009E73']
    plotted=[]
    for ax,c,color,letter in zip(axes,data['cases'],colors,'abc'):
        ref=c['reference']; uid=ref['instance_uid']
        for plat,y in [('cpu1',2),('cpu20',1),('gpu',0)]:
            group=sorted([r for r in rows if r['instance_uid']==uid and r['platform']==plat],key=lambda r:r['seed'])
            assert len(group)==10
            x=[r['common_work']['first_observed_seconds'] for r in group]
            assert all(r['common_work']['hit'] for r in group)
            yy=[y+(.34*(i/9-.5)) for i in range(10)]
            ax.scatter(x,yy,s=19,color=color,edgecolors='white',linewidths=.25,zorder=3)
            mean=sum(x)/10
            ax.scatter([mean],[y],s=34,color='#202020',marker='D',zorder=4)
            ax.text(mean,y+.25,f'{mean:.3g} s',ha='center',va='bottom',fontsize=8.6)
            plotted.extend(dict(instance_uid=uid,platform=plat,seed=r['seed'],seconds=v,display_y=off) for r,v,off in zip(group,x,yy))
        ax.set_xscale('log');ax.set_xlim(.06,200);ax.set_ylim(-.45,2.65)
        ax.set_xticks([.1,1,10,100],['0.1','1','10','100'])
        ax.set_yticks([2,1,0],['CPU · 1 thread','CPU · 20 threads','GPU'] if letter=='a' else ['','',''])
        ax.tick_params(axis='y',length=0,labelsize=8.4)
        ax.grid(axis='x',which='major',color='#d9d9d9',lw=.7)
        ax.grid(axis='y',color='#ededed',lw=.5)
        ax.set_axisbelow(True)
        ax.set_xlabel('Search time (s; log scale)')
        size=ref['name'].replace('bmcp_','')
        ax.set_title(f'({letter}) {size}\n{c["work_steps"]} steps/trajectory · H = {ref["seconds"]} s',pad=14)
        p={p['cpu_platform']:p['speedup']['mean'] for p in c['pairs']}
        ax.text(.5,-.30,f'Mean paired CPU/GPU ratio\n1 thread: {p["cpu1"]:.3g}×   |   20 threads: {p["cpu20"]:.3g}×',transform=ax.transAxes,ha='center',va='top',fontsize=8.5)
    fig.suptitle('Time to complete fixed work: Original on all platforms',x=.5,y=.985,fontsize=12)
    legend=[Line2D([],[],marker='o',color='none',markerfacecolor='#777777',markeredgecolor='white',markersize=5,label='Individual run (10 per platform)'),
            Line2D([],[],marker='D',color='none',markerfacecolor='#202020',markeredgecolor='#202020',markersize=5,label='Arithmetic mean')]
    fig.legend(handles=legend,loc='upper center',bbox_to_anchor=(.53,.943),ncol=2,frameon=False,fontsize=8.5)
    fig.text(.53,.025,'128 trajectories · batch = 1 · 90 runs · all checkpoints attained · includes observation and synchronization',ha='center',fontsize=8)
    stem='fig_cpu_gpu'
    for ext in ('png','pdf','svg'):
        fig.savefig(OUT/f'{stem}.{ext}',dpi=200 if ext=='png' else None,facecolor='white')
    plt.close(fig)

def main():
    data=json.loads((ROOT/'focused_metrics.json').read_text(encoding='utf-8'))
    for case in data['cases']:
        for a,b in [('Large','Large'),('Medium','Medium'),('Small','Small')]:
            case['display_title']=case['display_title'].replace(a,b)
    draw(data,OUT)
    draw_platform()
    print('Reconstructed fig_work_time and fig_cpu_gpu in',OUT)
if __name__=='__main__':main()
