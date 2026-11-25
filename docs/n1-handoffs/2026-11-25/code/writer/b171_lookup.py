import gzip,sys,json,xml.etree.ElementTree as ET,hashlib
from pathlib import Path
J=Path(r'C:\Users\romanko\n1-kanji-workspace\jmdict\JMdict_e.gz')
assert hashlib.sha256(J.read_bytes()).hexdigest()=='42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec'
want=set(sys.argv[1].split(','))
out=[]
with gzip.open(J) as f:
    for _,e in ET.iterparse(f,events=['end']):
        if e.tag!='entry':continue
        ks=[k.findtext('keb') for k in e.findall('k_ele')];rs=[r.findtext('reb') for r in e.findall('r_ele')]
        if want&(set(ks)|set(rs)):
            d=dict(id=e.findtext('ent_seq'),k=[(k.findtext('keb'),[p.text for p in k.findall('ke_pri')],[p.text for p in k.findall('ke_inf')]) for k in e.findall('k_ele')],
                   r=[(r.findtext('reb'),[p.text for p in r.findall('re_pri')],[p.text for p in r.findall('re_inf')],[p.text for p in r.findall('re_restr')]) for r in e.findall('r_ele')],
                   s=[dict(pos=[p.text for p in s.findall('pos')],misc=[p.text for p in s.findall('misc')],g=[p.text for p in s.findall('gloss')],xref=[p.text for p in s.findall('xref')],stagk=[p.text for p in s.findall('stagk')],inf=[p.text for p in s.findall('s_inf')]) for s in e.findall('sense')])
            if set(ks)&want or not ks: out.append(d)
            elif set(rs)&want: out.append(d)
        e.clear()
json.dump(out,open(sys.argv[2],'w',encoding='utf-8'),ensure_ascii=False,indent=0)
