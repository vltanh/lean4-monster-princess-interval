"""Restore an exact frozen-path checkpoint from text-safe compressed archives.

This reconstructs strategy geometry and numerical master weights. It does not
certify a value against an unrestricted opponent.
"""
from pathlib import Path
import argparse
import base64
import gzip
import hashlib
import json

def decode(path):
    raw=gzip.decompress(base64.b64decode(Path(path).read_bytes()))
    return raw,json.loads(raw)

def canonical(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':')).encode()

def restore(checkpoint,repository,output):
    raw,data=decode(checkpoint)
    if data['version']!=1:
        raise ValueError('unsupported checkpoint version')
    parts={}
    for name in ('base_rows','base_bank'):
        spec=data[name]; content,value=decode(Path(repository)/spec['path'])
        if hashlib.sha256(content).hexdigest()!=spec['uncompressed_sha256'] or len(value)!=spec['count']:
            raise ValueError('base snapshot identity failed: '+name)
        parts[name]=value
    rows=parts['base_rows']+data['new_rows']; atoms=parts['base_bank']+data['new_atoms']
    identity=data['identity']
    for name,value in [('rows',rows),('atoms',atoms)]:
        if hashlib.sha256(canonical(value)).hexdigest()!=identity[name+'_sha256']:
            raise ValueError('reconstructed '+name+' identity failed')
    if len(rows)!=identity['rows'] or len(atoms)!=identity['columns']:
        raise ValueError('reconstructed dimensions failed')
    if data['m1_complete_row_ids']!=[r['id'] for r in rows]:
        raise ValueError('M1 coverage row identities failed')
    master=data['master']
    if len(master['princess_weights'])!=len(rows) or len(master['monster_weights'])!=len(atoms):
        raise ValueError('probability dimensions failed')
    target=Path(output);target.mkdir(parents=True,exist_ok=True)
    for name,value in [('rows',rows),('bank',atoms),('master',master)]:
        (target/(name+'.json')).write_bytes(canonical(value)+b'\n')
    report={'scope':data['scope'],'identity':identity,'new_rows':len(data['new_rows']),
            'new_atoms':len(data['new_atoms']),'master_report':master['report'],
            'checkpoint_sha256':hashlib.sha256(raw).hexdigest()}
    (target/'restore_report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkpoint');parser.add_argument('repository');parser.add_argument('output')
    args=parser.parse_args()
    print(json.dumps(restore(args.checkpoint,args.repository,args.output),indent=2))
