"""Optimize a coarse legal P1 field against a finer complete physical bank.

The full-width common-threshold interpolation is linear in its nodal values.
Every fine-node coefficient is retained as an integer over 2*refinement.
Only the floating LP discovers candidates; final fine-field pricing is exact.
"""
from __future__ import annotations
import numpy as np
from scipy.sparse import coo_matrix

from solve_normalized import Master


class InterpolatedMaster(Master):
    def __init__(self,n,profile_grid,directory,denominator=10**8):
        if n%profile_grid or profile_grid<1 or profile_grid>=n:
            raise ValueError('fine grid must be a strictly larger integer refinement')
        self.profile_grid=profile_grid
        self.refinement=n//profile_grid
        self.interpolation_denominator=2*self.refinement
        self.coarse=Master(profile_grid,directory,denominator,True)
        self.n,self.R,self.C,self.H=n,2*n,4*n,12*n
        self.D=denominator*self.interpolation_denominator
        self.directory=directory;self.normalized_profile=True
        self.nodes=self.coarse.nodes;self.index=self.coarse.index;self.K=self.coarse.K
        self.order=self.coarse.order;self.order_matrix=self.coarse.order_matrix
        self.profile_horizon=self.coarse.profile_horizon
        self.binary=directory/'pricing.input.bin';self.executable=self.coarse.executable
        self.columns=[];self.seen=set()
        rr=[];cc=[];vv=[];W=self.interpolation_denominator
        def coordinate(numerator):
            cell,alpha=divmod(numerator,W)
            plus=cell%(2*profile_grid)<profile_grid
            return cell,alpha,plus,alpha if plus else W-alpha
        for j in range(self.C+1):
            for k in range(1,self.R+1):
                if (j+k)%2:continue
                row=j*n+(k-1)//2
                u=coordinate(j+k);w=coordinate(j-k)
                cuts=sorted({0,W,u[3],w[3]});weights={}
                for left,right in zip(cuts,cuts[1:]):
                    if left==right:continue
                    twice_z=left+right
                    def rounded(c):
                        cell,a,plus,_=c
                        return cell+int(a>0 and (twice_z<2*a if plus else twice_z>2*(W-a)))
                    U,V=rounded(u),rounded(w);time,radius=U+V,U-V
                    if radius<0 or time<0:raise AssertionError('illegal common threshold image')
                    if radius==0:continue
                    i=self.coarse.variable(time,radius)
                    if i is not None:weights[i]=weights.get(i,0)+right-left
                if sum(weights.values())>W:raise AssertionError('invalid interpolation weights')
                for i,a in weights.items():rr.append(row);cc.append(i);vv.append(a)
        self.interpolation=coo_matrix((np.asarray(vv,dtype=np.int64),(rr,cc)),
                                      shape=((self.C+1)*n,self.K)).tocsr()
        self.interpolation.sum_duplicates()

    def repair(self,values):
        coarse=self.coarse.repair(values)
        vector=np.asarray([int(coarse[j,k]) for j,k in self.nodes],dtype=np.int64)
        pre=self.interpolation@vector
        assert np.min(pre)>=0 and np.max(pre)<=self.D
        table=np.zeros((self.H+1,self.R+1),dtype=np.uint64)
        for j in range(self.C+1):
            first=2 if j%2==0 else 1
            table[j,first::2]=pre[j*self.n:(j+1)*self.n]
        for j in range(self.C+1,self.C+self.R+1):
            for k in range(1,self.R+1):
                if (j+k)%2==0 and k>j-self.C:
                    table[j,k]=table[self.C,k-j+self.C]
        return table

    def profile_values(self,table):
        ratio=self.refinement
        return np.asarray([int(table[j*ratio,k*ratio])/self.D for j,k in self.nodes])

    def interpolate_seed(self,seed):
        return self.coarse.interpolate_seed(seed)

    def _coefficients(self,plan):
        positions=[plan['start_grid']]
        for step in plan['moves']:positions.append(positions[-1]+step)
        total=0;coeff={};A=self.interpolation
        for name,sign in [('minus_charges',1),('plus_charges',-1)]:
            for j,a in plan[name]:
                total+=a;position=sign*positions[j]
                if position==0:continue
                k=abs(position);time=min(j,self.C);foot=k-max(0,j-self.C)
                if foot<=0:continue
                row=time*self.n+(foot-1)//2
                for at in range(A.indptr[row],A.indptr[row+1]):
                    i=int(A.indices[at]);v=int(A.data[at])*a*(1 if position>0 else -1)
                    coeff[i]=coeff.get(i,0)+v
        return total,{i:v/self.interpolation_denominator for i,v in coeff.items() if v}

    def calendar(self,path,table,latest=False):
        positions=[path['start_grid']]
        for step in path['moves']:
            assert step in (-1,1)
            positions.append(positions[-1]+step)
        assert all(abs(k)<=self.R for k in positions)
        assert 0 in positions[:self.C+1] and -self.R in positions and self.R in positions
        plan={'start_grid':positions[0],'moves':path['moves']}
        for name,sign,endpoint in [('minus_charges',1,-self.R),('plus_charges',-1,self.R)]:
            counts={};minimum=2*self.D+1;when=None
            for j in range(positions.index(endpoint)):
                k=sign*positions[j]
                value=self.D+(1 if k>=0 else -1)*int(table[j,abs(k)])
                if value<minimum or latest and value==minimum:minimum,when=value,j
                counts[when]=counts.get(when,0)+1
            plan[name]=list(map(list,sorted(counts.items())))
        mass,coeff=self._coefficients(plan)
        return plan,mass,coeff

    def add_plan(self,plan):
        mass,coeff=self._coefficients(plan);key=mass,tuple(sorted(coeff.items()))
        if key in self.seen:return False
        self.seen.add(key);self.columns.append({'plan':plan,'mass':mass,'coeff':coeff})
        return True
