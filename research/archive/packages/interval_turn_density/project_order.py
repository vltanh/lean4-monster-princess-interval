"""Exact projection of the event-grid order onto priced threshold nodes.

For nodes (i,k), (i,k) implies (j,l) precisely when i<=j and k>=l.
The skyline graph is a transitive reduction sufficient for the induced poset;
it does not quantize controls or change a payoff coefficient.
"""
import json,random,argparse

def skyline(rows,label_count):
    last_row=[-1]*label_count;last_node=[-1]*label_count;edges=[]
    for i,points in enumerate(rows):
        for k,node in sorted(points,reverse=True):
            record=-1
            for l in range(k,label_count):
                r=last_row[l]
                if r>record:
                    edges.append((last_node[l],node));record=r
                    if r==i:break
            last_row[k]=i;last_node[k]=node
    return edges

def verify():
    rng=random.Random(7731);checks=0
    for _ in range(120):
        nr=rng.randrange(2,13);nl=rng.randrange(2,18)
        points=[(i,k) for i in range(nr) for k in range(nl) if rng.random()<.27]
        rows=[[] for _ in range(nr)]
        for j,(i,k) in enumerate(points):rows[i].append((k,j))
        edges=skyline(rows,nl);adj=[[] for _ in points]
        for u,v in edges:adj[u].append(v)
        for a,(i,k) in enumerate(points):
            seen={a};todo=[a]
            while todo:
                u=todo.pop()
                for v in adj[u]:
                    if v not in seen:seen.add(v);todo.append(v)
            for b,(j,l) in enumerate(points):
                assert (b in seen)==(i<=j and k>=l),(i,k,j,l,edges)
                checks+=1
    return checks

def project(m):
    used=sorted({b for d in m['defs'] for b in d['bits']});new={b:i for i,b in enumerate(used)}
    rows=[]
    for i,(lo,hi) in enumerate(m['bounds']):
        rows.append([(k,new[m['offset'][i]+k-lo-1]) for k in range(lo+1,hi+1)
                     if m['offset'][i]+k-lo-1 in new])
    hard=skyline(rows,3*len(m['base']))
    defs=[{'pos':d['pos'],'bits':[new[b] for b in d['bits']]} for d in m['defs']]
    return {'scope':'Exact dominance-order projection; no payoff or control discretization.',
            'N':len(used),'defs':defs,'units':m['units'],'threshold_hard':hard,
            'projection':{'original_N':m['N'],'old_nodes':used,'row_thresholds':rows}}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',default='full_model.json');p.add_argument('--output',default='projected_model.json')
    p.add_argument('--verify-only',action='store_true')
    a=p.parse_args();checks=verify()
    if a.verify_only:
        print({'exact_order_checks':checks,'status':'PASS'});raise SystemExit
    m=json.load(open(a.input));out=project(m)
    json.dump(out,open(a.output,'w'))
    print({'exact_order_checks':checks,'old_thresholds':m['N'],'priced_thresholds':out['N'],
           'projected_order_edges':len(out['threshold_hard']),'reward_definitions':len(out['defs'])})
