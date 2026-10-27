## Snapshot
The frozen commit is `c84fdd3ce4b8467016517e5a21219a0dc54ea5da` (parent `2101fdd861825c254d34132e8586b030d2ac460a`). I only have file tools, not Git, so I couldn't confirm the commit, the hashes or that the working tree matches the commit. I read the files on disk and relied on the receipt's statement that the committed content is clean.

## Scope
- **Model:** claude-opus-5.5 (Claude family).
- **New articles:** all 20 assigned articles, read completely. No articles were reused.
- **Kanji edits:** the patch plus the changed passages in context in `kanji\紅.md` (lines 32, 39, 49), `kanji\区.md` (lines 30, 42, 50) and `kanji\読.md` (line 31). I didn't review the unchanged teaching on these cards.
- **Mappings:** TSV rows N2:422–441 and their evidence rows, the 20 principal JMdict families, the relevant KANJIDIC2 records, the author's inspection receipts, the quiz declarations and the 146 existing comparison labels.
- **Comparison families:** I read only the relevant parts of the 269 families, not all of them.
- **Title collisions:** I searched the titles in `words\` for the key English labels.
- **Not read:** none of the forbidden files.

## Verdicts
| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 砕く | CLEAN | CLEAN | CLEAN |
| 砕ける | CLEAN | CLEAN | CLEAN |
| くたびれる | CLEAN | CLEAN | CLEAN |
| くだらない | CLEAN | CLEAN | CLEAN |
| 下る | CLEAN | CLEAN | CLEAN |
| 唇 | CLEAN | CLEAN | CLEAN |
| 口紅 | CLEAN | CLEAN | CLEAN |
| くっつく | CLEAN | CLEAN | CLEAN |
| くっつける | CLEAN | CLEAN | CLEAN |
| くどい | CLEAN | CLEAN | CLEAN |
| 句読点 | CLEAN | CLEAN | CLEAN |
| 配る | CLEAN | CLEAN | CLEAN |
| 工夫 | NEEDS FIX (B22-01) | CLEAN | CLEAN |
| 区分 | CLEAN | CLEAN | CLEAN |
| 組み合わせ | CLEAN | CLEAN | CLEAN |
| 組み立てる | CLEAN | CLEAN | CLEAN |
| 汲む | CLEAN | CLEAN | CLEAN |
| 酌む | CLEAN | CLEAN | CLEAN |
| 悔しい | NEEDS FIX (B22-02) | CLEAN | CLEAN |
| 悔やむ | CLEAN | CLEAN | CLEAN |

**Kanji edits:** 紅 (口紅 at べに, plus its source attribution), 区 (区分 at ク, plus its source attribution) and 読 (only a link added around 句読点 at トウ) are CLEAN on all three counts.
- The readings match KANJIDIC2.
- Only 紅 and 区 are N2 kanji, and both now have the reciprocal example.
- There are no cards for 砕, 汲, 酌, 悔, 唇 or 句, and none were invented.

**Mappings:** all 20 are CLEAN on all three counts.
- Each spelling, reading and entry ID matches, and the selected senses are actually taught.
- The 工夫 source gloss "labourer, worker" belongs to a different word, 工夫 (こうふ, entry 1278230). The article explicitly separates it from くふう.
- The 組合せ source spelling correctly maps to the 組み合わせ article, which also mentions the other spellings.

## Findings
**B22-01 — Medium — Correctness (quiz)**
- **Where:** `words\工夫.md:4,9` and `words\知恵.md:4`.
- **Problem:** 工夫 is titled "ingenuity; devising a method" and 知恵 is titled "wisdom; practical ingenuity". Neither lists the other in `quiz_exclusions`. A learner could reasonably accept either title for either word, so a correct answer could be marked wrong.
- **Remedy:** add 知恵 to 工夫's `quiz_exclusions`, or reword one of the titles.
- **Evidence:** the rule at `docs\content-format.md:95` ("a learner could reasonably accept either title"). 知恵's own article describes it as "the ingenuity used to find a way forward". 知恵 is also missing from the evidence packet's comparison labels, so the author never considered this pair.
- **Confidence:** high.

**B22-02 — Low — Correctness (title and quiz)**
- **Where:** `words\悔しい.md:4,9,12`.
- **Problem:** In current English, "mortified" means "acutely embarrassed", but the article describes frustration, not embarrassment. 恥ずかしい ("embarrassed; embarrassing") isn't excluded, so learners may link 悔しい with embarrassment and the quiz can be ambiguous.
- **Remedy:** replace "mortified" with "vexed" or "galling". Alternatively, add 恥ずかしい to the exclusions along with a short contrast.
- **Evidence:** Wiktionary defines the adjective "mortified" as "acutely embarrassed". The source dictionary (JMdict) does gloss sense 1 as "mortifying", but in the older sense of vexing.
- **Confidence:** medium.

## Optional
- **汲む:** could teach sense 4, 流れを汲む ("inherit a tradition").
- **`くっつく.md:25`:** the sentence about pronunciation is unclear. Simpler wording: "くっ付く is still read くっつく."
- **`悔しい.md:25`:** could note that 口惜しい is also a separate, literary word read くちおしい.
- **くっつく / べたべた ("clingy"):** a borderline overlap; consider adding an exclusion.
- **句読点 / 区切る and 汲む / 描く ("draw; depict"):** no exclusion is needed. The parts of speech differ, or the titles are already specific enough.

## Limits
- I couldn't run Git or compute hashes. The evidence packet's equivalence and the frozen file hashes are as the author stated them.
- I didn't read all 269 comparison families completely. The title-collision check was targeted searching, not exhaustive.
- Example naturalness is my own judgement; I didn't check it against a corpus.
- I didn't fetch Weblio or Daijisen myself, so the author's inspection receipts are unverified. Merriam-Webster (403) and Cambridge (520) failed to load; only Wiktionary worked.
