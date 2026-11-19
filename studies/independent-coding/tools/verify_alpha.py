"""Check nominal alpha against a published numerical example, not our own outputs.

Data: Hayes & Krippendorff (2007), Table 1, DOI 10.1080/19312450709336664.
Their reported nominal alpha is 0.4765; the example includes missing ratings.
"""
import json
from supplementary_alpha import nominal_alpha,R
data='''1 1 2 . 2
1 1 0 1 .
2 3 3 3 .
. 0 0 . 0
0 0 0 . 0
0 0 0 . 0
1 0 2 . 1
1 . 2 0 .
2 2 2 . 2
2 1 1 1 .
. 1 0 0 .
0 0 0 0 .
1 2 2 2 .
3 3 2 2 3
1 1 1 . 1
1 1 1 . 1
2 1 2 . 2
1 2 3 3 .
1 1 0 1 .
0 0 0 . 0
0 0 1 1 .
0 0 . 0 0
2 3 3 3 .
0 0 0 0 .
1 2 . 2 2
0 1 1 1 .
0 0 0 1 0
1 2 1 2 .
1 1 2 2 .
1 1 2 . 2
1 1 0 . 0
2 1 2 1 .
2 2 . 2 2
3 2 2 2 .
2 2 2 . 2
2 2 3 . 2
2 2 2 . 2
2 2 . 1 2
2 2 2 2 .
1 1 1 . 1'''
rows=[[v for v in line.split() if v!='.'] for line in data.splitlines()]
result=nominal_alpha(rows)
pairs=sum(len(row)*(len(row)-1)//2 for row in rows)
assert len(rows)==40 and result['labels']==159 and pairs==239
assert round(result['alpha'],4)==0.4765
out={'status':'pass','reference':'Hayes and Krippendorff (2007), Table 1 and page 6; DOI 10.1080/19312450709336664','source_url':'https://chukharev.github.io/520/Hayes_Krippendorff_2007.pdf','expected_nominal_alpha_rounded':0.4765,'computed_nominal_alpha':result['alpha'],'units':len(rows),'labels':result['labels'],'unordered_pairs':pairs,'purpose':'Independent published numerical benchmark, including variable coder counts and missing ratings. Does not validate semantic alignment or source interpretation.'}
(R/'analysis/alpha_verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
