**Snapshot:** Signed parent 0d6fe29033157a4417def2b503ad3d02e7cb43da plus the one-field `quiz_exclusions` change to `words\冒す.md` (SHA256 6a74af58…). The packet says the manifest was regenerated, but it does not include the manifest, and I did not check it.

**Scope:** Model: Claude Opus 5.5 (claude-opus-5.5). I read `docs\n1-reviews\batch-077-confirmation-packet.txt` once, with forceReadLargeFiles=true and no range. It came back complete through the editorial-disposition paragraph with no truncation marker; I can't confirm the 21011-byte size myself. What I checked:
- the exact diff and the revised 冒す article;
- 攻める.md, whose hash matches the earlier copy;
- JMdict entries 1519820 (冒す) and 1279130 (攻める);
- the frozen N1 list, the source-index row and the batch membership file;
- the mechanical inventory.

Everything is supplied evidence. I did no Git or upstream retrieval of my own.

**Verdicts:**
| Article | Correctness | Scoped coverage | Text comprehensibility |
| --- | --- | --- | --- |
| 冒 (new) | CLEAN | CLEAN | CLEAN |
| 冒す (new, revised) | CLEAN | CLEAN | CLEAN |
| 冒険 line 24 link | CLEAN | CLEAN | CLEAN |
| 険 line 22 link | CLEAN | CLEAN | CLEAN |

- **The change:** It adds one list item: 攻める is an existing word, not 冒す itself, and not a duplicate. The other five exclusions are unchanged, and so are the title, prose, examples and links. 攻める.md itself is unchanged, which is fine because one declaration covers both directions. No regression found.
- **Membership:** In the frozen list, 冒 is entry 86 when counting from 1, which matches the source-index row. That row's metadata (9 strokes, radical 冂 no. 13, ボウ and おか.す) matches the card. Membership comes from this list, not the legacy KANJIDIC2 jlpt field.

**Findings:** None open.
- **Original finding 1 (冒す/攻める exclusion): resolved.** The exclusion is a reasonable quiz guard because the titles overlap ("act boldly" vs "brave danger; take a risk"). It does not mean the two words are interchangeable: the JMdict senses and constructions stay distinct. I agree with the packet that this creates no wider set of exclusions.
- **My sub-count: corrected.** The lexical file has 29 entries and the comparison file 11, for 40 in total. I wrote 30/10 earlier, which was a counting error. No family was missing.

**Optional (both still optional, deliberately not added):**
- the Nelson-under-日 note;
- 冒涜 and 感冒 as extra compounds.

**Limits:**
- **Title uniqueness: partially resolved.** The mechanical inventory finds the 冒 title on only one of 1,089 records, but I did not check that myself.
- **No independent checks:** I did no manifest, hash, Git or upstream checking. I can't confirm the list has 1,232 members; I only confirmed 冒's position in it.
- **Rendering and native checks: unresolved and pending.** There is no font, rendering, drawing, route, native-speaker or phone evidence, and how 冂 renders with the bundled fonts is still unknown.
- **Quiz safety:** This is still not an exhaustive or live-quiz guarantee.
