"""Prepare a field-masked proposition-alignment input after coding is frozen."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
assert (ROOT/'protocol/frozen_outputs.json').exists(), 'Freeze all three coders first.'
packet = json.loads((ROOT/'common_input/packet.json').read_text())
focal = packet['selection_design']['focal_source_ids']
out = {'purpose':'Align propositions against source meaning without agreement scores or institutional labels.',
       'masked_fields':['grammar','deontic_force','institution','statement_target_level','observed_action_level'],
       'caveat':'Component symbols and text remain available to distinguish focal actions and layers; masking is incomplete.',
       'sources':[]}
annotations = {l:json.loads((ROOT/f'reviewers/{l}/annotation.json').read_text()) for l in 'ABC'}
for sid in focal:
    entry = next(e for e in packet['entries'] if e['source_id']==sid)
    row = {'source_id':sid,'source_text':entry['text'],'reviewers':{}}
    for label,a in annotations.items():
        row['reviewers'][label] = [
            {'unit_id':u['unit_id'],'span':u['span'],'parse_mode':u['parse_mode'],
             'components':[{k:c[k] for k in ['symbol','text','basis','inference_note']}
                           for c in u['components']]}
            for u in a['units'] if u['source_id']==sid and u['record_role']=='statement']
    out['sources'].append(row)
(ROOT/'analysis/alignment_input.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Prepared field-masked alignment input for',len(out['sources']),'source records.')
