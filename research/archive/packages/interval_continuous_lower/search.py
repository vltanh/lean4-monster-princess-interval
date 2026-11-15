#!/usr/bin/env python3
"""Improve continuous attack screens while preserving an exact bank floor.

The continuous objective is NEVER a lower certificate. Every accepted field
passes a complete normalized-bank oracle; its only certified game lower is
the resulting bank value minus 1/(2n). New center-engine results require the
original verifier and independent replay before promotion.
"""
from __future__ import annotations

import argparse
import base64
from fractions import Fraction as Q
import gzip
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import time
import zlib

import numpy as np

ROOT=Path(__file__).resolve().parents[2]
NATIVE=ROOT/'packages/interval_clock_grid/normalized_native'
sys.path[:0]=[str(NATIVE),str(ROOT/'packages/interval_discovery'),
              str(ROOT/'packages/interval_quantile_certificate')]
from solve_normalized import Master
from cached_path_pricing import CachedPathPricing,normalize_path
from verify_native_field import load_table
from princess_search import full_seed,read_json
from score_continuous_attack import supporting_plane,Field
from event_lp import EventLP,SolveError
FRONT_TWO=False


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path,data):
    path=Path(path);raw=(json.dumps(data,separators=(',',':'))+'\n').encode()
    if path.suffix=='.gz':raw=gzip.compress(raw,mtime=0)
    temp=path.with_suffix(path.suffix+'.tmp');temp.write_bytes(raw);temp.replace(path)


def pack_field(master,table):
    if master.D>=2**32:raise ValueError('compact field requires uint32 probabilities')
    values=np.array([table[j,k] for j,k in master.nodes],dtype='<u4').tobytes()
    return {'format':'qout-clock-grid-field-u32-zlib-v1','n':master.n,
            'field_denominator':str(master.D),'normalized_profile':True,
            'encoding':{'count':master.K,'integer_type':'uint32 little-endian','compression':'zlib',
                        'uncompressed_sha256':hashlib.sha256(values).hexdigest()},
            'pre_two_values_base64':base64.b64encode(zlib.compress(values,9)).decode(),
            'scope':'Legal full-width CDF candidate. This encoding alone certifies no security.'}


def retain_trial_field(master,table,output,iteration):
    """Keep every exact candidate before screening, without replacing old bytes."""
    if not isinstance(iteration,int) or iteration<0:raise ValueError('invalid trial iteration')
    data=pack_field(master,table)
    raw=(json.dumps(data,separators=(',',':'))+'\n').encode()
    field_hash=hashlib.sha256(raw).hexdigest()
    relative=Path('trials')/f'trial_{iteration:06d}_{field_hash}.field.json.gz'
    path=Path(output)/relative;path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists():
        # Link a fully written temporary file exclusively. A restart or
        # another writer may reuse matching content, but cannot overwrite it.
        with tempfile.NamedTemporaryFile(dir=path.parent,suffix='.tmp',delete=False) as stream:
            temporary=Path(stream.name)
            stream.write(gzip.compress(raw,mtime=0))
        try:
            try:os.link(temporary,path)
            except FileExistsError:pass
        finally:temporary.unlink()
    packed=path.read_bytes()
    if gzip.decompress(packed)!=raw:
        raise ValueError(f'immutable trial field mismatch: {relative}')
    return {'path':relative.as_posix(),'compressed_sha256':hashlib.sha256(packed).hexdigest(),
            'field_json_sha256':field_hash,'raw_nodal_sha256':data['encoding']['uncompressed_sha256'],
            'compressed_bytes':len(packed),'field_json_bytes':len(raw),
            'scope':'Exact exploratory trial only; no security certificate is assigned.'}


def check_trial_binding(output,reference):
    """Check a retained trial's hashes, without any response pricing."""
    relative=Path(reference['path'])
    if relative.is_absolute() or '..' in relative.parts:raise ValueError('invalid trial reference path')
    packed=(Path(output)/relative).read_bytes()
    if len(packed)!=reference['compressed_bytes'] or hashlib.sha256(packed).hexdigest()!=reference['compressed_sha256']:
        raise ValueError(f'retained trial compressed hash mismatch: {relative}')
    raw=gzip.decompress(packed)
    if len(raw)!=reference['field_json_bytes'] or hashlib.sha256(raw).hexdigest()!=reference['field_json_sha256']:
        raise ValueError(f'retained trial JSON hash mismatch: {relative}')
    data=json.loads(raw)
    nodes=zlib.decompress(base64.b64decode(data['pre_two_values_base64'],validate=True))
    if hashlib.sha256(nodes).hexdigest()!=reference['raw_nodal_sha256'] or \
            data['encoding']['uncompressed_sha256']!=reference['raw_nodal_sha256']:
        raise ValueError(f'retained trial nodal hash mismatch: {relative}')
    return data


def add_certificate(master,data,answer):
    units=int(answer['minimum_units']);den=4*master.n*master.D
    exact=answer.get('minimum_is_exact',True)
    return dict(data,**({'minimum_units':str(units),'normalized_bank_dual_value':str(Q(units,den))} if exact else
        {'certified_bank_lower_units':str(units),'normalized_bank_lower':str(Q(units,den))}),
        minimum_is_exact=exact,objective_denominator=str(den),global_lower=str(Q(units-2*master.D,den)),
        global_lower_decimal=float(Q(units-2*master.D,den)),pricing=answer,
        native_source_sha256=answer.get('engine_source_sha256',digest(NATIVE/'price_normalized.cpp')),
        pricing_engine=answer.get('engine','original normalized integer oracle'),
        scope=('Exact complete normalized-bank minimum.' if exact else 'Inherited normalized-bank lower bound; no attaining path or exact minimum is asserted.')+
              ' Game lower subtracts1/(2n). Continuous screen values are upper attacks, not security guarantees.')


def price_table(master,table,keep):
    master.binary.write_bytes(struct.pack('<IIQ',1,master.n,master.D)+table.astype('<u8').tobytes())
    command=[str(master.executable),str(master.binary),str(keep)]
    if getattr(master,'center_engine',False):command.append('2' if keep else '3')
    done=subprocess.run(command,
                        check=True,text=True,stdout=subprocess.PIPE)
    answer=json.loads(done.stdout)
    if answer.get('status')!='PASS' or answer.get('certifies_lower') is False:
        raise ValueError('incomplete response oracle cannot accept a field')
    if getattr(master,'center_engine',False):
        answer.update({'engine':'complete center-normal-form integer oracle',
            'engine_source_sha256':digest(master.pricing_source),'center_normal_form_policy':2 if keep else 3,
            'independent_original_oracle_replay_required_before_promotion':True})
    return answer


def add_calendar(master,path,table):
    if getattr(master,'bank_model','calendars')=='records':
        path=normalize_path(master.n,path)
        key=(int(path['start_grid']),tuple(map(int,path['moves'])))
        if key in master.physical_seen:return False
        plan,mass,coef=master.calendar(path,table,latest=False)
        master.physical_seen.add(key)
        # Equal active calendars do not make two physical paths equivalent:
        # their other record calendars can differ at the next field.
        master.columns.append({'plan':plan,'mass':mass,'coeff':coef})
        return True
    plan,mass,coef=master.calendar(path,table,latest=False)
    key=mass,tuple(sorted(coef.items()))
    if key in master.seen:return False
    master.seen.add(key);master.columns.append({'plan':plan,'mass':mass,'coeff':coef});return True


def path_route(n,path):
    x=int(path['start_grid']);out=[(Q(0),Q(x,2*n))]
    moves=path['moves']
    for j,step in enumerate(moves):
        if j and step!=moves[j-1]:out.append((Q(j,2*n),Q(x,2*n)))
        x+=step
    out.append((Q(len(moves),2*n),Q(x,2*n)))
    return tuple(out)


def route_key(route):return tuple(tuple(map(Q,p)) for p in route)


def json_route(route):return [[str(t),str(x)] for t,x in route]


def score_routes(master,table,routes,model,output,prefix):
    data=pack_field(master,table);field=Field(data,Q(1,2))
    values=[];new=0;reports=[]
    for index,route in enumerate(routes):
        plane=supporting_plane(field,route)
        plane.update({'route':json_route(route),'contour_n':master.n,
            'scope':'Exact cost of one physical route against this full-width field, and a supporting causal-clock plane for this nodal field class. Not a lower certificate.',
            'field_pre_two_sha256':data['encoding']['uncompressed_sha256']})
        new+=model.add_plane(plane);values.append(Q(plane['value']))
        reports.append(plane)
    write(output/f'{prefix}.planes.json.gz',reports)
    return min(values),values,new,data


def discover_routes(args,master,table,prefix,seed_offset=0):
    if args.attack_seconds<=0:return []
    from search_continuous_attacks import search
    path=args.output/f'{prefix}.attack_source.json'
    write(path,pack_field(master,table))
    found=search(path,args.output/prefix,starts=args.attack_starts,
        seed=args.random_seed+seed_offset,seconds=args.attack_seconds,
        denominator=1000000,exact_top=0,coarse=master.n,
        max_evaluations=args.attack_evaluations)
    unique=[]
    for item in found['floating_discoveries']:
        route=route_key(item['route'])
        if route not in unique:unique.append(route)
        if len(unique)>=args.new_attacks:break
    return unique


def save_state(args,master,model,cache,routes,floor,incumbent,screen,inc_answer,history,status,began,radius):
    c=Q(int(inc_answer['minimum_units']),4*master.n*master.D)
    write(args.output/'incumbent.field.json',add_certificate(master,pack_field(master,incumbent),inc_answer))
    write(args.output/'state.json.gz',{'scope':'Discovery checkpoint; continuous objective is a finite-attack upper screen only.',
        'n':master.n,'denominator':master.D,'bank_floor':str(floor),
        'bank_model':args.bank_model,
        'hybrid_model':model.checkpoint() if args.bank_model=='hybrid' else None,
        'trust_radius':radius,'seed_sha256':digest(args.seed_field),
        'incumbent_sha256':digest(args.output/'incumbent.field.json'),
        'columns':[{'plan':x['plan']} for x in master.columns],
        'continuous_planes':[{'constant':str(x['constant']),
                            'coefficients':[[j,k,str(a)] for (j,k),a in sorted(x['coeff'].items())]} for x in model.attacks],
        'continuous_routes':[json_route(r) for r in routes],
        'incumbent_continuous_screen':str(screen),'history':history})
    write(args.output/'manifest.json',{'status':status,
        'scope':'Continuous geometry discovery at an independently enforced exact finite-bank floor.',
        'n':master.n,'native_bank_floor':str(floor),'native_bank_model':args.bank_model,
        'incumbent_exact_bank_value':str(c) if inc_answer.get('minimum_is_exact',True) else None,
        'incumbent_certified_bank_lower':str(c),'incumbent_minimum_is_exact':inc_answer.get('minimum_is_exact',True),
        'incumbent_certified_game_lower':str(c-Q(1,2*master.n)),
        'continuous_attack_screen_upper':str(screen),'continuous_attack_screen_upper_decimal':float(screen),
        'continuous_screen_is_lower_bound':False,'same_fullwidth_cdf_security_claimed':False,
        'cached_physical_paths':len(cache),'native_calendar_rows':len(master.columns),
        'continuous_routes':len(routes),'continuous_clock_planes':len(model.attacks),
        'elapsed_seconds':time.monotonic()-began,
        'seed_sha256':digest(args.seed_field),
        'arguments':{k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()},
        'files':{str(p.relative_to(args.output)):{'sha256':digest(p),'bytes':p.stat().st_size}
                 for p in args.output.rglob('*') if p.is_file() and 'work' not in p.parts and
                 p.name not in ('manifest.json','search.log')}})


def run(args):
    began=time.monotonic();args.output.mkdir(parents=True,exist_ok=True)
    seed_data,raw,seed_hash=load_table(args.seed_field)
    D=args.denominator or int(seed_data['field_denominator'])
    master=Master(args.n,args.output/'work',D,True)
    master.bank_model=args.bank_model;master.physical_seen=set()
    if args.oracle=='center':
        master.pricing_source=ROOT/'packages/interval_center_pricing/price_center.cpp'
        master.executable=args.output/'work/price_center'
        subprocess.run(['g++','-O3','-std=c++17',str(master.pricing_source),'-o',str(master.executable)],check=True)
        master.center_engine=True
    answer=None
    if seed_data['n']==args.n and int(seed_data['field_denominator'])==D:
        table=np.frombuffer(raw,dtype=np.uint64).reshape((master.H+1,master.R+1)).copy()
        replay_path=args.seed_replay
        if replay_path is None and args.seed_field.resolve()==(ROOT/'packages/interval_clock_grid/lower_n256_field.json').resolve():
            replay_path=ROOT/'packages/interval_clock_grid/lower_n256_native_replay.json'
        if replay_path:
            replay=read_json(replay_path)
            if replay['input_sha256']!=seed_hash or replay['verifier_source_sha256']!=digest(NATIVE/'price_normalized.cpp'):
                raise ValueError('seed replay does not bind this field and verifier')
            answer=replay['pricing']
            if int(answer['minimum_units'])!=int(seed_data['minimum_units']):raise ValueError('seed replay fraction mismatch')
        elif 'pricing' in seed_data:answer=seed_data['pricing']
    else:table=master.repair(master.interpolate_seed(full_seed(args.seed_field)))
    if answer is None:answer=price_table(master,table,args.keep)
    if answer['status']!='PASS':raise ValueError('seed lacks complete response certificate')
    floor=Q(int(answer['minimum_units']),4*args.n*D)-Q(args.bank_slack)
    state=None
    if args.resume and (args.output/'state.json.gz').exists():
        state=read_json(args.output/'state.json.gz')
        if state['n']!=args.n or state['denominator']!=D or state['seed_sha256']!=seed_hash:
            raise ValueError('resume parameters or original seed changed')
        if state.get('bank_model',args.bank_model)!=args.bank_model:
            raise ValueError('resume bank model changed')
        if state['incumbent_sha256']!=digest(args.output/'incumbent.field.json'):
            raise ValueError('incumbent hash does not match discovery state')
        for row in state['history']:
            if 'trial_field' in row:check_trial_binding(args.output,row['trial_field'])
        saved,buffer,_=load_table(args.output/'incumbent.field.json')
        table=np.frombuffer(buffer,dtype=np.uint64).reshape((master.H+1,master.R+1)).copy()
        answer=saved['pricing'];floor=Q(state['bank_floor'])
    cache=CachedPathPricing(args.n,D)
    bank=read_json(args.response_bank)
    plans=bank.get('paths',[c['plan'] for c in bank.get('columns',[])])
    cache.add_many(plans,source_n=bank['n'])
    cache.add_many(answer.get('paths',[]))
    cache.add({'start_grid':master.R,'moves':[-1]*(2*master.R)})
    prices=cache.price(table,keep=max(args.initial_routes,2))
    for p in prices['paths'][:args.initial_routes]:add_calendar(master,p,table)
    for p in answer.get('paths',[]):add_calendar(master,p,table)
    if state:
        for column in state['columns']:
            if args.bank_model=='records':add_calendar(master,column['plan'],table)
            else:master.add_plan(column['plan'])
        cache.update_columns(master.columns)
        if args.bank_model=='records':
            master.physical_seen.update((int(c['plan']['start_grid']),tuple(map(int,c['plan']['moves']))) for c in master.columns)
    # A small explicit discovery buffer absorbs numerical LP feasibility and
    # integer flooring. It strengthens, never weakens, the exact floor gate.
    buffer=min(Q(args.bank_slack)/4,Q(1,10**8))
    if args.bank_model=='hybrid':
        from hybrid_lp import HybridLP
        model=HybridLP(master,floor+buffer,args.lp_seconds,args.level_fraction,
                       front=FRONT_TWO,secants=args.continuous_secants)
        if state:
            if not state.get('hybrid_model'):raise ValueError('missing hybrid checkpoint')
            model.restore(state['hybrid_model'])
    elif args.bank_model=='records':
        from record_lp import RecordLP
        model=RecordLP(master,floor+buffer,args.lp_seconds,args.level_fraction,front=FRONT_TWO)
    else:model=EventLP(master,floor+buffer,args.lp_seconds,args.level_fraction)
    witness=read_json(args.attack)
    routes=[route_key(witness.get('route',witness.get('physical_route'))),
            ((Q(0),Q(1)),(Q(2),Q(-1))),
            ((Q(0),Q(0)),(Q(1),Q(1)),(Q(3),Q(-1)))]
    routes += [path_route(args.n,p) for p in prices['paths'][:args.initial_attacks]]
    if getattr(args,'route_bank',None):
        extra=read_json(args.route_bank)
        extra=extra['routes'] if isinstance(extra,dict) else extra
        routes += [route_key(r['route'] if isinstance(r,dict) else r) for r in extra]
    if state:routes=[route_key(r) for r in state['continuous_routes']]
    else:routes+=discover_routes(args,master,table,'initial_attack_search')
    routes=list(dict.fromkeys(routes))
    if state:
        for plane in state['continuous_planes']:model.add_plane(plane)
        screen=Q(state['incumbent_continuous_screen'])
    else:screen,_,_,_=score_routes(master,table,routes,model,args.output,'initial')
    incumbent=table;inc_answer=answer
    history=state['history'] if state else [];radius=state['trust_radius'] if state else args.radius
    print(json.dumps({'event':'initial','exact_bank_floor':str(floor),
        'continuous_attack_upper':str(screen),'continuous_attack_upper_decimal':float(screen),
        'cached_paths':len(cache),'continuous_routes':len(routes),'seconds':time.monotonic()-began}),flush=True)
    save_state(args,master,model,cache,routes,floor,incumbent,screen,inc_answer,history,'RUNNING',began,radius)
    status='ITERATION_LIMIT'
    for _ in range(args.iterations):
        # Use persistent indices for artifact names too: a resumed run must
        # never overwrite the exact rejected fields/planes from an earlier run.
        iteration=len(history)
        if time.monotonic()-began>=args.seconds:status='BUDGET_STOPPED';break
        try:candidate,upper,level,stats=model.solve(incumbent,screen,radius)
        except SolveError as error:
            if 'Time limit reached' not in str(error):raise
            status='LP_BUDGET_STOPPED';break
        trial_field=retain_trial_field(master,candidate,args.output,iteration)
        cached=cache.price(candidate,keep=args.cached_keep,level=floor,tolerance='0')
        new=sum(add_calendar(master,p,candidate) for p in cached['violating_paths'])
        promoted=(sum(model.note_violation(p,args.promotion_after) for p in cached['violating_paths'])
                  if args.bank_model=='hybrid' else 0)
        row={'iteration':len(history),'lp_continuous_screen_upper':upper,'trial_screen_target':level,
             'bank_floor':str(floor),'cached_bank_upper':str(Q(int(cached['cached_minimum_units']),4*args.n*D)),
             'new_bank_calendars':new,'radius':radius,'lp':stats,'trial_field':trial_field}
        if args.bank_model=='records':row['new_physical_paths']=new
        if args.bank_model=='hybrid':
            row['lp_secant_model_value']=row.pop('lp_continuous_screen_upper')
            row['lp_secant_model_is_upper_bound']=False
            row['new_promoted_physical_paths']=promoted
        if new or promoted:row['status']='CACHED_BANK_FLOOR_REJECTED'
        elif Q(int(cached['cached_minimum_units']),4*args.n*D)<floor:
            # Exact floor failures remain failures even if a floating row is
            # violated only by rounding. Never silently widen the floor.
            row['status']='INTEGER_FLOOR_REJECTED';radius=max(args.minimum_radius,radius/2)
        else:
            measured,_,planes,data=score_routes(master,candidate,routes,model,args.output,f'trial_{iteration:04d}')
            row.update({'continuous_attack_upper':str(measured),'continuous_attack_upper_decimal':float(measured),
                        'new_continuous_clock_planes':planes})
            if measured< Q(str(level))-Q(args.screen_tolerance):
                row['status']='CONTINUOUS_CLOCK_SEPARATED'
            elif measured<=screen+Q(args.screen_tolerance):
                row['status']='NO_SCREEN_IMPROVEMENT';radius=min(args.maximum_radius,2*radius)
            else:
                exact=price_table(master,candidate,args.keep)
                value=Q(int(exact['minimum_units']),4*args.n*D)
                cache.add_many(exact['paths'])
                additions=sum(add_calendar(master,p,candidate) for p in exact['paths'])
                row.update({'complete_bank_value':str(value),'complete_bank_value_decimal':float(value),
                            'new_complete_bank_calendars':additions,'states':exact['retained_states']})
                write(args.output/f'trial_{iteration:04d}.certified.json.gz',add_certificate(master,data,exact))
                # The most dangerous sampled route is scored in continuous
                # time too. A new path changes the finite upper-screen bank.
                route=path_route(args.n,exact['paths'][0])
                if route not in routes:
                    routes.append(route)
                    baseline,_,_,_=score_routes(master,incumbent,[route],model,args.output,f'new_route_{iteration:04d}_old')
                    latest,_,_,_=score_routes(master,candidate,[route],model,args.output,f'new_route_{iteration:04d}_trial')
                    screen=min(screen,baseline);measured=min(measured,latest)
                    row['new_continuous_route']=json_route(route)
                    row['screen_after_new_route']=str(measured)
                if value>=floor and iteration%args.attack_every==0:
                    extra=[r for r in discover_routes(args,master,candidate,f'attack_search_{len(history):04d}',len(history)+1)
                           if r not in routes]
                    if extra:
                        routes+=extra
                        old,_,_,_=score_routes(master,incumbent,extra,model,args.output,f'new_family_{len(history):04d}_old')
                        fresh,_,_,_=score_routes(master,candidate,extra,model,args.output,f'new_family_{len(history):04d}_trial')
                        screen=min(screen,old);measured=min(measured,fresh)
                        row['new_continuous_family_routes']=[json_route(r) for r in extra]
                        row['screen_after_family_search']=str(measured)
                if value<floor:
                    row['status']='COMPLETE_BANK_FLOOR_REJECTED';radius=max(args.minimum_radius,radius/2)
                elif measured>screen+Q(args.screen_tolerance):
                    incumbent=candidate;inc_answer=exact;screen=measured
                    row['status']='ACCEPTED_GEOMETRY_WITH_COMPLETE_BANK_FLOOR'
                else:row['status']='NEW_CONTINUOUS_ROUTE_REJECTED'
        row['seconds']=time.monotonic()-began;history.append(row)
        print(json.dumps(row),flush=True)
        save_state(args,master,model,cache,routes,floor,incumbent,screen,inc_answer,history,'RUNNING',began,radius)
    save_state(args,master,model,cache,routes,floor,incumbent,screen,inc_answer,history,status,began,radius)
    return read_json(args.output/'manifest.json')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--n',type=int,default=256)
    p.add_argument('--seed-field',type=Path,default=ROOT/'packages/interval_clock_grid/lower_n256_field.json')
    p.add_argument('--seed-replay',type=Path)
    p.add_argument('--response-bank',type=Path,default=ROOT/'packages/interval_lower_bundle/initial_paths_n128.json.gz')
    p.add_argument('--attack',type=Path,default=ROOT/'packages/interval_quantile_certificate/current_fullwidth_attack.json')
    p.add_argument('--route-bank',type=Path,help='Additional specified unit-speed continuous attacks (JSON routes list)')
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--denominator',type=int)
    p.add_argument('--oracle',choices=('classic','center'),default='center')
    p.add_argument('--bank-model',choices=('calendars','records','hybrid'),default='calendars')
    p.add_argument('--continuous-secants',type=int,default=16)
    p.add_argument('--promotion-after',type=int,default=3)
    p.add_argument('--bank-slack',default='1/10000000')
    p.add_argument('--seconds',type=float,default=1200.)
    p.add_argument('--lp-seconds',type=float,default=180.)
    p.add_argument('--iterations',type=int,default=120)
    p.add_argument('--radius',type=float,default=.002)
    p.add_argument('--minimum-radius',type=float,default=.00005)
    p.add_argument('--maximum-radius',type=float,default=.05)
    p.add_argument('--level-fraction',type=float,default=.5)
    p.add_argument('--keep',type=int,default=24)
    p.add_argument('--cached-keep',type=int,default=128)
    p.add_argument('--initial-routes',type=int,default=128)
    p.add_argument('--initial-attacks',type=int,default=2)
    p.add_argument('--screen-tolerance',default='1/1000000')
    p.add_argument('--attack-seconds',type=float,default=40.)
    p.add_argument('--attack-starts',type=int,default=4)
    p.add_argument('--attack-evaluations',type=int,default=500)
    p.add_argument('--attack-every',type=int,default=4)
    p.add_argument('--new-attacks',type=int,default=2)
    p.add_argument('--random-seed',type=int,default=20261114)
    p.add_argument('--resume',action='store_true')
    args=p.parse_args()
    if not (0<args.minimum_radius<=args.radius<=args.maximum_radius<=1):raise ValueError('trust radii')
    if Q(args.bank_slack)<0 or args.keep<1 or not 0<args.level_fraction<1:raise ValueError('invalid search parameters')
    if min(args.attack_starts,args.attack_evaluations,args.attack_every,args.new_attacks)<1:raise ValueError('attack search controls')
    if args.continuous_secants<1 or args.promotion_after<1:raise ValueError('hybrid model controls')
    print(json.dumps(run(args)),flush=True)


if __name__=='__main__':main()
