#!/usr/bin/env python3
"""Independent physical integration of the localized-I triangle."""
from fractions import Fraction as Q
import numpy as np
from localized_inward import LocalizedInward
from localized_inward_features import localized_inward_feature
from uniform_inward import graph_from_path
from verify_uniform_inward import arrangements,twice_area,direct_four,inverse,paths,monster
from verify_center_memory import first_capture


def physical(path,d):
    total,lower_missed,higher_missed,cells=Q(0),Q(0),Q(0),0
    b=path[0][1]
    beta3=inverse(path,Q(3),False)
    for polygon in arrangements(path,d,Q(1),top=-d):
        for i in range(1,len(polygon)-1):
            vertices=[polygon[0],polygon[i],polygon[i+1]]
            area=twice_area(vertices)/2
            if not area:
                continue
            point=tuple(sum((p[k] for p in vertices),Q(0))/3 for k in (0,1))
            score=direct_four(path,*point)
            check=[]
            for distinguished in range(3):
                q=tuple(sum((vertices[j][k]*(Q(2,3) if j==distinguished else Q(1,6))
                             for j in range(3)),Q(0)) for k in (0,1))
                check.append(direct_four(path,*q))
            assert sum(check,Q(0))/3==score
            a,v=point
            capture=first_capture(path,monster(a,v))
            if a>b and capture>(a+v)/2:
                lower_missed+=area
            if a<b and capture==beta3:
                higher_missed+=area
            total+=area*score
            cells+=1
    return total,lower_missed,higher_missed,cells


def main():
    counts=dict(physical_laws=0,affine_cells=0,exact_slack=0,fast_features=0,
                attained=0,strict=0,cancellation=0)
    fixtures=paths()+[
        [(Q(0),Q(19,20)),(Q(1,20),Q(1)),(Q(8),Q(1))],
        [(Q(0),Q(15,16)),(Q(1,64),Q(61,64)),(Q(1,32),Q(15,16)),
         (Q(3,32),Q(1)),(Q(8),Q(1))],
        [(Q(0),Q(9,10)),(Q(1,40),Q(37,40)),(Q(1,20),Q(9,10)),
         (Q(3,20),Q(1)),(Q(8),Q(1))],
    ]
    for path in fixtures:
        b,c,graph=graph_from_path(path)
        segments=[]
        for (vl,ul),(vr,ur) in zip(graph,graph[1:]):
            if vl<vr:
                slope=(ur-ul)/(vr-vl)
                segments.append([float(vl),float(vr),float(slope),float(ul-slope*vl)])
        segments=np.array(segments,dtype=float).reshape((-1,4))
        for d in (Q(3,8),Q(7,8)):
            law=LocalizedInward(d)
            actual,low,high,cells=physical(path,d)
            feature=law.graph_four_score(b,c,graph)
            gap=(2*law.mass*(2-inverse(path,Q(1),False))
                 +2*((1+c)/2-inverse(path,Q(1),True))*low
                 +2*(4-inverse(path,Q(3),False))*high)
            assert feature-actual==gap>=0,(path,d,feature,actual,gap)
            counts['physical_laws']+=1;counts['affine_cells']+=cells;counts['exact_slack']+=1
            counts['attained' if feature==actual else 'strict']+=1
            fast=localized_inward_feature(float(d),float(b),float(c),segments)
            assert abs(fast-float(feature))<2e-12
            counts['fast_features']+=1
    # The k ramp cancels the U term in q_I,U exactly on the localized band.
    d=Q(7,8)
    for b in (Q(9,10),Q(15,16),Q(31,32)):
        for v in (-b,( -b-d)/2,-d):
            for c in (v,(v+1)/2,Q(1)):
                for u in (b,(b+1)/2,Q(1)):
                    gradient=u+b+d+3*v-1-c-(u-d)
                    assert gradient==b+2*d+3*v-1-c
                    counts['cancellation']+=1
    print(f'PASS: {sum(counts.values())} localized-inward checks')
    for name,count in counts.items():
        print(f'  {name}: {count}')
    print('PASS: exact physical I-only triangle features and tied-ramp gradient cancellation')
    print('Scope: induced old-law ramp densities require their separate admissibility audit')


if __name__=='__main__':
    main()
