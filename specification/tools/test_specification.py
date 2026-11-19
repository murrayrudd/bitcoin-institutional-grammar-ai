"""Regression tests for demonstrated integrity failures; no accuracy estimate."""
import copy
import hashlib
import json
import tempfile
from pathlib import Path
import jsonschema
from check_annotation import check, profile

ROOT=Path(__file__).resolve().parents[1]
PACKET=ROOT/'calibration/packet.json'
BASE=json.loads((ROOT/'calibration/annotation.json').read_text())

def run():
    tests=[]
    def test(name,edit=None,expected='pass',code=None,flag=None):
        a=copy.deepcopy(BASE)
        if edit:edit(a)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'annotation.json';p.write_text(json.dumps(a))
            r=check(PACKET,p)
        ok=r['status']==expected
        if code:ok=ok and any(x['code']==code for x in r['errors'])
        if flag:ok=ok and any(x['code']==flag for x in r['review_flags'])
        tests.append({'test':name,'expected_status':expected,'observed_status':r['status'],
            'expected_error_code':code,'expected_review_flag':flag,'pass':ok,
            'observed_error_codes':sorted({e['code'] for e in r['errors']})})
    def unit(a,id):return next(u for u in a['units'] if u['unit_id']==id)
    def mutate_metadata(a):
        e=unit(a,'C01')['disposition_events'][0]['evidence'][0];e['source_id']='M32381'
        p=json.loads(PACKET.read_text());t=next(x['text'] for x in p['entries'] if x['source_id']=='M32381')
        q=e['span']['quote'];i=t.index(q);e['span'].update(start=i,end=i+len(q))
    test('Complete source-grounded development example')
    test('Wrong proposal with matching closed-unmerged labels',mutate_metadata,'fail','metadata_object')
    def false_only(a):
        e=unit(a,'C01')['disposition_events'][0]['evidence'][0];q='"merged": false';i=e['span']['start']+e['span']['quote'].index(q);e['span']={'start':i,'end':i+len(q),'quote':q}
    test('Unmerged is not enough to prove closed',false_only,'fail','status_parts')
    test('Later document cannot prove earlier standing',lambda a:unit(a,'C05')['institution']['documentary_support'][0].update(temporal_fit='established'),'fail','backdating')
    test('Dated support cannot omit revision basis',lambda a:unit(a,'C04')['institution']['documentary_support'][0].update(date_basis='unknown'),'fail','document_date')
    test('Broad documentary support remains acceptable',None,'pass','', 'document_scope')
    def false_exact(a):
        i=unit(a,'C04')['institution'];i['documentary_support'][0]['coverage']='exact';i['standing_profile']=profile(i)
    test('Mechanical checker cannot settle documentary entailment',false_exact,'pass',flag='document_scope')
    test('Ordinary assent cannot become expectation recognition',lambda a:unit(a,'C02')['institution']['recognition'][0].update(mode='ordinary_assent'),'fail','recognition_mode')
    def same_actor(a):
        u=unit(a,'C02');e=u['institution']['recognition'][0];e.update(mode='same_actor_restatement',speaker_relation='same_actor');e['evidence']=[{'source_id':u['source_id'],'span':u['span']}]
        u['institution']['standing_profile']=profile(u['institution'])
    test('Same speaker retained without interpersonal promotion',same_actor)
    def promote_same(a):same_actor(a);unit(a,'C02')['institution']['standing_profile']['recognition']='interpersonal'
    test('Same speaker cannot become interpersonal by label',promote_same,'fail','support_profile')
    test('Invented recognition episode rejected',lambda a:unit(a,'C02')['institution']['recognition'][0].update(independence_key='invented'),'fail','recognition_episode')
    def duplicate(a):
        i=unit(a,'C02')['institution'];i['recognition'].append(copy.deepcopy(i['recognition'][0]));i['standing_profile']['recognition']='repeated_interpersonal'
    test('Repeated comments in one episode do not establish repeated support',duplicate,'fail','support_profile')
    test('Scoped application challenge must remain visible',lambda a:unit(a,'C03')['institution'].update(dispute_present=False),'fail','challenge_flag')
    def broader_challenge(a):
        i=unit(a,'C03')['institution'];i['challenges'][0]['target']='broader_proposal';i['dispute_present']=False
    test('Broader challenge does not automatically dispute focal proposition',broader_challenge)
    def wrong_predicate(a):
        u=unit(a,'C01');c=next(c for c in u['components'] if c['symbol']=='A')
        # Exact word in another source passes string matching but fails declared local scope.
        t=next(e['text'] for e in json.loads(PACKET.read_text())['entries'] if e['source_id']=='32714-body');i=t.index('we should')
        c['evidence']=[{'source_id':'32714-body','span':{'start':i,'end':i+2,'quote':'we'}}]
    test('Exact pronoun from another governing clause rejected',wrong_predicate,'fail','predicate_scope')
    def bad_link(a):
        q=unit(a,'C06')['proposition']['qualifiers'][0];q.update(attachment='linked_unit',linked_unit_id='absent')
    test('Lost qualifier attachment detected',bad_link,'fail','qualifier_link')
    test('Unknown higher-level target with bounded alternatives permitted')
    test('Higher-level label requires evidence',lambda a:(unit(a,'C06').update(statement_target_level='constitutional',target_level_alternatives=['epistemic']),unit(a,'C06')['level_evidence'].update(evidence=[])),'fail','higher_level')
    def incomplete_summary(a):a['episode_summary']['observed_outcomes'][0]['evidence']=[]
    test('Summary must carry all clause evidence',incomplete_summary,'fail','claim_parts')
    test('Unresolved status recognition permitted')
    test('Question mismatch raises semantic review flag',lambda a:unit(a,'C09b').update(speech_act='asserted'),'pass',flag='question_audit')
    test('Old scalar standing is rejected by the new schema',lambda a:unit(a,'C02')['institution'].update(standing='locally_supported'),'fail','schema')
    schema=json.loads((ROOT/'protocol/annotation_schema.json').read_text());jsonschema.Draft202012Validator.check_schema(schema)
    tests.append({'test':'JSON Schema is well formed','pass':True})
    prov=json.loads((ROOT/'development/input_provenance.json').read_text())
    for x in prov['files']:
        ok=hashlib.sha256((ROOT/x['retained_path']).read_bytes()).hexdigest()==x['sha256']
        tests.append({'test':'Unchanged retained input '+x['retained_path'],'pass':ok})
    result={'status':'pass' if all(t['pass'] for t in tests) else 'fail',
        'passed':sum(t['pass'] for t in tests),'total':len(tests),'tests':tests,
        'interpretation':'These tests check intended safeguards and schema behavior on development material. They do not measure semantic accuracy, independent agreement, or generalization.'}
    (ROOT/'release/regression_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='tests'},indent=2))
    if result['status']!='pass':
        print(json.dumps([t for t in tests if not t['pass']],indent=2));raise SystemExit(1)

if __name__=='__main__':run()
