from shape_search import *
from plateau import plateau

def op(a,b,u,s,e=1e-6):
 if a==1:return [[0.,1.]]
 a=max(a,2*e);u=max(a,u-e);b=min((u+a)/2,max(b,e));s=max(u-b,s-e)
 return clean([[0,a],[(u-a)/2,(u+a)/2],[u-b,b],[s,b],[s+1-b,1]])
if __name__=='__main__':
 n=int(sys.argv[1]);st=time.time();hn=[('end',1,1,1,0)];hs=[[[0,1]]]
 for ia in range(n):
  for iu in range(ia,n+1):
   for ib in range((iu+ia)//2+1):
    for is_ in range(iu-ib,n+1):
     a,b,u,s=ia/n,ib/n,iu/n,is_/n
     hn.append(('out',a,b,u,s));hs.append(op(a,b,u,s))
  for ib in range(ia+1):
   for iu in range(ia,n+1):
    for is_ in range(iu-ib,n+1):
     a,b,u,s=ia/n,ib/n,iu/n,is_/n
     hn.append(('wait',a,b,u,s));hs.append(plateau(a,b,u,s))
 mn=[];ms=[]
 for ix in range(-n,n+1):
  for ic in range(ix,2*n-ix+1):
   mn.append((ix/n,ic/n));ms.append(monster(ix/n,ic/n))
 hp,nh=packed(hs);mp,nm=packed(ms);print('MATRIX',len(hs),len(ms),'GB',len(hs)*len(ms)*8/1e9,flush=True)
 A=payoffs(hp,nh,mp,nm);rows=[0];cols=list(range(0,len(ms),max(1,len(ms)//100)))
 for it in range(500):
  v,w,q=solve(A[np.ix_(rows,cols)]);hr=A[:,cols]@w;mr=q@A[rows,:];U=hr.max();L=mr.min()
  print('ITER',it,len(rows),len(cols),v,L,U,'secs',time.time()-st,flush=True)
  if U-L<1e-8:break
  nr=np.argsort(hr)[-min(50,np.count_nonzero(hr>v+1e-8)): ] if np.any(hr>v+1e-8) else []
  nc=np.argsort(mr)[:min(50,np.count_nonzero(mr<v-1e-8))] if np.any(mr<v-1e-8) else []
  rows+=list(set(map(int,nr))-set(rows));cols+=list(set(map(int,nc))-set(cols))
 hw=np.zeros(len(hs));mw=np.zeros(len(ms));hw[rows]=q;mw[cols]=w
 hi=np.where(hw>1e-9)[0];mi=np.where(mw>1e-9)[0]
 D=dict(n=n,value=v,paths_h=[hs[i] for i in hi],names_h=[hn[i] for i in hi],weights_h=hw[hi].tolist(),paths_m=[ms[i] for i in mi],names_m=[mn[i] for i in mi],weights_m=mw[mi].tolist())
 json.dump(D,open('out_plateau_%d.json'%n,'w'));print('ACTIVE H',[(hn[i],float(hw[i]))for i in hi]);print('ACTIVE M',[(mn[i],float(mw[i]))for i in mi]);print('DONE',time.time()-st,flush=True)
