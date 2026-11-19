"""Record proposed implications without modifying inherited coding or manuscripts."""
from pathlib import Path
import json

R=Path(__file__).resolve().parents[1]
P=json.loads((R/'common_input/packet.json').read_text())
T={e['source_id']:e['text'] for e in P['entries']}
def ev(s,q):
    i=T[s].index(q)
    return {'source_id':s,'span':{'start':i,'end':i+len(q),'quote':q}}
items=[
 {'impact_id':'BI01','prior_unit_ids':['U02'],'model_links':['IL01'],
  'action':'Clarify the preferred grammatical representation; retain proposition-specific recognition.',
  'assessment':'All three fresh coders use a regulative parse for review weighting. The inherited constitutive parse describes the criterion that constitutes review weight. These can preserve the same substantive arrangement; a harmonized preferred parse would improve comparability without implying a new authority finding. The later 32406-169 explanation recognizes content over count. Keep the narrower inherited local-support claim; the June guide documents discretionary merit weighting, not the exact April categorical sentence or every participant’s acceptance.',
  'evidence':[ev('32359-115','Reviews are weighted by the merit of their arguments, not the number of times they are posted.'),ev('32406-169','The technical content of those review comments is what matters, not how many are registered in what category.')],
  'proposed_status':'representation_clarification'},
 {'impact_id':'BI02','prior_unit_ids':['N16'],'model_links':['IL10'],
  'action':'Prefer a regulative representation of the transparency requirement and retain explicit governance-level alternatives.',
  'assessment':'All three fresh coders parse the explicit require predicate as regulative. The substantive finding remains a contested legitimacy claim about decision-making and diverse input. Target-level alternatives include epistemic and collective-choice readings. The inherited operational observed-action coding remains a cautious representation of the visible contribution exchange; no adopted constitutional redesign or authoritative value ranking follows.',
  'evidence':[ev('32406-228','Open-source principles are a little more evolved than "the code is public" and require transparent decision-making that respects diverse input.'),ev('32406-229','all I\'m trying to say is, don\'t drag "open source" into this conversation.')],
  'proposed_status':'representation_clarification'},
 {'impact_id':'BI03','prior_unit_ids':['U32'],'model_links':['IL07'],
  'action':'Add an explicit application-dispute qualification to the absolute translation-freeze claim.',
  'assessment':'The inherited U32 has text_only standing and dispute_present=false. All three fresh coders flag the absolute no-update statement as disputed in light of a source-update workaround. Prefer retaining its asserted status while setting dispute_present=true with a rationale that the scope/application, rather than the value of a freeze, faces a counterproposal. A disputed standing label is a compatible reporting alternative. No supplied evidence establishes a formally authorized exception or verifies final translation processing.',
  'evidence':[ev('33224-010','there must not be any translation source updates after the final translation string freeze.'),ev('33224-015','If this doc change is desired by contributors, and the 9 acks suggested that it is, then I think this workaround of modifying `bitcoin_en.ts` would be suitable.')],
  'proposed_status':'evidence_qualification'},
 {'impact_id':'BI04','prior_unit_ids':['U25'],'model_links':['IL06'],
  'action':'Retain the inherited local recognition of the conditional warning principle and clarify why it exceeds bare assent.',
  'assessment':'The later retained proposal body attributes, quotes, and applies the same conditional warning expectation to its own proposal. This meets the project’s local-recognition convention without requiring a binding project-wide rule. The two fresh text_only classifications demand more than that convention requires. The retained bodies establish a textual connection; absent body histories, they do not date the insertion of every sentence or isolate an effect on merger.',
  'evidence':[ev('32714-body','IMO we should not have removal warnings if there is no current plan to actually remove them.'),ev('33453-body','This echo’s Ava Chow’s comment from #32714 that “_IMO we should not have removal warnings if there is no current plan to actually remove them._”'),ev('33453-body','In months since that comment, partially due to increased feedback from Bitcoin Core users wanting to keep this option, there is even less likelihood of a near term plan to remove these options.')],
  'proposed_status':'retain_with_explanation'},
 {'impact_id':'BI05','prior_unit_ids':['U18','U39'],'model_links':['IL08','IL11'],
  'action':'Retain the distinction between general documented responsibilities and the specific claim in this exchange.',
  'assessment':'For U18, the general moderation guidance documents warnings and bans, but the particular announced future ban remains a specific assertion. For U39, broad maintainer release responsibility has documentary support and the particular backport decision has attributable local recognition. Documented and locally_supported labels therefore refer to different grains of evidence; retaining the inherited narrower labels avoids treating general documentation as verification of the specific act. No observed ban or network-wide authority follows.',
  'evidence':[ev('32406-252','Failure to keep future comments focused on review of the proposed changes will result in a temporary ban.'),ev('33453-018',"that's a maintainer's call (burden of backporting, badgering for review, and cutting RCs)"),ev('33453-069','I defer to you and the other maintainers on this.')],
  'proposed_status':'retain_with_explanation'},
 {'impact_id':'BI06','prior_unit_ids':['N14','N04'],'model_links':[],
  'action':'Preserve bounded alternatives for majority authority and deprecation status recognition.',
  'assessment':'N14 is not among the 46 inherited Round 11 units. Its unknown target level remains defensible because the majority claim supplies no electorate, threshold, jurisdiction, or procedure. N04 is also outside those 46. Exactly quoted assent supports a locally recognized interpretation of an institutional status if that status reading is explicit; ordinary terminological assent remains a bounded alternative. Neither case warrants an operative majority rule or a project-wide deprecation commitment.',
  'evidence':[ev('32359-227','Only the majority decides the winner.'),ev('32406-180',"Agree on all you said, that's what I tried to argue in few words :)")],
  'proposed_status':'retain_alternatives'}
]
inherited=json.loads((R/'prior_inputs/round11/inherited_units_used.json').read_text())
focal=set(P['selection_design']['focal_source_ids'])
covered=[{'unit_id':u['unit_id'],'source_id':u['source_id']} for u in inherited if u['source_id'] in focal]
claims=[
 {'claim_id':'K11_1','assessment':'The sampled role, moderation, and release claims remain compatible with differentiated control. The entire actor/event mapping was not independently revalidated in this round.'},
 {'claim_id':'K11_2','assessment':'All three reproduce merged versus closed-unmerged status boundaries. Distinguishing the actual closer or author withdrawal depends on additional Round 11 platform-event evidence outside this fresh focal test.'},
 {'claim_id':'K11_3','assessment':'All three reproduce the supplied patch sequence from added deprecation and warning, through softened warning, to removal of deprecation and warning. This remains a bounded repository-state claim.'},
 {'claim_id':'K11_4','assessment':'The retained attribution and quotation support a common warning principle across proposals with different recorded outcomes. Local recognition survives source reconciliation; timing of edited sentences and causal influence remain unestablished.'},
 {'claim_id':'K11_5','assessment':'The new round supplies overlapping repeatability evidence for selected inputs to the linked analysis. It does not turn the comparative overlay into an independently validated causal model.'},
 {'claim_id':'K11_6','assessment':'The sampled transparency and majority statements sustain comparison of contested legitimacy claims. The exact governance-level labels remain less secure than the observed disagreement, and no operative community voting procedure follows.'}
]
out={'scope':'Proposed implications only. No prior package, annotation, codebook, or manuscript is changed.',
     'inherited_round11_statement_units':len(inherited),'directly_overlapping_units':len(covered),
     'covered_units':covered,'important_scope_limit':'Twelve inherited units occur in the 24 focal sources. Additional context is shared, but podcast coding, the entire source corpus, the original Paper 1 sample, and the full causal or governance model are not revalidated by this round.',
     'unit_level_impacts':items,'model_claim_review':claims,
     'overall_assessment':'No sampled finding requires rebuilding the bounded repository reconstruction. Add overlap results, clarify coding and evidence conventions, and qualify the translation-freeze application. This assessment concerns the examined evidence rather than the complete model or corpus.',
     'applied_to_prior_files':False}
(R/'analysis/baseline_impact.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Recorded',len(items),'proposed implications and',len(covered),'overlapping inherited units.')
