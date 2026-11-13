"""Reproduce the manuscript's IC figures from its frozen website snapshot.

Run from any directory: python3 anc/make_figures.py
Dependencies: matplotlib and numpy. No network access is used.
"""
from pathlib import Path
import collections
import json
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, LogFormatterMathtext, MaxNLocator
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT/'anc/survey_snapshot.json').read_text())
ic = [r for r in data['records'] if r['category']=='ICs' and r.get('chartEligible') is True]
years = [r['year'] for r in ic if isinstance(r.get('year'),(int,float))]
first, last = int(min(years)), int(max(years))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.labelsize':9,
    'axes.titlesize':10,'axes.edgecolor':'#b7bec7','axes.linewidth':0.6,
    'xtick.labelsize':8,'ytick.labelsize':8,'pdf.fonttype':42,'ps.fonttype':42,
    'text.color':'#18171c','axes.labelcolor':'#18171c','savefig.facecolor':'white'})
BLUE='#0056b3'; RED='#c52214'; BLACK='#18171c'
def style(ax):
    ax.spines[['top','right']].set_visible(False)
    ax.set_xlim(first-0.6,last+0.6)
    ax.set_xticks([2006,2010,2015,2020,2026])
    ax.tick_params(length=3,color='#b7bec7')

fig,ax=plt.subplots(figsize=(7.0,1.85))
counts=collections.Counter(years)
xs=np.arange(first,last+1)
bars=ax.bar(xs,[counts[y] for y in xs],width=.72,color=BLUE,zorder=2)
for b in bars:
    if b.get_height():ax.text(b.get_x()+b.get_width()/2,b.get_height()+.2,str(int(b.get_height())),ha='center',va='bottom',fontsize=7)
ax.set_ylim(0,max(counts.values())+2.0)
ax.set_yticks([0,5,10,15]);ax.set_ylabel('IC publications')
ax.set_xlabel('Publication year',labelpad=3)
ax.grid(axis='y',color='#e5e9ee',lw=.6,zorder=0)
style(ax)
fig.subplots_adjust(left=.075,right=.99,top=.96,bottom=.25)
fig.savefig(ROOT/'figures/ic_publications.pdf')
fig.savefig(ROOT/'figures/ic_publications.png',dpi=200)
plt.close(fig)

fig,axs=plt.subplots(3,1,figsize=(7.0,7.5))
for ax,(key,label,color) in zip(axs,[('S','(a) Transmitter (TX)',RED),('T','(b) Receiver (RX)',BLUE),('U','(c) Combined transmitter and receiver (TX + RX)',BLACK)]):
    pts=[(r['year'],p[key],r['id']) for r in ic if isinstance(r.get('year'),(int,float))
         for p in r.get('points',[]) if isinstance(p.get(key),(int,float)) and math.isfinite(p[key]) and p[key]>0]
    vals=[p[1] for p in pts]
    ax.set_yscale('log')
    ax.set_ylim(10**math.floor(math.log10(min(vals))),10**math.ceil(math.log10(max(vals))))
    ax.yaxis.set_major_locator(LogLocator(base=10,numticks=10))
    ax.yaxis.set_major_formatter(LogFormatterMathtext())
    ax.minorticks_off()
    ax.grid(axis='y',which='major',color='#e5e9ee',lw=.6,zorder=0)
    ax.scatter([p[0] for p in pts],vals,s=26,color=color,alpha=.83,edgecolors='white',linewidths=.55,zorder=3)
    ax.set_title(label,loc='left',fontweight='bold',pad=10,color=color)
    ax.text(1,1.06,f'{len(pts)} points / {len({p[2] for p in pts})} publications',ha='right',va='bottom',fontsize=8,transform=ax.transAxes)
    ax.set_ylabel('Energy (pJ/bit)')
    style(ax)
    ax.set_xlabel('Publication year',labelpad=2)
fig.subplots_adjust(left=.09,right=.99,top=.955,bottom=.05,hspace=.55)
fig.savefig(ROOT/'figures/ic_energy.pdf')
fig.savefig(ROOT/'figures/ic_energy.png',dpi=200)
plt.close(fig)
print('Generated IC publication and energy figures from',len(ic),'IC records.')
