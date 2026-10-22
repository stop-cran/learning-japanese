## Snapshot
I reviewed frozen commit `0648ec4f05747bfcfbc7d56fb82cf6ad20076ea7` (parent `2500e68f52564eafccb432331df5b1681b5bf11b`, `cleanCommittedContent: true`) and the committed content only.

I had file-reading and web-fetch tools but could not run Git. So I read the working-tree files, which match the frozen patch, but I could not check them against the commit or recompute the receipt's file hashes.

## Scope
- **Model:** claude-opus-5.5 (Claude family), working sequentially with no delegation or edits.
- **New articles:** I read all 18 in full and checked them against TSV rows N2:122–141 and the pinned JMdict/KANJIDIC2 evidence in `batch-07.json` (row records, main entry families, the relevant comparison families, components and inspections).
- **Related edits:** I checked the nine changed passages in context: 占.md:20,32,37; 河.md:38,46; 裏.md:38,47; あの.md:26; さあ.md:28; まあ.md:30; ペンキ.md:36; うろうろ.md:5; 液体.md:5.
- **Reuse and aliases:** I assessed the うろうろ and 液体 reuse claims and the aliases 売上, 売行き and ええと.
- **Kotobank:** I fetched the four pages the author cited (うんと, 売上, 売れ行き, 運河) myself. All four support the article claims.
- **Quiz check:** I searched word titles in `words\` with targeted patterns.
- **Not covered:**
  - The forbidden review and notes documents, which I did not read.
  - Unchanged teaching in the nine related files, which I did not review comprehensively.
  - New kanji or stroke files: the batch has none. 恨 and 羨 have no kanji cards, so it is correct that they are not linked.

## Verdicts

| Article (row) | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 裏口 (122) | NEEDS FIX (F-03) | CLEAN | CLEAN |
| 占う (123) | CLEAN | CLEAN | CLEAN |
| 恨み (124) | CLEAN | CLEAN | CLEAN |
| 恨む (125) | CLEAN | CLEAN | CLEAN |
| 羨ましい (126) | CLEAN | CLEAN | CLEAN |
| 羨む (127) | CLEAN | CLEAN | CLEAN |
| 売り上げ (128, source 売上) | CLEAN | CLEAN | CLEAN |
| 売り切れ (129) | NEEDS FIX (F-02) | CLEAN | CLEAN |
| 売り切れる (130) | NEEDS FIX (F-02) | CLEAN | CLEAN |
| 売れ行き (131, source 売行き) | CLEAN | CLEAN | CLEAN |
| 運河 (133) | CLEAN | CLEAN | CLEAN |
| うんと (134) | CLEAN | CLEAN | CLEAN |
| 英文 (135) | CLEAN | CLEAN | CLEAN |
| 英和 (136) | NEEDS FIX (F-01) | CLEAN | CLEAN |
| えっと (137, source ええと) | CLEAN | CLEAN | CLEAN |
| エチケット (139) | CLEAN | CLEAN | CLEAN |
| 絵の具 (140) | CLEAN | CLEAN | CLEAN |
| エプロン (141) | CLEAN | CLEAN | CLEAN |

**Related edits:** all nine are CLEAN on all three facets.
- 占, 河 and 裏 gain correct links at the right readings (占う/うらなう, 運河/うんが, 裏口/うらぐち), and their JMdict entry IDs are updated.
- あの, さあ and まあ now link "ええと" to えっと.md, which explicitly teaches ええと.
- ペンキ now links 絵の具.
- うろうろ and 液体 gain only `jlpt: 2`. Neither had an easier level before, and their titles and IDs are unchanged.

**Reuse claims:** both are CLEAN.
- うろうろ (N2:132), senses 1–2: the existing article teaches restless, aimless wandering, with うろうろする and うろうろと歩く (うろうろ.md:16–21).
- 液体 (N2:138): the existing article teaches "liquid" (液体.md:16–19). 液.md:30,34 already links to it. The source's extra gloss "fluid" is reasonably not turned into a separate sense.

**Aliases:** all three are CLEAN.
- **売上 → 売り上げ:** the article teaches it as the same noun (売り上げ.md:17–18). JMdict lists 売上 as a recognized spelling (spec1), and Daijisen's headword is 【売（り）上（げ）】.
- **売行き → 売れ行き:** the article teaches it (売れ行き.md:23–24), and its search-only label is accurate.
- **ええと → えっと:** the article teaches it as the same thinking pause (えっと.md:23–25), and its search-only label is accurate. It is kept separate from ええ "yes" (JMdict entry 1001140, senses 1–2).

## Findings

**F-01 (Minor, correctness / quiz metadata): 英和 vs 字引**
- **Where:** `words\英和.md:9`
- **Problem:** 英和 excludes 辞書 ("dictionary") and 辞典 ("dictionary; lexicon"), but not 字引, which has the same title, "dictionary".
- **Why it matters:**
  - The app only deduplicates 字引 against 辞書, and exclusions don't carry over from one pair to another.
  - So when the prompt is "dictionary", the choices can include both 字引 and 英和, and both are defensible answers.
  - Both cards are type kango and share the noun and language tags, so the quiz is fairly likely to pick them together.
- **Fix:** add 字引 to 英和's `quiz_exclusions`.
- **Evidence:** 字引.md:4 and 辞書.md:5 (both titled "dictionary"); 字引 has no exclusions; content-format.md says exclusions are pairwise only.
- **Confidence:** high.

**F-02 (Minor, correctness / quiz metadata): 売り切れる and 売り切れ vs 無くなる**
- **Where:** `words\売り切れる.md:9`, `words\売り切れ.md:9`
- **Problem:** both articles exclude 切れる because of its "run out" gloss. They don't exclude 無くなる, titled "go missing; run out", which carries the same "run out" gloss.
- **Why it matters:**
  - 切れる.md:9 excludes 無くなる, but that doesn't carry over to these articles.
  - "The tickets ran out" is a natural reading of 売り切れる.
  - 売り切れる and 無くなる are both type wago and share the wago and verb tags, so they are likely to appear together.
- **Fix:** add 無くなる to 売り切れる's exclusions. 売り切れ ("no stock left") should probably get it too.
- **Confidence:** medium.

**F-03 (Minor, correctness / quiz metadata): 裏口 vs 玄関**
- **Where:** `words\裏口.md:9` and `:33–34`
- **Problem:** 裏口 excludes 入口 ("entrance"), which accepts that a rear entrance answers a generic "entrance" prompt. Its own comparison card 玄関 is titled "entrance; entryway" but is excluded from neither side.
- **Fix:** add 玄関 to 裏口's exclusions.
- **Confidence:** medium-low. "Entryway" may steer learners to 玄関, and the two cards share only the noun tag. I'm reporting it because it is inconsistent with the 入口 exclusion.

## Optional
- **うんと:** a brief note that it is mainly conversational. Daijisen gives no register label, so this is unverified.
- **羨ましい:** a note on 羨ましがる for other people's envy.
- **裏口:** a mention of figurative sense 2 (裏口入学).
- **英文:** a mention of sense 2 (English literature / 英文科).
- **占う.md:20:** "I told the future with cards" → "I read my future with cards."
- **売り上げ.md:27–28:** the sentence ruling out "a rule that anything written with 上 must mean financial profit" doesn't follow from anything before it; reword or remove it.
- **えっと:** say that ええと is a common standard spelling despite JMdict's search-only flag.
- **売れ行き vs 売れる:** consider excluding the pair. Both use 売, and "sell well" overlaps with 売れ行きがいい.
- **Polish:** an エチケット collocation such as 咳エチケット. Also reconsider the odd negative asides "not an i-adjective" (英和) and "not a verb to conjugate" (えっと).

## Limits
- Without Git, I could not verify the commit, the patch or the file hashes; I relied on the receipt for these.
- The JMdict and KANJIDIC2 evidence comes from the pinned batch file, not a fresh retrieval from EDRDG.
- My Kotobank lookup for ええと failed, so I make no claim about its headword status.
- I had no corpus frequency data, so the register of うんと and 羨む is unverified.
- The quiz-overlap check relied on targeted title searches, not every card and not running the app's choice selection.
- This is not a native-speaker certification. I did not comprehensively review unchanged teaching in the related files.
