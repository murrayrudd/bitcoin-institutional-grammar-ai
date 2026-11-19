from pathlib import Path
import json, hashlib, copy
ROOT=Path.cwd()
packet_bytes=Path('packet.json').read_bytes()
p=json.loads(packet_bytes)
sources={e['source_id']:e for e in p['entries']}
texts={k:v['text'] for k,v in sources.items()}

def span(s,q,start=0):
    pos=texts[s].index(q,start)
    return {'start':pos,'end':pos+len(q),'quote':q}
def ev(s,q=None,start=0):
    return {'source_id':s,'span':span(s,texts[s] if q is None else q,start)}
def uev(u):return {'source_id':u['source_id'],'span':copy.deepcopy(u['span'])}
units=[]
def unit(n,s,q,role='statement',speech='proposed',mode='literal',force='recommendation',itype='undetermined',alt='',unc='',level='',scope='case_specific',flags=None,pres='none'):
    u={'unit_id':f'F03-U{n:02d}','source_id':s,'span':span(s,q),'parent_unit_id':None,
       'grammar':'regulative' if role=='statement' else 'not_institutional','speech_act':speech,'scope':scope,
       'components':[], 'institution':{'type':itype if role=='statement' else 'not_applicable','standing':'text_only' if role=='statement' else 'not_applicable','dispute_present':False,'rationale':'','evidence':[],'recognition':[],'authority_evidence':[]},
       'statement_target_level':'operational' if role=='statement' else 'not_applicable','observed_action_level':'operational',
       'level_rationale':level or ('The focal action concerns proposing, reviewing, or updating this contribution within ordinary repository work; it does not revise a recurring governance arrangement.' if role=='statement' else 'This visible communicative act occurs in ordinary contribution review; it is not a separately coded institutional prescription.'),
       'complexity_flags':flags or ['none'],'alternative_interpretation':alt,'confidence':'plausible' if role=='statement' else 'clear','uncertainty_reason':unc,
       'record_role':role,'parse_mode':mode,'deontic_force':force if role=='statement' else 'nondeontic','level_alternatives':[],
       'template_note':'','presentation':{'quotation':pres,'markup':'plain','rationale':'Supplied prose; no visible strike-through or suggestion fence.'},'disposition_events':[]}
    if role=='statement':
        u['institution']['rationale']='A case-specific technical or review proposal is expressed. The packet does not establish authorized rule making, enforcement, or recognition of an ongoing obligation.'
        u['institution']['evidence']=[uev(u)]
    else:u['institution']['rationale']='Record retained as '+role+' rather than as an additional institutional proposition.'
    units.append(u);return u

def comp(u,symbol,text,anchor=None,basis='explicit',role='local',note='',sid=None,start=None):
    sid=sid or u['source_id']; anchor=text if anchor is None else anchor
    if start is None:start=u['span']['start'] if sid==u['source_id'] and role=='local' else 0
    c={'symbol':symbol,'text':text,'basis':basis,'evidence':[ev(sid,anchor,start)],'inference_note':note,'occurrence_role':role}
    u['components'].append(c);return c

def recog(u,kind,target,evidence,rationale,basis='explicit'):
    u['institution']['recognition'].append({'kind':kind,'target':target,'basis':basis,'evidence':evidence,'rationale':rationale})
def disposition(u,kind,target,evidence,rationale,basis='explicit'):
    u['disposition_events'].append({'kind':kind,'target':target,'basis':basis,'evidence':evidence,'rationale':rationale})
body='pr7819:body'; c=lambda n:f'pr7819:comments:{n}'
meta='pr7819:metadata'; smeta='pr7819:supplement_metadata'; nextmeta='pr8182:supplement_metadata'
close7819=[ev(meta,'"closed_at": "2016-06-09T09:21:57+00:00"'),ev(meta,'"merged_at": null'),ev(meta,'"merged": false')]
close8182=[ev(nextmeta,'"number": 8182'),ev(nextmeta,'"closed_at": "2016-12-06T10:15:00Z"'),ev(nextmeta,'"merged": false'),ev(nextmeta,'"merged_at": null')]

u1=unit(1,body,'Adds a checkbox to the Send-Coins-Pannel (next to "Add Recipient") that allows to set the according nSequence to signal BIP125 RBF.',force='nondeontic',alt='Literal summary of the contributed implementation, without an independent governance prescription. Retained as the focal proposed edit rather than an institutional definition of the checkbox.',unc='The proposal is an engineering contribution; its institutional type and any generalized expectation remain unestablished.',level='The focal action is adding this checkbox in a contribution. Feature semantics do not constitute repository authority or network adoption.')
comp(u1,'I','Adds')
comp(u1,'Bdir','a checkbox')
comp(u1,'Cex','to the Send-Coins-Pannel (next to "Add Recipient")')
comp(u1,'Bdir,p','that allows to set the according nSequence to signal BIP125 RBF')
u1['institution'].update(standing='disputed',dispute_present=True,rationale='The stand-alone timing/scope of exposing this checkbox is questioned in comment 0. This contests immediate applicability, not the legitimacy of every possible checkbox implementation. It remains a technical contribution, with no supplied rule-making authority.')
u1['institution']['evidence'].append(ev(c(0)))
recog(u1,'response','this_proposition',[ev(c(0)),ev(body,'This PR does not include a way to actually replace a transaction with the GUI.')],'The response questions exposing this feature before actual replacement is possible; the deictic target is recovered from the contribution.',basis='context_inferred')
recog(u1,'reported_implementation','broader_proposal',[ev(c(8))],'The author reports that the contribution is included in #8182. This does not verify the precise patch there or integration into a repository.')
recog(u1,'recorded_status','broader_proposal',close7819,'Metadata records #7819 closed without merge. It does not reject each design proposition.')
disposition(u1,'reported_implemented','broader_proposal',[ev(c(8))],'Reported inclusion in a successor PR, not verified merge, exact implementation, or network adoption.')
disposition(u1,'recorded_closed_unmerged','broader_proposal',close7819,'The contribution was closed without recorded merge; no inference of sanction or substantive rejection follows.')

u2=unit(2,body,"So not sure if we want this without a GUI based replacement workflow (which I'm working on but it is a bigger chunk).",speech='asserted',mode='pragmatic',force='unresolved',alt='An expression of uncertainty about product usefulness, without a request to postpone acceptance. The source does not name merge or release as the requested action.',unc='The negative scope preference is tentative. Accepting the checkbox as a stand-alone contribution is a pragmatic interpretation of want this without, not an explicit integration instruction.')
comp(u2,'A','we',basis='context_inferred',role='semantic_inference',note='We is the expressed subject of want; treating that group as the decision makers for accepting the feature is inferred. Its membership and powers are unspecified.')
comp(u2,'I','defer accepting',anchor='not sure if we want this without',basis='context_inferred',role='semantic_inference',note='Reconstructs the tentative preference against accepting the feature alone; the source does not explicitly say defer or merge.')
comp(u2,'Bdir','this checkbox contribution',anchor='this',basis='context_inferred',role='semantic_inference',note='This is the object of want; its role as the target of accepting is reconstructed, and its referent is the contribution described in the preceding sentence.',start=u2['span']['start'])
comp(u2,'Cac','without a GUI based replacement workflow')
u2['institution']['rationale']='The author tentatively questions a contribution without the missing GUI workflow. This could be a proposed scope condition or only product-design uncertainty; no institutional type is established.'

u3=unit(3,body,"But I don't want to hold back review of this PR.",speech='asserted',force='nondeontic',itype='strategy_candidate',alt='A pragmatic invitation for others to review immediately is also plausible. The selected literal parse retains the author\'s own stated intention, without converting reviewers into the explicit actor.',unc='The author states an intention, not a binding commitment or a duty on reviewers.',level='The focal intention is not delaying review of this PR while the complementary workflow is being developed; this is ordinary operational review sequencing.')
comp(u3,'A','I')
comp(u3,'I',"don't want to hold back")
comp(u3,'Bdir','review of this PR')
u3['institution']['rationale']='The author articulates a personal process strategy: avoid holding back review while the broader replacement workflow is unfinished. The negative intention is nondeontic and provides no authority or duty.'

u4=unit(4,c(0),texts[c(0)].rstrip('\n'),speech='asserted',mode='pragmatic',alt='A technical judgment about the usefulness of an incomplete user interface; the recommendation to defer exposure is inferred.',unc='The reviewer hedges the judgment. Agreement later supports endorsement of the concern, not a recognized obligation.',level='The focal recommendation concerns when to expose this particular GUI feature, as part of operational review. The wallet capability condition is technical, not a new recurring review procedure.')
comp(u4,'I','defer exposing',anchor='Not sure it makes sense to expose',basis='context_inferred',role='semantic_inference',note='The recommendation to defer is reconstructed from the skeptical assertion. Expose itself is explicit; the negative timing force is inferred.')
comp(u4,'Bdir','this',note='This remains the explicit object of expose in the pragmatic parse. The preceding PR body resolves it to the proposed checkbox; no actor role is inferred for the author.')
comp(u4,'Cex','until the wallet actually _can_ do replacement')
u4['institution']['rationale']='This is a hedged, case-specific readiness recommendation. The author later agrees with it, but agreement with the technical condition does not establish authority or a socially binding expectation.'
recog(u4,'endorsement','this_proposition',[ev(c(2),'> Not sure it makes sense to expose this until the wallet actually can do replacement...'),ev(c(2),'Right. I totally agree.')],'An attributed repeat of the concern is followed by the author\'s direct agreement. This is endorsement, not expectation recognition.')
recog(u4,'response','this_proposition',[ev(c(2),"I'm working on the replacement GUI process but this can be reviewed already.")],'The author distinguishes ongoing GUI work from the possibility of reviewing the contribution now.',basis='context_inferred')

u5=unit(5,c(1),"I don't think the confirmation window deserves red text and the bang for it.",speech='asserted',mode='pragmatic',flags=['compound'],alt='An aesthetic evaluation of the interface, without a request to change it. Removal of the two forms of emphasis can also be represented as two coordinated edit children without changing the meaning.',unc='The edit action is inferred from a negative evaluation; no implementation or acceptance of that edit is supplied.')
comp(u5,'I','remove',anchor="don't think the confirmation window deserves",basis='context_inferred',role='semantic_inference',note='Negative evaluation of the current emphasis is interpreted as a recommendation to remove it.')
comp(u5,'Bdir','red text and the bang',basis='context_inferred',role='semantic_inference',note='The literal objects of deserves become the targets of the reconstructed remove action. Both coordinated display treatments are preserved as one coupled de-emphasis request.')
comp(u5,'Cex','from the confirmation window',anchor='the confirmation window',basis='context_inferred',role='semantic_inference',note='The literal subject is reconstructed as the interface location from which emphasis should be removed; it is not an explicit actor or object of remove.')

u6=unit(6,c(1),'Also "replaceable" there may have the user thinking that it\'s more replaceable than it is...',speech='asserted',mode='pragmatic',alt='A prediction of user misunderstanding offered as technical rationale, without a distinct wording-change request.',unc='No replacement wording is specified in this occurrence; the revision action is inferred. Comment 5 later proposes alternatives, but its provenance does not establish an earlier mandatory edit.')
comp(u6,'I','revise',anchor='may have the user thinking',basis='context_inferred',role='semantic_inference',note='The criticism of misleading wording is interpreted as a recommendation to revise it.')
comp(u6,'Bdir','"replaceable"',basis='context_inferred',role='semantic_inference',note='The literal subject of may have becomes the target of the reconstructed revision, so its role is inferred.')
comp(u6,'Cex','avoid suggesting greater replaceability than is available',anchor="may have the user thinking that it's more replaceable than it is",basis='context_inferred',role='semantic_inference',note='Recasts the stated concern as the purpose of the inferred edit, preserving the relative degree limitation without inventing technical capabilities.')

u7=unit(7,c(1),"arguably it should be the non-replacable case that should get red text (because you can't update fees later).",speech='proposed',mode='pragmatic',alt='Literal technical design claim with non-replacable case as grammatical subject of get; it does not establish an institutional actor or obligation.',unc='The implied editor and the strength of this hedged design recommendation are not specified.')
comp(u7,'D','should',start=texts[c(1)].index('that should')+5)
comp(u7,'I','apply',anchor='get red text',basis='context_inferred',role='semantic_inference',note='Reconstructs a contributor-facing edit from the desired display behavior; get is not treated as an action performed by a human actor.')
comp(u7,'Bdir','red text',basis='context_inferred',role='semantic_inference',note='The literal object of get becomes the target of the inferred apply action; its transformed role is recorded as inferred.')
comp(u7,'Bind','the non-replacable case',basis='context_inferred',role='semantic_inference',note='The literal subject of get becomes the receiving display case to which red text would be applied; this is a distinct receiver of acting on the red text.')
u7['institution']['rationale']='A hedged design recommendation shifts emphasis to the non-replacable case, with inability to update fees as its explicit technical reason. It does not select a rule or socially recognized norm.'

q8='I\'m wondering if we should even have a "replaceable switch" and not, instead, have an "adaptive fee switch" (that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees-- and the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks])'
u8=unit(8,c(1),q8,speech='proposed',flags=['compound','nested_component'],alt='Exploratory design speculation framed as wondering whether, rather than a settled recommendation. The adaptive switch includes a coupled computational and display specification, not independent duties to perform every user choice.',unc='We is an unspecified collaborative actor; no authorized collective-choice procedure or implementation commitment is shown.')
comp(u8,'A','we')
comp(u8,'D','should')
comp(u8,'I','have',start=texts[c(1)].index('instead, have')+9)
comp(u8,'Bdir','an "adaptive fee switch"')
comp(u8,'Bdir,p','(that does the compute N replacements, with locktimes in the future, and multiplicatively higher fees-- and the fee line changes to [x btc, or y,z,q,r after 3,4,5,6 blocks])')
comp(u8,'Cex','instead of the replaceable switch',anchor='even have a "replaceable switch" and not, instead, have',basis='context_inferred',role='semantic_inference',note='Preserves the contrasted alternative, including not/instead. It is not a universal ban on a replaceable switch, and the text does not impose explicit XOR exclusivity.')
recog(u8,'endorsement','this_proposition',[ev(c(3),'> '+q8),ev(c(3),'Yes. This might be a solution.')],'The exact proposal is quoted and tentatively endorsed as a possible solution; the endorsement does not verify implementation or recognized obligation.')

u9=unit(9,c(2),'> Not sure it makes sense to expose this until the wallet actually can do replacement...',role='quotation',speech='asserted',force='nondeontic',pres='repeated',alt='The italic emphasis on can in the original is absent in the repeated quotation; the proposition is otherwise recoverable.',unc='No edit history establishes why markup differs.')
u9['presentation']['rationale']='A block quote repeats the earlier comment, with its italic delimiters omitted; no independent endorsement is attributed to the quotation itself.'
u10=unit(10,c(2),'Right. I totally agree.',role='context',speech='reported_action',alt='Assent to the immediately quoted technical concern; it does not by itself acknowledge a binding rule.')
u11=unit(11,c(2),'this can be reviewed already.',speech='asserted',mode='literal',force='unresolved',alt='A capability/readiness claim that review is possible now. In context it also invites review despite unfinished GUI work; can is not automatically institutional permission.',unc='The source does not settle capability versus authorized discretion, nor identify who has authority to permit review.',level='The focal activity is immediate review of the existing PR, distinct from exposing the complete replacement feature. That sequencing is operational.')
comp(u11,'I','be reviewed')
comp(u11,'Bdir','this',basis='context_inferred',role='semantic_inference',note='This is the literal passive grammatical subject, interpreted as the target of review. Its Bdir role is semantically reconstructed, even though the word is explicit.')
comp(u11,'Cex','already')
u11['institution']['rationale']='The author asserts current reviewability and pragmatically invites review. Technical possibility versus permission remains unresolved; no authority evidence supports a rule.'

u12=unit(12,c(3),'> '+q8,role='quotation',speech='proposed',pres='repeated')
u12['presentation']['rationale']='The block quote repeats the adaptive-switch proposal already represented in unit F03-U08, without independent endorsement by mere repetition.'
u13=unit(13,c(3),'Yes. This might be a solution.',role='context',speech='reported_action',alt='Tentative approval of technical possibility rather than acceptance of an obligation or report of implementation.')
u14=unit(14,c(3),'I somehow was also trying to allow adding additional outputs (edit the transaction back in the sendcoins dialog).',speech='reported_action',force='nondeontic',itype='strategy_candidate',flags=['nested_component'],alt='A report of a previous development attempt, which can be treated as technical context rather than an independent institutional strategy.',unc='The report does not show completed behavior or a commitment to finish the attempt.')
comp(u14,'A','I')
comp(u14,'I','was also trying to allow')
comp(u14,'Bdir','adding additional outputs')
comp(u14,'Cex','(edit the transaction back in the sendcoins dialog)')
u14['institution']['rationale']='The author describes an attributable development approach: allow additional outputs by returning to the sendcoins dialog. This explicit attempted method is nondeontic, not an adopted contribution rule.'
recog(u14,'response','this_proposition',[ev(c(4))],'The following comment explains technical complexity specifically associated with additional outputs; the correspondence is substantive, but reply threading is unavailable.',basis='context_inferred')
recog(u14,'endorsement','this_proposition',[ev(c(5),'doing the add output thing would be pretty interesting...')],'The named add-output idea receives a favorable technical evaluation, without implementation or obligation.',basis='context_inferred')
u15=unit(15,c(3),'But maybe we should just focus on increasing the fees?',speech='question',alt='An exploratory question about scope rather than a settled requirement. The exclusive focus is a tentative proposal, not evidence that additional outputs were actually removed.',unc='The author uses maybe and a question; the packet does not record a final scope decision.')
comp(u15,'A','we')
comp(u15,'D','should')
comp(u15,'I','focus')
comp(u15,'Bdir','increasing the fees')
comp(u15,'Cex','just')

q16='workflow for additional outputs is more complex because you need to handle also making a child transaction of the original transaction for use in case the original confirms...'
u16=unit(16,c(4),q16,speech='asserted',force='unresolved',flags=['nested_component'],alt='A technical necessity explanation, not an institutional obligation. It can pragmatically advise the developer to accommodate a fallback child transaction if pursuing additional outputs.',unc='Need expresses an implementation dependency here; normative force and any institutional standing beyond the statement are unresolved.')
comp(u16,'A','you',note='The literal addressee of handle is supplied as you. It denotes the person implementing the discussed workflow; no named role, employment status, or maintainer authority is inferred.')
comp(u16,'D','need to')
comp(u16,'I','handle')
comp(u16,'Bdir','making a child transaction of the original transaction')
comp(u16,'Cac','when pursuing the additional-output workflow',anchor='workflow for additional outputs',basis='context_inferred',role='semantic_inference',note='The technical topic is reconstructed as the activation condition for the implied implementation advice; it is not an unqualified duty for all transactions.')
comp(u16,'Cex','for use in case the original confirms')
u16['institution']['rationale']='A technical necessity can function as advice in review, so the candidate is retained. The explicit need is not sufficient evidence of an institutional duty, rule, or enforceable standard.'
u17=unit(17,c(4),'and if you do this multiple times there is a bit of exponential blowup in the number of versions you must compute.',role='context',speech='technical_description',alt='Could contribute rationale for avoiding additional outputs. Must compute describes a technical computational burden, not a sanction or separately imposed duty.')

q18='Instead of the word "replacable" perhaps the word "updatable" or "amendable" would better express what the it\'ll do?'
u18=unit(18,c(5),q18,speech='question',mode='pragmatic',pres='proposed_wording',alt='An informational question about wording quality; the replacement request is pragmatic. Updatable and amendable are alternatives, not a requirement to use both.',unc='The source offers two alternatives without selecting one; no acceptance or completed wording change is established.')
comp(u18,'I','use',anchor='perhaps the word "updatable" or "amendable" would better express',basis='context_inferred',role='semantic_inference',note='The comparison of wording quality is reconstructed as a recommendation to use one of the offered alternatives.')
comp(u18,'Bdir','"updatable" or "amendable"',basis='context_inferred',role='semantic_inference',note='The proposed words are the literal subject of would better express; their Bdir role under use is inferred. The OR is retained inside the complete alternative object.')
comp(u18,'Cex','Instead of the word "replacable"')
u18['presentation']['rationale']='The sentence explicitly offers new replacement wording, retaining the original misspelling as the target and both suggested alternatives.'
recog(u18,'response','this_proposition',[ev(c(6))],'The spelling correction is conditional on not following Greg\'s suggestion. Matching alternative word content and adjacency support the reference, but the alias is not independently authenticated.',basis='context_inferred')
u19=unit(19,c(5),'doing the add output thing would be pretty interesting...',role='context',speech='asserted',alt='Positive technical evaluation of the add-output approach, without a new instruction to implement it.')
q20='though it would be nice to have a [send immediately] option which delays sending it, thus avoids having to do the extra just in case transactions if you amend with in the timeout. (and could also let you abort before it was initially set).'
u20=unit(20,c(5),q20,speech='proposed',flags=['nested_component'],alt='Exploratory feature speculation. The bracketed option label and its stated delay behavior are preserved together; the packet does not establish the option\'s on/off semantics. The abort effect is a possibility, not an independent instruction to abort.',unc='Conditional technical benefits and possible abort capability are proposed, not implemented or institutionally authorized.')
comp(u20,'I','have')
comp(u20,'Bdir','a [send immediately] option which delays sending it')
comp(u20,'Bdir,p','thus avoids having to do the extra just in case transactions if you amend with in the timeout. (and could also let you abort before it was initially set).',note='These adjuncts describe the option\'s stated conditional benefit and possible additional capability. They do not activate a duty to amend or abort, and are not an institutional consequence relation.')

q21='Hate to be that guy Jonas, but I believe "replaceab"... is the more accepted spelling, if you don\'t go with Greg\'s suggestion.'
u21=unit(21,c(6),q21,speech='asserted',mode='pragmatic',pres='proposed_wording',alt='A statement about accepted spelling rather than a direct editorial instruction. The quoted fragment replaceab is deliberately incomplete in the supplied text and is not expanded to a guessed full word.',unc='The request is indirect and conditional. Jonas and Greg are the names as supplied; their formal roles are not known.')
comp(u21,'A','Jonas',basis='context_inferred',role='context_reference',note='The vocative supplies an addressee, reconstructed as the actor of the inferred spelling edit; being named is not itself an explicit grammatical actor role.')
comp(u21,'I','use',anchor='is the more accepted spelling',basis='context_inferred',role='semantic_inference',note='The asserted spelling preference is interpreted as an editorial recommendation.')
comp(u21,'Bdir','"replaceab"...',basis='context_inferred',role='semantic_inference',note='The literal subject of is the more accepted spelling becomes the target of use. The exact incomplete spelling fragment and ellipsis are preserved.')
comp(u21,'Cac',"if you don't go with Greg's suggestion")
u21['presentation']['rationale']='The supplied proposed spelling is an explicitly quoted fragment followed by ellipsis; it is not silently completed.'

u22=unit(22,c(7),'Needs rebase.',speech='asserted',mode='pragmatic',itype='norm_candidate',alt='A technical diagnosis of stale contribution state, without a binding request. The terse form does not identify a responsible actor or a formally authorized condition of integration.',unc='The review context supports an expectation to rebase this PR, but no response, implementation, enforcement, or authority is supplied.')
comp(u22,'D','Needs')
comp(u22,'I','rebase',basis='context_inferred',role='semantic_inference',note='Rebase is a noun complement in the terse diagnosis; it is reconstructed as the requested action.')
comp(u22,'Bdir','this PR (#7819)',anchor='Needs rebase.',basis='context_inferred',role='semantic_inference',note='The action target is omitted in the utterance. The source object_id identifies PR #7819; no later successor PR is substituted.')
u22['institution']['rationale']='Needs rebase expresses a case-specific review expectation, retained as a text-only norm candidate. Its technical-diagnosis alternative remains open; no authority or actual rebase is evidenced.'

u23=unit(23,c(8),'Closing in favor of #8182 (included there).',role='context',speech='reported_action',alt='A report of replacement by another contribution, not a rejection of every comment or evidence of repository integration.',unc='Included there is an author report; the packet has successor metadata but no successor patch.')
disposition(u23,'recorded_closed_unmerged','broader_proposal',close7819,'Metadata verifies the closure status of #7819 reported in this context; it does not establish rejection or a sanction.')

relations=[]
def rel(a,b,t,evs,rationale,basis='context_inferred',logic='not_applicable'):
    relations.append({'from_unit_id':a['unit_id'],'to_unit_id':b['unit_id'],'type':t,'basis':basis,'rationale':rationale,'evidence':evs,'logic_scope':logic})
rel(u4,u1,'challenges',[uev(u4),ev(body,'This PR does not include a way to actually replace a transaction with the GUI.')],'Challenges the timing of exposing the proposed feature without actual replacement capability; it does not challenge every possible checkbox implementation.')
rel(u9,u4,'quotes',[uev(u9),uev(u4)],'Attributed block quote repeats the earlier concern; omission of italic delimiters does not change its referent.','explicit')
rel(u4,u10,'uptake',[uev(u9),uev(u10)],'The request-like concern receives direct agreement after its quotation. Agreement is an endorsement, not expectation recognition.','explicit')
rel(u11,u3,'clarifies',[uev(u11),uev(u3),ev(c(2),"I'm working on the replacement GUI process but this can be reviewed already.")],'Clarifies the author\'s earlier intention not to delay review by distinguishing reviewability from completion of the companion GUI.')
rel(u12,u8,'quotes',[uev(u12),uev(u8)],'The adaptive-switch proposition is repeated as a block quote.','explicit')
rel(u8,u13,'uptake',[uev(u12),uev(u13)],'The exactly quoted proposal receives tentative endorsement as a possible solution, not a verified design decision.','explicit')
rel(u15,u8,'clarifies',[uev(u12),uev(u13),uev(u15)],'The response narrows the discussed direction toward fee increases while retaining question form; it does not prove that the alternative was adopted.')
rel(u16,u14,'challenges',[uev(u14),uev(u16)],'Explains complexity of the additional-output approach. This is a challenge to implementation simplicity, not a prohibition or sanction.')
rel(u17,u16,'clarifies',[uev(u16),uev(u17)],'The coordinated continuation adds the repeated-use computational complication to the child-transaction requirement.','explicit')
rel(u14,u19,'uptake',[uev(u14),uev(u19)],'The later add-output evaluation corresponds to the author\'s attempted approach, but remains a favorable technical response.')
rel(u18,u6,'clarifies',[uev(u6),uev(u18)],'The same contributor later offers concrete wording alternatives for the earlier misleading-label concern; causation and edit history remain unobserved.')
rel(u21,u18,'clarifies',[uev(u21),uev(u18)],'The spelling fallback is expressly conditional on not taking Greg\'s suggestion; matching wording content supports reference to the alternatives in comment 5, without assuming a formal actor identity.')
rel(u22,u23,'temporal',[uev(u22),uev(u23)],'The supplied comment timestamps place the rebase request before the closure report on 2016-06-09. This is ordering only; closure is not evidence of rebase compliance or punishment.')

screen_reasons={
body:'Candidate: proposed checkbox edit, tentative scope condition, and author strategy not to delay review. Ongoing GUI work, refactoring provenance, and unrendered image links are context.',
c(0):'Candidate: hedged recommendation to defer exposure until replacement capability, with a literal technical-judgment alternative.',
c(1):'Candidate: coordinated removal of visual emphasis, indirect wording revision, alternative emphasis for the non-replacable case, and the qualified adaptive-fee-switch proposal.',
c(2):'Candidate: review-now statement with unresolved capability/permission force. The repeated quotation and direct agreement are separately retained without creating extra prescriptions.',
c(3):'Candidate: reported development strategy for additional outputs and tentative fee-only focus. Repeated quotation and possible-solution assent are nonstatement records.',
c(4):'Candidate: technical necessity concerning a child transaction, retained with an unresolved institutional reading. Repeated-use computational blowup is technical context, not an institutional sanction.',
c(5):'Candidate: alternative wording suggestion and delayed-send option with all conditional benefits retained. Interest in additional outputs is an evaluative response.',
c(6):'Candidate: indirect conditional spelling edit, preserving the incomplete quoted fragment and the alternative suggestion condition.',
c(7):'Candidate: terse rebase expectation with technical-diagnosis alternative and no inferred authority.',
c(8):'Context only: author reports closure and inclusion in successor #8182; no independently prescribed recurring governance arrangement is asserted.',
meta:'Supplement screened as context: original PR state and file-change metadata provide bounded outcome evidence. This is not an exhaustive extraction claim or proof that metadata has no institutional relevance.',
smeta:'Supplement screened as context: archived #7819 metadata corroborates closure without merge. Its merge_commit_sha does not override merged=false or prove integration.',
nextmeta:'Supplement screened as context: #8182 is a distinct successor object, also closed without merge. No successor body, discussion, or patch is supplied for exhaustive proposition extraction.'}
patch_reasons={0:'Proposed checkbox text and tooltip, including higher-fee and unconfirmed-transaction qualifiers.',1:'Call-site changes and confirmation text; the retained head still shows red styling, replacable, and an exclamation mark, without a trustworthy review-to-patch chronology.',2:'Wallet-model forwarding of the opt-in flag into transaction creation.',3:'Wallet-model function signature and false default.',4:'Transaction flags, sequence computation, and signing-related changes.',5:'Flag enum and transaction-creation signature; these technical definitions are not automatically institutional constitutions.'}
for k,v in patch_reasons.items():screen_reasons[f'pr7819:patch:{k}']='Supplement screened as context: '+v+' The selection design does not require exhaustive extraction from supplemental patches.'
screen=[]
for e in p['entries']:
    us=[u for u in units if u['source_id']==e['source_id']]
    d='candidate' if any(u['record_role']=='statement' for u in us) else 'context_only' if e['text'].strip() else 'empty'
    screen.append({'source_id':e['source_id'],'disposition':d,'reason':screen_reasons[e['source_id']],'unit_ids':[u['unit_id'] for u in us]})
summary={
'observed_outcomes':[
 {'claim':'The author reports closing #7819 in favor of #8182 and says the contribution is included there. The #7819 metadata records closure on June 9, 2016 with merged=false and no merge timestamp. This establishes closure without recorded integration, not rejection of every proposed edit.', 'evidence':[uev(u23)]+close7819},
 {'claim':'The separately supplied successor record #8182 is also closed without merge, with a December 6, 2016 closure timestamp. A merge_commit_sha string in the archived metadata is not evidence that this successor was merged.', 'evidence':close8182+[ev(nextmeta,'"merge_commit_sha": "1987a7a11a1a9513f2eca7a54c751178e2ef518c"')]},
 {'claim':'The retained #7819 head patch contains red confirmation styling and the message "This transaction is replacable (optin-RBF)!". It therefore does not demonstrate implementation of the requested visual de-emphasis or the proposed replacement spellings; the snapshot supplies no causal edit chronology.', 'evidence':[ev('pr7819:patch:1','+        questionString.append("<hr /><span style=\'color:#aa0000;\'>");\n+        questionString.append(tr("This transaction is replacable (optin-RBF)!"));'),uev(u5),uev(u18),uev(u21)]}
],
'mechanisms':[
 {'category':'review_coordination','claim':'The author states an intention not to delay review while the GUI replacement workflow is unfinished. A reviewer questions exposure before replacement is possible; the author quotes that concern, agrees, and says the existing contribution can already be reviewed. This supports a communicative distinction between reviewing an incomplete contribution and exposing its feature; it does not demonstrate authority or actual review completion.', 'evidence':[ev(body,'This PR does not include a way to actually replace a transaction with the GUI.'),uev(u3),uev(u4),uev(u9),uev(u10),ev(c(2),"I'm working on the replacement GUI process but this can be reviewed already.")], 'unit_ids':[u['unit_id'] for u in [u3,u4,u9,u10,u11]],'alternative_explanation':'The exchange may merely describe product readiness and technical reviewability, without establishing a shared institutional expectation about staging review.','status':'supported_sequence'},
 {'category':'reason_giving','claim':'The adaptive-fee-switch suggestion receives an attributed quotation and a tentative possible-solution response. The author reports trying additional outputs and asks whether to focus only on increasing fees. A subsequent comment explains child-transaction handling and repeated-use version growth for additional outputs. This is a source-supported exchange of design alternatives and reasons, without a demonstrated final design or causal implementation effect.', 'evidence':[uev(u8),uev(u12),uev(u13),uev(u14),uev(u15),uev(u16),uev(u17)],'unit_ids':[u['unit_id'] for u in [u8,u12,u13,u14,u15,u16,u17]],'alternative_explanation':'Participants may be exploring independent possibilities rather than negotiating a binding scope decision. The complexity explanation occurs after the fee-focus question and cannot be assumed to have caused it.','status':'supported_sequence'},
 {'category':'scope_management','claim':'The author reports replacing this contribution with #8182, where it is said to be included. Metadata confirms #7819 closed without merge and separately records #8182 closed without merge. The report supports relocation of the proposal as the stated reason for closure; it does not verify code transfer, integration, or a response to the earlier rebase request.', 'evidence':[uev(u23)]+close7819+close8182,'unit_ids':[u23['unit_id']],'alternative_explanation':'The closure statement may summarize a broader reworking not visible in this packet. Successor metadata does not establish preservation of the exact code or review suggestions.','status':'supported_sequence'}
],
'missing_evidence':[
 'No complete edit history, reliable reply threading, or original comment IDs beyond corpus array positions.',
 'Image links are not rendered; visual claims rely only on supplied prose and the retained #7819 patch.',
 'No patches, full discussion, or verified incorporation details for #8182; #7159 is only referenced, without outcome evidence.',
 'No evidence of recognized rule-making authority, enforcement, sanctions, or expectation recognition sufficient for locally_supported standing.',
 'No supplied verification of a rebase, removal of display emphasis, chosen replacement wording, delayed-send option, adaptive-fee switch, or completed replacement GUI.',
 'No evidence of repository integration or Bitcoin network adoption, nor of constitutional or epistemic governance activity.'
],
'unresolved_questions':[
 'Do the hedged readiness and review-now statements prescribe contribution conduct or only express technical feasibility and product-design judgments?',
 'Does Needs rebase impose an expected contribution step in this episode or merely diagnose stale code?',
 'What is the precise meaning of the [send immediately] option label given the explicitly described delay behavior?',
 'Which code and discussion points were included in #8182, and what happened beyond its separately recorded unmerged closure?',
 'Were any of the wording, display, or scope suggestions implemented in another revision or contribution not supplied here?'
]}
a={'schema_version':'0.3','run_id':'F03_v03_r3','episode_id':'F03','packet_sha256':hashlib.sha256(packet_bytes).hexdigest(),'entry_screening':screen,'units':units,'relations':relations,'episode_summary':summary}
Path('annotation.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
Path('annotation.first_complete.json').write_bytes(Path('annotation.json').read_bytes())
print(json.dumps({'units':len(units),'statements':sum(u['record_role']=='statement' for u in units),'relations':len(relations),'entries':len(screen),'packet_sha256':a['packet_sha256']}))
