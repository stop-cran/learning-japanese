# Author's statement for the reviewer of `reports-137\initial-gpt.md`

This statement answers only the points in YOUR initial report. G1 and G2 are your report's own Findings labels. Your two
Optional bullets had no labels; here the first (presentation for phone use) is OP and the second (`卸.md:25`) is OW. The
statement is the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`,
`diffs\fix.patch` and independent sources; do not rely on this text as evidence. Card line numbers refer to the revised
cards in this packet; other line numbers refer to the named file in this packet unless the original packet is named.
Twelve of the 15 cards changed (丁 仰 但 傑 僕 卸 司 吐 呂 哲 唯 善), the other three did not, and no word article, stroke file
or front matter changed (see `CHANGES.md`). Give a disposition for each of G1, G2, OP and OW.

## Findings

### G1 (minor): 仰 — the 仰山 example lacks its Kansai-dialect qualification

Author action: **changed**, as your remedy describes.

- `仰.md:59` now ends: `and 仰山 ぎょうさん, "a lot; plenty; abundant; great many," which JMdict marks as Kansai dialect in
  this sense and as usually written in kana.` (it ended `which JMdict marks as usually written in kana.`). The example
  stays, and no quiz setting changed.
- Support: `evidence\jmdict-cited-entries.xml`, entry 1238920 (sense 1, the quantity sense quoted on the card, carries
  `<dial>Kansai-ben</dial>` and `word usually written using kana alone`; sense 2, "exaggerated; grandiose", has no
  dialect tag).

To verify: that line 59 now qualifies the quantity sense as Kansai dialect and that nothing else on the card presents it
as standard vocabulary.

### G2 (minor): verbatim linked-title quotations in ten new cards

Author action: **changed**, as your remedy describes.

- All 16 quotations in your table now copy the linked card's title exactly, with the space after the comma restored: 丁
  line 68; 仰 line 58 (two); 但 lines 27 and 47; 傑 lines 27, 46 and 47; 僕 line 50; 司 lines 55 and 56; 吐 lines 48 and
  49; 呂 line 52; 哲 line 55; 善 line 58. `CHANGES.md` gives the old and new text.
- Cause: the author's working table of card titles, used when drafting the Notes, had lost the space after every comma
  inside a title. It was rebuilt from the cards' front matter.
- Scope check: a script compared every quoted title of a linked card or word article in all 15 cards (143 quotations)
  with the target's `title:` and found no other mismatch. No title metadata, exclusion or quiz setting changed.
- Support: `checks\link-targets.tsv` lists every link on a changed line, the target's `title:` and whether the quotation
  equals it.

To verify: that the 16 quotations now equal the titles and that no other quoted title in the 15 cards differs from its
target's title.

## Optional points

| ID | Author action | Where | Reason |
| --- | --- | --- | --- |
| OP | **declined** | all cards (unchanged) | The long sense inventories and the explanations of metadata versus practiced readings follow the current card layout, not this batch alone. For example, the sentence `Being outside the practice set is not proof that a reading is invalid.` is in all 15 cards of this batch and in 42 published cards, and a closing `For reference, more Daijisen examples …` bullet is in 11 cards of this batch and in 10 published cards. Moving or subordinating this material is a presentation change for the whole collection, outside this revision. |
| OW | **changed** | `卸.md:25` | The Daijisen おろし entry is now described as one that `defines as the act of a wholesaler selling goods to retail shops` (it read `defines as a wholesale dealer selling goods to retail shops`). The wording keeps the wholesaler as the actor, because the Daijisen text names one: `問屋が商品を小売店に売り渡すこと`. Support: `evidence\weblio-卸-daijisen.txt` (the page's only Digital Daijisen block, おろし【卸（し）】, verbatim, with the page URL, retrieval time and the sha256 of the cached raw HTML). The original packet's `evidence\public-source\weblio-卸.txt` lacks this block because its retrieval kept only the page header text; the evidence file explains this. |

## Other limits in your report

No disposition is needed for these.

- The Android JVM content tests and the Kotlin reading-audit cross-check were not run for this revision either (see
  `CHANGES.md`).

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; review them like any other changed hunk.

- **丁: where JMdict has よほろ** (`丁.md:40`). The card said that JMdict has no entry for よほろ. The sentence now ends
  `KANJIDIC2 does not list よほろ, and JMdict has no standalone entry for it; it appears only in つかえのよほろ, one reading
  of 仕丁 しちょう, which JMdict marks archaic and glosses "men pressed into forced labor (ritsuryō system)."` Support:
  `evidence\jmdict-cited-entries.xml`, entry 2829360 (sense 1, tagged `archaic`, applies to all four readings including
  つかえのよほろ; sense 2 is restricted to しちょう, じちょう and してい). In the pinned JMdict, 2829360 is the only entry
  with a reading containing よほろ (author's search).
- **傑: register labels of 傑作** (`傑.md:33`, `:42`). Both glosses now read `masterpiece; hilarious absurdity (jocular,
  dated)`. Support: `evidence\jmdict-cited-entries.xml`, entry 1253840 (sense 2 carries `jocular, humorous term` and
  `dated term`; sense 1 carries neither). The word article `words\傑作.md` (unchanged) already gives these labels.
- **卸: 卸下 is a military term** (`卸.md:33`). The シャ row now glosses 卸下 しゃが as `cargo unloading (military term)`.
  Support: `evidence\jmdict-cited-entries.xml`, entry 2537870 (`<field>military</field>`).
- **丁, 呂 and 唯: missing JMdict ids in the Metadata line** (`丁.md:71`, `呂.md:55`, `唯.md:54`). The author's writing
  rule is that the Metadata line lists the JMdict entry of every word the card names. The 丁 line now includes 2829360
  (仕丁, named in line 40 since this revision), the 呂 line 1448890 (当て字, line 27), and the 唯 line 2672330 (唯々 いい)
  and 1623580 (諾々 だくだく), which line 39 names as the two halves of 唯々諾々. The 呂 and 唯 gaps were already in the
  reviewed snapshot; a script found them (`evidence\meta-scan.txt`; its scope is in `CHANGES.md`). No teaching text
  changed. Support: `evidence\jmdict-cited-entries.xml`, entries 2829360, 1448890, 2672330 and 1623580.

## Process notes

- There are two fix commits. `2bc8e9b1` makes every change above except the three Metadata lines, which its child
  `48332d32` adds. `diffs\fix.patch` is the whole change from the reviewed snapshot `d3c7394d` to `48332d32`.
- The second commit had two earlier local versions, `0c7f25fe` (丁 only) and `fa9be05c` (丁 and 呂). Both were replaced
  before this packet was built; neither was reviewed or published.
- The checks in `checks\` were run on the committed revision.
