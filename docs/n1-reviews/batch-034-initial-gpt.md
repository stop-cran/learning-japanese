**Snapshot:** `9800f1a1935fff861e4a9c0374bc6cad8ecf2f34`, as identified by the frozen task; no uncommitted teaching included. Read-only review; no changes made. Git state was not independently inspected.

**Scope:** GPT-6.1 Sol (`gpt-6.1-sol`), initial independent review of all 63 lines of `kanji\猪.md` and all 51 lines of `words\猪.md`, covering correctness, scoped coverage and textual phone comprehensibility.

Completed all assigned instruction/reference ranges; all four raw KANJIDIC2 character elements; all 39 families in `batch-034-jmdict.xml` (1–796) and all 21 comparison families (1–647), including every spelling, reading, restriction, sense and flag. This includes complete families 1427010, 1427020, 1427050, 1427060, 1913260, 2203180, 2203230 and the separate 2833885 family. Read all three comparison kanji cards and all seven comparison word articles. Inspected the supplied Digital Daijisen HTML at 1770–1807 and 1808–1845, including the actual bodies of all four specified entries. Searched the confusable-word inventory for the assigned words; that inventory inspection was partial.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| `kanji\猪.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\猪.md` | **NEEDS FIX** — quiz ambiguity; prose clean | **CLEAN** | **CLEAN** |

**Findings:**

1. **Minor; correctness / quiz answer uniqueness; `words\猪.md:1–8,32–35`.** The new word has title `wild boar` but no direct exclusion against `動物`, whose displayed title is `animal`. In a Japanese-to-English meaning question showing 猪, both labels are defensible descriptions. Explaining the broader category in the article does not prevent those choices from appearing together.

   **Remedy:** Declare the direct 猪/動物 exclusion on either article, retaining both accurate titles and the useful category comparison.

   **Evidence:** `words\動物.md:4` supplies `title: animal`; its meaning and distinctive-meaning sections explicitly include wild mammals. Frozen JMdict 1427010 identifies 猪/いのしし as “wild boar” or “wild pig,” while 1451470 defines 動物 as “animal.” `docs\content-format.md:115–148` establishes title-based choices, semantic rather than string-only review, and direct, nontransitive exclusions. The comparable `words\熊.md:8` already excludes 動物; that declaration does not protect 猪.

   **Confidence:** High that the labels overlap and the direct guard is absent; actual selection in a running quiz was not observed.

No other actionable defect established. The complete source reading order **チョ; い, いのしし** is preserved, and `quizOnyomi: []` / `quizKunyomi: [いのしし]` correctly separates metadata from practice. The selected reading has its own linked example, with the required reciprocal link present. Kana recognition respects the usually-kana and `re_nokanji` distinctions. The archaic い and しし identities are explicitly separated from modern いのしし; the mushroom reading いぐち does not contradict the qualified 猪口/ちょこ sake-cup note.

The examples, translations, existence/action particles, sex/number explanation and English *boar* warning are sound. The radical clarification, explicitly nonhistorical mnemonic and name-use qualification are appropriate. The three curated kanji distractor titles remain semantically distinct. No 猪/豚 exclusion is established by their modern taught animal senses; the archaic い overlap does not make those modern nouns interchangeable. The word appropriately omits an unsupported vocabulary level.

**Optional:** None.

**Limits:** No assigned read was truncated or left unfinished. Dictionary evidence was supplied frozen XML and supplied external HTML, not independently retrieved upstream; their stated hashes and provenance were not independently verified. No other reviewers’ reports, author rationale or prohibited records were inspected. Tool calls were serial; no overlapping read ranges occurred in this review.

Comprehensibility findings concern text only, not actual phone layout or glyph rendering. The supplied 17-Han/16-cmap summary is not new native certification; cmap absence alone does not establish glyph failure. Unchanged pilot acceptance was not reassessed. Fresh batch-034 Android, combined-main, CI and public-ZIP checks remain pending; physical-phone/general-release acceptance remains outstanding, with compatible Android `f9b59a2` or later required. These limits do not constitute a blanket veto on bounded owner testing.
