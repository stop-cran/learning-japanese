"""Build the B150 --extra reading lists for reading_exposure.py / reading_options.py from saved evidence:
Kanjipedia outside (外) readings (kanjipedia-b150-data.json from lean kanjipedia.py; page text in kanjipedia-verified.txt),
Digital Daijisen character-entry [音]/[訓] lists (webcheck\\weblio-K.txt; transcribed below because the Weblio text splits
some kun readings at furigana spans, and every transcription is asserted against the extract with spaces removed), and
Daijisen headwords whose bracket lists the searched form (daijisen-heads.txt). 蒔 has no Daijisen character entry.
Writes extras.json next to this script and prints a summary."""
import json, os, re

H = os.path.dirname(os.path.abspath(__file__))
B = os.path.dirname(H)
K = '葬 蒔 蓄 薦 虚 融 衆 街 衝 裁 裂 裸 覆 視 覧'.split()
DCHAR = {
    '葬': (['ソウ'], ['ほうむる']),
    '蒔': None,
    '蓄': (['チク'], ['たくわえる']),
    '薦': (['セン'], ['すすめる', 'こも']),
    '虚': (['キョ', 'コ'], ['むなしい', 'うそ', 'そら', 'から', 'うつけ', 'うつろ', 'うろ']),
    '融': (['ユウ'], ['とける', 'とおる']),
    '衆': (['シュウ', 'シュ'], []),
    '街': (['ガイ', 'カイ'], ['まち']),
    '衝': (['ショウ'], ['つく']),
    '裁': (['サイ'], ['たつ', 'さばく']),
    '裂': (['レツ'], ['さく', 'さける', 'きれ']),
    '裸': (['ラ'], ['はだか']),
    '覆': (['フク', 'フウ'], ['おおう', 'くつがえす', 'くつがえる']),
    '視': (['シ'], ['みる']),
    '覧': (['ラン'], ['みる']),
}
ex = {k: [] for k in K}
src = {k: {} for k in K}


def add(k, r, s):
    r = r.strip()
    if not r:
        return
    if r not in ex[k]:
        ex[k].append(r)
    src[k].setdefault(r, [])
    if s not in src[k][r]:
        src[k][r].append(s)


kp = json.load(open(os.path.join(B, 'kanjipedia-b150-data.json'), encoding='utf-8'))
for k in K:
    for r in kp[k]['outside']:
        add(k, r, 'Kanjipedia outside')

page = None
for line in open(os.path.join(B, 'daijisen-heads.txt'), encoding='utf-8'):
    m = re.match(r'^(\S+) \(https://', line)
    if m:
        page = m.group(1)
        continue
    m = re.match(r'^\s+D (.+?)【(.+)】\s*$', line)
    if m and page and page[0] in ex:
        forms = [re.sub(r'〔.*?〕', '', f).replace('▽', '').replace('×', '').strip() for f in m.group(2).split('／')]
        if page not in forms:
            continue
        reading = re.sub(r'〔.*?〕', '', m.group(1)).replace('‐', '').replace('・', '.')
        if not re.fullmatch(r'[ぁ-ゖァ-ヶー.]+', reading):
            continue
        add(page[0], reading, 'Daijisen headword ' + page)

for k in K:
    if DCHAR[k] is None:
        continue
    t = ''.join(open(os.path.join(B, 'webcheck', 'weblio-%s.txt' % k), encoding='utf-8').read().splitlines()[5:]).replace(' ', '')
    m = re.search(r'［音］(.*?)(?:［訓］(.*?))?(?=［学|［名|［難|〈|１|$)', t)
    assert m, k
    onsec, kunsec = m.group(1), m.group(2) or ''
    ons, kuns = DCHAR[k]
    assert ons == re.findall(r'[ァ-ヶー]+', re.sub(r'（.*?）', ' ', onsec)), (k, onsec)
    pos = 0
    for r in kuns:
        i = kunsec.find(r, pos)
        assert i == pos, (k, r, kunsec[:60])
        pos = i + len(r)
    for r in ons:
        add(k, r, 'Daijisen character entry [音]')
    for r in kuns:
        add(k, r, 'Daijisen character entry [訓]')


def fold(s):
    return ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in s).replace('.', '')


final = {}
for k in K:
    seen = {}
    for r in ex[k]:
        f = fold(r)
        if f in seen:
            for s in src[k][r]:
                if s not in src[k][seen[f]]:
                    src[k][seen[f]].append(s)
            continue
        seen[f] = r
    final[k] = list(seen.values())
    src[k] = {r: src[k][r] for r in final[k]}
json.dump({'extras': final, 'sources': src,
           'daijisen_character_entries': {k: ({'on': v[0], 'kun': v[1]} if v else None) for k, v in DCHAR.items()}},
          open(os.path.join(H, 'extras.json'), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=2)
for k in K:
    d = DCHAR[k]
    print(k, 'D音', ' '.join(d[0]) if d else '-', 'D訓', ' '.join(d[1]) if d else '-', '| KP外', ' '.join(kp[k]['outside']), '| extras', ','.join(final[k]))
