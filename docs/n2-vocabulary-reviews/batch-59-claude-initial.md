I reviewed all twenty rows. Nine cells need fixes: eight are about which words may appear together as quiz choices, and one is about a confusing sentence in 動作. Everything else is clean within what I read, including the kanji edits and the mappings.

# Snapshot
`54b4f9d77337e80b47f42b9a0b7a9acd6f8eb846` (parent `51d5355510987eef1816e164903d8c1ec6907067`). Committed content only. File tools can't run Git, so I didn't check the commit, the cleanliness flag, whether `related.patch` matches the commit, or the "no reused edits" claim myself. Those come from the author.

# Scope
- **Model:** Claude Opus 5.5 (`claude-opus-5.5`, claude family), working alone and read-only.
- **Instructions:** `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md`, and `docs\content-format.md:18-103`. A grep also showed some lines outside that range; I didn't rely on them.
- **Assigned files, read in full:** all 20 new articles, `related.patch`, and the complete `kanji\池.md`, `柱.md`, `波.md` and `銅.md`.
- **Mappings and evidence:** the TSV header and rows 1162–1181, and the private files `frozen-snapshot.json`, `review-mappings.jsonl` (20), `review-principals.jsonl` (20 families, 31 senses), `review-components.jsonl` (29), `review-labels.jsonl` (231) and `public-bodies.txt` (20 Daijisen captures).
- **Older articles, read in full:** 移動, 方々, 採点, 合図, 転がす, 散らかる, 速力, 境, 次々, サイン, 頂点.
- **Older articles, partial:** title and exclusion lines across `words\` via grep, plus parts of 罹る. A grep of `confusable-words.md` found none of the 20 words.
- **Not read:**
  - private files: `review-evidence.json`, `public-bodies.json`, family-inspection-01–09, and the support and electrical comparison files
  - docs: `jlpt-levels.md`, `n2-vocabulary-snapshot.json`, `n2-source-snapshot.json`
  - no external pages fetched

# Verdicts
C = correctness, Cov = scoped coverage, Comp = comprehensibility.

| Row | Article | C | Cov | Comp |
|---|---|---|---|---|
| N2:1162 | 電球 | CLEAN | CLEAN | CLEAN |
| N2:1163 | 点数 | NEEDS FIX | CLEAN | CLEAN |
| N2:1164 | 伝染 | CLEAN | CLEAN | CLEAN |
| N2:1165 | 電池 | CLEAN | CLEAN | CLEAN |
| N2:1166 | 点々 | NEEDS FIX | CLEAN | CLEAN |
| N2:1167 | 転々 | NEEDS FIX | CLEAN | CLEAN |
| N2:1168 | 電柱 | CLEAN | CLEAN | CLEAN |
| N2:1169 | 天皇 | CLEAN | CLEAN | CLEAN |
| N2:1170 | 電波 | NEEDS FIX | CLEAN | CLEAN |
| N2:1171 | テンポ | NEEDS FIX | CLEAN | CLEAN |
| N2:1172 | 電流 | CLEAN | CLEAN | CLEAN |
| N2:1173 | 電力 | CLEAN | CLEAN | CLEAN |
| N2:1174 | 問い合わせ | CLEAN | CLEAN | CLEAN |
| N2:1175 | 銅 | CLEAN | CLEAN | CLEAN |
| N2:1176 | 統一 | CLEAN | CLEAN | CLEAN |
| N2:1177 | 同格 | CLEAN | CLEAN | CLEAN |
| N2:1178 | 峠 | NEEDS FIX | CLEAN | CLEAN |
| N2:1179 | 統計 | CLEAN | CLEAN | CLEAN |
| N2:1180 | 動作 | NEEDS FIX | CLEAN | NEEDS FIX |
| N2:1181 | 東西 | CLEAN | CLEAN | CLEAN |

**Kanji edits: all CLEAN.**
- **池:** links the existing 電池 text in the チ row and in Common words. Source ID 1443620 was already present.
- **柱:** adds 電柱 to the チュウ row and keeps 支柱; adds a Common words entry and ID 1443630.
- **波:** adds 電波 (でんぱ) to the ハ row and keeps 波長; adds a Common words entry and ID 1443720.
- **銅:** links 銅 in the ドウ and あかがね rows and in Common words. The medal sense stays restricted to どう.
- Front matter is unchanged in all four. All four word articles link back to their kanji.

**Baseline metadata preservation: CLEAN, based on the author's assertions.**
- No old word articles were edited, and the どう adverb article is untouched.
- Every primary written kanji is in metadata: テンポ has `[]` and 問い合わせ has `[問, 合]`.
- 染, 皇, 統 and 峠 have no kanji cards and are left as plain text, which is correct.

**Mappings: all 20 CLEAN.**
- The main and additional senses match what each article teaches.
- Raw source fields are kept as they are: the wrong 統計 gloss, the empty 転々 gloss and the empty テンポ kanji field.
- Spelling and reading restrictions are taught correctly:
  - 電波: kana-only デンパ/デムパ readings
  - 銅: どう/あか/あかがね
  - 東西: the attention-call use is restricted to とうざい, and ひがしにし is obsolete

# Findings
All findings except B59-08 concern `quiz_exclusions`. Per `content-format.md:95`, a pair needs an exclusion when "a learner could reasonably accept either title" for either word.

- **B59-01** · Medium · quiz exclusions · `words\動作.md:4,9`
  - **Claim:** 動作 ("movement; behavior; operation") and 移動 ("movement; relocation", `移動.md:4`) share the first gloss "movement". They also share 動 and the tags kango, movement and suru-verb, so the app is likely to offer them together. Neither article excludes the other, yet 転々 excludes 移動 for a weaker overlap.
  - **Remedy:** add 移動 to 動作's exclusions.
  - **Confidence:** high.
- **B59-02** · Low · quiz exclusions · `words\電波.md:4,9`
  - **Claim:** 電波's title includes "signal", and 合図 ("signal; cue") and サイン ("…; signal") are not excluded. Only 信号 is.
  - **Evidence:** existing words with "signal" in the title already guard each other: サイレン excludes 合図/信号/サイン, サイン excludes 合図, and 合図 excludes 信号.
  - **Remedy:** add 合図 and サイン.
  - **Confidence:** medium.
- **B59-03** · Low · quiz exclusions · `words\転々.md:4,9,23`
  - **Claim:** 転がす ("roll something along; tip over") shares 転 and overlaps "rolling" (JMdict sense 2, "rolling about"). 転がる is excluded but 転がす is not. 転がす's own exclusions (`転がす.md:9`) closely mirror 転々's list.
  - **Remedy:** add 転がす.
  - **Confidence:** medium.
- **B59-04** · Low · quiz exclusions · `words\点々.md:4,9`
  - **Claim:** 散らかる ("be untidy; lie scattered around", `散らかる.md:4,16`) overlaps "scattered here and there". ぽつぽつ and ぱらぱら, which also mean "scattered", are already excluded.
  - **Remedy:** add 散らかる.
  - **Confidence:** medium.
- **B59-05** · Low · quiz exclusions · `words\点数.md:4,9`
  - **Claim:** 採点 ("marking; grading; scoring") shares 点. `採点.md:21` notes that Daijisen also uses 採点 for the score itself. JMdict 点数 sense 1 is "marks; points; score; grade".
  - **Remedy:** add 採点.
  - **Confidence:** medium.
- **B59-06** · Low · quiz exclusions · `words\峠.md:4,9`
  - **Claim:** 峠 excludes 山, 頂上 and 盛り, but not 頂点 ("summit; apex; vertex"). 頂点 itself excludes those same three words and teaches a figurative peak (人気の頂点, `頂点.md:17,23`). Daijisen 峠 sense 2 is 絶頂.
  - **Remedy:** add 頂点.
  - **Confidence:** medium.
- **B59-07** · Low · quiz exclusions · `words\テンポ.md:4,9`
  - **Claim:** 速度 ("speed; rate") is excluded but 速力 ("speed; rate of motion", `速力.md:4,9`) is not. "Pace" overlaps 速力 at least as much as it overlaps 速度.
  - **Remedy:** add 速力.
  - **Confidence:** low–medium.
- **B59-08** · Low · comprehensibility · `words\動作.md:44`
  - **Claim:** the sentence 'The English gloss "manners" here…' points to a gloss the learner never sees. The title, examples and JMdict 1451350 senses 1–3 contain no "manners"; it appears only in the raw TSV gloss for N2:1180.
  - **Remedy:** reword, e.g. 'Some word lists gloss 動作 as "manners"; that does not mean…'.
  - **Confidence:** high.

# Optional
- **統計:** the Daijisen example 就業人口を統計する supports `調査結果を統計しました` (line 21). Since 統計を取る is the more common phrasing, consider leading with it.
- Pairs worth considering, but I didn't establish an exclusion is needed:
  - 伝染 / 罹る (both tagged health)
  - 電球 / スタンド (contrasted at line 35)
  - 動作 / 自動
  - 点々 / 散らす / 散らかす / 散る
- **電波:** the title's "reception" could read "signal reception" so it doesn't look like 受付 ("reception").

# Limits
- **Git:** the commit and parent, committed-content status, patch equivalence and "no reused edits" are the author's claims, not my checks.
- **Unread evidence:** the files listed under Scope. Wider-family claims beyond the 20 main records and 231 labels are not verified.
- **Older articles:** only 11 were read in full; the rest are judged from titles and exclusion lines.
- **Dictionary support:** the Daijisen captures come from one service and were retrieved by the author. I fetched no second dictionary for あくびが伝染, テンポ meaning pace, or how common 統計する is.
- **Naturalness:** examples have not been checked by a native speaker.
