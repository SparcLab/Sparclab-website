"""Regenerate the compact catalogue and data exports from the frozen snapshot.
Run: python3 anc/make_catalogue.py (Python standard library only).
"""
from pathlib import Path
import collections
import csv
import hashlib
import json
import math
import re
import shutil

PROJECT = Path(__file__).resolve().parent.parent
PROJECT.mkdir(parents=True, exist_ok=True)
(PROJECT / 'anc').mkdir(exist_ok=True)
(PROJECT / 'figures').mkdir(exist_ok=True)
source = PROJECT / 'anc/survey_snapshot.json'
data = json.loads(source.read_text())
records = data['records']

def tex(value):
    special = {'&':r'\&', '%':r'\%', '$':r'\$', '#':r'\#', '_':r'\_', '{':r'\{', '}':r'\}', '~':r'\textasciitilde{}', '\\':r'\textbackslash{}', '^':r'\textasciicircum{}', 'µ':r'\ensuremath{\mu}', 'μ':r'\ensuremath{\mu}', '²':r'\textsuperscript{2}', '×':r'\ensuremath{\times}', '−':'-', '‐':'-', '–':'--', '’':"'", '“':'``', '”':"''", 'İ':r'\.{I}'}
    return ''.join(special.get(c,c) for c in re.sub(r'\s+', ' ', str(value)).strip())

def authors(value):
    value = re.sub(r'\s+', ' ', value).strip()
    pieces = re.split(r';|,|\s+and\s+|\s*&\s*', value)
    return [a.strip() for a in pieces if a.strip() and a.strip() != '*']

def short_author(value):
    a = authors(value)
    if not a:
        return 'Author not recorded'
    # Affiliation markers were inherited in a few legacy author strings.
    first = re.sub(r'[\d*]+$', '', a[0]).strip()
    return tex(first) + (r' \emph{et al.}' if len(a)>1 else '')

ordered = []
cat_names = [('ICs','Integrated circuits'), ('Channels & models','Channels and models'), ('Other literature','Other literature')]
for category, heading in cat_names:
    group = sorted([r for r in records if r['category']==category], key=lambda r: (-(r.get('year') or 0), r['id']))
    ordered.extend(group)

# The printed catalogue deliberately uses compact author and venue strings.
# The full stored strings remain in both machine-readable exports.
out = [r'% Generated from anc/survey_snapshot.json. Do not edit entries by hand.']
for category, heading in cat_names:
    group = [r for r in ordered if r['category']==category]
    out += ([r'\clearpage'] if category=='ICs' else [r'\vspace{6pt}'])
    out += [r'\section{' + heading + ' (' + str(len(group)) + ' records)}', r'\label{cat:' + ('ic' if category=='ICs' else 'channel' if category.startswith('Channels') else 'other') + '}',
            r'\begin{multicols}{2}', r'\cataloguefont']
    for r in group:
        doi = r.get('doi','').strip()
        link = 'https://doi.org/' + doi if doi else r.get('source','').strip()
        title = tex(r['title'])
        if link:
            title = r'\href{' + tex(link) + '}{' + title + '}'
        year = str(r['year']) if r.get('year') else 'year not recorded'
        venue = tex(r.get('venue') or r.get('venueFull') or 'venue not recorded')
        src = r'DOI: \href{' + tex(link) + r'}{\nolinkurl{' + doi + '}}' if doi else (r'\href{' + tex(link) + '}{source}' if link else 'link not recorded')
        author = short_author(r.get('authors',''))
        punctuation = ' ' if author.endswith(r'\emph{et al.}') else '. '
        line = r'\entry{' + r['id'].split('-')[-1] + '}{' + r['id'] + '}{' + title + '}{' + author + punctuation + venue + ', ' + year + '. ' + src + '.}'
        out.append(line)
    out.append(r'\end{multicols}')
(PROJECT/'catalogue.tex').write_text('\n'.join(out)+'\n')

fields = ['id','year','category','chartEligible','mode','title','authors','venue','venueFull','doi','source','notes']
with (PROJECT/'anc/catalogue.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader()
    for r in ordered:w.writerow({k:r.get(k,'') for k in fields})

# All retained citations are exported. The entries retain archive metadata and
# do not imply an independent publisher audit. Braced titles preserve units.
bib=[]
for r in ordered:
    fields={'title':'{'+tex(r['title'])+'}', 'author':' and '.join(tex(a) for a in authors(r.get('authors',''))), 'year':str(r['year']) if r.get('year') else '', 'howpublished':tex(r.get('venueFull') or r.get('venue') or ''), 'doi':r.get('doi',''), 'url':'https://doi.org/'+r['doi'] if r.get('doi') else r.get('source',''), 'note':'Catalogue ID: '+r['id'].split('-')[-1]+'. Collection: '+tex(r['category'])+'. Archive snapshot: 2026-11-13.'}
    bib.append('@misc{'+r['id']+',\n'+',\n'.join('  '+k+' = {'+v+'}' for k,v in fields.items() if v)+'\n}')
(PROJECT/'catalogue.bib').write_text('\n\n'.join(bib)+'\n')

plot=[]
for r in ordered:
    if r['category']!='ICs' or r.get('chartEligible') is not True: continue
    if not isinstance(r.get('year'),(float,int)): continue
    for i,p in enumerate(r.get('points',[]),1):
        for k,scope in [('S','TX'),('T','RX'),('U','TX+RX')]:
            if isinstance(p.get(k),(float,int)) and math.isfinite(p[k]) and p[k]>0:
                plot.append({'id':r['id'],'year':r['year'],'operating_point':i,'scope':scope,'energy_pJ_per_bit':p[k],'mode':r.get('mode',''),'doi':r.get('doi',''),'notes':r.get('notes','')})
with (PROJECT/'anc/energy_points.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(plot[0]),lineterminator="\n");w.writeheader();w.writerows(plot)
stats={'snapshot':data['updated'],'records':len(records),'categories':dict(collections.Counter(r['category'] for r in records)), 'energy':{s:{'points':sum(p['scope']==s for p in plot),'publications':len({p['id'] for p in plot if p['scope']==s})} for s in ['TX','RX','TX+RX']}, 'snapshot_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
(PROJECT/'anc/statistics.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(stats,indent=2))
