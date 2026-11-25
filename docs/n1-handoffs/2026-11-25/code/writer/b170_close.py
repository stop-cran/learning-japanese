import ast,hashlib,json,sys,subprocess as sp
from pathlib import Path
from b170_panel import base,git,s,runs,profiles

def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,obj):p.write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode())
src=Path('docs/n1-sources/batch-170-progress.json')
j=json.loads(src.read_bytes())
out=Path('docs/n1-reviews/batch-170-closure');reports=out/'reports'
stages={'initial':s}
for stage in ['followup','final']:
    if (runs/(stage+'-snapshot')).is_file():
        stages[stage]=(runs/(stage+'-snapshot')).read_text('ascii')
upstream=git('rev-parse','origin/main').decode().strip()
assert len(stages)>=2
if upstream==j['baseCommit']:
    assert git('rev-parse','HEAD').decode().strip()==list(stages.values())[-1]
    j['integration']=dict(upstream=upstream,merged=False,note='origin/main was unchanged since the base at closure, so the reviewed snapshot is closed directly without a merge.')
else:
    assert git('rev-parse','HEAD^1').decode().strip()==list(stages.values())[-1] and git('rev-parse','HEAD^2').decode().strip()==upstream
    j['integratedSnapshot']=git('rev-parse','HEAD').decode().strip()
    j['integration']=dict(upstream=upstream,merged=True)
assert (out/'reconciliation.md').is_file()
reports.mkdir(exist_ok=False);(out/'.gitattributes').write_bytes(b'* -text\n')
items=[];last=''
for stage,h in stages.items():
    for k,m,facet in profiles:
        n=k+'-'+stage
        ev=[json.loads(line) for line in (runs/(n+'.jsonl')).read_bytes().splitlines() if line.strip()]
        msgs=[e for e in ev if e['type']=='assistant.message'];calls=[e for e in ev if e['type']=='model.call_start']
        assert ev[-1]['type']=='result' and ev[-1]['exitCode']==0
        assert {e['data']['model'] for e in msgs}=={e['data']['model'] for e in calls}=={m}
        first,lastnow=calls[0]['timestamp'],ev[-2]['timestamp'];assert last<first<=lastnow;last=lastnow
        b=(runs/(n+'.md')).read_bytes();assert b==(msgs[-1]['data']['content'].rstrip()+'\n').encode()
        rp=reports/(n+'.md');rp.write_bytes(b)
        items.append(dict(stage=stage,snapshot=h,facet=facet,responseModel=m,dispatchModels=[m],firstCall=first,finished=last,assistantResponses=len(msgs),unsuccessfulToolCalls=sum(e['type']=='tool.execution_complete' and not e['data']['success'] for e in ev),report=rp.relative_to(out).as_posix(),sha256=sha(b)))
heads=list(stages.values())
save(out/'provenance.json',dict(batch=170,base=base,reports=items,reconciliation='reconciliation.md',reconciliationSha256=sha((out/'reconciliation.md').read_bytes()),teachingDiffSha256=[sha(git('-c','core.quotepath=false','diff',a,b,'--','words','kanji')) for a,b in zip(heads,heads[1:])],limits='Blind reviews and bounded confirmations, not native-speaker or Android acceptance.'))
j.update(status='review closed; publication pending',initialSnapshot=s,reviewedSnapshot=heads[-1],reviewClosure='../n1-reviews/batch-170-closure/provenance.json',limits=['Packet-based blind facet reviews and bounded confirmations; no native-speaker, device or whole-set acceptance.'])
j['accounting'].update(reviewClosedPendingRecordsWithCards=728,localUnreviewedDrafts=0)
j['finalCandidateChecks']=dict(contentVersion=json.loads(Path('manifest.json').read_bytes())['contentVersion'],localBudget=ast.literal_eval(sp.check_output([sys.executable,'-X','utf8','-B','tools/check_content_budget.py']).decode()),wordDirectPairs=sum(len(x['exclude']) for x in j['wordQuizAudit']['directExclusions']),kanjiDirectPairs=sum(len(x['exclude']) for x in j['kanjiQuizAudit']['directExclusions']))
save(src,j)
print(len(items),'reports archived')
