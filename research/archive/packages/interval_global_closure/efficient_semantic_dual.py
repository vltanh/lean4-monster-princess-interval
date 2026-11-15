"""Recover a CDF dual's physical controls from labels and exact provenance.

Independent physical turn-position rounding is deliberately not used. Named
M1/M2/M3/I parameters define their light-coordinate equalities directly;
external attacks are matched to original records so exact rational routes
survive. Remaining floating-only records are reconstructed by unit runs and
one coherent light-coordinate map, with that inference reported explicitly.
Every output is a new, completely specified legal law requiring its own
unrestricted Princess response check.
"""
from __future__ import annotations
import argparse,json,math,sys
from collections import Counter,defaultdict
from fractions import Fraction as Q
from pathlib import Path
from bisect import bisect_left

HERE=Path(__file__).parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'packages/interval_turn_density'))
from atom_survival_cut import light_route
from continuous_response_waits import unitize_center_waits


def route_of(record):
    for key in ('route','monster_route','attacking_route'):
        if key in record:return record[key]


def records(value):
    if isinstance(value,dict):
        if route_of(value) is not None:yield value
        for child in value.values():yield from records(child)
    elif isinstance(value,list):
        for child in value:yield from records(child)


def family_records(value):
    if isinstance(value,dict):
        if value.get('sign') in ('positive','negative') and 'start' in value:
            a=Q(value['start']);light=light_route(dict(kind='M1',parameters=(a,)))
            yield dict(kind='M1',parameters=[str(a)],route=[[str((u+v)/2),str((u-v)/2)]for u,v in light])
        for child in value.values():yield from family_records(child)
    elif isinstance(value,list):
        for child in value:yield from family_records(child)


def float_path(route):
    out=[]
    for t,x in route:
        t,x=float(Q(t)) if isinstance(t,str) else float(t),float(Q(x)) if isinstance(x,str) else float(x)
        x=min(1.,max(-1.,x))
        if out and t<=out[-1][0]+1e-13:
            if abs(x-out[-1][1])<1e-10:continue
            raise ValueError('ambiguous zero-time source leg')
        out.append((t,x))
    out[0]=(0.,out[0][1]);walls={int(round(x)) for t,x in out if abs(abs(x)-1)<1e-10}
    for wall in ((1.,-1.) if out[-1][1]>=0 else (-1.,1.)):
        if len(walls)==2:break
        t,x=out[-1]
        if x!=wall:out.append((t+abs(wall-x),wall))
        walls.add(int(wall))
    clean=[];walls=set()
    for t,x in out:
        if len(clean)>=2:
            a,b=clean[-2:]
            s=(b[1]-a[1])/(b[0]-a[0]);z=(x-b[1])/(t-b[0])
            if abs(s-z)<1e-9:clean.pop()
        clean.append((t,x))
        if abs(abs(x)-1)<1e-10:walls.add(1 if x>0 else -1)
        if len(walls)==2:break
    return clean


def route_key(route):
    r=tuple((round(t,10),round(x,10)) for t,x in float_path(route))
    return min(r,tuple((t,-x) for t,x in r))


def same_route(left,right,tolerance=5e-10):
    a,b=float_path(left),float_path(right)
    if len(a)!=len(b):return False
    return any(all(abs(t-s)<tolerance and abs(x-sign*y)<tolerance
        for(t,x),(s,y)in zip(a,b))for sign in(1,-1))


def clean_exact(route):
    route=[tuple(map(Q,p)) for p in route]
    assert route and route[0][0]==0
    r=[]
    for t,x in route:
        assert t>=0 and -1<=x<=1
        if r and t==r[-1][0]:assert x==r[-1][1];continue
        if r:assert t>r[-1][0] and abs(x-r[-1][1])<=t-r[-1][0]
        r.append((t,x))
    walls={x for t,x in r if abs(x)==1}
    for wall in ((Q(1),Q(-1)) if r[-1][1]>=0 else (Q(-1),Q(1))):
        if len(walls)==2:break
        t,x=r[-1]
        if x!=wall:r.append((t+abs(wall-x),wall))
        walls.add(wall)
    waits=any(abs(y-x)!=b-a for(a,x),(b,y)in zip(r,r[1:]))
    if waits:r=unitize_center_waits(r)
    out=[];walls=set()
    for t,x in r:
        if len(out)>=2:
            a,b=out[-2:]
            if (b[1]-a[1])*(t-b[0])==(x-b[1])*(b[0]-a[0]):out.pop()
        out.append((t,x))
        if abs(x)==1:walls.add(x)
        if len(walls)==2:break
    assert len(walls)==2
    assert all(abs(y-x)==b-a for(a,x),(b,y)in zip(out,out[1:]))
    return out,waits


class Coordinates:
    """Native mesh recovery, then shared phases for floating-only provenance."""
    def __init__(self):self.phases=[];self.inferred=0
    def register(self,value):
        q=Q(value);n=q.numerator//q.denominator;r=q-n;r=min(r,1-r)
        if r not in self.phases:self.phases.append(r)
    def get(self,value,native=False):
        if isinstance(value,(str,Q,int)):
            q=Q(value);self.register(q);return q
        x=float(value);simple=Q(str(x)).limit_denominator(2**22)
        if abs(float(simple)-x)<1e-14:
            self.register(simple);return simple
        assert not native,('named coordinate not on the declared native mesh',value)
        q=Q(str(x));n=q.numerator//q.denominator;r=q-n;flip=r>Q(1,2);phase=1-r if flip else r
        near=[p for p in self.phases if abs(float(p-phase))<8e-15]
        if near:
            phase=min(near,key=lambda p:abs(float(p-phase)));self.inferred+=1
        else:self.register(phase)
        return n+(1-phase if flip else phase)


def named(record,coords,native=False):
    label=record.get('label',record);kind=label.get('kind')
    if kind=='M2_full_native':kind='M2'
    if kind in ('M1','M2','M3','initial_inward','I') and 'start' in label:
        keys={'M1':['start'],'M2':['start','turn'],'M3':['start','first_turn','second_turn'],
              'initial_inward':['start','first_v','second_u'],'I':['start','first_v','second_u']}[kind]
        p=[coords.get(label[k],native=native) for k in keys];kind='I' if kind=='initial_inward' else kind
    elif kind in ('M1','M2','M3','I') and 'parameters' in label:
        p=[coords.get(x,native=False) for x in label['parameters']]
    elif record.get('family')=='full_signed_M3':
        kind='M3';p=[coords.get(x) for x in record['parameters']]
    elif isinstance(record.get('parameters'),dict) and all(k in record['parameters']for k in('a','first_v','second_u')):
        kind='I';p=[coords.get(record['parameters'][k])for k in('a','first_v','second_u')]
    elif isinstance(record.get('parameters'),list) and len(record['parameters'])==3:
        # Earlier signed-M3 discovery exports omitted their family name.
        # Accept this interpretation only if its complete physical route
        # matches the exported route after redundant unit vertices collapse.
        kind='M3';p=[coords.get(x)for x in record['parameters']]
        x,s,t=p
        if abs(float(s-x))<1e-12:s=x
        if abs(float(t+x))<1e-12:t=-x
        if abs(float(s-(2-x)))<1e-12:s=2-x
        if abs(float(t-(s-2)))<1e-12:t=s-2
        p=[x,s,t]
    else:return None
    r=light_route(dict(kind=kind,parameters=tuple(p)))
    physical=[((u+v)/2,(u-v)/2) for u,v in r]
    result=clean_exact(physical)[0]
    if route_of(record) is not None and not same_route(result,route_of(record)):return None
    return result


def inferred_runs(route,coords):
    raw=float_path(route);a=coords.get(raw[0][1]);u,v=a,-a;result=[(Q(0),a)]
    for(t0,x0),(t1,x1)in zip(raw,raw[1:]):
        if abs(x1-x0)<1e-12:
            assert abs(x0)<1e-12 and abs(x1)<1e-12
            duration=coords.get(t1-t0);u+=duration;v+=duration
        elif x1>x0:
            if abs(x1-1)<1e-12:u=v+2
            elif abs(x1)<1e-12:u=v
            else:u=coords.get(t1+x1)
        else:
            if abs(x1+1)<1e-12:v=u+2
            elif abs(x1)<1e-12:v=u
            else:v=coords.get(t1-x1)
        result.append(((u+v)/2,(u-v)/2))
    return clean_exact(result)[0]


class Resolver:
    def __init__(self):self.cache={};self.coords=Coordinates();self.modes=Counter()
    def index(self,filename):
        path=Path(filename)
        if not path.is_absolute():path=(ROOT/path if (ROOT/path).exists() else HERE/path)
        if path in self.cache:return self.cache[path]
        data=json.loads(path.read_text());index=defaultdict(list)
        for r in list(records(data))+list(family_records(data)):
            try:key=route_key(route_of(r))
            except (TypeError,ValueError,AssertionError,IndexError,ZeroDivisionError):continue
            index[key].append(r)
            raw=route_of(r)
            if all(isinstance(z,(str,int)) for p in raw for z in p):
                try:
                    exact,_=clean_exact(raw)
                    for t,x in exact:self.coords.register(t+x);self.coords.register(t-x)
                except (AssertionError,ValueError):pass
        self.cache[path]=(data,index);return data,index
    def from_record(self,record,native=False):
        raw=route_of(record)
        if raw and all(isinstance(z,(str,int)) for p in raw for z in p):
            try:return clean_exact(raw)[0],'exact_source_route'
            except (AssertionError,ValueError):pass
        try:r=named(record,self.coords,native)
        except AssertionError:r=None
        if r is not None:return r,'named_light_parameters'
        if raw:
            # Many fixed-grid saved routes use JSON numbers whose decimal
            # values already satisfy every unit-leg equality exactly.
            try:
                exact=[(Q(str(t)),Q(str(x)))for t,x in raw]
                result,_=clean_exact(exact)
                return result,'exact_decimal_unit_route'
            except (AssertionError,ValueError):pass
            # A monotone run to one wall and then to the other is an M1
            # control, irrespective of redundant intermediate checkpoints.
            reduced=float_path(raw)
            if len(reduced)<=3 and all(abs(x)==1 for t,x in reduced[1:]):
                start=self.coords.get(reduced[0][1]);direction=1 if reduced[1][1]>start else -1
                rr=light_route(dict(kind='M1',parameters=(direction*start,)))
                result=clean_exact([((u+v)/2,direction*(u-v)/2)for u,v in rr])[0]
                return result,'recognized_m1_control'
        return inferred_runs(raw,self.coords),'coherent_light_run_inference'
    def resolve(self,item):
        label=item['label']
        if label['kind'] not in ('global_attack','external_separator'):
            result,mode=self.from_record(item,native=True);self.modes[mode]+=1;return result,dict(mode=mode)
        data,index=self.index(label['source']);target=route_key(item['route'])
        candidates=index.get(target,[])
        if not candidates:candidates=[r for group in index.values()for r in group if same_route(route_of(r),item['route'])]
        if not candidates:raise ValueError(('missing frozen attack-bank route',label))
        source_row=candidates[0];origin=source_row.get('source')
        if origin and origin!='complete_sixteenth_wait_bank':
            try:
                _,original=self.index(origin)
                options=original.get(target,[])
                if not options:options=[r for group in original.values()for r in group if same_route(route_of(r),item['route'])]
            except FileNotFoundError:options=[]
            options.sort(key=lambda r:0 if all(isinstance(z,(str,int))for p in route_of(r)for z in p) else 1)
            for option in options:
                try:
                    result,mode=self.from_record(option)
                    if not same_route(result,item['route']):continue
                    self.modes[mode]+=1;return result,dict(mode=mode,source=origin)
                except (AssertionError,ValueError,TypeError):continue
        result,mode=self.from_record(source_row)
        if not same_route(result,item['route']):raise ValueError(('reconstruction changed the exported physical route',label,mode))
        self.modes[mode]+=1;return result,dict(mode=mode,source=origin or label['source'])


def main():
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('prefix',type=Path);a=p.parse_args()
    data=json.loads(a.source.read_text());resolver=Resolver();atoms=[];weights=[];provenance=[]
    for j,item in enumerate(data['routes']):
        try:route,how=resolver.resolve(item)
        except Exception as error:raise RuntimeError(f'route {j}, label {item["label"]}: {error}')from error
        light=[[str(t+x),str(t-x)]for t,x in route]
        atoms.append(dict(kind='PATH',parameters=sum(light,[]),exact_light=light,
            light=[[float(Q(u)),float(Q(v))]for u,v in light]))
        weights.append(item['weight']);provenance.append(dict(index=j,label=item['label'],**how))
    total=sum(weights);weights=[w/total for w in weights]
    bank=dict(atoms=atoms,reconstruction=provenance)
    law=dict(scope='New exact physical law reconstructed from named light controls and exact source routes where available; floating-only provenance is explicitly marked. No source-dual response is transferred without global verification.',
        source=str(a.source),original_master=data['master_value'],atoms=[dict(kind=x['kind'],parameters=x['parameters'])for x in atoms],weights=weights,
        reconstruction_counts=dict(resolver.modes),shared_phase_inferences=resolver.coords.inferred)
    a.prefix.with_suffix('.bank.json').write_text(json.dumps(bank,separators=(',',':'))+'\n')
    a.prefix.with_suffix('.law.json').write_text(json.dumps(law,separators=(',',':'))+'\n')
    print(json.dumps(dict(pairs=len(atoms),weight_sum=sum(weights),reconstruction_counts=dict(resolver.modes),shared_phase_inferences=resolver.coords.inferred),indent=2))


if __name__=='__main__':main()
