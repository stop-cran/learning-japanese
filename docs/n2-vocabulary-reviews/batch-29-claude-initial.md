## Snapshot
Frozen commit: `abb39bbd85d529380cb2506b9ca7f3c2df59c8b3` (parent `c44d056b40fa6dba43fcd6be27543367f6f07adf`). I reviewed committed content only, as the receipt records it. I had file tools but no Git or hash execution, so I could not confirm the commit, the diff, or any hash myself.

## Scope
- **Reviewer:** claude-opus-5.5 (Claude family), working sequentially with no delegation and no edits.
- **Articles:** I read all twenty new articles in full.
- **Related edit:** I read the `kanji\零.md` patch and the changed passages in context.
- **Mappings:** I checked `docs\n2-vocabulary-sources.tsv`, rows N2:562–581 (file lines 562–581).
- **Evidence packet:** I read the rows, principal families, component records, provenance, existing labels, receipts, quiz declarations and the homograph and limits sections. I only spot-checked the comparison families (lines 3170–12255).
- **Other files:** I checked neighbouring words and kanji cards as needed.
- **Not read:** none of the forbidden files.

## Verdicts
Quiz, title and exclusion problems are scored under comprehensibility.

| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 琴 | NEEDS FIX | CLEAN | NEEDS FIX |
| 言付ける | CLEAN | CLEAN | NEEDS FIX |
| 言葉遣い | CLEAN | CLEAN | CLEAN |
| こないだ | CLEAN | CLEAN | NEEDS FIX |
| 御無沙汰 | CLEAN | CLEAN | CLEAN |
| こぼす | CLEAN | CLEAN | CLEAN |
| 零れる | CLEAN | CLEAN | CLEAN |
| ゴム | CLEAN | CLEAN | CLEAN |
| ごめん | CLEAN | CLEAN | NEEDS FIX |
| ごめんください | CLEAN | CLEAN | CLEAN |
| 小指 | CLEAN | CLEAN | CLEAN |
| こらえる | CLEAN | CLEAN | CLEAN |
| 娯楽 | CLEAN | CLEAN | CLEAN |
| 御覧 | CLEAN | CLEAN | CLEAN |
| コレクション | CLEAN | CLEAN | CLEAN |
| 転がす | CLEAN | CLEAN | CLEAN |
| 転がる | CLEAN | CLEAN | CLEAN |
| 紺 | CLEAN | CLEAN | CLEAN |
| コンクール | CLEAN | CLEAN | CLEAN |
| コンクリート | CLEAN | CLEAN | CLEAN |

**零 edit: CLEAN / CLEAN / CLEAN.**
- It keeps the card's identity, metadata and existing content.
- The 零す link goes to the kana-primary `こぼす.md`, and the 零れる link goes to `零れる.md`.
- The new backlink's contrast (水がこぼれる vs 水をこぼす) does appear in `零れる.md:18,30`.
- 零 is the only N2 kanji card involved, and both of its new links match readings the articles actually teach.
- Missing kanji (琴, 遣, 無, 沙, 汰, 娯, 覧, 紺, 免) stay as metadata only.

**Mappings N2:562–581: CLEAN / CLEAN / CLEAN for all twenty.**
- Every source spelling, reading and selected sense is actually taught.
- 御免 is taught in the kana-primary ごめん article: senses 1, 3, 4 and 5, plus sense 2 as an additional sense.
- The コレクション "correction" meaning is presented as a separate Digital Daijisen headword, with no invented JMdict identity.
- Reading restrictions are respected: そう only with 箏/筝, こたえる only with 堪える.

## Findings
**B29-CL-01 — Minor — Correctness — `words\琴.md:24`**
- **Claim:** "The dictionary also records 筝 as an older character form."
- **Evidence:** The cited JMdict family 1241450 lists 筝 with no age or outdated flag. Wiktionary describes 筝 as the simplified form of traditional 箏, and as an "alternative form of 箏" in Japanese. The claim is unsupported and probably backwards.
- **Remedy:** Call 筝 a variant form of 箏 and drop "older".
- **Confidence:** High that the claim is unsupported; medium-high that it is backwards.

**B29-CL-02 — Minor — Comprehensibility (quiz) — `words\琴.md:1-9`**
- **Problem:** The article declares no exclusions, so 楽器 ("musical instrument") can appear as a defensible wrong choice for "koto".
- **Precedent:** `楽器.md:9` already excludes ピアノ, バイオリン, ギター, 笛 and オルガン for the same reason, and this batch excludes the parent term 指 from 小指. The evidence label list did not include 楽器.
- **Remedy:** Add `quiz_exclusions: [楽器]`.
- **Confidence:** High.

**B29-CL-03 — Minor — Comprehensibility (quiz) — `words\こないだ.md:4,9`**
- **Problem:** The title "the other day; recently" overlaps "lately", which appears in 近頃 ("lately; nowadays", `近頃.md:4`) and このごろ ("these days; lately", `このごろ.md:5`). Only 最近 is excluded.
- **Evidence:** The source row (TSV:565) and JMdict 1004610 (evidence lines 401–403) both gloss こないだ as "lately". Those three words already exclude one another (`近頃.md:9`, `このごろ.md:3`).
- **Counterpoint:** In Japanese, こないだ marks a single recent event while 近頃/このごろ describe an ongoing period. The ambiguity lives in the English labels.
- **Remedy:** Add 近頃 and このごろ to the exclusions.
- **Confidence:** Medium.

**B29-CL-04 — Minor — Comprehensibility (quiz) — `words\言付ける.md:4,9`**
- **Problem:** The article excludes 預ける ("entrust; leave in someone's care") because of the shared word "entrust". It does not exclude 任せる ("entrust; leave to", `任せる.md:4`), which leads with the same word.
- **Evidence:** 任せる and 預ける already exclude each other (`任せる.md:9`). The evidence label list did not include 任せる.
- **Remedy:** Add 任せる, or retitle away from "entrust".
- **Confidence:** Medium.

**B29-CL-05 — Minor — Comprehensibility (quiz) — `words\ごめん.md:4,9`**
- **Problem:** The title "sorry; no thanks" overlaps お待ちどおさま ("sorry to have kept you waiting") and お待たせしました ("thank you for waiting; sorry to have kept you waiting").
- **Evidence:** Both of those words already exclude the near-equivalent ごめんなさい ("I am sorry") (`お待ちどおさま.md:9`, `お待たせしました.md:9`). Neither appears in the evidence label list.
- **Remedy:** Add both; optionally consider あいにく ("unfortunately; sorry, but").
- **Confidence:** Medium.

## Optional
- **ごめん.md:40:** The bare ごめん before honorific いらっしゃいますか mixes registers. Daijisen's own examples are ごめん、お邪魔するよ and では、ごめん.
- **御無沙汰 vs 久しぶり:** Both are used in "long time no see" greetings, so an exclusion could be considered. The article already explains the difference.
- **こないだ:** Could mention that it can be written 此間.
- **琴:** Could link the mention of 弾く and note that technically 琴 and 箏 are different instruments.
- **N2:573 note:** こたえる sits inside entry 2827352 itself as a reading limited to 堪える. Calling it a "distinct" reading is accurate but could be read as "a separate entry".

## Limits
- I ran no Git or hash commands, so the snapshot, patch and file hashes are taken from the receipt.
- I only spot-checked the comparison families.
- **Public receipts:** Of the author's public-dictionary receipts, I independently retrieved only Daijisen 御免, via the weblio raw HTML. It confirms 名字帯刀が―になる and お役が―になる. I also checked 筝 on Wiktionary. The first weblio 筝 lookup returned an unrelated page. The Kotobank Daijisen section did not load, and goo failed to resolve. The other receipts remain the author's assertions.
- There was no native-speaker or corpus check. The naturalness of ごめん、どなたかいらっしゃいますか is unverified.
- My tool calls saved some raw HTML to `%TEMP%`. I had no delete tool, so those files remain.
