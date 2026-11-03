Snapshot: Intended commit `42e9732b305f1a83f4e5bf3a86a78fbb538c9350`. I could not confirm it independently. The worktree's `.git` points to a gitdir outside the worktree, and I did not read it. No uncommitted changes were included, and I made no edits.

Scope: Claude Opus 5.5 (`claude-opus-5.5`), single reviewer. All reads were complete and serial, with one tool call per response.
- **Rules:** `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md`, `docs\content-format.md` lines 42–148 and `docs\jlpt-levels.md` lines 1–110.
- **Teaching files:** `kanji\桂.md`, `kanji\梢.md`, `words\桂.md` and `words\梢.md`.
- **Metadata:** `batch-012-input-metadata.json`, with both raw KANJIDIC2 records.
- **Dictionary packets:** all four, every line. The main packet was read as lines 1–250, 250–500, 500–750 and 750–803. The comparisons packet was read as 1–250, 250–500 and 500–782. The notes packet was read as 1–200 and 200–358. The supplement was read as 1–265.
- **Comparison kanji:** 柱, 村, 掛, 消, 晴, 深, 末, 先, 枝 and 木.
- **Comparison words:** 木, 植物, 植える, 植木, 枝, 先, 端, 末, 先端, 頂上, トップ and 楠.
- **Confusable pairs:** two scoped searches of `docs\confusable-words.md`.
- **Web sources:** all four Kotobank pages. The 桂 page needed a second request to read the rest of the page.

Verdicts:
- `kanji\桂.md`: correctness NEEDS FIX; scoped coverage CLEAN; comprehensibility NEEDS FIX.
- `kanji\梢.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `words\桂.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `words\梢.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.

Findings:
1. Minor; comprehensibility; `kanji/桂.md:22`.
   - **Claim and impact:** "In other words 桂 can refer to different aromatic trees, including cinnamon, or to a shogi piece." In English, "In other words" usually means "that is to say". A learner may read the sentence as restating the katsura meaning, which suggests that the katsura tree is cinnamon or a shogi piece. That is the confusion the next sentence tries to prevent.
   - **Remedy:** Write "In other vocabulary (compounds and separate nouns), 桂 can refer…".
   - **Evidence:** The sentence itself. Daijisen's 漢字項目 ケイ gives separate senses: ①香木の総称, ③将棋の駒. Seisenban gives けい【桂】① and ③ separately from かつら【桂】①.
   - **Confidence:** Medium-high.
2. Minor; correctness; `kanji/桂.md:46`.
   - **Claim and impact:** The card describes 掛 as 桂-like "with a hand-side form and an extra far-right stroke". 掛 actually adds 卜, which has two strokes. The description gives the wrong count of added strokes for this look-alike comparison.
   - **Remedy:** Say "an extra 卜 at the far right".
   - **Evidence:** 掛 = 扌(3) + 圭(6) + 卜(2) = 11 strokes. 桂 = 木(4) + 圭(6) = 10 strokes. The existing `kanji\掛.md` itself says "the far-right 卜" and "the final 卜".
   - **Confidence:** High.

No other actionable defects:
- **Metadata:** All five KANJIDIC2 readings (ケイ / かつら; ショウ / こずえ / くすのき) are preserved in source order. Strokes, radical and grade match. `quizOnyomi: []` turns off on'yomi questions without deleting the readings.
- **Unselected readings:** Each is explained. ケイ: 桂馬 (1821380), 桂 けい as a shogi abbreviation (1921970) and 桂皮 (1250930). ショウ: 末梢 (1525440) and 末梢神経 (1525450). For 梢 くすのき, the claim that no word/reading pair exists is accurate: entry 1460720 is written only 樟 / 楠.
- **Selected readings:** かつら (1250890) and こずえ (1349980) are verified, and the 杪 rare-spelling flag is described as a spelling qualification.
- **桂 senses:** The deciduous claim is supported by Seisenban's 落葉大高木. The wig homophone (1609590, usually written in kana) is handled correctly.
- **梢 compounds:** The treetop/twig-tip meaning, 末梢's figurative and anatomical senses, and the separation of those compounds from the noun こずえ match JMdict, Daijisen and Seisenban. Seisenban also attests 小鳥梢に囀ず, supporting the bird example.
- **Quiz exclusions:** All are direct pairs justified by actual titles or ordinary senses. KANJIDIC's "twig" meaning for 梢 supports the 梢–枝 exclusion. The 梢–先 exclusion fits 先's ordinary "tip" sense.
- **Distractors:** The kanji distractors are semantically distinct.

Optional:
- 桂: The cards could state explicitly that Chinese 桂 usually refers to osmanthus or cinnamon. Daijisen けい② and 世界大百科 (Japanese katsura is 別物) support this.
- 桂: The cards could also note the "Japanese Judas tree" label in KANJIDIC2/JMdict.
- 桂馬's go sense is usually written ケイマ.
- 字通 classifies both kanji as 形声 (phonetic 圭 / 肖). The current `structure-unclassified` tag is permissible.
- `words/梢.md` second example: "perched in the treetop" may read more naturally than "at a branch tip".

Limits:
- **Not opened:** `kanji\楠.md`. The `[楠](楠.md)` link in `kanji/梢.md` is unverified.
- **Not run:** the validator and manifest build.
- **Not checked:** the per-packet family counts (44 / 25 / 9 / 10).
- **Partial read:** only searches of `docs\confusable-words.md`, not the full file.
- **Web sources:** Kotobank was fetched live on 2026-11-03, not as a frozen copy. 字通 gaiji images were not decoded. The マイペディア section for 桂 had no body text. These gaps don't affect the conclusions.
- **Review type:** This was a text-only review. No phone rendering, native-speaker check, frequency check or effectiveness measurement was done.
- **Tool use:** Every tool call was serial, with no parallel calls or overlap.
