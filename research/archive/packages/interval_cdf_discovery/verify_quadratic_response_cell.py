#!/usr/bin/env python3
"""Exact whole-tetrahedron negative-M3 response diagnostic, not a bound."""
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path
from audit_fixed_one import early_m3_route,negative_early_m3,positive,negative
from quadratic_response_forms import GeometryForms,Form,matrix_forms,ATTACK_TETRAHEDRON
from quadratic_simplex import minimum,evaluate,matrix_from_function
PACKAGE=Path(__file__).resolve().parent
def pack(v):
    return dict(exact=str(v),value=float(v))
def compositions(total,parts):
    if parts==1:
        yield(total,);return
    for head in range(total+1):
        for tail in compositions(total-head,parts-1):
            yield(head,)+tail
def combine(vertices,weights):
    return tuple(sum(w*v[k] for w,v in zip(weights,vertices))
                 for k in range(len(vertices[0])))
def form_matrix_value(matrix,weights):
    return sum((weights[i]*weights[j]*matrix[i][j]
                for i in range(len(weights)) for j in range(len(weights))),Form())
def line_breaks(field,fixed,left,right,axis):
    cuts={left,right};other=1-axis
    for points,_,_ in field.triangles:
        if not min(p[axis] for p in points)<=fixed<=max(p[axis] for p in points):
            continue
        for p,q in zip(points,points[1:]+points[:1]):
            if p[axis]==q[axis]:
                if p[axis]==fixed:
                    cuts.update(z[other] for z in(p,q) if left<z[other]<right)
            elif min(p[axis],q[axis])<=fixed<=max(p[axis],q[axis]):
                cut=p[other]+(fixed-p[axis])*(q[other]-p[other])/(q[axis]-p[axis])
                if left<cut<right:
                    cuts.add(cut)
    return sorted(cuts)
def inverse_cut(field,fixed,left,right,axis,threshold):
    cuts=line_breaks(field,fixed,left,right,axis)
    value=(lambda t:field.radial(fixed,t)) if axis==0 else(lambda t:field.radial(t,fixed))
    roots=[]
    for lo,hi in zip(cuts,cuts[1:]):
        fl,fh=value(lo)-threshold,value(hi)-threshold
        if fl==0:roots.append(lo)
        if fl*fh<0:roots.append(lo+(hi-lo)*fl/(fl-fh))
        if fh==0:roots.append(hi)
    return sorted(set(cuts[:1]+cuts[-1:]+roots))
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--field',type=Path,default=PACKAGE/'snapshots/endpoint_joint_i1_field.json')
    p.add_argument('--output',type=Path,default=PACKAGE/'snapshots/negative_m3_quadratic_cell.json')
    args=p.parse_args()
    geom=GeometryForms(json.loads(args.field.read_text()));field=geom.geometry
    reference=field.positive_m1(Q(1))
    assert geom.endpoint_four().value(field.values)==4*reference
    vertices=ATTACK_TETRAHEDRON
    report=dict(scope='Exact continuum negative-M3 constraint on one geometric tetrahedron; no unrestricted certificate or new bound.',
                source=args.field.name,
                domain='0<=a<=s-13/16;13/16<=s<=b<=7/8',
                variables=['a','s','b'],
                vertices=[[str(x) for x in v] for v in vertices],
                endpoint_reference=pack(reference),branches=[])
    affine_checks=capture_checks=root_checks=0
    for branch in(0,1):
        callback=lambda point:geom.negative_m3_four(*point,branch)-geom.endpoint_four()
        forms=matrix_forms(vertices,callback)
        matrix=[[form.value(field.values) for form in row] for row in forms]
        assert matrix==matrix_from_function(vertices,lambda p:callback(p).value(field.values))
        for integers in compositions(5,4):
            weights=tuple(Q(i,5) for i in integers)
            point=combine(vertices,weights)
            assert form_matrix_value(forms,weights)==callback(point)
            affine_checks+=1
            raw=callback(point).value(field.values)/4+reference
            actual=field.unit_route_payoff(early_m3_route(*point[:2]))
            assert actual==negative_early_m3(field,*point[:2])
            assert raw>=actual
            capture_checks+=2
        result=minimum(matrix);point=combine(vertices,result['weights'])
        assert evaluate(matrix,result['weights'])==callback(point).value(field.values)
        route_cost=field.unit_route_payoff(early_m3_route(*point[:2]))
        if branch==1:
            assert route_cost-reference==result['value']/4
            assert field.radial(point[2],point[1])==field.initial_value(point[0])
            assert field.radial(Q(1),point[1])>=field.initial_value(point[0])
            assert min(result['weights'])>0
            root_checks+=4
        report['branches'].append(dict(
            branch=branch,
            four_slack_matrix=[[str(x) for x in row] for row in matrix],
            four_score_forms=[[form.payload() for form in row]
                              for row in matrix_forms(vertices,lambda p:geom.negative_m3_four(*p,branch))],
            four_slack=pack(result['value']),cost_at_minimizer=pack(route_cost),
            weights=list(map(str,result['weights'])),minimizer=list(map(str,point)),
            minimizer_decimal=list(map(float,point)),exact_kkt_faces=result['faces'],
            maximum_affine_row_terms=max(len(form.terms) for row in forms for form in row)))
    family_checks=0
    for a in[Q(1,32),Q(3,5),Q(23,32),Q(127,128)]:
        assert geom.negative_m1_four(a).value(field.values)==4*field.negative_m1(a)
        assert geom.negative_m2_four(a).value(field.values)==4*negative(field,a)
        family_checks+=2
        A=field.initial_value(a)
        for name,fixed,expected in[('m1',2-a,field.positive_m1(a)),
                                   ('m2',Q(1),positive(field,a))]:
            cuts=inverse_cut(field,fixed,-a,Q(1),0,A)
            function=geom.positive_m1_four if name=='m1' else geom.positive_m2_four
            assert min(function(a,c).value(field.values) for c in cuts)==4*expected
            family_checks+=1
    for a,s in[(Q(1,32),Q(273,320)),(Q(1,4),Q(3,4)),
                (Q(3,5),Q(7,8)),(Q(127,128),Q(255,256))]:
        A=field.initial_value(a)
        cuts=inverse_cut(field,s,-a,s,0,A)
        value=min(geom.positive_m3_four(a,s,c).value(field.values) for c in cuts)/4
        route=[(Q(0),a),((s-a)/2,(s+a)/2),((s+1)/2,(s-1)/2),
               (Q(2),Q(1)),(Q(4),-Q(1))]
        assert value==field.unit_route_payoff(route)
        family_checks+=1
    report['checks']=dict(affine_in_all_field_values=affine_checks,
                          direct_record_comparisons=capture_checks,
                          minimizing_cutoff_and_branch=root_checks,
                          other_family_identities=family_checks,
                          total=affine_checks+capture_checks+root_checks+family_checks)
    report['cone_statement']='Subtract4V from every four-score matrix entry. Every route in the tetrahedron passes iff both4x4 matrices are copositive, equivalently PSD+entrywise nonnegative. Final rational verification uses face/KKT enumeration.'
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='branches'},indent=2))
    for item in report['branches']:
        print(json.dumps({k:v for k,v in item.items() if k not in('four_slack_matrix','four_score_forms')},indent=2))
    print('Saved',args.output)
if __name__=='__main__':main()
