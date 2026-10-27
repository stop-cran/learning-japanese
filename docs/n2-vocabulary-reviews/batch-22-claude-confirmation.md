## Snapshot
- **Corrected commit:** `fe0722835c3bb39ad8caf90433c2936658141bdb`, directly after the authored commit `c84fdd3ce4b8467016517e5a21219a0dc54ea5da`.
- **Provenance limit:** I have file tools only, no Git, so I couldn't confirm the commit, the parent link, that the content is clean, or any hashes. The commit identity, the patch's hash and the confirmation packet's byte hash and equivalence are all the author's claims.
- **manifest.json:** its entries for the four articles are the same hash strings as the receipt, but I can't compute hashes myself. manifest.json is not in the patch, so I couldn't confirm how it is tracked.

## Scope
- **Model:** claude-opus-5.5 (Claude family). No delegation and no edits.
- **Read:**
  - my original report, the correction receipt and the full patch
  - the four changed articles (工夫, くっつく, 組み立てる, 悔しい), complete
  - the comparison cards 知恵, べたべた, セット, 恥ずかしい, plus the titles and exclusions of がっかり and しょんぼり
- **Packet:** in the confirmation packet I read these complete dictionary families:
  - principals 1003860, 1397580 and 1592350
  - existing comparison 1074600
  - appended 1011440, 1420530 and 1421630
  - I also read the correctionEvidence record.
  - The packet contains no quizGuardRationale, and its original line layout is unchanged.
- **Label collisions:** I searched titles in `words\` near the new 悔しい label ("disappointed", "frustrated", "regret", "upset", "dejected", "sad", "resent").
- **Not redone:** I didn't re-audit the other 16 articles or the three kanji edits.

## Verdicts
| Item | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 工夫 | CLEAN | CLEAN | CLEAN |
| くっつく | CLEAN | CLEAN | CLEAN |
| 組み立てる | CLEAN | CLEAN | CLEAN |
| 悔しい | CLEAN | CLEAN | CLEAN |
| Packet additions (3 families + correctionEvidence) | CLEAN | CLEAN | CLEAN |

## Findings
**B22-01 (工夫 / 知恵) — resolved.**
- `words\工夫.md:9` now excludes 知恵. Exclusions work in both directions, so 知恵 doesn't need a matching entry.
- 1420530 sense 1 (wisdom, wit, sense) together with 知恵's title "practical ingenuity" supports guarding on the English answer alone.
- The source-gloss correction for 工夫 is unchanged.

**B22-02 (悔しい "mortified") — resolved.**
- The title and heading on `words\悔しい.md:4,12` now read "bitterly frustrated; disappointed".
- This is supported directly by 1592350 sense 1, which includes "(bitterly) disappointed", and matches the first example's translation.
- The "disappointed" overlap is with がっかり, 失望, 残念 and 惜しい, all of which are already excluded on line 9.
- I withdraw my alternative remedy of a 恥ずかしい guard. "Mortified" is no longer shown, and "embarrassed; embarrassing" no longer overlaps.

**Optional hypotheses from my original report:**
- **くっつく / べたべた guard:** adopted (`くっつく.md:9`). It is supported by 1011440 senses 1 and 4 ("sticky", "clinging") against 1003860 senses 1–2 ("stick to", "cling to", "keep close to").
- **くっつく pronunciation sentence:** resolved. `くっつく.md:25` now plainly says the spelling くっ付く is still read くっつく.
- **汲む tradition sense:** still optional; not adopting it is a defensible choice.
- **口惜しい as a separate くちおしい word:** still optional. I never verified it independently, so it is not a correctness claim. The article's "rare kanji spelling" matches JMdict's "rarely used kanji form".
- **句読点 / 区切る and 汲む / 描く:** no action, consistent with my original view.

**New guard:**
- **組み立てる / セット (author's addition):** CLEAN. 1397580 sense 1 includes "to set up" and 1074600 sense 2 is "setting up", so the broad English answer overlaps. The article doesn't equate assembly with every kind of setting.

**Regressions:** none actionable.

## Optional
- **しょんぼり ("downcast and dejected") vs 悔しい:** the new "disappointed" label sits nearer to it, and the collection guards がっかり against しょんぼり. Still, 悔しい's leading "bitterly frustrated" doesn't fit しょんぼり, and sharing a word inside a compound label isn't enough on its own. A guard is possible but not required.

## Limits
- **Git and hashes:** none run, so all hash and commit claims are the author's.
- **App:** I didn't run a quiz draw, so the exclusion behaviour is inferred from `docs\content-format.md` only.
- **Wiktionary:** this is consistent with my own earlier raw fetch, and it is not a survey of English usage over time.
- **Label check:** targeted searches, not an exhaustive comparison across the whole collection.
- **Certification:** none by a native speaker.
