## Snapshot

**4abf8105090403e90d2a950b90a733cd538d1424** (parent 303da3a4017ebf0405e76c88add06c490beaab6e). I reviewed committed content only. My file tools can't run Git, so the commit, the hashes, "unchanged" status and the patch's equivalence to the commit come from the author's frozen artifacts. I could not check them myself.

## Scope

**Model:** claude-opus-5.5 (family: claude). This was a read-only review with no edits and no delegation.

**Read in full:**
- **Frozen artifacts:** `frozen-snapshot.json` and `related.patch`.
- **Rules:** `.github\copilot-instructions.md`, `content-structure.instructions.md` and `docs\content-format.md:18-103`.
- **Articles:** all 20, including the unchanged `増える`.
- **Kanji:** all 8 edited bodies.
- **Source TSV:** line 1 and lines 1442–1461 only.
- **Private evidence:** the mappings, principals, components and labels JSONL files, `public-bodies.txt` and `supplement-comparison-reading.txt`.
- **Older article bodies (full):** 流行る, 流行, 回り, 宣伝, かわいそう, 気の毒, 乾燥, でたらめ.

**Other checks:**
- I checked titles and exclusions across `words\` with keyword searches, and checked that link targets exist in `words\` and `kanji\`.
- External pages I fetched:
  - jisho.org (a JMdict rendering, not the pinned version) for 流行る and 出鱈目.
  - kotobank, Nikkoku dictionary entry, for 含める.
  - One kotobank fetch returned an unrelated page, so it counts as a failed retrieval, not evidence.

**Not read:**
- **Private evidence:** `review-evidence.json`, `family-inspection-01..09`, `old-body-inspection-01..11` and `public-bodies.json`.
- **Docs:** `docs\confusable-words.md`, `docs\jlpt-levels.md` and the two snapshot JSONs.
- **Older bodies:** the other older bodies (for example でこぼこ, 暮れる, 様々, ぷくぷく and ぶくぶく). I judged those from titles and principal records only.

I did not touch any forbidden ledger or the `batch-73.json` sources file.

## Verdicts

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1442 | ピンク | CLEAN | CLEAN | CLEAN | Blank source spelling preserved; kanji: [] |
| N2:1443 | 便箋 | CLEAN | CLEAN | CLEAN | [紙] exclusion justified; 箋 left unlinked |
| N2:1444 | 瓶詰 | NEEDS FIX | CLEAN | CLEAN | B73-01; source spelling 瓶詰 kept; mixed on-first word correctly qualified as kango |
| N2:1445 | ファスナー | CLEAN | CLEAN | CLEAN | Blank source spelling preserved |
| N2:1446 | 風船 | CLEAN | CLEAN | CLEAN | Sense 2 marked dated, recognition only |
| N2:1447 | 不運 | NEEDS FIX | CLEAN | CLEAN | B73-04 |
| N2:1448 | 殖える→増える | CLEAN | CLEAN | CLEAN | N4, ふえる, title, [増] and no exclusions preserved; body teaches 殖える |
| N2:1449 | 深まる | CLEAN | CLEAN | CLEAN | Exclusions justified or conservative |
| N2:1450 | 不規則 | NEEDS FIX | CLEAN | CLEAN | B73-03 |
| N2:1451 | 普及 | NEEDS FIX | CLEAN | CLEAN | B73-02; transitive use supported (JMdict vt; Daijisen 新理論を―する) |
| N2:1452 | 付近 | CLEAN | CLEAN | CLEAN | 附近 noted as rare; exclusions complete for the area-word titles |
| N2:1453 | 拭く | CLEAN | CLEAN | CLEAN | 乾燥 is optional only |
| N2:1454 | 副詞 | CLEAN | CLEAN | CLEAN | Degree and statement-level adverbs match Daijisen |
| N2:1455 | 複写 | CLEAN | CLEAN | CLEAN | Exclusions justified |
| N2:1456 | 複数 | CLEAN | CLEAN | CLEAN | 復数 marked search-only |
| N2:1457 | 含める | CLEAN | CLEAN | CLEAN | Uses the ふくめる heading, not くくめる; senses 3–5 for recognition only |
| N2:1458 | 膨らます | CLEAN | CLEAN | CLEAN | Transitive/intransitive pair explained |
| N2:1459 | 膨らむ | CLEAN | CLEAN | CLEAN | ぷくぷく exclusion rests on family 2699730, not 5744803 |
| N2:1460 | 不潔 | CLEAN | CLEAN | CLEAN | 下品 justified by sense 2 |
| N2:1461 | 更ける | CLEAN | CLEAN | CLEAN | Season sense attributed to Daijisen, not to a JMdict sense |

**Kanji edits (all CLEAN; the patch only adds content, and headers and examples are preserved):**
- **瓶:** ビン row, footer 1491130.
- **詰:** -づ.め row with びんづめ, footer 1491130.
- **則:** ソク, footer 1491840.
- **普:** フ, footer 1497110.
- **副:** フク; existing entry converted to a link; footer 1500440 already present.
- **詞:** シ, footer 1500440 added.
- **複:** 複写 with footer 1501390 added; 複数 converted to a link, footer 1501400 already present.
- **含:** ふく.める; existing entry converted to a link; footer 1216890 already present.

No cards were invented for 箋, 殖, 及, 拭, 膨 or 潔.

**Baseline and mappings:**
- **増える baseline:** CLEAN on content. Git could not confirm it is unchanged.
- **Mappings:** all 20 CLEAN. Entries, selected and additional senses, and 殖える→1602440 at N4 all match the TSV rows.

## Findings

**B73-01**
- **Severity / facet:** Minor; Correctness (pronunciation).
- **Location:** `words\瓶詰.md:48-49`
- **Claim and impact:** "Learn the long vowel and voiced ending: びんづめ". びんづめ has no long vowel, so this may lead learners to lengthen a sound that isn't there.
- **Remedy:** Change it to "moraic ん and voiced ending", or drop "long vowel".
- **Evidence:** JMdict 1491130 gives the reading びんづめ; Daijisen gives びん‐づめ. The article's own line 33 says ビン + づめ.
- **Confidence:** High.

**B73-02**
- **Severity / facet:** Minor; Correctness (exclusion omitted).
- **Location:** `words\普及.md:9`
- **Claim and impact:** 流行る ("be popular; be prevalent; flourish") is not excluded. "Be prevalent" could fairly be accepted as an answer for 普及.
- **Remedy:** Add 流行る.
- **Evidence:** JMdict 流行る sense 2: "to be prevalent; to spread widely". 普及 (1497110): "diffusion; spread; popularization".
- **Confidence:** Medium.

**B73-03**
- **Severity / facet:** Minor; Correctness (exclusion omitted).
- **Location:** `words\不規則.md:9`
- **Claim and impact:** でたらめ ("nonsense; haphazard") is not excluded, though both words share the gloss "unsystematic".
- **Remedy:** Add でたらめ.
- **Evidence:** 1491840 gives "irregular; unsystematic; unsteady; disorderly". JMdict でたらめ sense 2, which the でたらめ article teaches, gives "random; haphazard; unsystematic", with the example でたらめに並べる.
- **Confidence:** Medium-high.

**B73-04**
- **Severity / facet:** Minor; Correctness (exclusion omitted).
- **Location:** `words\不運.md:9`
- **Claim and impact:** かわいそう ("pitiable; unfortunate") is not excluded. The article itself teaches 不運な as "unfortunate".
- **Remedy:** Add かわいそう.
- **Evidence:** `不運.md:17` ("an unfortunate event") and `不運.md:20` ("Unfortunately"). かわいそう's body says かわいそうな人, "an unfortunate person".
- **Confidence:** Low-medium.

## Optional

- **含める:** Say that the "make understand" sense is mostly heard in set phrases (かんで含める, 言い含める, 因果を含める). This is a usage tendency I could not verify; Daijisen's examples are only these phrases.
- **拭く:** Consider excluding 乾燥, which shares "drying" (乾燥 can be transitive: 木材を乾燥する). Low confidence.
- **瓶詰:** Mention the product-noun use, 瓶詰を開ける.
- **複写:** Add a register note contrasting it with コピー.
- **普及:** Note 普及させる and 普及に努める as common ways to say "promote".
- **複数:** Mention 複数形.

## Limits

- **No Git:** I could not check the commit, hashes or that 増える is unchanged.
- **Thin dictionary evidence:** Daijisen is one authority, and the jisho.org pages are not the pinned JMdict.
- **Unread inspection files and older bodies:** I did not read the 20 private inspection files, `review-evidence.json`, `public-bodies.json`, or most older bodies.
- **Exclusion search not exhaustive:** I searched for missing exclusions by title keywords, not across every article.
- **Not native-speaker certified:** my judgments on whether examples sound natural are my own.
