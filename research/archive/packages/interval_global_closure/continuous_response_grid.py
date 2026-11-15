#!/usr/bin/env python3
"""Discover unrestricted-turn physical grid routes against a complete CDF.

Unlike finite-quantile probes, every edge is priced against the continuous
law. Floating record interpolation only guides the search. Exact rational
rescoring of the returned legal routes supplies attack costs, not a lower
certificate for all continuous monsters.
"""
from __future__ import annotations
import argparse
from bisect import bisect_left,bisect_right
from fractions import Fraction as Q
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import subprocess
import time

from continuum_field import ExtendedExactField
from continuous_response_cost import route_payoff,hinge_area


def ceilq(q):return -((-q.numerator)//q.denominator)


def compress(route):
    result=[]
    for t,x in route:
        if result and t==result[-1][0]:
            assert x==result[-1][1];continue
        result.append((t,x))
        while len(result)>=3:
            (a,x),(b,y),(c,z)=result[-3:]
            if (y-x)*(c-b)!=(z-y)*(b-a):break
            result.pop(-2)
    return result


def completed_route(route):
    """Stop at the second distinct wall: continuity forces full capture."""
    route=compress(route);walls=set()
    for i,(t,x)in enumerate(route):
        if abs(x)==1:walls.add(x)
        if len(walls)==2:return route[:i+1]
    raise AssertionError('Endpoint completion did not visit both walls')


def route_counts(route):
    previous=None;turns=0;waits=0
    for(t,x),(s,y)in zip(route,route[1:]):
        direction=(y-x)/(s-t)
        if direction==0:waits+=1;continue
        if previous is not None and direction!=previous and abs(x)<1:turns+=1
        previous=direction
    return dict(interior_turns=turns,center_waits=waits)


class Geometry:
    def __init__(self,data,bins,center_waits=True):
        self.field=ExtendedExactField(data);self.horizon=self.field.terminal_time;self.bins=bins
        self.center_waits=center_waits;self.record_knots=None;self.edge_cache={}
        self.axis=sorted(set(x for p in self.field.nodes for x in p)|{Q(-1),Q(0),self.horizon+1})
        # Close the nonuniform coordinates under the arena and time faces.
        # This ensures that every legal row/column ends on an actual node.
        axis=set(self.axis)
        while True:
            new={y for x in axis for y in (-x,2*self.horizon-x,x-2,x+2) if -1<=y<=self.horizon+1}
            if new<=axis:break
            axis|=new
        self.axis=sorted(axis);self.nodes=[];self.index={}
        for i,u in enumerate(self.axis):
            for j,v in enumerate(self.axis):
                if not(0<=u+v<=2*self.horizon and abs(u-v)<=2):continue
                t,x=(u+v)/2,(u-v)/2;a,closed=self.field.cdf_sides(t,x);b=1-closed
                assert a>=0 and b>=0 and a+b<=1
                self.index[i,j]=len(self.nodes)
                self.nodes.append(dict(i=i,j=j,t=t,x=x,a=a,b=b,initial=t==0,terminal=t==self.horizon,
                                       na=ceilq(a*bins)+1,nb=ceilq(b*bins)+1))
        for node in self.nodes:
            i,j=node['i'],node['j'];node['right']=self.index.get((i+1,j),-1);node['up']=self.index.get((i,j+1),-1)
            node['wait']=self.index.get((i+1,j+1),-1)if center_waits and i==j else-1
            assert node['terminal']or max(node['right'],node['up'])>=0

    def set_record_knots(self,knots):
        self.record_knots=sorted(set(map(Q,knots)))
        assert self.record_knots[0]==0 and self.record_knots[-1]==1
        for node in self.nodes:
            node['na']=bisect_left(self.record_knots,node['a'])+1
            node['nb']=bisect_left(self.record_knots,node['b'])+1

    def record_grid(self,end):
        if self.record_knots is None:return [min(Q(i,self.bins),end)for i in range(ceilq(end*self.bins)+1)]
        return self.record_knots[:bisect_left(self.record_knots,end)]+[end]

    def carried_records(self,route):
        """All exact surviving records at a compressed route's vertices."""
        route=[tuple(map(Q,p))for p in route];a,closed=self.field.cdf_sides(*route[0]);b=1-closed
        records={a,b};center=[u for u,v in self.field.nodes if u==v]
        for(t,x),(s,y)in zip(route,route[1:]):
            assert s>t and(abs(y-x)==s-t or x==y==0)
            if x==y==0:
                g=min((1-self.radial(z,z))/2 for z in [t,s]+[z for z in center if t<z<s])
                a,b=min(a,g),min(b,g)
            else:
                left,right=self.field.cdf_sides(s,y);a,b=min(a,left),min(b,1-right)
            records.update((a,b))
        return records

    @lru_cache(None)
    def radial_line(self,fixed,axis):
        """Exact affine breakpoints of one complete radial coordinate line."""
        f=self.field
        if axis==1 and fixed>=f.vmax:return ()
        i=max(0,min(len(f.grid[axis])-2,bisect_right(f.grid[axis],fixed)-1))
        possible=set(f.strips[axis].get(i,[]))|set(f.strips[axis].get(i-1,[]))
        cuts=set();other=1-axis
        for number in possible:
            points=f.triangles[number][0]
            for a,b in zip(points,points[1:]+points[:1]):
                if a[axis]==b[axis]:
                    if a[axis]==fixed:cuts.update((a[other],b[other]))
                elif min(a[axis],b[axis])<=fixed<=max(a[axis],b[axis]):
                    cuts.add(a[other]+(fixed-a[axis])*(b[other]-a[other])/(b[axis]-a[axis]))
        return tuple(sorted(cuts))

    @lru_cache(None)
    def radial(self,u,v):return self.field.radial(u,v)

    @lru_cache(None)
    def payoff(self,route):return route_payoff(self.field,route)

    def edge_survival(self,node,child,right):
        """Open-leg affine survival threshold, keeping end atoms separate."""
        key=node['i'],node['j'],right
        if key in self.edge_cache:return self.edge_cache[key]
        t0,x0=node['t'],node['x'];t1,x1=child['t'],child['x']
        assert t1>t0 and abs(x1-x0)==t1-t0
        positive=x0+x1>0
        # On each nonuniform node edge the monster cannot cross the center
        # in its interior because both light-coordinate axes coincide.
        assert x0*x1>=0
        if right:
            fixed=t0-x0;left,right_coord=t0+x0,t1+x1
            axis=1 if positive else 0
        else:
            fixed=t0+x0;left,right_coord=t0-x0,t1-x1
            axis=0 if positive else 1
        knots=self.radial_line(fixed,axis)
        cuts=[left]+list(knots[bisect_right(knots,left):bisect_left(knots,right_coord)])+[right_coord]
        result=[]
        for variable in cuts:
            u,v=(fixed,variable)if axis==0 else(variable,fixed)
            r=self.radial(u,v)
            if right:g=(1-r)/2 if positive else(1+r)/2
            else:g=(1+r)/2 if positive else(1-r)/2
            result.append(((variable+fixed)/2,g))
        assert result[0][0]==t0 and result[-1][0]==t1
        assert all(a>=b for(t,a),(s,b)in zip(result,result[1:])),('edge survival monotonicity',node,child,result)
        self.edge_cache[key]=result
        return result

    def center_survival(self,node,child):
        t,s=node['t'],child['t'];assert node['x']==child['x']==0 and s>t
        g,h=(1-self.radial(t,t))/2,(1-self.radial(s,s))/2
        midpoint=(t+s)/2
        assert (1-self.radial(midpoint,midpoint))/2==(g+h)/2,'Non-affine center edge'
        return [(t,g),(s,h)]

    def costs(self,node,child,right,wait=False):
        count=node['nb'if right else'na'];end=node['b'if right else'a'];after=child['b'if right else'a']
        pieces=self.center_survival(node,child)if wait else self.edge_survival(node,child,right)
        assert pieces[0][1]>=end and pieces[-1][1]>=after
        # Only this discovery objective is floating. The geometry, atom
        # conventions and final route costs are checked with Fractions.
        segments=[(float(s-t),float(a),float(b))for(t,a),(s,b)in zip(pieces,pieces[1:])]
        result=[]
        for rank in self.record_grid(end):
            q=float(rank);integral=0.
            for duration,a,b in segments:
                fa,fb=q-a,q-b
                if fb<=0:continue
                if fa>=0:integral+=duration*(fa+fb)/2
                else:integral+=duration*fb*fb/(2*(fb-fa))
            capture=float(child['t'])*(q-min(q,float(after)))-integral
            assert capture>=-1e-10
            result.append(max(0.,capture))
        return result

    def write(self,path):
        with path.open('w')as out:
            out.write(f'{len(self.nodes)} {self.bins} {float(self.horizon):.17g} {int(self.center_waits)} {len(self.record_knots or [])}\n')
            if self.record_knots:out.write(' '.join(format(float(q),'.17g')for q in self.record_knots)+'\n')
            for n,node in enumerate(self.nodes):
                out.write(' '.join(map(str,[node['right'],node['up'],*([node['wait']]if self.center_waits else[]),
                                           *[format(float(node[k]),'.17g')for k in ('t','x','a','b')],
                                           int(node['initial']),int(node['terminal']),node['na'],node['nb']]))+'\n')
                for right,key,size in ((True,'right','nb'),(False,'up','na')):
                    values=self.costs(node,self.nodes[node[key]],right)if node[key]>=0 else[0.]*node[size]
                    out.write(' '.join(format(x,'.17g')for x in values)+'\n')
                if node['wait']>=0:
                    out.write(' '.join(format(x,'.17g')for x in self.costs(node,self.nodes[node['wait']],False,wait=True))+'\n')
                if n and n%3000==0:print('prepared',n,'nodes',flush=True)

    def rescore(self,ids):
        route=compress([(self.nodes[i]['t'],self.nodes[i]['x'])for i in ids])
        assert route[0][0]==0 and route[-1][0]==self.horizon
        choices=[];t,x=route[-1]
        # Independently accumulate the exact directional capture moments on
        # every original node edge, then compare to the complete route scorer.
        a,b=self.nodes[ids[0]]['a'],self.nodes[ids[0]]['b'];prefix=Q(0);survival_area=Q(0)
        for i,j in zip(ids,ids[1:]):
            node,child=self.nodes[i],self.nodes[j];right=j==node['right']
            wait=j==node['wait'];assert right or wait or j==node['up']
            pieces=self.center_survival(node,child)if wait else self.edge_survival(node,child,right)
            active=[(a,child['a']),(b,child['b'])]if wait else[(b,child['b'])]if right else[(a,child['a'])]
            total_hinge=Q(0)
            for q,threshold in active:
                after=min(q,threshold);integral=Q(0)
                for(s,g),(end,h)in zip(pieces,pieces[1:]):
                    integral+=hinge_area(q,g,h,end-s)
                prefix+=child['t']*(q-after)-integral;total_hinge+=integral
            survival_area+=(child['t']-node['t'])*(a+b)-total_hinge
            a,b=min(a,child['a']),min(b,child['b'])
        assert survival_area==prefix+self.horizon*(a+b),'Capture moments disagree with survival integration'
        for side in (-1,1):
            full=completed_route(route+[(t+abs(side-x),Q(side)),(t+abs(side-x)+2,Q(-side))])
            assert all(b>a and(abs(y-x)==b-a or x==y==0)for(a,x),(b,y)in zip(full,full[1:]))
            value=self.payoff(tuple(full))
            tail=(a*(t+1+x)+b*(t+3+x))if side==-1 else(a*(t+3-x)+b*(t+1-x))
            assert value==prefix+tail,('edge moment identity',value,prefix+tail)
            choices.append(dict(payoff=str(value),decimal=float(value),
                                route=[[str(t),str(x)]for t,x in full],**route_counts(full),
                                exact_edge_moment_check='pass',exact_survival_integral_check='pass'))
        return min(choices,key=lambda q:Q(q['payoff']))

    def prefix_completions(self,attack,all_routes=False):
        """Complete each discovered turning prefix by both endpoint orders.

        This checks whole legal routes rather than optimizing a chosen turn
        family. It also removes interpolation-induced excursions when a
        straightforward sweep after an earlier turn is already better.
        """
        route=[tuple(map(Q,p))for p in attack['route']];best=attack;completions=[]
        for end in range(len(route)-1):
            prefix=route[:end+1];t,x=prefix[-1]
            for side in (-1,1):
                full=completed_route(prefix+[(t+abs(side-x),Q(side)),(t+abs(side-x)+2,Q(-side))])
                value=self.payoff(tuple(full))
                candidate=dict(payoff=str(value),decimal=float(value),route=[[str(t),str(x)]for t,x in full],
                               **route_counts(full),
                               origin='Endpoint completion of a globally discovered route prefix')
                completions.append(candidate)
                if value<Q(best['payoff']):best=candidate
        if all_routes:
            unique={tuple(map(tuple,a['route'])):a for a in completions}
            return sorted(unique.values(),key=lambda a:Q(a['payoff']))
        return best


def main():
    parser=argparse.ArgumentParser();parser.add_argument('field');parser.add_argument('--bins',type=int,default=64)
    parser.add_argument('--route-count',type=int,default=8);parser.add_argument('--work',required=True)
    parser.add_argument('--unit-only',action='store_true',help='Disable exact center-wait edges')
    parser.add_argument('--adaptive-records',type=int,default=0,help='Number of optional global nonuniform record-grid rounds; zero keeps the uniform pipeline')
    parser.add_argument('--seed-attacks',action='append',default=[],help='Same-field exact report whose best routes seed carried-record knots')
    parser.add_argument('--seed-routes',action='append',default=[],help='Any-field route report; recompute its costs and carried records for the current field')
    parser.add_argument('--seed-count',type=int,default=4)
    parser.add_argument('--max-states',type=int,default=200000000,help='Memory gate for adaptive rounds, in stored double values')
    prefixes=parser.add_mutually_exclusive_group()
    prefixes.add_argument('--all-prefixes',dest='all_prefixes',action='store_true',default=True,
                          help='Return every distinct endpoint completion (default)')
    prefixes.add_argument('--best-prefix-only',dest='all_prefixes',action='store_false',
                          help='Return only the best endpoint completion per decoded route')
    parser.add_argument('--output',required=True);args=parser.parse_args();started=time.time()
    assert args.bins>=1 and args.route_count>=1
    raw=Path(args.field).read_bytes();data=json.loads(raw);work=Path(args.work);work.mkdir(parents=True,exist_ok=True)
    geometry=Geometry(data,args.bins,center_waits=not args.unit_only);inp=work/'node_input.txt'
    source_hash=hashlib.sha256(raw).hexdigest()
    seeded_attacks=[]
    if args.adaptive_records:
        knots={Q(i,args.bins)for i in range(args.bins+1)}|{n[k]for n in geometry.nodes if n['initial']for k in ('a','b')}
        for source,same_field in [(s,True)for s in args.seed_attacks]+[(s,False)for s in args.seed_routes]:
            seed=json.loads(Path(source).read_text())
            if same_field:
                if 'input_sha256'in seed:assert seed['input_sha256']==source_hash,'Record seed belongs to another field'
                knots.update(map(Q,seed.get('record_knots_exact')or[]))
                knots.update(map(Q,seed.get('pending_record_knots_exact')or seed.get('new_records_exact')or[]))
            for attack in seed['attacks'][:args.seed_count]:
                knots|=geometry.carried_records(attack['route'])
                route=tuple(tuple(map(Q,p))for p in attack['route']);value=geometry.payoff(route)
                seeded_attacks.append(dict(route=[[str(t),str(x)]for t,x in route],payoff=str(value),decimal=float(value),
                                           origin='Exactly rescored seed route',seed_report=Path(source).name,**route_counts(route)))
        geometry.set_record_knots(knots)
        if seeded_attacks:print('rescored seed minimum',min(a['decimal']for a in seeded_attacks),flush=True)
    binary=work/'node_search';here=Path(__file__).resolve().parent
    subprocess.run(['g++','-O3','-std=c++17',str(here/'continuous_response_grid.cpp'),'-o',str(binary)],check=True)
    attacks=list(seeded_attacks);history=[];reason='Uniform discovery round';result=None;executed_knots=None
    for iteration in range(max(1,args.adaptive_records)):
        states=sum(n['na']*n['nb']for n in geometry.nodes)
        if args.adaptive_records and states>args.max_states:
            reason='Adaptive state memory gate';assert result is not None,('Initial record grid exceeds memory gate',states);break
        executed_knots=None if geometry.record_knots is None else list(geometry.record_knots)
        geometry.write(inp)
        print('prepared all',len(geometry.nodes),'nodes; record knots',len(geometry.record_knots or []),
              'round',iteration,'in',time.time()-started,'seconds',flush=True)
        output=work/('node_output.json'if not args.adaptive_records else f'node_output_{iteration:02d}.json')
        subprocess.run([str(binary),str(inp),str(output),str(args.route_count)],check=True)
        result=json.loads(output.read_text());new_records=set()
        for entry in result['routes']:
            attack=geometry.rescore(entry['node_ids']);attack['interpolation_estimate']=entry['estimate'];attacks.append(attack)
            print('exact attack',attack['decimal'],'interior turns',attack['interior_turns'],flush=True)
            if args.adaptive_records:new_records|=geometry.carried_records(attack['route'])
            completions=geometry.prefix_completions(attack,all_routes=args.all_prefixes)
            if args.all_prefixes:
                attacks.extend(completions);simplified=completions[0]
            else:
                simplified=completions
                if simplified['route']!=attack['route']:attacks.append(simplified)
            if Q(simplified['payoff'])<Q(attack['payoff']):
                print('prefix completion',simplified['decimal'],'interior turns',simplified['interior_turns'],flush=True)
        estimate=min(r['estimate']for r in result['routes']);actual=float(min(Q(a['payoff'])for a in attacks));gap=actual-estimate
        fresh=new_records-set(geometry.record_knots or [])
        history.append(dict(round=iteration,states=states,record_knots=len(geometry.record_knots or []),
                            discovery_estimate=estimate,best_exact_attack=actual,numerical_interpolation_gap=gap,
                            new_carried_record_knots=len(fresh),seconds=time.time()-started))
        print('record round',iteration,'estimate',estimate,'exact attack',actual,'gap',gap,'new knots',len(fresh),flush=True)
        if args.adaptive_records:
            checkpoint=dict(input=Path(args.field).name,input_sha256=source_hash,adaptive_history=history,
                            record_knots_exact=list(map(str,executed_knots)),attacks=attacks,
                            new_records_exact=list(map(str,sorted(fresh))),
                            scope='In-progress adaptive physical-node discovery; exact attack costs, floating interpolation estimate')
            (work/'checkpoint.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
        if not args.adaptive_records:break
        if abs(gap)<=1e-10:reason='Numerical interpolation gap closed; floating discovery only';break
        if not fresh:reason='No new carried records; numerical gap remains';break
        reason='Adaptive round budget'
        if iteration+1<args.adaptive_records:geometry.set_record_knots(set(geometry.record_knots)|fresh)
    unique={tuple(map(tuple,a['route'])):a for a in attacks};attacks=list(unique.values())
    attacks.sort(key=lambda a:Q(a['payoff']))
    result.pop('routes')
    result.update(input=Path(args.field).name,input_sha256=source_hash,
                  terminal_time=str(geometry.horizon),axis_size=len(geometry.axis),
                  attacks=attacks,best_attack=attacks[0],all_prefixes=args.all_prefixes,
                  center_wait_edges=not args.unit_only,adaptive_history=history,
                  record_knots_exact=None if executed_knots is None else list(map(str,executed_knots)),
                  pending_record_knots_exact=list(map(str,sorted(fresh)))if args.adaptive_records else[],
                  stopping_rule=reason,seconds=time.time()-started)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
