"""Standalone standard-library replay of a physical clock/front certificate.

Usage: python replay_continuum_clock_certificate.py CERTIFICATE.physical.json.gz

No optimizer, scipy, numpy, compiled code, or saved model pickle is used.
"""

from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import gzip
import hashlib
import json
import sys


def read_certificate(path):
    if path.suffix == ".gz":
        with gzip.open(path,"rt",encoding="utf-8") as file:
            return json.load(file)
    return json.loads(path.read_text())


def replay(certificate_path):
    data=read_certificate(certificate_path)
    assert data["format"]=="finite-unit-speed-clock-front-certificate-v1"
    denominator=int(data["mass_denominator"])
    assert denominator>0
    pairs=[]
    total_weight=F(0)
    paths=[]
    knot_set=set()
    baseline=F(0)
    q=F(0)
    for item in data["law"]:
        weight=F(item["weight"])
        assert weight>0
        total_weight+=weight
        vertices=[(F(u),F(v)) for u,v in item["light_vertices"]]
        assert vertices and sum(vertices[0])==0
        # The supplied actual path visits both endpoints.
        assert any(u-v==2 for u,v in vertices)
        assert any(u-v==-2 for u,v in vertices)
        for (u,v),(U,V) in zip(vertices,vertices[1:]):
            assert U>=u and V>=v and (u==U)!=(v==V)
            assert -2<=u-v<=2 and -2<=U-V<=2
        pairs.append((weight,vertices))
        for reflected in (False,True):
            oriented=[(v,u) for u,v in vertices] if reflected else list(vertices)
            end=next(j for j,(u,v) in enumerate(oriented) if u-v==-2)
            oriented=oriented[:end+1]
            tau=sum(oriented[-1])/2
            fixed=bool(tau and oriented[0]==(F(1),F(-1)) and all(u==1 for u,v in oriented))
            if fixed:
                assert tau==2
                q+=weight
            paths.append({"vertices":oriented,"weight":weight/2,"tau":tau,"fixed":fixed})
            baseline+=weight*tau/2
            for u,v in oriented:
                knot_set.update((u,v))
    assert total_weight==1
    knots=sorted(knot_set)
    knot_index={k:j for j,k in enumerate(knots)}
    coords=[]
    for j,knot in enumerate(knots):
        coords.append(knot)
        if j+1<len(knots):
            coords.append((knot+knots[j+1])/2)
    clock_records={}
    for record in data["clocks"]:
        index=int(record["path"])
        assert 0<=index<len(paths) and index not in clock_records
        clock_records[index]=record
    positive=defaultdict(int)
    negative=defaultdict(int)
    fixed_front=defaultdict(int)
    center=0
    prefix_count=0
    interval_count=0

    def mass_integer(value):
        number=value*denominator
        assert number.denominator==1
        return number.numerator

    def add_pressure(rep,mass,fixed=False):
        nonlocal center
        assert mass>=0
        u,v=rep
        if u==v:
            center+=mass
            return
        key=(min(u,v),max(u,v))
        target=positive if u>v else negative
        target[key]+=mass
        if fixed and u>v:
            fixed_front[key]+=mass
        # Every active selected negative point is strictly above -1:
        # open cells have their midpoint strictly inside the arena,
        # and endpoint atoms have been excluded by the clock's truncation.
        if u<v:
            assert coords[v]-coords[u]<2

    for index,path in enumerate(paths):
        intervals=[]
        for (u,v),(U,V) in zip(path["vertices"],path["vertices"][1:]):
            axis=1 if u==U else 0
            fixed=u if axis else v
            low=v if axis else u
            high=V if axis else U
            for j in range(knot_index[low],knot_index[high]):
                atom=(2*knot_index[fixed],2*j) if axis else (2*j,2*knot_index[fixed])
                cell=(2*knot_index[fixed],2*j+1) if axis else (2*j+1,2*knot_index[fixed])
                intervals.append(((fixed+knots[j])/2,(fixed+knots[j+1])/2,atom,cell))
        interval_count+=len(intervals)
        assert sum((b-a for a,b,atom,cell in intervals),F(0))==path["tau"]
        if path["fixed"]:
            assert index not in clock_records
            for a,b,atom,cell in intervals:
                add_pressure(cell,mass_integer(path["weight"]*(b-a)),fixed=True)
            continue
        if not intervals:
            assert index not in clock_records and path["tau"]==0
            continue
        record=clock_records.pop(index)
        atom_masses={}
        uniform_masses={}
        for label,target in (("atoms",atom_masses),("uniforms",uniform_masses)):
            for j,value in record[label]:
                j=int(j);value=int(value)
                assert 0<=j<len(intervals) and value>0 and j not in target
                target[j]=value
        cumulative=0
        for j,(a,b,atom,cell) in enumerate(intervals):
            assert cumulative>=mass_integer(path["weight"]*a)
            A=atom_masses.get(j,0)
            B=uniform_masses.get(j,0)
            add_pressure(atom,A)
            add_pressure(cell,B)
            cumulative+=A+B
            assert cumulative>=mass_integer(path["weight"]*b)
            prefix_count+=1
        assert cumulative==mass_integer(path["weight"]*path["tau"])
    assert not clock_records
    assert sum(positive.values())+sum(negative.values())+center==mass_integer(baseline)
    source={}
    target={}
    for label,store in (("matching_sources",source),("matching_targets",target)):
        for left,right,value in data[label]:
            key=(int(left),int(right));value=int(value)
            assert value>0 and key not in store
            assert 0<=key[0]<key[1]<len(coords)
            store[key]=value
    deficit=0
    unmatched=[]
    for key,mass in positive.items():
        flow=source.get(key,0)
        assert 0<=flow<=mass
        residue=mass-flow
        assert residue<=fixed_front.get(key,0)
        if residue:
            left,right=key
            assert coords[right]==1 and left%2==1
            assert -1<coords[left]<1
            unmatched.append([left,right,str(residue)])
        deficit+=residue
    assert all(key in positive for key in source)
    for key,flow in target.items():
        assert 0<=flow<=negative.get(key,0)
    divergence=defaultdict(int)
    edge_count=0
    for left,right,L,R,value in data["order_flow"]:
        left,right,L,R=map(int,(left,right,L,R))
        value=int(value)
        assert value>0
        assert 0<=left<=right<len(coords) and 0<=L<=R<len(coords)
        assert (L,R) in ((left-1,right),(left,right+1))
        divergence[(left,right)]+=value
        divergence[(L,R)]-=value
        edge_count+=1
    for key,value in source.items():
        divergence[key]-=value
    for key,value in target.items():
        divergence[key]+=value
    assert all(value==0 for value in divergence.values())
    assert sum(source.values())==sum(target.values())
    deficiency=F(deficit,denominator)
    assert baseline==F(data["endpoint_baseline"])
    assert deficiency==F(data["matching_deficiency"])
    assert baseline+deficiency==F(data["unrestricted_upper"])
    assert baseline+deficiency<=F(data["source_exact_upper"])
    assert q==F(data["sweep_pair_weight"]) and q>0
    assert 0<=deficiency<=q/2
    completion=data["continuum_completion"]
    assert F(completion["cutoff_b"])==deficiency/q
    assert F(completion["pair_density_q_over_2"])==q/2
    assert F(completion["total_pair_weight"])==deficiency/2
    assert F(completion["remaining_sweep_pair_weight"])==q-deficiency/2
    assert F(completion["zero_deficiency_exact_value"])==baseline+deficiency
    # These exact inequalities are the hypotheses of the continuum
    # cumulative-capacity proof: b<=1/2, rho<=q dt/2, and |rho|=q*b.
    b=deficiency/q
    assert 0<=b<=F(1,2)
    assert 2-b/8>=1
    assert q*b==deficiency
    report={
        "certificate_sha256":hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
        "pairs":len(pairs),"oriented_paths":len(paths),"light_knots":len(knots),
        "physical_clock_prefix_checks":prefix_count,
        "matching_order_edges":edge_count,
        "positive_matching_cells":len(source),"negative_matching_cells":len(target),
        "all_off_front_positive_pressure_matched":True,
        "remaining_pressure_is_submeasure_of_current_sweep":True,
        "endpoint_baseline":str(baseline),
        "matching_deficiency":str(deficiency),
        "unrestricted_upper":str(baseline+deficiency),
        "continuum_zero_deficiency_exact_value":str(baseline+deficiency),
        "continuum_cutoff_b":str(b),
        "continuum_pair_density":str(q/2),
        "front_residual_cells":unmatched,
    }
    print(json.dumps(report,indent=2))
    print("PASS: exact physical clocks, full off-front matching, and continuum endpoint-front completion")
    return report


if __name__=="__main__":
    replay(Path(sys.argv[1]))
