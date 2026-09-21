"""Independently verify the 90 published witnesses against original instances."""
from pathlib import Path
import argparse,json,hashlib
from certificate import independent_certificate
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--instances',type=Path,default=R/'data/instances');a=p.parse_args()
rows=[]
for f in sorted((R/'solutions').glob('*.json')):
    s=json.loads(f.read_text());path=a.instances/(s['instance']+'.txt')
    assert hashlib.sha256(path.read_bytes()).hexdigest()==s['instance_sha256'],s['instance']
    c=independent_certificate(path,s['selected_items_0based'])
    assert c['feasible'] and all(c[k]==s[k] for k in ['profit','cost','capacity','selected_count','covered_elements']),s['instance']
    assert s['selected_items_1based']==[i+1 for i in s['selected_items_0based']]
    rows.append(dict(instance=s['instance'],**c))
assert len(rows)==90
out=R/'runs';out.mkdir(exist_ok=True)
(out/'solution_audit.json').write_text(json.dumps(rows,indent=2)+'\n')
print('90/90 feasible witnesses independently verified; objectives and costs match.')
