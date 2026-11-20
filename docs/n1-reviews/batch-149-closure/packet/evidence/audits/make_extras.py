"""Build the B149 --extra reading lists for reading_exposure.py / reading_options.py from saved evidence:
Kanjipedia outside (外) readings (kanjipedia-verified.txt), Digital Daijisen character-entry [音]/[訓] lists
(webcheck\\weblio-K.txt), and Daijisen headwords whose bracket lists the searched form (daijisen-heads.txt).
Writes extras.json and kanjipedia-b149-data.json next to this script and prints a summary."""
import json, os, re

H = os.path.dirname(os.path.abspath(__file__))
B = os.path.dirname(H)
K = '翻 翼 脈 腐 臨 臭 興 舌 舎 艶 芝 芽 茂 荘 華'.split()
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


def kp_items(sec):
    sec = re.sub(r'\((?:中|高)\)', '', sec)
    out = []
    for it in re.split(r'[・]', sec):
        it = it.strip()
        if not it:
            continue
        parts = it.split()
        if all(re.fullmatch(r'[ァ-ヶー]+', p) for p in parts):
            out.extend(parts)
        else:
            out.append('.'.join(parts) if len(parts) == 2 else ''.join(parts))
    return out


kp = {}
cur = None
for line in open(os.path.join(B, 'kanjipedia-verified.txt'), encoding='utf-8'):
    m = re.match(r'^(\S) sha256=', line)
    if m:
        cur = m.group(1)
        continue
    m = re.match(r'^\s+読み: \[音\](.*?)\[訓\](.*)$', line.rstrip())
    if m and cur in ex:
        rec = {'on': [], 'kun': [], 'outside': []}
        for key, sec in (('on', m.group(1)), ('kun', m.group(2))):
            inside, _, outside = sec.partition('外')
            a, b = kp_items(inside), kp_items(outside)
            rec[key] = a + b
            rec['outside'] += b
        kp[cur] = rec
        for r in rec['outside']:
            add(cur, r, 'Kanjipedia outside')
assert len(kp) == 15, sorted(kp)
for k in K:
    card = open(os.path.join(r'C:\Users\romanko\n1-kanji-workspace\b149-wt\kanji', k + '.md'), encoding='utf-8').read()
    u = re.findall(r'https://www\.kanjipedia\.jp/kanji/\d+', card)
    assert len(set(u)) == 1, (k, u)
    kp[k]['url'] = u[0]

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
        okuri = page[1:]
        if okuri and '.' not in reading and reading.endswith(okuri) and reading != okuri:
            reading = reading[:-len(okuri)] + '.' + okuri
        add(page[0], reading, 'Daijisen headword ' + page)

char = {}
for k in K:
    t = ' '.join(open(os.path.join(B, 'webcheck', 'weblio-%s.txt' % k), encoding='utf-8').read().splitlines()[5:])
    m = re.search(r'［音］(.*?)(?:［訓］(.*?))?(?=［|１|〈|$)', t)
    assert m, k
    ons = [x for x in re.findall(r'[ァ-ヶー]+', re.sub(r'（.*?）', ' ', m.group(1)))]
    kuns = []
    for tok in (m.group(2) or '').split():
        if not re.fullmatch(r'[ぁ-ゖー]+', tok):
            break
        kuns.append(tok)
    char[k] = (ons, kuns)
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
json.dump({'extras': final, 'sources': src, 'daijisen_character_entries': {k: {'on': v[0], 'kun': v[1]} for k, v in char.items()}},
          open(os.path.join(H, 'extras.json'), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=2)
json.dump(kp, open(os.path.join(H, 'kanjipedia-b149-data.json'), 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
for k in K:
    print(k, 'D音', ' '.join(char[k][0]), 'D訓', ' '.join(char[k][1]), '| KP外', ' '.join(kp[k]['outside']), '| extras', ','.join(final[k]))
