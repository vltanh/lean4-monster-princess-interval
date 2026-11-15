from symbolic import *
import subprocess, pathlib
ROOT=pathlib.Path(__file__).resolve().parent

def monster(hs,ws,limit=2_000_000,ordered=False):
    lines=[f'{len(hs)} {limit} {S}']
    for p,w in zip(hs,ws):
        lines.append(f'{len(p)} {w:.18g}')
        for t,x in p:
            for z in (t,x):lines.append(str(len(z.c))+' '+' '.join(str(a) for a in z.c))
    inp='\n'.join(lines)+'\n';out=subprocess.run([str(ROOT/('ordered_monster' if ordered else 'poly_monster'))],input=inp,text=True,capture_output=True,check=True).stdout.splitlines()
    value,nodes,leaves,prunes,done,npath=out[0].split();it=iter(out[1:]);p=[]
    def read(line):
        a=list(map(int,line.split()));assert len(a)==a[0]+1;return P(coeff=tuple(a[1:]))
    for k in range(int(npath)):p.append((read(next(it)),read(next(it))))
    p=simplify(p);caps=[meet(p,h) for h in hs];assert all(t is not None for t in caps)
    value2=sum(w*float(t) for w,t in zip(ws,caps));assert abs(value2-float(value))<1e-7,(value,value2)
    return dict(value=value2,path=p,nodes=int(nodes),leaves=int(leaves),complete=bool(int(done)))

def matrix(hs,ms):
    lines=[f'{len(hs)} {len(ms)} {S}']
    for p in hs+ms:
        lines.append(str(len(p)))
        for t,x in p:
            for z in(t,x):lines.append(str(len(z.c))+' '+' '.join(map(str,z.c)))
    out=subprocess.run([str(ROOT/'poly_matrix')],input='\n'.join(lines)+'\n',text=True,capture_output=True,check=True).stdout
    return np.fromstring(out,sep=' ').reshape(len(hs),len(ms))
