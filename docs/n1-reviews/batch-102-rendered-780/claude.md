# Batch 102 rendered confirmation (snapshot 54be1c9a)

**Bottom line:** No proven defects. The 劣 and 優劣 articles, the two navigation changes in 劣る and 優, the sampled meaning quiz, both reading questions, and drawing presentation are all CLEAN within the sampled scope. Font family identity and real-phone use remain unverified.

## Snapshot
- **Model:** Claude Opus 5.5 (`claude-opus-5.5`).
- **Versions:** teaching snapshot 54be1c9a, unchanged (empty diff); docs-evidence HEAD b1300635; app bf30cdea.
- **This is a dependent rendered confirmation, not a blind initial review.**

## Scope
- **Text resources:**
  - resource-01: full view, then lines 3300–3463 re-viewed.
  - resource-02: full view, then lines 2325–2339 re-viewed.
  - resource-03, resource-04, resource-05: one full view each; each ended at its expected closing content.
  - The combined packet was not read this turn.
- **Images:** 43 of 43 PNGs opened, one view each.
  - **Protocol deviation:** curated-kun-feedback and curated-kun-question were opened in a single parallel batch. Every other view was serial.
- **Unique visual states: 25.** Clock differences mean the "identical" screenshots aren't byte-identical.

| Group | Opens | Unique states |
|---|---|---|
| 劣 article | 16 | 6: 00; 02=03; 04; 06=08; 07=09=10 (scrolled sideways); 12=13=15–19 |
| 優劣 article | 10 | 2: 01–04; 06=08=09=11=12=components |
| Curated reading screens | 5 | 5 |
| Drawing | 3 | 3 |
| Font panels | 4 | 4 |
| Meaning quiz | 2 | 2 |
| otoru-components, selection, yuu-new-reciprocal | 3 | 3 |

## Verdicts (correctness / scoped coverage / comprehensibility)

| Item | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji/劣.md` | CLEAN | CLEAN | CLEAN |
| `words/優劣.md` | CLEAN | CLEAN | CLEAN |
| `words/劣る.md:26` | CLEAN | CLEAN | CLEAN |
| `kanji/優.md:42` | CLEAN | CLEAN | CLEAN |
| Sampled meaning quiz | CLEAN | CLEAN (finite sample) | CLEAN |
| Reading questions, feedback and done screen | CLEAN | CLEAN | CLEAN |
| Drawing presentation | CLEAN | CLEAN | CLEAN; handwriting mastery UNVERIFIED |
| Fonts (all 31 Han, four panels) | CLEAN (no tofu) | CLEAN | CLEAN; family identity UNVERIFIED |

What the images show for each item:

- **`kanji/劣.md`:** the whole article is visible:
  - metadata: 6 strokes, radical 力 no. 19 at the bottom, N1 (community list);
  - the line saying 優劣 does not mean inferiority alone, and the favourable 劣らない;
  - the mnemonic, labelled as not etymology;
  - the readings table with both readings (レツ, おと.る), plus the ユウ/レツ split;
  - notes on the lookalikes 努, 功 and 省;
  - the note on naming the comparison dimension, and the sources.
- **`words/優劣.md`:** the whole article is visible. Both examples and their English are natural, including 優劣はない and 優劣をつけがたい. It covers the long ゆう, the 比較 and 質 comparisons, and the warning against judging a person's worth.
- **`words/劣る.md:26`:** the linked 劣 passage is visible (otoru-components).
- **`kanji/優.md:42`:** the 優劣 bullet is visible (yuu-new-reciprocal).
- **Six link directions:** every anchor is visible (劣→劣る, 劣→優劣, 劣る→劣, 優劣→劣, 優劣→優, 優→優劣). The actual taps, Back and offline behaviour are supported only by the JSON evidence.
- **Meaning quiz:** the screen shows N1 · 134 cards. The live options were 劣 inferior; worse / 冗 superfluous / 蛍 firefly / 功 merit (the opposite).
  - All 40 sampled fallback labels look defensibly wrong. Nearest neighbours: 乏, 凡 (HOST only), 凶, 丙, 凹.
  - The guards are direct and are not treated as transitive.
- **Reading questions:**
  - on'yomi: コウ / チョウ / レツ / トツ.
  - kun'yomi: おかす / つくる / ほたる / おとる.
  - Both were answered correctly, feedback shows "レツ、おとる", and the done screen shows 2/2.
- **Drawing:** stroke numbering 1–6 is correct. The trace is labelled ungraded. Recall reveals the answer.
- **Fonts:** all 31 Han are present in all four panels, with no tofu. The lookalike pairs 少/奴 and 力/目 are distinguishable, and the 少 sweep crossing 力 is visible.

## Adjudication of original items
- **Resolved** (rendered evidence now covers what the text review left open): article presentation, the six link anchors, N1 selection, the meaning question, both reading questions and the done screen, trace and recall presentation, and glyph rendering.
- **Partially resolved:** the runtime choice semantics, which are verified only for the finite sample.
- **Withdrawn:** the earlier 110-family and 23-article miscounts.
- **Still optional:** 劣化, 卑劣/下劣, 優劣つけがたい.
- **Unresolved:** phone acceptance, native-speaker review, and measured learning effect.

## Findings
None proven.

## Optional
- **drawing-feedback.png (low; app UI, not batch content):** "Practice only: this attempt is not graded" appears alongside "Graded by stroke shapes only". Possible remedy: reword one of the two messages.
- **Font panels:** at panel scale, the Mincho and Textbook rows look close to Gothic. This is not a defect; it's just unconfirmed.

## Limits
- No independent Git or upstream verification, and no new tests or retrieval.
- Evidence comes from an API 35 emulator, not a physical phone, and there was no native-speaker review.
- The installed font family face wasn't identified.
- Drawing and handwriting were not graded. Random pools beyond the samples aren't certified, and learning effect wasn't measured.
