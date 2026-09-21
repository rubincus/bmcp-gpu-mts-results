from pathlib import Path
import hashlib, re

def independent_certificate(path,selected):
    """Stream original text and union selected rows using Python sets, no GPU state."""
    path=Path(path); selected=list(selected)
    if len(set(selected))!=len(selected) or any(type(i) is not int for i in selected): raise ValueError('Selection IDs')
    chosen=set(selected); mode='header'; costs=[]; profits=[]; covered=set(); matrix_tokens=0
    h=None
    with path.open(encoding='utf-8-sig') as f:
        for line in f:
            line=line.strip()
            if not line: continue
            if mode=='header':
                h=re.fullmatch(r'm\s*=\s*(\d+)\s+n\s*=\s*(\d+)\s+knapsack\s+size\s*=\s*(\d+)',line,re.I)
                if not h: raise ValueError('Certificate header')
                m,n,cap=map(int,h.groups()); mode='cost_header'; continue
            if line.lower().startswith('the weight'): mode='cost'; continue
            if line.lower().startswith('the profit'): mode='profit'; continue
            if line.lower().startswith('relation'): mode='matrix'; continue
            if mode=='cost': costs.extend(map(int,line.split()))
            elif mode=='profit': profits.extend(map(int,line.split()))
            elif mode=='matrix':
                # The VDLS files put the ENTIRE matrix on one line. Accept arbitrary
                # line breaks while mapping positions to (item, element) independently.
                vals=line.split()
                if any(v not in ('0','1') for v in vals): raise ValueError('Certificate matrix token')
                for i in chosen:
                    lo=max(i*n,matrix_tokens);hi=min((i+1)*n,matrix_tokens+len(vals))
                    covered.update(pos-i*n for pos in range(lo,hi) if vals[pos-matrix_tokens]=='1')
                matrix_tokens+=len(vals)
            else: raise ValueError('Certificate section')
    if h is None or len(costs)!=m or len(profits)!=n or matrix_tokens!=m*n or any(i<0 or i>=m for i in chosen): raise ValueError('Certificate shape')
    cost=sum(costs[i] for i in chosen); profit=sum(profits[e] for e in covered)
    return dict(profit=profit,cost=cost,capacity=cap,feasible=cost<=cap,selected_count=len(chosen),
                covered_elements=len(covered),selection_sha256=hashlib.sha256(','.join(map(str,sorted(chosen))).encode()).hexdigest())
