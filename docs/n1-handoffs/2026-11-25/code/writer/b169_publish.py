import json,sys,subprocess as sp,time,hashlib
from pathlib import Path
r=Path.cwd();assert r.name=='b169-wt'
repo='stop-cran/learning-japanese';key='D4C9A275A218AF747B787AFA9D94B9D311BD26A7'
def read(*args):return sp.check_output(args).decode('utf8').strip()
def run(*args):sp.run(args,check=True)
def git(*args):return read('git',*args)
def gh(*args):return read('gh',*args)
def tool(name,*args):run(sys.executable,'-X','utf8','-B',name,*args)
def remote():return git('ls-remote','origin','refs/heads/main').split()[0]
def sign(msg):run('git','-c','gc.auto=0','-c','user.signingkey='+key,'commit','-S','-m',msg,'-m','Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>');run('git','verify-commit','HEAD')
def release(base):
    h=git('rev-parse','HEAD');assert not git('status','--porcelain') and remote()==base
    run('git','merge-base','--is-ancestor',base,h)
    run('git','-c','credential.helper=','-c','credential.helper=!gh auth git-credential','push','origin','HEAD:main')
    assert remote()==h
    sig=json.loads(gh('api',f'repos/{repo}/commits/{h}','--jq','.commit.verification | {verified,reason}'))
    assert sig=={'verified':True,'reason':'valid'},sig
    for _ in range(20):
        jobs=json.loads(gh('run','list','--repo',repo,'--workflow','378446878','--commit',h,'--branch','main','--event','push','--limit','1','--json','databaseId,headSha'))
        if jobs and jobs[0]['headSha']==h:break
        time.sleep(5)
    else:raise RuntimeError('No exact CI run yet')
    rid=str(jobs[0]['databaseId'])
    run('gh','run','watch',rid,'--repo',repo,'--exit-status','--interval','15','--compact')
    z=r.parent/('b169-zip-'+h[:12]);tool('docs/n1-reviews/batch-112-publication/verify-zip.py',str(r),h,str(z))
    return h,rid,z/'receipt.json'
assert gh('api','user','--jq','.login')=='stop-cran'
ledger='docs/n1-sources/batch-169-progress.json';closure='docs/n1-reviews/batch-169-closure';pub='docs/n1-reviews/batch-169-publication';j=json.loads(Path(ledger).read_bytes())
if sys.argv[1]=='content':
    assert j['status']=='review closed; publication pending' and git('rev-parse','HEAD')==j['integratedSnapshot'] and remote()==j['baseCommit'] and git('rev-parse','HEAD^1')==j['reviewedSnapshot'] and git('rev-parse','HEAD^2')==j['baseCommit']
    run('git','-c','core.safecrlf=false','add','--',ledger,closure);run('git','-c','core.whitespace=cr-at-eol','diff','--cached','--check')
    prov=json.loads(Path(closure,'provenance.json').read_bytes())
    for a,h in [(row['report'],row['sha256']) for row in prov['reports']]+[('reconciliation.md',prov['reconciliationSha256'])]:
        assert hashlib.sha256(sp.check_output(['git','show',':'+closure+'/'+a])).hexdigest()==h
    sign('Close independent reviews for N1 kanji batch 169')
    h,rid,z=release(j['baseCommit'])
    tool('tools/n1_record_publication.py','--batch','169','--commit',h,'--run-id',rid,'--zip-receipt',str(z),'--review-identity','Three serial reviewer processes; three distinct verified response and dispatch families. original reviewers confirmed actual revisions. See closure for tool-call and evidence limits.')
elif sys.argv[1]=='receipt':
    assert j['runtimePublished'] and j['accounting']['publishedPendingRecordsWithCards']==718 and j['accounting']['undelivered']==510
    base=j['publication']['commit'];assert base==git('rev-parse','HEAD')==remote()
    run('git','-c','core.safecrlf=false','add','--',pub,ledger);run('git','-c','core.whitespace=cr-at-eol','diff','--cached','--check')
    sign('Record verified B169 content CI and archive receipt')
    h,rid,z=release(base)
    orig=json.loads(Path(pub,'zip-receipt.json').read_bytes());got=json.loads(z.read_bytes())
    assert all(orig[k]==got[k] for k in ['contentVersion','manifestSha256','verifiedRuntimeHashes','zipFiles','retainedBytes','inflatedBytes'])
    members=json.loads(Path('docs/n1-sources/source-index.json').read_bytes())
    pending=[r for r in members if r['statusAtFreeze']=='pending'];delivered=[r for r in pending if Path(r['article']).is_file()]
    assert len(delivered)==718 and len(pending)-len(delivered)==510
    print('RECEIPT',h,rid,got['manifestSha256'],len(delivered),len(pending)-len(delivered))
else:raise ValueError(sys.argv[1])
