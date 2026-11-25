from pathlib import Path
import collections,json,gzip,hashlib,os,re,subprocess as sp,sys,urllib.parse,xml.etree.ElementTree as ET
import yaml
sys.path.insert(0,str(Path(__file__).parent))
from b170_content import words,cards,chars,EXC,EXTRA_MAP
r=Path.cwd();assert r.name=='b170-wt'
BASE='4dff7a1c46fa3b06de2f7a97004f9837ec2dc445'
src=Path('docs/n1-sources')
def get(n):return json.loads((src/n).read_bytes())
def dump(o):return json.dumps(o,ensure_ascii=False,indent=2)+'\n'
def git(*a):return sp.check_output(['git',*a])
def arr(seq):return '['+', '.join(seq)+']'
def fmt(t,d):
    for sym,folder,pattern in [('@','kanji','[一-鿿]'),('&','words','[ぁ-ヿ一-鿿]+')]:
        t=re.sub(sym+'('+pattern+')',lambda m:f"[{m[1]}]({'' if folder==d else '../'+folder+'/'}{m[1]}.md)",t)
    return t
EXTRA={'懲りる':'; 性懲りもなく, entry 1882440; 羹に懲りて膾を吹く, entry 2082570; 羹, entry 2002120; 膾, entry 1957170','遺憾':'; 遺憾なく, entry 2007260; 遺憾ながら, entry 2761370; 遺憾の意, entry 2851165','慶弔':'; 慶弔休暇, entry 2856288; 慶弔見舞金, entry 2873015; 弔事, entry 2116690; 弔辞, entry 1427690','感慨':'; 感慨深い, entry 2272660; 感慨無量, entry 1212320'}
FIX={'憤る':'1504640','遺言':'1159130','恨む':'1289780','嘆く':'1418090','喜ぶ':'1218760','喜び':'1606140','恨み':'1289740','怒る':'1445690'}
kd='https://www.edrdg.org/wiki/index.php/KANJIDIC_Project';jm='https://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project';JM=f'[JMdict]({jm})'
km=json.loads(Path('../b170-readings.json').read_bytes());memb=get('batch-170-membership.json');members=memb['membership'];base=memb['baseCommit']
assert base==BASE;sp.check_call(['git','merge-base','--is-ancestor',base,'HEAD'])
idx=get('source-index.json');source={x['kanji']:x['metadata'] for x in idx}
absent=[r['kanji'] for r in idx if not Path(r['article']).exists()]
assert [x[0] for x in cards]==members==[m['kanji'] for m in memb['members']]==[k for k in absent if int(source[k]['grade'])<=8][:9]+['遺']
assert '遺' in absent and int(source['遺']['grade'])==6
sys.path.insert(0,'tools');from audit_n1_pilot import offered_keys
from extract_n1_jmdict import extract,pinned_hash
raw=Path('../jmdict/JMdict_e.gz').read_bytes();h=pinned_hash('continuation');assert hashlib.sha256(raw).hexdigest()==h
QUAL={'ichi1','spec1','news1','gai1','news2','spec2'}
forms=collections.defaultdict(set);primary={row[3] for row in cards}|{x[2] for v in EXTRA_MAP.values() for x in v};families={};kanqual=set()
with gzip.open(Path('../jmdict/JMdict_e.gz')) as f:
    for _,e in ET.iterparse(f,events=['end']):
        if e.tag!='entry':continue
        eid=e.findtext('ent_seq')
        for k in e.findall('k_ele'):
            v=k.findtext('keb');forms[v].add(eid)
            if '憾' in v and {p.text for p in k.findall('ke_pri')}&QUAL:kanqual.add(v)
        if eid in primary:families[eid]=ET.fromstring(ET.tostring(e))
        e.clear()
assert kanqual=={'遺憾'},kanqual
out={};old={};changes=[];maps=[];supp=[];disp=[];projs=[];labels={};kex=[];wex=[]
ids=set()
def original(n):return git('show',base+':'+n).decode().replace('\r\n','\n')
def read(n):return out[n] if n in out else original(n)
def edit(n,a,b):
    text=read(n);assert text.count(a)==1,(n,a);old.setdefault(n,original(n));changes.append(dict(article=n,before=a,after=b));out[n]=text.replace(a,b)
def addline(c,line):
    n=f'kanji/{c}.md';a=read(n).split('## Common words\n',1)[1].split('\n## ',1)[0].strip().splitlines()[-1]
    edit(n,a,a+'\n'+line)
def cite(t,pre):
    found=set(pre)
    for v in re.findall(r'[ぁ-ヿ一-鿿々ー]+',re.sub(r'\]\([^)]*\)',']',t)):
        match=forms.get(v,set())
        if v in FIX and FIX[v] in match and not match&found:found.add(FIX[v]);continue
        if len(v)>1 and not match&found:
            if len(match)==1:found.update(match)
            elif match:print('CHECK',v,','.join(sorted(match)))
    return found
def head(n):return yaml.safe_load(read(n).split('---',2)[1])
def sensecount(w):return list(range(1,int(words[w][4].split('–')[-1])+1))
def mapping(c,w,spell,y,eid,senses):
    e=families[eid];ke=next(v for v in e.findall('k_ele') if v.findtext('keb')==spell);rr=next(v for v in e.findall('r_ele') if v.findtext('reb')==y)
    assert not ke.findall('ke_inf') and not rr.findall('re_inf') and (not rr.findall('re_restr') or spell in [x.text for x in rr.findall('re_restr')])
    assert len(senses)==len(e.findall('sense')),(w,len(e.findall('sense')))
    row=dict(kanji=c,article=f'words/{w}.md',newArticle=w in words,primaryReading=y,entryIds=[eid],senseNumbers=senses,priorityTags=[v.text for v in ke.findall('ke_pri') if v.text in QUAL],readingPriorityTags=[v.text for v in rr.findall('re_pri')])
    if not set(row['priorityTags'])&QUAL:row['exceptionReason']=EXC[c]
    print(c,spell,row['priorityTags'],row['readingPriorityTags'])
    return row
titles={z[0]:z[5] for z in cards}
for w,v in words.items():
    for k in v[3]:assert Path(f'words/{k}.md').exists(),(w,k)
for z in cards:
    for k in z[6]+z[7]:assert k in titles or Path(f'kanji/{k}.md').exists(),(z[0],k)
for c,w,y,eid,rd,title,ds,xs in cards:
    n=f'kanji/{c}.md';wp=f'words/{w}.md';m=source[c]
    linked={rd:[]};pre={eid}
    for w2,y2,eid2,rd2 in [(w,y,eid,rd)]+EXTRA_MAP.get(c,[]):
        row=mapping(c,w2,w2,y2,eid2,sensecount(w2));maps.append(row);linked.setdefault(rd2,[]).append((row,words[w2][0]));pre.add(eid2)
    senses=sensecount(w)
    gloss,kind,tags,exc,sensestr,intro,a,b,form,comp,note=words[w];components=re.findall('[一-鿿]',w)
    for ch in components:
        if ch!=c and ch not in members:supp.append({**maps[-1-len(EXTRA_MAP.get(c,[]))],'kanji':ch});addline(ch,f'- [{w}](../{wp}) {y} — {gloss}')
    if exc:wex.append(dict(word=w,exclude=exc))
    out[wp]=f'---\nword: {w}\nreading: {y}\ntitle: {gloss}\ntype: {kind}\nkanji: {arr(components)}\ntags: [{kind}, {tags}]\n'+(f'quiz_exclusions: {arr(exc)}\n' if exc else '')+f'---\n\n# {w} ({y}) — {gloss}\n\n'+fmt(f'## Meaning\n\n{intro}\n\n- {a}\n- {b}\n\n## How the kanji combine\n\n{form}\n\n## Synonyms and antonyms\n\n{comp}\n\n## Distinctive meaning\n\n{note}\n','words')+f'\nDictionary: [JMdict]({jm}), entry {eid}, {"sense" if len(senses)==1 else "senses"} {sensestr}{EXTRA.get(w,"")}; [Digital Daijisen, {w}](https://www.weblio.jp/content/{urllib.parse.quote(w)}).\n'
    ids.update(cite(out[wp].split('---',2)[-1],{eid}));ids.update(re.findall(r'\d{7}',EXTRA.get(w,'')))
    intro,cue,note,other=chars[c];table=[];common=[];proj=dict(kanji=c)
    for kind,field,cap in [('on','onyomi','Onyomi'),('kun','kunyomi','Kunyomi')]:
        picked=[v for v in m[field] if v in linked];proj['quiz'+cap]=picked;proj[kind+'Keys']=offered_keys(picked)
        for v in m[field]:
            d=dict(kanji=c,kind=kind,reading=v,selected=v in linked)
            if v in linked:
                ms=linked[v];cells=[f"[{mp['article'][6:-3]}](../{mp['article']}) {mp['primaryReading']} — {g}" for mp,g in ms];shown='; '.join(cells)
                common.extend('- '+x for x in cells);d.update(article=ms[0][0]['article'],reason='Mapped writing exemplifies this reading in the specified sense.' if len(ms)==1 else 'Mapped writings exemplify this reading in the specified sense.',entryIds=[i for mp,g in ms for i in mp['entryIds']])
            else:
                shown,es=other[v];d.update(reason=shown,entryIds=es.split());pre.update(es.split())
                if 'source-only' in shown:d['sourceOnly']=True
            table.append(f'| {v} | {kind} | {shown} |');disp.append(d)
    assert set(other)|set(linked)==set(m['onyomi'])|set(m['kunyomi']) and not set(other)&set(linked),c
    projs.append(proj)
    if xs:kex.append(dict(kanji=c,exclude=list(xs)))
    labels[c]=dict(title=title,distractors=list(ds),labels=[titles[d] if d in titles else head(f'kanji/{d}.md')['title'] for d in ds])
    body=fmt(f'\n# {c} — {title}\n\n**Strokes:** {m["strokes"]} · **Key (radical):** {m["radical"]} (no. {m["radicalNumber"]}) · **JLPT:** N1 (community list)\n\n## Meaning and origin\n\n{intro}\n\n**Shape mnemonic, not etymology:** {cue}\n\n## Readings\n\n| Reading | Type | Typical words |\n| --- | --- | --- |\n'+'\n'.join(table)+'\n\n## Common words\n\n'+'\n'.join(common)+f'\n\n## Notes\n\n{note}\n','kanji')
    refs=cite(body,pre);ids.update(refs)
    out[n]=f"---\nkanji: {c}\ntitle: {title}\njlpt: 1\ntags: [jlpt-n1, grade-{m['grade']}, structure-unclassified]\nstrokes: {m['strokes']}\nradical: {m['radical']}\nradicalNumber: {m['radicalNumber']}\nonyomi: {arr(m['onyomi'])}\nkunyomi: {arr(m['kunyomi'])}\nquizOnyomi: {arr(proj['quizOnyomi'])}\nquizKunyomi: {arr(proj['quizKunyomi'])}\ndistractors: {arr(ds)}\n"+(f'quiz_exclusions: {arr(xs)}\n' if xs else '')+'---\n'+body+f"\nMetadata: [KANJIDIC2]({kd}), frozen 2026-11-02; [Kanjipedia, {c}]({km[c]['url']}); [JMdict]({jm}), entries "+', '.join(sorted(refs))+'.\n'
assert sum(n.startswith('words/') for n in out)==10 and all(x['article'].startswith('kanji/') for x in changes)
# Constituent Metadata: all six constituents already have a Metadata line; append the word-pair entries to it.
os.environ.setdefault('N1_LEAN',str(Path('../lean').resolve()))
sys.path.insert(0,'docs/n1-reviews/batch-137-closure/confirm-packet/gpt/evidence');import meta_scan
PICK={'生産':'1378990'}
tmp=Path('../b170-scan');(tmp/'kanji').mkdir(parents=True,exist_ok=True)
for c in dict.fromkeys(i['kanji'] for i in supp):
    n=f'kanji/{c}.md';t=read(n);(tmp/n).write_text(t,'utf8')
    have=set(re.findall(r'\b\d{7}\b',t));gap=set()
    for row in meta_scan.scan(str(tmp),c):
        if ' part of ' in row:continue
        w,es=row.split(': ',1)[1].split(' ')[:2];es=es.split('/')
        if len(es)==1:gap.add(es[0])
        elif w in PICK and PICK[w] in es:gap.add(PICK[w])
        else:raise SystemExit(f'ambiguous gap {row}')
    rr=sorted(have|gap|{i['entryIds'][0] for i in supp if i['kanji']==c});ids.update(rr);lst=', '.join(rr)
    ml=[l for l in t.splitlines() if l.startswith('Metadata:')];assert len(ml)==1 and 'Word pairs' not in t,c
    a=ml[0];mids=set(re.findall(r'\b\d{7}\b',a));need=(gap|{i['entryIds'][0] for i in supp if i['kanji']==c})-mids
    if not need:continue
    if mids:
        # The Metadata line already lists JMdict entries: extend that list rather than repeating it.
        ms=list(re.finditer(r'entries (\d{7}(?:, \d{7})*)\.',a));assert len(ms)==1 and set(ms[0].group(1).split(', '))==mids,c
        b=a[:ms[0].start(1)]+', '.join(sorted(mids|need))+a[ms[0].end(1):]
    else:b=a+f' Word pairs: {JM}, entries {lst}.'
    edit(n,a,b)
notes={
 '慈':'慈善 (ichi1/news1) is a standard-use example for ジ (PDF p. 68); 善 has a card. いつく.しむ is shown with 慈しむ and 慈しみ and not offered.',
 '慕':'慕う (ichi1/news2) is the kun example in the standard-use table (PDF p. 140). ボ is shown with 慕情 and 思慕 and not offered.',
 '慨':'感慨 (news1) is a standard-use example for ガイ, the only reading in the table; 感 has a card. 憤慨 (ichi1/news1), the 憤 support, also writes ガイ and is a second mapping in the same reading row. KANJIDIC2 なげく is source-only: JMdict’s なげく entry 1418090 lists only 嘆く and 歎く, and a full scan of the pinned JMdict found no spelling containing 慨 with a reading beginning なげ.',
 '慶':'慶弔 carries news2 and spec2 (with nf33) on both spelling and reading; news2 and spec2 qualify under the owner decision in issue #60 comment 7112026459, applied since B160. It is a standard-use example for ケイ, the only reading in the table; 弔 has a card. 慶び and 慶ぶ are rarely used kanji forms of 喜び and 喜ぶ and are shown, not offered.',
 '憂':'憂慮 (news1) is a standard-use example for ユウ; 慮 has a card. The four kun readings are shown with dictionary words and not offered.',
 '憤':'憤慨 (ichi1/news1) is a standard-use example for フン; both constituents are in this batch. 憤る and 憤り are shown for いきどお.る and not offered.',
 '憾':'遺憾 (ichi1/news1) is the only example for 憾 in the standard-use table (PDF p. 30), and the full pinned-JMdict scan in the render asserts it is the only spelling containing 憾 that carries ichi1, news1, spec1, gai1, news2 or spec2 on the spelling. 遺 (source row 1091) is pulled into this batch so that the route has a constituent card. 憾む is shown for うら.む and not offered.',
 '懇':'懇談 (news1) supports コン; 談 has a card. The standard-use examples for コン are 懇切 (news2/spec2) and 懇親会; both are shown as dictionary words. No claim is made that one route is preferable. ねんご.ろ is shown with 懇ろ and not offered.',
 '懲':'懲りる (ichi1/news2) is the first kun example in the standard-use table (PDF p. 111). チョウ, こ.らす and こ.らしめる are shown with dictionary words and not offered.',
 '遺':'遺 (grade 6, source row 1091) is pulled forward because 遺憾 is the only qualifying route for 憾. 遺産 (ichi1/news1) is a standard-use example for イ; 産 has a card. 遺憾 also writes イ and is a second mapping in the same reading row. ユイ and のこ.す are shown with dictionary words and not offered.'}
acc=dict(frozenPendingRecords=1228,publishedPendingRecordsWithCards=718,publishedN1Additions=712,n2Placements=6,undelivered=510,localUnreviewedDrafts=10,notStarted=500,overallN1TaskComplete=False)
ledger=dict(schemaVersion=1,batch='170',governingIssue=60,base=base,baseCommit=base,selectionBase=base,members=members,membership=members,drafted=members,runtimePublished=False,status='unreviewed draft',selectionReason='First nine absent Jōyō rows on the 4dff7a1c receipt plus 遺 (source row 1091), pulled forward because 憾’s only qualifying route is 遺憾; 戒 moves to B171. Supports qualify through JMdict ichi1, news1, spec1 or gai1, with news2 and spec2 also qualifying under issue #60 comment 7112026459.',selectionNotes=notes,supportMappings=maps,supplementaryMappings=supp,requiredReciprocalPairs=[[i['kanji'],i['article']] for i in maps+supp],changedReusedPassages=changes,wordQuizAudit=dict(directExclusions=wex,evidence='docs/n1-reviews/batch-156-closure/packet/evidence/audits/word_quiz_audit.py run on the draft snapshot over all ten new words reported 0 problems.'),kanjiQuizAudit=dict(directExclusions=kex),dictionaryPackets=[dict(selection='batch-170-jmdict-selection.json',xml='batch-170-jmdict.xml')],readingDispositions=disp,curatedProjection=projs,quizAudit=labels,sources=dict(dictionaryPin='continuation-inputs.json',characterEntries=km),accounting=acc,limits=['Unpublished draft; no native-speaker or device acceptance.'])
ledger['sources']['dictionaryChecks']='Author re-read the Digital Daijisen bodies on Weblio for 慈善 (じぜん), 慕う (したう), 感慨 (かんがい), 憤慨 (ふんがい), 慶弔 (けいちょう), 憂慮 (ゆうりょ), 遺憾 (いかん), 遺産 (いさん), 懇談 (こんだん) and 懲りる (こりる); the 実用日本語表現辞典 entries 慶弔, 憂慮, 遺憾 and 慶; the Digital Daijisen character entries for 善, 慨, 慶, 弔, 慮, 遺, 産 and 談 cited in the word articles; and the official standard-use table rows for all ten kanji (PDF pages 68, 140, 25, 45, 151, 136, 30, 58, 111 and 13). Daijisen examples quoted in the articles are attributed to it; the bulleted example sentences are original.'
out[str(src/'batch-170-progress.json')]=dump(ledger);out[str(src/'batch-170-jmdict-selection.json')]=dump(dict(schemaVersion=1,batch='170',entryIds=sorted(ids)))
for n in out:assert (n in old and Path(n).read_text('utf8').replace('\r\n','\n')==old[n]) or not Path(n).exists(),n
xml=src/'batch-170-jmdict.xml';assert not xml.exists();xml.write_bytes(extract(raw,h,sorted(ids)))
for n,t in out.items():
    cr=n in old and b'\r\n' in git('show',base+':'+n);Path(n).write_bytes(t.replace('\n','\r\n' if cr else '\n').encode())
print(len(words),'new words;',len(ids),'families;',len(disp),'reading rows;',len(maps+supp),'pairs;',len(changes),'edits')
