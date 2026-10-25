## Snapshot
The corrected commit is `5c9570bb46ccbee8376d7cbfa48eca1ca916b6a2`, with parent `7359a791ab051c71c555a1931bfbaeea7ab07578`. I took both from `batch-66-correction-snapshot.json`, which I read first. This review covers committed content only. File tools can't run Git, hash or cleanliness checks, and I did not inspect `.git`.

## Scope
**Model:** claude-opus-5.5 (family claude). This was a read-only resumed confirmation: no edits, agents or delegation.

**Read completely this session:**
- `correction-snapshot.json`, the complete `correction.patch` and `correction-public.json`.
- All seven changed bodies: 残らず, 売店, バイバイ, 乗り換え, 這う, 覗く and 上り. Each matches the patch, and only front matter changed apart from 上り line 16.
- Both correction-family chunks, with 18 complete families and 54 senses.
- Both older-body chunks, with all 16 bodies.
- The TSV header plus rows N2:1302 to N2:1321 only, matched by exact source ID.

**Read partly:**
- `corrected-review-evidence.json` (ranges): the access limits, changed declarations, dispositions, extra public attempt and author reads. This also exposed the GPT reviewer's read receipts (paths and hashes only), not its report.
- Comparison bodies: じゃ, 売り場 and さて.
- Targeted title, quiz-exclusion and existence searches within `words\`.

**Inherited from my initial review without rereading:**
- The other eight new articles and the five reused articles.
- The 延, 換, 灰 and 鈍 kanji edits, plus unchanged 伸.
- The related patch, the four compact derivatives and the Daijisen captures.

## Verdicts
| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1302 | words\のこぎり.md | inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1303 | words\残らず.md | fresh full reread | CLEAN | CLEAN | CLEAN |
| N2:1304 | words\乗せる.md | inherited | CLEAN | CLEAN | CLEAN |
| N2:1305 | words\覗く.md | fresh full reread | CLEAN | CLEAN | CLEAN |
| N2:1306 | words\伸ばす.md | inherited | CLEAN | CLEAN | CLEAN |
| N2:1307 | words\伸びる.md | inherited, plus fresh full body in an older-body chunk | CLEAN | CLEAN | CLEAN |
| N2:1308 | words\上り.md | fresh full reread | CLEAN | CLEAN | CLEAN |
| N2:1309 | words\登る.md | inherited | CLEAN | CLEAN | CLEAN |
| N2:1310 | words\糊.md | inherited | CLEAN | CLEAN | CLEAN |
| N2:1311 | words\乗り換え.md | fresh full reread | CLEAN | CLEAN | CLEAN |
| N2:1312 | words\載る.md | inherited | CLEAN | CLEAN | CLEAN |
| N2:1313 | words\のろい.md | inherited | CLEAN | CLEAN | CLEAN |
| N2:1314 | words\のろのろ.md | inherited | CLEAN | CLEAN | CLEAN |
| N2:1315 | words\のんき.md | inherited | CLEAN | CLEAN | CLEAN |
| N2:1316 | words\灰色.md | inherited | CLEAN | CLEAN | CLEAN |
| N2:1317 | words\俳句.md | inherited | CLEAN | CLEAN | CLEAN |
| N2:1318 | words\売店.md | fresh full reread | CLEAN | CLEAN | CLEAN |
| N2:1319 | words\バイバイ.md | fresh full reread | NEEDS FIX (B66-Q4) | CLEAN | CLEAN |
| N2:1320 | words\売買.md | inherited | CLEAN | CLEAN | CLEAN |
| N2:1321 | words\這う.md | fresh full reread | CLEAN | CLEAN | CLEAN |

- **Kanji edits (inherited):** 延, 換, 灰 and 鈍 are CLEAN. 鈍 links のろい through Common words/Notes with the 2838553 footer, adds no のろ reading row, and のろい's primary kanji array stays empty.
- **Unchanged 伸:** CLEAN. It links to both 伸ばす and 伸びる.
- **Reciprocal links:** CLEAN for all of these:
  - 換 ↔ 乗り換え (のりかえ), footer 1600460.
  - 灰 ↔ 灰色 (はいいろ), footer 1201970.
  - 伸 ↔ 伸ばす and 伸 ↔ 伸びる (both のばす/のびる).
  - Alias pairs 延/延ばす and 延/延びる. Both Readings and Common words reach the shared articles, with footers 1600290 and 1358870. Sense 1358870:8 stays restricted to 延びる.
- **Baseline preservation:** CLEAN. The patch touches only the seven new articles. Levels are kept (N3 乗せる/伸ばす/伸びる, N5 登る), and のろのろ only gains `jlpt: 2`.
- **Mappings:** CLEAN. All 20 TSV rows match the associations, selected senses and additional senses.

## Findings
**My original findings:**
- **B66-Q1 (乗り換え): resolved.** 接続 and 移す are added at `乗り換え.md:9`.
  - 接続 is strong: 1385480:2 is "changing trains", and `接続.md:9` already excludes 乗り換える.
  - 移す is moderate but defensible: 1158160:1 is "transfer (to a different place, group)", and the titles share "transfer".
- **B66-Q2 (じゃあ): accepted but incomplete.** Adding じゃあ is supported at medium-low confidence, based on the じゃあね closing taught in its body. See B66-Q4 for the gap.
- **B66-Q3 (這う): resolved.** I accept that my initial quote of the article was slightly wrong. The removal rests on meaning: 1358870 senses 1 and 3 (lengthen, spread) do not match 1474200:3 (plant trailing). 広がる is kept, and no card declares 這う in reverse, so the removal takes effect.

**My optional observations:**
- **上り:** "designated starting point" at line 16 is correct, and the not-every-route-Tokyo qualification is kept. No regression.
- **覗く/見物:** removal adopted and effective. 1260000:1 sightseeing/viewing does not compete with peeking.
- **送別:** agree. 1402850:1 "farewell; send-off" and 1983760:2 "parting" support a bounded guard.
- **全然/さっぱり:** my polarity concern stays withdrawn, and both guards are kept.
- **No extra guards needed** (bounded judgments, not proof that overlap is impossible):
  - 載る/刷る and 載る/印刷: print production versus appearing in print.
  - 残らず/全般: the 全般 body teaches overall scope, not every item.
  - 上り/昇る: 昇る is titled for sun/moon rising and promotion.
  - のんき/ゆっくり and のんき/楽: 1013050 and 1207230 cover pace and comfort, not temperament.

**GPT findings:**
- **GPT-01 (残らず):** accept いちいち (1587320:2 "without omission") and 皆さん (1202170:1 "all; everyone").
- **GPT-02 (売店):** accept スタンド (1069930:2 "stand (e.g. newspaper stand); counter").
- **GPT-03 (バイバイ):** accept それでは (1406050:4 "bye then").

**Regressions:** none found. All eight added targets exist as cards, and both removals take effect.

**New finding, B66-Q4** (Low; quiz-exclusion omission; `words\バイバイ.md:9`):
- **Claim:** バイバイ excludes では, じゃあ and それでは, but not じゃ.
- **Why it matters:** じゃ has the identical title "well then". Exact-title deduplication only keeps じゃ and じゃあ apart from each other; it does not exclude じゃ against バイバイ. So the "well then" choice can still compete through じゃ, which undoes the B66-Q2 fix.
- **Evidence:**
  - Family 1005900 (`correction-families-01.txt:2`) has the readings じゃあ and じゃ, with one shared sense: "then; well; so; well then" (from では).
  - `じゃ.md:4` has the title "well then".
  - `じゃ.md:15` explicitly teaches using じゃ for "farewell", and line 33 has the 1005900 footer.
  - `さて.md:9` already treats じゃ as its own card.
- **Not a blanket rule:** I do not propose さて (moving on, not leave-taking) or また ("again").
- **Remedy:** add じゃ to `バイバイ.md:9`.
- **Confidence:** medium. This is a pre-existing omission I missed initially, not a regression.

## Optional
- 売店/売り場 ("sales area"): the referents differ (one section of a store versus a small standalone shop), so no guard is established.
- 残らず/一人一人 and 残らず/それぞれ: these are distributive "each", so no guard is established.
- Title polish for のこぎり and 乗り換え, and extra examples on reused cards, remain nonblocking. No change is required.

## Limits
- I ran no Git, hash, manifest or validator checks. Baseline preservation relies on the patch plus author assertions.
- The eight unchanged new articles, the five reused articles and the five kanji files were not reread this session; their verdicts are inherited.
- All public evidence comes from one source (Digital Daijisen via Weblio). The じゃあ attempt gave no positive confirmation, and no じゃ capture exists.
- There were no live quiz draws, no native-speaker certification, no frequency checks and no exhaustive ambiguity audit.
- The batch-61 issues (飛ぶ/飛行, 止まる/止む) remain deferred.
