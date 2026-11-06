**Snapshot:** 0f7f20e93b1e20cbc9943011e9ac69b20f75086e, as supplied in the packet. I did not check Git or upstream sources myself. Hashes, diffs and dictionary observations are taken from the packet as given.

**Scope:**
- **Model:** Claude Opus 5.5 (`claude-opus-5.5`), working alone with no delegation.
- **Read:** one `view` call with `forceReadLargeFiles=true` and no `view_range` on `docs\n1-reviews\batch-079-initial-packet.txt`.
  - The output showed no truncation notice and ended at the final inventory section, which is the packet's last item.
  - The tool showed no packet line numbers, so I couldn't confirm the stated 5364 lines / 218080 bytes myself.
- **What I covered:**
  - The four assignments: new `kanji\冠.md`, new `words\王冠.md`, all of reused `words\冠.md` (including its line-25 link change), and only the added line 39 in `kanji\王.md`.
  - All 13 comparison articles.
  - The three JMdict files (158 + 18 + 1 families). I read them as supplied but did not recount the 177 total.
  - The five KANJIDIC2 records, the input metadata, the frozen N1 list (row 88 = 冠, confirmed by counting), the pinned SVG and the stroke JSON.
  - The coordinator's dictionary observations, the guides and the inventory.
- I treated the existing 王 teaching as background only.

**Verdicts:**

| Assignment | Correctness | Scoped coverage | Text comprehensibility |
| --- | --- | --- | --- |
| `kanji\冠.md` | CLEAN | CLEAN | CLEAN |
| `words\王冠.md` | CLEAN (one low-impact unsourced claim, Finding 1) | CLEAN | CLEAN |
| `words\冠.md` (reused, with nav change) | CLEAN | CLEAN | CLEAN |
| `kanji\王.md` line 39 only | CLEAN | CLEAN | CLEAN |

What these verdicts rest on:
- **冠 metadata** matches KANJIDIC2 and the frozen source row:
  - 9 strokes, radical 冖 no. 14, grade 8, N1 from the community list (not the official syllabus or the KANJIDIC legacy level).
  - On reading [カン] and kun reading [かんむり]; the quiz lists use both, each with its own linked row.
  - 王冠 おうかん splits as 王オウ + 冠カン (JMdict 1181450). 冠 かんむり is JMdict 1577620.
- **Reading restrictions are kept apart correctly:**
  - "Best / peerless / first" and the title counter are limited to かん (senses 5 and 7). 冠たる かんたる is a pre-noun adjective (2272420), so "used before a noun" is right.
  - The kanji-top component and name/sponsorship senses are limited to かんむり (senses 3 and 6). The かむり-only haikai sense is not taught.
- **Shape notes are right:** 冖 + 元 + 寸 (KanjiVG groups) against 宀+元 (完) and 宀+寸 (守). 冖 lacks 宀's top dot.
  - The mnemonic is labelled as invented, and the article claims no phonetic. KanjiVG's `kvg:phon="元"` is not asserted, so nothing unsupported is claimed.
- **Stroke data:** the JSON matches the SVG for all 9 strokes (types, start/end points, order 冖→二→儿→寸). This only shows the conversion matches; it says nothing about how it actually draws.
- **Wrong choices for 冠** ("crown; peerless"): 冗 "superfluous; redundant", 完 "complete" and 守 "guard; obey" don't overlap in ordinary meaning.
  - 完's KANJIDIC meaning "perfect" is not its displayed title and is not "peerless".
  - With three curated choices, the default four-choice quiz uses no fallback labels. Those fallback labels and 帽 "hat; headgear" also don't overlap, but I am not claiming the large pool is safe.
- **王冠 exclusions:** 冠, 帽子, 蓋 and 栓 each share a "crown" or "cap/closure" meaning with 王冠's title. 冠's eight original exclusions and its sourced N2 level are kept, and 王冠 has no level, as required.
- **Reciprocal links:** all six directions exist with correct relative paths: 冠↔words/冠, 冠↔王冠, 王↔王冠.

**Findings:**
1. **Minor (hypothesis; not a proven defect).**
   - **Facet:** correctness / evidence.
   - **Where:** `words\王冠.md:16,27`.
   - **Claim:** "extends the name to an object shaped like a crown" explains why the bottle cap is called 王冠. Neither the supplied Daijisen observation ("metal closure on a beer bottle") nor JMdict ("bottle cap") supports that reason. The physical description is accurate, so learning impact is low.
   - **Remedy:** cite a source for the naming reason, or reword it to describe the object without giving a reason.
   - **Confidence:** high that the packet doesn't support it; low that it is wrong.

**Optional:**
- `kanji\王.md:49`: add JMdict 1181450 to the source line, to match the 王様/王国 entries.
- `words\王冠.md:19`: 瓶の王冠を外しました reads as acceptable. 栓抜きで王冠を開ける/取る might be more typical (low confidence, not native-checked). Daijisen attests 王冠をいただく, which could be mentioned.
- The title "bottle cap" is broader than the body's crown-cap limit; "crown cap" would be more exact.
- `kanji\冠.md`: one compound where 冠 isn't a physical crown (e.g. 冠婚葬祭, marked ichi1/news1 in JMdict) would illustrate line 24.
- `kanji\冠.md:45`: the note says かん in hiragana while the table says カン; one bridging phrase would help.
- `words\冠.md:29`: an example such as 冠大会 would illustrate the sponsorship sense. JMdict lists 冠る as a spelling of かぶる, but it isn't a KANJIDIC reading, so nothing is required.

**Limits:**
- No independent Git, hash or upstream retrieval; the Daijisen material is the coordinator's evidence.
- No native-speaker, phone, font, drawing or route certification. 冖 and 宀 are missing from the main fonts, so their display depends on system fallback and is unverified.
- No check of title uniqueness across the whole deck, safety in large or random quiz pools, the validator, or the manifest.
- I didn't recount the line or family totals myself.
