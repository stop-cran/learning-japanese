I've finished the confirmation review of the corrected snapshot. All 20 rows come out CLEAN, I found no new actionable defect, and my two original findings and the 匂う limitation are each resolved or withdrawn.

# Snapshot
- **Corrected commit:** 451529a65ebc8a063e13c716bab1254d0a31afa1
- **Parent:** 9eb5a046068bdf31aed69a6bdb6f505bc81a39b6
- I reviewed committed content only. My file tools can't run Git, hash or cleanliness checks, and I didn't look inside `.git`. The commit IDs come from `correction-snapshot.json`.

# Scope
**Model:** claude-opus-5.5 (claude family).

**Complete reads this session:**
- `correction-snapshot.json` and the complete `correction.patch`.
- The four changed articles in full: `words\なんとも.md`, `words\煮える.md`, `words\憎らしい.md`, `words\匂う.md`. Each matches the patch exactly.
- Unchanged `words\憎い.md` in full.
- `correction-families-01.txt` (12 families, 31 senses) and `correction-old-bodies-01.txt` (まさに, 実際, 本当, 焼ける, なかなか).
- `correction-public.json`.
- TSV line 1 plus lines 1262–1281 only, not 1282.
- `kanji\憎.md` in full and `words\実は.md`.
- Two ranges of `corrected-review-evidence.json`: 25962–26140 and 27273–27420. These hold the changed articles, the revised exclusion lists (they match the committed front matter) and the dispositions.
- Title searches and globs inside `words\` only.
- One web fetch of my own: https://kotobank.jp/word/中中-587944. It returned the Nikkoku body; the Daijisen heading had no text, so I don't count it.

**Inherited from my initial session (not reread):**
- The 15 other assigned articles.
- `kanji\課.md` and `kanji\鈍.md`.
- `related.patch` and `frozen-snapshot.json`.
- The four compact derivatives: mappings, principals, components, labels.
- The initial Weblio/Daijisen captures and my initial Kotobank 匂う fetch.

**Omissions:**
- Most of the large corrected derivative.
- The family and old-body chunks I didn't read initially.
- Every forbidden ledger, report and `batch-64.json`.

# Verdicts
| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1262 | words\なんとなく.md | Inherited initial full read; not in patch | CLEAN | CLEAN | CLEAN |
| N2:1263 | words\なんとも.md | Fresh full reread + patch | CLEAN | CLEAN | CLEAN |
| N2:1264 | words\ナンバー.md | Inherited | CLEAN | CLEAN | CLEAN |
| N2:1265 | words\南米.md | Inherited | CLEAN | CLEAN | CLEAN |
| N2:1266 | words\南北.md | Inherited | CLEAN | CLEAN | CLEAN |
| N2:1267 | words\煮える.md | Fresh full reread + patch | CLEAN | CLEAN | CLEAN |
| N2:1268 | words\匂う.md | Fresh full reread + patch | CLEAN | CLEAN | CLEAN |
| N2:1269 | words\逃がす.md | Inherited | CLEAN | CLEAN | CLEAN |
| N2:1270 | words\憎い.md | Fresh full reread; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1271 | words\憎む.md | Inherited; reused, jlpt:2 only | CLEAN | CLEAN | CLEAN |
| N2:1272 | words\憎らしい.md | Fresh full reread + patch | CLEAN | CLEAN | CLEAN |
| N2:1273 | words\にこにこ.md | Inherited; reused, jlpt:2 only | CLEAN | CLEAN | CLEAN |
| N2:1274 | words\濁る.md | Inherited | CLEAN | CLEAN | CLEAN |
| N2:1275 | words\虹.md | Inherited | CLEAN | CLEAN | CLEAN |
| N2:1276 | words\日時.md | Inherited | CLEAN | CLEAN | CLEAN |
| N2:1277 | words\日用品.md | Inherited | CLEAN | CLEAN | CLEAN |
| N2:1278 | words\日課.md | Inherited | CLEAN | CLEAN | CLEAN |
| N2:1279 | words\日程.md | Inherited | CLEAN | CLEAN | CLEAN |
| N2:1280 | words\鈍い.md | Inherited; reused, jlpt:2 only | CLEAN | CLEAN | CLEAN |
| N2:1281 | words\入社.md | Inherited | CLEAN | CLEAN | CLEAN |

**Separate assessments, all CLEAN:**
- **Five reciprocal pairs:**
  - 憎/憎い にくい (1403390): `kanji\憎.md:32,39`.
  - 憎/憎らしい にくらしい (1403450): `kanji\憎.md:33,40`.
  - 憎/憎む にくむ (1403440): `kanji\憎.md:31,38`. The footer at `kanji\憎.md:50` lists 1403390, 1403440 and 1403450.
  - 課/日課 にっか (1463860) and 鈍/鈍い にぶい (1582430): inherited.
  - Reading rows, Common words entries, word-side links and footer IDs are all present.
- **憎 edit:** CLEAN; header preserved. The "ironically darling" wording is a nonblocking Optional item.
- **課 edit:** CLEAN (inherited).
- **Unchanged 鈍:** CLEAN (inherited).
- **Baseline preservation:** CLEAN. 憎む, にこにこ and 鈍い still show only the jlpt:2 insertion; the correction patch doesn't touch them.
- **Mappings:** CLEAN. The 20 TSV rows are unchanged, にこにこ's source gloss stays empty, and 鈍い 1582430 stays separate from the のろい identity.

# Findings
**B64-CL-01 (my 憎らしい title finding): RESOLVED.**
- `words\憎らしい.md:4,12` now read "hateful; annoyingly good". That matches the example on line 20 (憎らしいほど上手) and Daijisen sense ② (気にさわるほどすばらしい).
- The "darling" mention on line 23 is accurate JMdict 1403450:2 recognition wording; nothing was invented.
- No regression. うるさい ("noisy; annoying") shares only the word "annoy", and 上手 ("skillful; good at") shares only the word "good". The full titles tell them apart, so neither is an established pair.

**B64-CL-02 (my なかなか-guard removal proposal): WITHDRAWN as actionable.**
- JMdict 1599420:4 has "excellent; wonderful; very good" with no rare or obsolete tag.
- My own Kotobank fetch independently confirms Nikkoku [1][二]①: 「肯定できる程度であるさま。かなりよいさま」.
- The direct overlap with 憎い sense 2 ("amazing; admirable") and with 憎らしい's new title is real. The residual disagreement is only a preference; see Optional.

**匂う register and spelling limitation: RESOLVED.**
- `words\匂う.md:42-47` drops the "literary" claim and uses kana におう for the suspicion use.
- The glow and hint senses are supported by JMdict 1599780:3–4 and by my initial Nikkoku fetch (senses ③ and ⑨).
- The literal 臭う on line 44 is the preserved spelling preference for an unpleasant odor.

**N2-64-01 (なんとも guards for まさに, 実際, 本当): ACCEPTED, no regression.**
- Exclusion list at `words\なんとも.md:9`.
- Basis: 1188690:1 "really", 1376640:1 "really; truly", and 1321110:3 "truly; really".
- 本当 is the least direct of the three but defensible, because the older 本当 article teaches 本当に and "Really?". I don't merge 1523060 with 1611580 or infer anything through 実に.
- Remaining omission checks found nothing missing: 実は ("actually; to tell the truth") is used to reveal something, not as "really", and 本当に, 誠に and 確かに have no articles.

**N2-64-02 (煮える/焼ける guard): ACCEPTED.**
- Exclusion list at `words\煮える.md:9`. 1350610:2 "thoroughly cooked" is the same cooked-through result.
- 焼く ("bake; grill", transitive) isn't established as a pair, and no 茹でる or 煮る articles exist.

**Earlier optional observations:** I agree none are mandatory: a 濁る moral example, kana styling, 逃す for missed chances, and 臭い read as におい. The 良い/いい, 非常, 光る/輝く and 怪しい/疑わしい guards remain qualified direct judgments, not defects.

**New actionable defects:** none.

# Optional
1. `kanji\憎.md:40,47` still describe 憎らしい as "ironically darling". The wording is accurate, but it could be aligned with the new "annoyingly good" title.
2. `words\憎らしい.md:23`: the "darling" sense could get a short gloss that doesn't invent a collocation, or be left as it is.
3. The TSV `source_note` for N2:1268 still says "literary brightness…". Learners don't see it, but it is now stale.
4. I still lean slightly toward the なかなか guards on 憎い/憎らしい being more cautious than needed. Nikkoku calls the favorable sense a 軽い評価 (mild evaluation), and the older なかなか article doesn't teach it. The guard is defensible, so this is a preference, not a defect.
5. 憎い/憎らしい exclude 上手い but not 上手. This asymmetry predates the correction and the titles disambiguate, so it's nonblocking.

# Limits
- **Author-run checks:** I couldn't run Git, hash, manifest or cleanliness checks. I'm relying on the author for:
  - baseline preservation;
  - the unchanged status of the other 15 articles and three kanji cards;
  - the four lower-level no-match checks.
- **Reading depth:** my initial older-article reads covered 8 articles (5 for comparison plus the 3 reused ones). My family reads were one 20-family chunk, the 20 principals and the アメリカ record, which is shallower than GPT's. This session added 12 families and 5 older articles.
- **Single authorities:** the Daijisen (Weblio) and Nikkoku (Kotobank) evidence each comes from one dictionary. The `correction-public.json` entries are the author's paraphrases.
- **Unverified spelling claim:** my 臭う fetches failed, so the spelling preference for the literal unpleasant smell rests only on JMdict.
- **Not attempted:** live quiz draws, native-speaker certification, measured frequency, or an exhaustive synonym audit.
- **Deferred:** the earlier batch-61 飛ぶ/飛行 and 止まる/止む debt.
