I confirm both of my original items are fixed and the changed text introduces nothing wrong. Both teaching files are now CLEAN on all three facets. I made no edits.

**Snapshot:** revised commit `4fb01fa2a1a2c8d610480e7e2d5cdbae36c8bfdb`, compared against initial commit `ba95ac3fb68c4cc9a6d9c6e3c96faa956898af1b`. No uncommitted teaching was included.

**Scope:**
- **Reviewer:** Claude Opus 5.5 (`claude-opus-5.5`), as reported by the runtime. This is the same session that wrote the initial report.
- **Read in this order:**
  1. My own initial report, `docs\n1-reviews\batch-014-initial-claude.md`, in full.
  2. The whole `control\batch-014-correction.diff`.
  3. The whole revised `kanji\椎.md`.
  4. The whole unchanged `words\椎骨.md`.
  5. `docs\n1-sources\batch-014-review-external-evidence.json` in full.
  6. `batch-014-jmdict.xml` lines 176–202 (entry 1956700, つち "hammer/mallet") and lines 230–249 (entry 2183460, しい "chinquapin").
  7. The raw Kotobank 椎 page from index 70000, length 14000. This returned the full Jitsū heading, 字訓 and 訓義 sections.
- **Out of scope:** I did not repeat the full review of all 117 dictionary families.

**Verdicts:**
- `kanji\椎.md`: correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.
- `words\椎骨.md`: correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.

**Findings:**
- **My Finding 1 (しい is usually written in kana) is resolved.** The paragraph after the readings table now says: "JMdict marks the tree word as usually written in kana: しい or シイ."
  - This matches entry 2183460, which carries "word usually written using kana alone". シイ in that entry is a kana-only form, and the sentence does not attach シイ to the 椎 spelling.
  - The note is stated as a JMdict tendency, not a strict rule. It fits next to the existing nanori explanation and the 椎茸 kana note.
- **The new う.つ wording (the other reviewer's item, checked here for regressions) introduces no errors.** I checked it against Jitsū (普及版 字通) myself:
  - The heading reads "椎 / 常用漢字 12画".
  - 字訓 lists つち・うつ・たたく・しい.
  - 訓義 2 reads "うつ、つちでうつ", which supports the card's gloss "strike; hit with a mallet".
  - The row correctly calls this a character meaning and keeps "no verified modern word with this exact written boundary". It does not suggest 椎つ as a spelling.
  - The reading stays labelled "source-only here", and `quizKunyomi: []` is unchanged.
- **Unchanged parts and the 椎骨 article:**
  - The full metadata and its order (ツイ, スイ / つち, う.つ), `quizOnyomi: [ツイ]`, the wrong-answer choices, the mnemonic and the Notes section are all unchanged.
  - Nothing in the revised character card contradicts 椎骨: its ツイ reading, its anatomy register, its examples, or its statement that the しい reading is not used in the word.
  - The new source line correctly points to Jitsū on the same Kotobank page.

**Optional:**
- **My optional mallet-spelling wording item is resolved.** The row now reads "JMdict marks 椎 as a rare spelling; alternative spellings include 槌 and 鎚". That matches 1956700, where only 椎 carries "rarely used kanji form".
- **My optional 脊髄 contrast remains optional and was not taken up.** That is acceptable.
- **My 幹/椎骨 quiz note was already non-defective** and needs no action.
- **Jitsū classifies 椎 as a phonetic compound (形声) with 隹 as the sound component.** The card keeps `structure-unclassified`, and this task says not to reclassify structure, so this is not a defect. Any future structural revision would need a separate, qualified source review.
- **Jitsū 訓義 5 links "しい、しいの木" to "スイの音でよむ".** This does not show a modern word read スイ, so the card's "no verified lexical example" for スイ still holds.

**Limits:**
- **Process:** in this follow-up I made exactly one tool call per response and waited for each result, with no parallel calls. My initial report's disclosed parallel read is preserved unchanged.
- **Kotobank page:** the raw fetch was cut off at index 84000, but the rest was related-links boilerplate. I did not reconstruct the gaiji images in Jitsū's etymology section, nor use them for anything.
- **Frozen evidence:** the JMdict excerpts are frozen supplied copies, not a fresh download from the upstream source.
- **Not tested:** this closure is text-only. It is not a native-speaker check, a physical-phone or app test, or publication acceptance.
