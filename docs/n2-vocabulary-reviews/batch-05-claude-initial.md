## Snapshot
- **Frozen commit:** `7cc99e2535f9e4ac917278a5b4f2e49db954e4fa` (parent `5a85c2bc96780a9d2fdb2df0e64d33887bbb7902`). The receipt says the content is clean and committed, with no reused articles.
- **Git limit:** I had file tools only and could not run Git. I reviewed the files on disk and the receipt's patch, but could not confirm they match the commit or re-check any hashes.

## Scope
- **Reviewer:** claude-opus-5.5 (Claude family), working alone and in order, without delegating.
- **Read in full:** all 19 new articles; the instruction files; `docs\content-format.md:18-112`; source rows N2:82–101; and the relevant parts of `batch-05.json` (rows, entry families, kanji evidence, comparison families and inspection receipts).
- **Related edits:** the five changed passages (戸, 植, 移, インク:28, 従兄弟:34), read in context against the patch. The unchanged teaching in those files was not reviewed.
- **Other cards:** existing cards were checked only to confirm link targets, comparisons and quiz titles.
- **Not read:** all forbidden notes, reviews and ledgers. I did not search the whole repository.

## Verdicts

| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| いってまいります | CLEAN | CLEAN | CLEAN |
| いつのまにか | CLEAN | CLEAN | NEEDS FIX (R1, R2) |
| 移転 | CLEAN | CLEAN | CLEAN |
| 井戸 | CLEAN | CLEAN | CLEAN |
| 緯度 | CLEAN | CLEAN | CLEAN |
| 従姉妹 | CLEAN | CLEAN | CLEAN |
| 威張る | CLEAN | CLEAN | CLEAN |
| 嫌がる | CLEAN | CLEAN | CLEAN |
| いよいよ | CLEAN | CLEAN | CLEAN |
| 煎る | CLEAN | CLEAN | CLEAN |
| 入れ物 | CLEAN | CLEAN | CLEAN |
| インキ | CLEAN | NEEDS FIX (R4) | CLEAN |
| インタビュー | CLEAN | CLEAN | CLEAN |
| 引力 | CLEAN | CLEAN | CLEAN |
| ウーマン | CLEAN | CLEAN | NEEDS FIX (R3) |
| ウール | CLEAN | CLEAN | CLEAN |
| ウェイトレス | CLEAN | CLEAN | CLEAN |
| 植木 | CLEAN | CLEAN | CLEAN |
| 飢える | CLEAN | CLEAN | CLEAN |

**Related edits** (all CLEAN on all three facets):
- **戸, 植, 移:** each gains a link to the new word at its article reading (いど, うえき, いてん). The added entry IDs 1160330, 1587970 and 1158390 are correct.
- **インク.md:28:** the new link to インキ and its "same substance" sentence are accurate.
- **従兄弟.md:34:** the new link to 従姉妹 is accurate.

**Alias mappings** (all CLEAN):
- **N2:91 煎る:** this is the article's headword.
- **N2:92 炒る:**
  - `煎る.md:28-31` teaches it explicitly as another spelling of the same verb.
  - JMdict entry 1391500 supports this; it lists 炒る first.
  - I fetched Digital Daijisen's 煎る page myself. It lists 煎る／炒る／熬る and says the spellings are hard to tell apart clearly.
- **N2:99 ウエートレス → ウェイトレス:** `ウェイトレス.md:25-28` names it explicitly as a spelling of the same word. JMdict 1025690 marks it as a search-only form.

**Metadata and links:** every article's kanji list contains every kanji in its headword. All required links to existing kanji cards are present.

## Findings

**R1 — いつのまにか / こっそり quiz overlap**
- **Severity:** Minor. **Facet:** comprehensibility (quiz).
- **Where:** `words\いつのまにか.md:1-9`. The title on line 4 is "before one knows; unnoticed", and there is no `quiz_exclusions`.
- **Problem:** `words\こっそり.md:4` is titled "secretly; without being noticed". "Unnoticed" is a valid English rendering of こっそり, as in "slipped out unnoticed". Both cards are kana-only wago and share the wago tag, and neither excludes the other. In either quiz direction, a learner could pick the "wrong" answer correctly.
- **Fix:** add `quiz_exclusions: [こっそり]` to いつのまにか.md. Exclusions apply both ways, so one side is enough.
- **Evidence:** JMdict 1188850 glosses いつのまにか as "unnoticed; unawares".
- **Confidence:** medium-high. Whether the pair actually appears together depends on the app's candidate scoring, which I did not run.

**R2 — いつのまにか dangling "departure" sentence**
- **Severity:** Minor. **Facet:** comprehensibility.
- **Where:** `words\いつのまにか.md:42-43`, "Not noticing a departure does not imply that the departing person deliberately acted secretly."
- **Problem:** the article has no departure example, and the sentence hints at the secrecy contrast without naming or linking こっそり. Learners won't know what it refers to.
- **Fix:** name the contrast directly, for example: "Compare [こっそり](こっそり.md): someone deliberately avoids being noticed. いつのまにか only says the observer did not notice." Optionally add an example such as いつのまにか彼はいなくなっていました.
- **Confidence:** high.

**R3 — ウーマン romanised as "Uman"**
- **Severity:** Low. **Facet:** comprehensibility.
- **Where:** `words\ウーマン.md:20`, which translates 「ウーマン」 as "Uman".
- **Problem:** this drops the long vowel that line 29 teaches ("The first ー lengthens ウ"), which could mislead learners about pronunciation.
- **Fix:** write "Ūman", or keep ウーマン in the English line.
- **Confidence:** high.

**R4 — インキ gives no usage guidance against インク**
- **Severity:** Minor. **Facet:** scoped coverage.
- **Where:** `words\インキ.md:32-34` and `39-41`.
- **Problem:** the article says インク has "the same material meaning" and warns against assuming a strict printer-versus-pen split. It never says which form is the everyday default. That is the main practical reason for a separate インキ card, and without it learners may treat the two as freely interchangeable, for example saying プリンターのインキ.
- **Fix:** add one sentence saying this is a tendency, not a rule. インク is the usual everyday word. インキ is older and remains standard in printing and technical terms such as 印刷インキ.
- **Evidence:**
  - The Japanese Wikipedia article on インク (read via a Weblio mirror) says インキ was common in the Meiji era, インク later became general, and インキ is still the formal technical term in printing.
  - JMdict gives both words the same frequency markers, so the pinned source cannot settle this.
- **Confidence:** medium. The tendency comes from an encyclopedia, not a dictionary.

## Optional
- **いよいよ:** the "beyond doubt" use (いよいよもって) is not taught. That is acceptable for the article's scope; Wiktionary confirms both senses the article does teach.
- **植木.md:20:** gloss 鉢 (はち, "pot"). Consider mentioning 植木鉢 ("flowerpot") or adding an example where 植木 alone means a potted plant.
- **戸 kanji notes:** the voicing note explains と→ど only for 雨戸; 井戸 could be added. `井戸.md:27` already explains it.
- **威張る.md:30:** consider giving えばる a register label. It may be colloquial or regional; I did not verify this.
- **ウェイトレス:** consider reassuring learners that ウエートレス is common in print, so "search variant" isn't read as "wrong". I did not verify this.
- **インク.md:28:** could add the reciprocal usage note once R4 is fixed.
- **従姉妹:** could mention the single-cousin spellings 従姉 and 従妹.

## Limits
- **Git:** I could not run Git, so I could not confirm the files match the commit or verify any hashes.
- **External checks:** the author's Daijisen receipts are not independent evidence. I re-fetched Digital Daijisen's 煎る and 炒める pages myself, and both are consistent with the articles.
- **Failed lookups:** goo could not be reached, kotobank search needs JavaScript, and one guessed kotobank address returned an unrelated entry. None of these counted as evidence.
- **R4:** the tendency rests on an encyclopedia, not a dictionary.
- **Quiz overlap:** how often R1's pair actually appears depends on app scoring I did not run.
- **従兄弟:** many people use 従兄弟 for cousins of either sex in practice, but JMdict supports "male cousin". This is unchanged teaching and outside scope.
- **Naturalness:** judgements are a reviewer's view, not corpus- or native-speaker-certified.
- **Dictionary coverage:** the evidence file holds selected entries only, so a missing entry does not prove a word or sense doesn't exist.
