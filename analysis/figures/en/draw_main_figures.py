from pathlib import Path
import os,json,statistics
import numpy as np
from decimal import Decimal
DATA=Path(__file__).resolve().parent
O=OUT=W=Path(os.environ['BMCP_FIGURE_OUT']);O.mkdir(exist_ok=True,parents=True)
os.environ['MPLCONFIGDIR']=str(DATA/'mplcache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
from matplotlib.colors import LinearSegmentedColormap,Normalize
BLUE=BLACK='#000000'
groups=[('I','I: small'),('II_medium','II: medium'),('II_large','II: large')]
A=json.loads((DATA/'analysis.json').read_text(encoding='utf-8'))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(1,3,figsize=(7.2,3.5),sharex=True,sharey=True)
for ax,c,(g,label),color in zip(axes,A['attainment'],groups,['#009E73','#D55E00','#0072B2']):
    tt=c['times'];ax.step([.003]+tt+[180],[0]+list(np.arange(1,301)/3)+[100],where='post',color=color,lw=1.8)
    for cut in [1,5,10,30,60]:
        y=sum(t<=cut for t in tt)/3;ax.plot(cut,y,'o',ms=3.2,color=color)
    ax.set_xscale('log');ax.set_xlim(.003,180);ax.set_ylim(-2,107);ax.set_xticks([.01,1,100]);ax.set_xticklabels(['.01','1','100']);ax.grid(alpha=.16);ax.set_title(label,color=BLUE,fontsize=10);ax.set_xlabel('Search time (s)',color=BLUE,fontsize=8)
    ax.text(.04,.10,f'Last hit: {max(tt):.3g} s',transform=ax.transAxes,fontsize=8,color=BLUE)
axes[0].set_ylabel('Runs attaining R (%)',color=BLUE,fontsize=9)
fig.subplots_adjust(top=.88,bottom=.19,left=.09,right=.99,wspace=.10)
fig.savefig(O/'fig_attainment.pdf',bbox_inches='tight');fig.savefig(W/'fig_attainment.png',dpi=160,bbox_inches='tight');plt.close(fig)
D=json.loads((DATA/'ablation.json').read_text(encoding='utf-8'))
variants=['base','no_local_search','no_tabu_filter','no_swaps','positive_moves_only','restart_best_only','restart_empty_only']
labels=['Baseline','No local search','No tabu filter','No exchanges','Strict improvements only','Perturbed incumbent only','Empty restart only'];loss=np.zeros((7,6));hits=np.zeros((7,6),int)
for j,c in enumerate(D['cases']):
    base=statistics.mean(r['profit'] for r in c['runs'] if r['variant']=='base')
    for i,v in enumerate(variants):
        rr=[r for r in c['runs'] if r['variant']==v];assert len(rr)==10
        loss[i,j]=100*(base-statistics.mean(r['profit'] for r in rr))/c['target'];hits[i,j]=sum(r['target_hit'] for r in rr)
fig,ax=plt.subplots(figsize=(7.2,4.5));fig.subplots_adjust(left=.27,right=.86,top=.92,bottom=.13)
cmap=LinearSegmentedColormap.from_list('loss',['white','#FFD8AA','#D96812','#713508']);im=ax.imshow(loss,aspect='auto',cmap=cmap,norm=Normalize(0,.075))
for i in range(7):
    for j in range(6):
        ax.text(j,i-.12,f'{hits[i,j]}/10',ha='center',va='center',fontsize=8.5,color='white' if loss[i,j]>.045 else 'black',fontweight='bold' if i==0 else 'normal')
        ax.text(j,i+.22,'0%' if not loss[i,j] else f'{loss[i,j]:.3g}%',ha='center',va='center',fontsize=6.9,color='white' if loss[i,j]>.045 else BLUE)
ax.set_yticks(range(7));ax.set_yticklabels(labels,fontsize=8);ax.set_xticks(range(6));ax.set_xticklabels(['D1','D2','D3','D4','D5','D6']);ax.tick_params(length=0)
ax.set_xticks(np.arange(-.5,6,1),minor=True);ax.set_yticks(np.arange(-.5,7,1),minor=True);ax.grid(which='minor',color='#D8D8D8',lw=.5)
cax=fig.add_axes([.89,.13,.025,.79]);cb=fig.colorbar(im,cax=cax);cb.set_label('Mean loss (%)',fontsize=8);cb.ax.tick_params(labelsize=7)
fig.savefig(O/'fig_component_quality.pdf',bbox_inches='tight');fig.savefig(W/'fig_component_quality.png',dpi=160,bbox_inches='tight');plt.close(fig)
OUT=O;BLUE=BLACK
fig,ax=plt.subplots(figsize=(7.2,5.5));ax.set_xlim(0,10.6);ax.set_ylim(.35,6.2);ax.axis('off')
def box(x,y,w,h,text,face='#F4F8FD',size=9,bold=False):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.07,rounding_size=.08',facecolor=face,edgecolor=BLUE,lw=1.05))
    ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=size,color=BLUE,fontweight='bold' if bold else 'normal',linespacing=1.3)
def arrow(a,b,style='-',rad=0):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=11,color=BLUE,lw=1.0,linestyle=style,connectionstyle=f'arc3,rad={rad}'))
box(.15,5.4,2.75,.62,'Prepare data and GPU\nInitialize states',size=9)
box(3.7,5.4,3.2,.62,'Host control\nLaunch search batch',size=9)
arrow((2.97,5.71),(3.62,5.71))
ax.add_patch(FancyBboxPatch((.65,1.67),9.1,3.3,boxstyle='round,pad=.08',facecolor='#F9FBFE',edgecolor=BLUE,lw=1.2))
ax.text(.85,4.82,'GPU: B independent blocks; one trajectory per block',fontweight='bold',fontsize=9,color=BLUE)
box(.95,3.64,2.1,.64,'Current selection\nBest selection\nPhase and hash',size=8.3)
box(3.57,3.57,5.66,.82,'',size=9)
ax.text(4.98,3.98,'Construction\nAdd feasible item\nRandomized score',ha='center',va='center',fontsize=8.8,color=BLUE)
ax.text(7.84,3.98,'Tabu phase\nAdditions, removals\nand exchanges',ha='center',va='center',fontsize=8.3,color=BLUE)
ax.plot([6.40,6.40],[3.66,4.30],color=BLUE,lw=.7,ls=':')
ax.text(6.40,4.55,'Choose by phase',ha='center',fontsize=8,color=BLUE)
arrow((3.13,3.98),(3.49,3.98))
box(3.57,2.31,5.66,.72,'Threads cooperate to evaluate exact gains\nSelect move and update coverage,\nmemory, incumbent, and stagnation',size=8.5)
arrow((4.74,3.53),(4.74,3.11));arrow((7.94,3.53),(7.94,3.11))
box(.95,2.31,2.10,.72,'Empty restart\nor perturbation of\nown incumbent',size=8.3)
arrow((3.49,2.66),(3.13,2.66));ax.text(3.30,3.13,'Stagnation\nor no admissible move',ha='center',fontsize=7.3,color=BLUE)
arrow((2.0,3.11),(2.0,3.56))
arrow((9.29,2.64),(9.29,4.44),rad=.2);arrow((9.29,4.44),(9.05,4.44))

arrow((5.3,5.32),(5.3,5.04))
box(3.50,.72,3.63,.60,'Synchronize summaries\nObserve and record\nbest solution across blocks',size=8.2)
arrow((5.3,1.60),(5.3,1.40))
box(7.72,.72,2.48,.60,'Budget reached\nCertify and return\nbest solution',size=8.3)
arrow((7.20,1.02),(7.64,1.02))
arrow((3.42,1.03),(.33,1.03));arrow((.33,1.03),(.33,5.12));arrow((.33,5.12),(3.48,5.12));arrow((3.48,5.12),(3.70,5.4))
ax.text(.43,.47,'Time remains:\nnext batch',fontsize=8,color=BLUE)
fig.savefig(OUT/'fig_algorithm_overview.pdf',bbox_inches='tight');fig.savefig(W/'fig_algorithm_overview.png',dpi=170,bbox_inches='tight');plt.close(fig)
print('Figures generated; no solver runs.')


