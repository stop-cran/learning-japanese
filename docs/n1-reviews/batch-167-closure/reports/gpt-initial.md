**Snapshot:** `a22f26b78ce52a4991391092490dd1a118ea80b6`, based on `de6dd519bc6efc9e8d0b392daf7291727ce4a915`. No uncommitted material was identified in the packet.

**Scope and outcome:** One independent, blind, read-only reviewer (GPT-6.2 Sol). Read all eight numbered card files in full, `changed.txt`, the full `安い` comparison, and the rubric, source, quiz, and label files. Reviewed consistency, meaning and reading quiz safety, navigation, evidence, counts, and scoped coverage. **Four direct meaning-quiz safeguards are missing from the supplied projection, and two teaching statements need clarification.**

**Per-card verdicts** — correctness includes static quiz safety; verdicts for existing cards apply only to the supplied changes and comparison.

| Cards | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| Kanji: 己・帆・帝・帥・幻・庶・庸・廃・廉 | CLEAN | CLEAN | CLEAN |
| Kanji: 幽 | NEEDS FIX | CLEAN | CLEAN |
| Words: 帆・帝国・元帥・庶民・廉価 | CLEAN | CLEAN | CLEAN |
| Words: 自己・幻・幽閉・廃止 | NEEDS FIX | CLEAN | CLEAN |
| Word: 凡庸 | CLEAN | NEEDS FIX | CLEAN |
| Existing kanji changes: 価・元・凡・国・止・民・自・閉; existing word: 安い | CLEAN | CLEAN | CLEAN |

**Findings**

| Severity / facet | Location | Evidence, impact, and exact remedy |
|---|---|---|
| Moderate · meaning quiz | `kanji/幽.md:3,14` | **Add `淡` to `幽`’s direct exclusions.** Both displayed labels offer “faint.” JMdict `1590290` also confirms 幽か in this sense. Excluding 微 does not exclude 淡. High confidence. |
| Moderate · meaning quiz | `words/幽閉.md:4–8` | **Add `缶詰` to `幽閉`’s direct exclusions.** The supplied label for 缶詰 includes “being confined,” a plausible answer for the broad “confinement” gloss. The difference in register or force is not in the labels. High confidence in the displayed overlap, not in runtime co-occurrence. |
| Minor · meaning quiz | `words/幻.md:4,8` | **Add `空想` to `幻`’s direct exclusions.** The label “daydream; fantasy; imagined vision” overlaps the vision and short-lived-dream senses of 幻 (`1262880`, senses 1–2). Their separate exclusions with 夢 do not protect this pair. Medium confidence: the overlap is sense-specific. |
| Minor · meaning quiz | `words/廃止.md:4,8` | **Add `取り消す` to `廃止`’s direct exclusions.** JMdict `1472100` includes repeal and annulment, which overlap the displayed “revoke” sense of 取り消す. The existing 中止 and 止める exclusions do not protect this pair. Medium confidence: the overlap concerns formal rescission, not every cancellation. |
| Minor · correctness | `words/自己.md:15` | The definition makes the actor also being the object sound like a requirement. JMdict `1317580` defines a noun meaning “the self,” not a constraint on who performs an action. **Define it as “the self” first, then say that the actor and object coincide in these examples.** High confidence. |
| Minor · scoped coverage | `words/凡庸.md:15` | “Before a noun, use 凡庸な” reads as a general attachment rule, but `1523660` records both な-adjectival and の-taking use. **Say “Use 凡庸な to describe a noun, as in 凡庸な案,”** without implying that な is the only possible attachment. High confidence. |

**Coverage and evidence:** Reconciled **10 support mappings, 10 distinct new word articles, 10 primary JMdict entries covering 13 selected senses, and 104 supplied family records**. All **23 frozen kanji reading rows** are taught or qualified; the **10 offered keys** match the cards and projection (8 on, 2 kun). Checked all **18 required reciprocal pairs** in both directions with the word readings: 己・自↔自己, 帆↔帆, 帝・国↔帝国, 帥・元↔元帥, 幻↔幻, 幽・閉↔幽閉, 庶・民↔庶民, 庸・凡↔凡庸, 廃・止↔廃止, 廉・価↔廉価. The additional **廉↔安い** recognition pair is present in both directions and is not counted among the 18. JMdict `1153670` supports 廉い for price, not for the calm sense; `1435810` supports 帝（みかど）but restricts the imperial-residence sense to 御門. Neither distinction calls for adding a frozen quiz key.

**Optional:** Clarify on 帥 and 元帥 that 元帥 is the spelling to learn and that JMdict `1260890` records 元師 as irregular. Mark 廉（かど）as usually written in kana. Check whether 安価 has its own deck card; if it does, add a direct 廉価–安価 exclusion, since `1153740` confirms the low-price overlap. The packet does not establish that card’s presence.

**Limits:** `sources.json` records the author’s Digital Daijisen checks for **ほ【帆】**, **まぼろし【幻】**, the **state sense only of 帝国**, and the other seven word headwords. The historical 帝国 sense was checked against local JMdict evidence. The examples are original, not dictionary attestations. No external-page, native-speaker, device, whole-deck, or manifest verification was performed. The reported removal of the 帝／タイ collision, three remaining latent collisions, citation metrics, and contributor tests are author-side results; the packet does not include the generated options or per-collision traces needed to reproduce them.
