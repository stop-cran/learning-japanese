from pathlib import Path
import collections,json,gzip,hashlib,os,re,subprocess as sp,sys,urllib.parse,xml.etree.ElementTree as ET
import yaml
sys.path.insert(0,str(Path(__file__).parent))
from b169_content import words,cards,chars,EXC,REUSE
r=Path.cwd();assert r.name=='b169-wt'
BASE='894d30525e87a394b0b5a6de9767d2d1084b6ed3'
src=Path('docs/n1-sources')
def get(n):return json.loads((src/n).read_bytes())
def dump(o):return json.dumps(o,ensure_ascii=False,indent=2)+'\n'
def git(*a):return sp.check_output(['git',*a])
def arr(seq):return '['+', '.join(seq)+']'
def fmt(t,d):
    for sym,folder,pattern in [('@','kanji','[一-鿿]'),('&','words','[ぁ-ヿ一-鿿]+')]:
        t=re.sub(sym+'('+pattern+')',lambda m:f"[{m[1]}]({'' if folder==d else '../'+folder+'/'}{m[1]}.md)",t)
    return t
EXTRA={'忠実':'; the separate word まめ written 忠実, entry 2827450','忍ぶ':'; 人目を忍ぶ, entry 2126560; 偲ぶ, entry 1321590; 忍びない, entry 2154730','郷愁':'; 懐古, entry 1200550','愚か':'; …はおろか (疎か), entry 2832535'};FIX={'故郷':'2853884','疎か':'2832535'};kd='https://www.edrdg.org/wiki/index.php/KANJIDIC_Project';jm='https://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project';JM=f'[JMdict]({jm})'
km=json.loads(Path('../b169-readings.json').read_bytes());memb=get('batch-169-membership.json');members=memb['membership'];base=memb['baseCommit']
assert base==BASE;sp.check_call(['git','merge-base','--is-ancestor',base,'HEAD'])
idx=get('source-index.json');source={x['kanji']:x['metadata'] for x in idx}
assert [x[0] for x in cards]==members==[m['kanji'] for m in memb['members']]==[r['kanji'] for r in idx if int(r['metadata']['grade'])<=8 and not Path(r['article']).exists()][:10]
sys.path.insert(0,'tools');from audit_n1_pilot import offered_keys
from extract_n1_jmdict import extract,pinned_hash
raw=Path('../jmdict/JMdict_e.gz').read_bytes();h=pinned_hash('continuation');assert hashlib.sha256(raw).hexdigest()==h
forms=collections.defaultdict(set);primary={row[3] for row in cards};families={}
with gzip.open(Path('../jmdict/JMdict_e.gz')) as f:
    for _,e in ET.iterparse(f,events=['end']):
        if e.tag!='entry':continue
        eid=e.findtext('ent_seq')
        for v in e.findall('k_ele/keb'):forms[v.text].add(eid)
        if eid in primary:families[eid]=ET.fromstring(ET.tostring(e))
        e.clear()
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
QUAL={'ichi1','spec1','news1','gai1','news2','spec2'}
def mapping(c,w,spell,y,eid,senses):
    e=families[eid];ke=next(v for v in e.findall('k_ele') if v.findtext('keb')==spell);rr=next(v for v in e.findall('r_ele') if v.findtext('reb')==y)
    assert not ke.findall('ke_inf') and not rr.findall('re_inf') and (not rr.findall('re_restr') or spell in [x.text for x in rr.findall('re_restr')])
    row=dict(kanji=c,article=f'words/{w}.md',newArticle=w in words,primaryReading=y,entryIds=[eid],senseNumbers=senses,priorityTags=[v.text for v in ke.findall('ke_pri') if v.text in {'ichi1','spec1','news1','gai1','news2','spec2'}],readingPriorityTags=[v.text for v in rr.findall('re_pri')])
    return row
titles={z[0]:z[5] for z in cards}
ATTR={'惨':'ichi1 and news2 are recorded on both the 惨め spelling and the reading みじめ; the kana-headed article teaches this entry, sense 1.'}
for c,w,y,eid,rd,title,ds,xs in cards:
    n=f'kanji/{c}.md';wp=f'words/{w}.md';m=source[c];ru=REUSE.get(c)
    if ru:
        spell=ru['spelling'];senses=ru['senses'];gloss=ru['gloss']
        row=mapping(c,w,spell,y,eid,senses);row.update(spelling=spell,senseNumber=senses[0],priorityTagAttribution=ATTR[c])
        assert head(wp)['title']==gloss and head(wp)['reading']==y;edit(wp,ru['anchor'],ru['anchor']+ru['add'])
    else:
        spell=w;senses=list(range(1,int(words[w][4].split('–')[-1])+1));row=mapping(c,w,spell,y,eid,senses)
    if not set(row['priorityTags'])&QUAL:row['exceptionReason']=EXC[c]
    print(c,spell,row['priorityTags'],row['readingPriorityTags'])
    maps.append(row);linked={rd:row};pre={eid}
    if not ru:
     gloss,kind,tags,exc,sensestr,intro,a,b,form,comp,note=words[w];components=re.findall('[一-鿿]',w)
     for ch in components:
        if ch!=c:supp.append({**row,'kanji':ch});addline(ch,f'- [{w}](../{wp}) {y} — {gloss}')
     if exc:wex.append(dict(word=w,exclude=exc))
     out[wp]=f'---\nword: {w}\nreading: {y}\ntitle: {gloss}\ntype: {kind}\nkanji: {arr(components)}\ntags: [{kind}, {tags}]\n'+(f'quiz_exclusions: {arr(exc)}\n' if exc else '')+f'---\n\n# {w} ({y}) — {gloss}\n\n'+fmt(f'## Meaning\n\n{intro}\n\n- {a}\n- {b}\n\n## How the kanji combine\n\n{form}\n\n## Synonyms and antonyms\n\n{comp}\n\n## Distinctive meaning\n\n{note}\n','words')+f'\nDictionary: [JMdict]({jm}), entry {eid}, {"sense" if len(senses)==1 else "senses"} {sensestr}{EXTRA.get(w,"")}; [Digital Daijisen, {w}](https://www.weblio.jp/content/{urllib.parse.quote(w)}).\n'
     ids.update(cite(out[wp].split('---',2)[-1],pre));ids.update(re.findall(r'\d{7}',EXTRA.get(w,'')))
    intro,cue,note,other=chars[c];table=[];common=[];proj=dict(kanji=c)
    for kind,field,cap in [('on','onyomi','Onyomi'),('kun','kunyomi','Kunyomi')]:
        picked=[v for v in m[field] if v in linked];proj['quiz'+cap]=picked;proj[kind+'Keys']=offered_keys(picked)
        for v in m[field]:
            d=dict(kanji=c,kind=kind,reading=v,selected=v in linked)
            if v in linked:
                mp=linked[v];shown=f"[{spell}](../{mp['article']}) {mp['primaryReading']} — {gloss}"
                common.append('- '+shown);d.update(article=mp['article'],reason='Mapped writing exemplifies this reading in the specified sense.',entryIds=mp['entryIds'])
            else:
                shown,es=other[v];d.update(reason=shown,entryIds=es.split());pre.update(es.split())
                if 'source-only' in shown:d['sourceOnly']=True
            table.append(f'| {v} | {kind} | {shown} |');disp.append(d)
    assert set(other)|set(linked)==set(m['onyomi'])|set(m['kunyomi']),c
    projs.append(proj)
    if xs:kex.append(dict(kanji=c,exclude=list(xs)))
    labels[c]=dict(title=title,distractors=list(ds),labels=[titles[d] if d in titles else head(f'kanji/{d}.md')['title'] for d in ds])
    body=fmt(f'\n# {c} — {title}\n\n**Strokes:** {m["strokes"]} · **Key (radical):** {m["radical"]} (no. {m["radicalNumber"]}) · **JLPT:** N1 (community list)\n\n## Meaning and origin\n\n{intro}\n\n**Shape mnemonic, not etymology:** {cue}\n\n## Readings\n\n| Reading | Type | Typical words |\n| --- | --- | --- |\n'+'\n'.join(table)+'\n\n## Common words\n\n'+'\n'.join(common)+f'\n\n## Notes\n\n{note}\n','kanji')
    refs=cite(body,pre);ids.update(refs)
    out[n]=f"---\nkanji: {c}\ntitle: {title}\njlpt: 1\ntags: [jlpt-n1, grade-{m['grade']}, structure-unclassified]\nstrokes: {m['strokes']}\nradical: {m['radical']}\nradicalNumber: {m['radicalNumber']}\nonyomi: {arr(m['onyomi'])}\nkunyomi: {arr(m['kunyomi'])}\nquizOnyomi: {arr(proj['quizOnyomi'])}\nquizKunyomi: {arr(proj['quizKunyomi'])}\ndistractors: {arr(ds)}\n"+(f'quiz_exclusions: {arr(xs)}\n' if xs else '')+'---\n'+body+f"\nMetadata: [KANJIDIC2]({kd}), frozen 2026-11-02; [Kanjipedia, {c}]({km[c]['url']}); [JMdict]({jm}), entries "+', '.join(sorted(refs))+'.\n'
TAI=[('| タイ | on | 怠惰 たいだ - lazy; idle; indolent; slothful; no word article yet, not selected for questions here |','| タイ | on | [怠惰](../words/怠惰.md) たいだ — lazy; idle; indolent; slothful; not selected for questions here |'),
 ('In 怠惰, 怠 supplies タイ and 惰 supplies ダ.','In 怠惰, 怠 supplies タイ and [惰](惰.md) supplies ダ.'),
 ('Practice selects おこた.る and なま.ける, the readings with linked word articles. タイ is the reading of 怠 compounds, but no word article uses it yet; it is illustrated with a dictionary word.','Practice selects おこた.る and なま.ける. タイ is shown with the linked word 怠惰, but it is not selected for questions on this card.'),
 ('- Both common words are 怠 with okurigana only.','- 怠る and 怠ける write 怠 with okurigana only; [怠惰](../words/怠惰.md) is a compound with [惰](惰.md).')]
for a,b in TAI:edit('kanji/怠.md',a,b)
# Constituent Metadata: one first Metadata line listing existing ids, whole-run gaps and the new entry.
os.environ.setdefault('N1_LEAN',str(Path('../lean').resolve()))
sys.path.insert(0,'docs/n1-reviews/batch-137-closure/confirm-packet/gpt/evidence');import meta_scan
PICK={'忠実':'1012210'}
tmp=Path('../b169-scan');(tmp/'kanji').mkdir(parents=True,exist_ok=True)
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
    if c in ('郷','怠'):
        a=next(l for l in t.splitlines() if l.startswith('Metadata:'));b=a+f' Word pairs: {JM}, entries {lst}.'
    else:
        assert 'Metadata:' not in t,c;a=t.rstrip().splitlines()[-1];b=a+f'\n\nMetadata: Word pairs: {JM}, entries {lst}.'
    assert a!=b;edit(n,a,b)
notes={
 '忍':'忍ぶ (news2/ichi1) is the kun example in the standard-use table (PDF p. 123). ニン and しの.ばせる are shown with dictionary words and not offered. 偲ぶ is a separate JMdict entry and is not taught as a spelling of 忍ぶ.',
 '忠':'忠実 (news1/ichi1) is the first example for チュウ in the standard-use table; 実 has a card. The same spelling also writes まめ, a separate word not taught here.',
 '恒':'恒例 (news1/ichi1) is a standard-use example for コウ; 例 has a card. KANJIDIC2 つねに is source-only: JMdict has no 恒に.',
 '恭':'No spelling containing 恭 carries a priority tag; see the mapping exceptionReason. 恭しい is the kun example in the standard-use table.',
 '悦':'満悦 carries news2 and spec2 (with nf37) on both spelling and reading; news2 and spec2 qualify under the owner decision in issue #60 comment 7112026459, applied since B160. It is the only spelling containing 悦 with any priority tag. 悦ぶ, 悦び and 悦ばす are rarely used kanji forms and are shown, not offered.',
 '悼':'追悼 (news1/ichi1) is a standard-use example for トウ; 追 has a card. 悼む is shown on the card for いたむ.',
 '惨':'惨め (ichi1/news2) is the standard-use kun example 惨めだ; the mapping reuses the kana-headed article みじめ (entry 1303280, sense 1), as B164 reused おばあさん for 婆. KANJIDIC2 いたむ is source-only: JMdict has no 惨む.',
 '惰':'怠惰 (news2/ichi1) is a standard-use example for ダ, the only reading in the table; 怠 has a card, whose reading row already named 怠惰 and now links it.',
 '愁':'郷愁 (news1/ichi1) supports シュウ; 郷 has a card. The standard-use examples for シュウ are 哀愁 (spec1/news2) and 憂愁; 憂 has no card. 哀愁 would also qualify through 哀 and remains an unlinked dictionary word on the 哀 reading row; no claim is made that one route is preferable. 愁える and 愁い are shown with their JMdict spelling status.',
 '愚':'愚か (news2/ichi1) is the standard-use kun example 愚かだ. グ is shown with 愚問 and 愚痴 and not offered.'}
acc=dict(frozenPendingRecords=1228,publishedPendingRecordsWithCards=708,publishedN1Additions=702,n2Placements=6,undelivered=520,localUnreviewedDrafts=10,notStarted=510,overallN1TaskComplete=False)
ledger=dict(schemaVersion=1,batch='169',governingIssue=60,base=base,baseCommit=base,selectionBase=base,members=members,membership=members,drafted=members,runtimePublished=False,status='unreviewed draft',selectionReason='First ten absent Jōyō rows on the B168 receipt. Supports qualify through JMdict ichi1, news1, spec1 or gai1, with news2 and spec2 also qualifying under issue #60 comment 7112026459; 恭 alone uses a documented untagged route.',selectionNotes=notes,supportMappings=maps,supplementaryMappings=supp,requiredReciprocalPairs=[[i['kanji'],i['article']] for i in maps+supp],changedReusedPassages=changes,wordQuizAudit=dict(directExclusions=wex,evidence='docs/n1-reviews/batch-156-closure/packet/evidence/audits/word_quiz_audit.py run on the draft and revised snapshots over all nine new words reported 0 problems. In particular, the word 忠実 is always drawn with its reading ちゅうじつ, so the separate JMdict word まめ (2827450) written 忠実 cannot appear as a quiz answer or reading option for it.'),kanjiQuizAudit=dict(directExclusions=kex),dictionaryPackets=[dict(selection='batch-169-jmdict-selection.json',xml='batch-169-jmdict.xml')],readingDispositions=disp,curatedProjection=projs,quizAudit=labels,sources=dict(dictionaryPin='continuation-inputs.json',characterEntries=km),accounting=acc,limits=['Unpublished draft; no native-speaker or device acceptance.'])
ledger['sources']['dictionaryChecks']='Author re-read the Digital Daijisen bodies on Weblio for 惨め (みじめ), 忍ぶ (しのぶ), 忠実 (ちゅうじつ), 恒例 (こうれい), 恭しい (うやうやしい), 満悦 (まんえつ), 追悼 (ついとう), 怠惰 (たいだ), 郷愁 (きょうしゅう) and 愚か (おろか); the 実用日本語表現辞典 entries ご満悦 (2023; 「心から喜び、満足している状態を表す言葉」) and 御満悦 (2010; 「満悦」の丁寧な表現, 別表記 ご満悦), and its entry 恭しい (2023; often written in hiragana as うやうやしい, e.g. うやうやしい態度 and うやうやしくお辞儀をする; seldom deliberately used in present-day everyday conversation; sometimes used ironically, with a nuance of affectation such as 「必要以上に丁重っぽく」); the Weblio example 恭しい態度を執る; the Digital Daijisen character entries じつ【実〔實〕】 (sense 4 「まごころ。まこと」, which lists 忠実), れい【例】 (sense 3 「以前から行われている事柄。ならわし。いつもどおり」, which lists 恒例) and つい【追】 (sense 4 「以前のことをあとからたどる」, which lists 追悼); and the official standard-use table rows for all ten kanji (PDF pages 123, 108, 54, 38, 16, 118, 63, 102, 74 and 42). Daijisen examples quoted in the articles are attributed to it; the bulleted example sentences are original.'
out[str(src/'batch-169-progress.json')]=dump(ledger);out[str(src/'batch-169-jmdict-selection.json')]=dump(dict(schemaVersion=1,batch='169',entryIds=sorted(ids)))
for n in out:assert (n in old and Path(n).read_text('utf8').replace('\r\n','\n')==old[n]) or not Path(n).exists(),n
xml=src/'batch-169-jmdict.xml';assert not xml.exists();xml.write_bytes(extract(raw,h,sorted(ids)))
for n,t in out.items():
    cr=n in old and b'\r\n' in git('show',base+':'+n);Path(n).write_bytes(t.replace('\n','\r\n' if cr else '\n').encode())
print(len(words),'new words;',len(ids),'families;',len(disp),'reading rows;',len(maps+supp),'pairs;',len(changes),'edits')
