#!/usr/bin/env python3
"""Independent rank-mask audit of the integer light-cell relaxation.

The verifier enumerates individual captured ranks, without the two-record
recurrence or its interpolation. Small complete-record instances must agree
exactly; coarse interpolated instances must be lower bounds.
"""
from pathlib import Path
from functools import lru_cache
import json,subprocess,tempfile
import numpy as np
from light_bellman import prepare,HERE
from continuum_field import ExtendedFieldMesh


def mask_optimum(cells,den):
    full=(1<<den)-1
    def captured(c):return ((1<<(den-c['a']-c['b']))-1)<<c['a']
    @lru_cache(None)
    def visit(i,mask):
        c=cells[i];answers=[];uncaught=full^mask
        if c['terminal']:
            left=(uncaught&((1<<c['a'])-1)).bit_count()
            right=(uncaught&(full^((1<<(den-c['b']))-1))).bit_count()
            assert left+right==uncaught.bit_count()
            la,lb,ra,rb=c['tail'];answers.extend((la*left+lb*right,ra*left+rb*right))
        for j in (c['right'],c['up']):
            if j<0:continue
            new=mask|captured(cells[j])
            answers.append(cells[j]['time']*(new^mask).bit_count()+visit(j,new))
        return min(answers)
    value=min(visit(i,captured(c))for i,c in enumerate(cells)if c['initial'])
    return value,visit.cache_info().currsize


def main():
    reports=[]
    with tempfile.TemporaryDirectory(prefix='light_bellman_audit_')as temp:
        work=Path(temp);binary=work/'solver'
        subprocess.run(['c++','-O3','-std=c++17',str(HERE/'light_bellman.cpp'),'-o',str(binary)],check=True)
        mesh=ExtendedFieldMesh([0.,.5,1.],1)
        ordinary=mesh.seed();outward=np.maximum(0.,-mesh.nodes[:,1])
        for name,values in [('ordinary',ordinary),('outward',outward),('mixture',(ordinary+outward)/2)]:
            source=work/f'{name}.json';mesh.save(source,values)
            folder=work/name;folder.mkdir();inp,cells,meta=prepare(source,16,16,1,folder)
            exact,states=mask_optimum(cells,16)
            original=inp.read_text().splitlines();bounds=[]
            for bins in [1,2,4,8,16]:
                header=original[0].split();header[1]=str(bins)
                inp.write_text(' '.join(header)+'\n'+'\n'.join(original[1:])+'\n')
                output=folder/f'{bins}.json'
                subprocess.run([str(binary),str(inp),str(output)],check=True,capture_output=True)
                value=json.loads(output.read_text())['bound_numerator']
                assert value<=exact,(name,bins,value,exact)
                if bins==16:assert value==exact,(name,value,exact)
                bounds.append(value)
            assert all(x<=y for x,y in zip(bounds,bounds[1:])),(name,bounds)
            reports.append(dict(field=name,cells=len(cells),independent_mask_states=states,
                                exact_numerator=exact,interpolated_numerators=bounds))
        overflow_rejected=False
        try:prepare(source,1,2**63,1,work)
        except AssertionError as error:
            assert 'overflow' in str(error);overflow_rejected=True
        assert overflow_rejected
    result=dict(scope='Independent finite verification of the global light-cell certificate algorithm; no new optimal-strategy claim',
                cases=reports,independent_rank_mask_equalities=3,coarse_lower_bounds=12,
                integer_overflow_guard_verified=True)
    (HERE/'light_bellman_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
