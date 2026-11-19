"""Add checker metadata aliases to a new packet without changing source text.

Run before freezing and dispatching a new coding packet. Historical annotation
hashes must not be rebound in place. No network requests or inferred identities.
"""
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path

def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode('utf-8')

def normalize(packet):
    result=copy.deepcopy(packet)
    changes=[]
    ids=[e['source_id'] for e in packet['entries']]
    if len(ids)!=len(set(ids)):
        raise ValueError('Duplicate source identifiers')
    for entry in result['entries']:
        if not isinstance(entry.get('text'),str) or 'object_id' not in entry:
            raise ValueError('Each entry requires text and a declared object_id, possibly null')
        for old,new in [('revision','revision_id'),('git_blob_sha','blob_sha')]:
            value=entry.get(old)
            if value:
                if not isinstance(value,str):
                    raise ValueError('Nonstring metadata alias: '+entry['source_id'])
                if new in entry and entry[new]!=value:
                    raise ValueError('Conflicting metadata aliases: '+entry['source_id'])
                if new not in entry:
                    entry[new]=value
                    changes.append({'source_id':entry['source_id'],'from':old,'to':new,'value':value})
        if entry.get('kind')=='commit_metadata':
            obj=json.loads(entry['text'])
            value=obj.get('sha')
            url=obj.get('html_url')
            if not isinstance(value,str) or not re.fullmatch('[0-9a-fA-F]{40}',value):
                raise ValueError('Commit metadata lacks a full hexadecimal SHA')
            if not isinstance(url,str) or url!=entry['object_id'] or not url.endswith('/'+value):
                raise ValueError('Commit SHA, object identity, and retained URL disagree')
            if entry.get('revision_id') and entry['revision_id']!=value:
                raise ValueError('Commit revision alias conflicts with retained SHA')
            if not entry.get('revision_id'):
                entry['revision_id']=value
                changes.append({'source_id':entry['source_id'],'from':'sha in retained commit metadata and matching object URL','to':'revision_id','value':value})
    for old,new in zip(packet['entries'],result['entries']):
        if any(new[k]!=v for k,v in old.items()):
            raise ValueError('An original entry field changed')
    return result,changes

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path);p.add_argument('output',type=Path);p.add_argument('log',type=Path)
    a=p.parse_args()
    paths=[x.resolve() for x in [a.input,a.output,a.log]]
    if len(set(paths))!=3 or a.output.exists() or a.log.exists():
        p.error('Input, output, and log must be distinct; output and log must not exist')
    original=a.input.read_bytes();packet=json.loads(original)
    normalized,changes=normalize(packet);data=encoded(normalized)
    record={'release_version':'0.4.1','episode_id':packet['episode_id'],
            'original_packet_sha256':hashlib.sha256(original).hexdigest(),
            'adapted_packet_sha256':hashlib.sha256(data).hexdigest(),
            'added_metadata':changes,'source_text_unchanged':True,
            'original_entry_fields_unchanged':True}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.log.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_bytes(data);a.log.write_bytes(encoded(record))
    print(json.dumps({'status':'pass','added_fields':len(changes),'source_entries':len(packet['entries'])}))

if __name__=='__main__':main()
