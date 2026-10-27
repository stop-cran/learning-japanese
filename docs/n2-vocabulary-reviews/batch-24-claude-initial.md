## Snapshot
**15d8c88a4e49aef85600feb3a6cb1886f7425b14**, parent 3fedae16ef2885a2873b3e63275f0a5813c3c091. I reviewed committed content only.

I had file tools but could not run Git. The commit hash comes from the frozen receipt; `.git\HEAD` points to `refs/heads/jlpt-n2-vocabulary`, but I could not resolve the commit independently. I also could not recompute the evidence or source hashes.

## Scope
- **Model:** claude-opus-5.5 (Claude family). I worked sequentially, without delegating or editing any files.
- **New articles:** all 20 read completely. No reused principal articles.
- **Related edits:** 圧.md, 血.md and 液.md, checked against the patch and the current files.
- **Mappings:** TSV rows N2:462–481, checked against the evidence packet. That covered the rows, all 20 principal families, the comparison families cited in footers (1178940, 1460850, 1155400, 1298100), the existing comparison labels, the quiz declarations and the inspection receipts.
- **Other files read:** existing words\/kanji\ files for links, titles and exclusions, plus docs\confusable-words.md (no batch entries).
- **Web checks:** Weblio/Daijisen entries for 気配, 下水, 傑作 and 険しい.
- **Not read:** all forbidden files, as instructed.
- **Disclosure:** earlier, I accidentally viewed unassigned TSV rows 450–499. I did not assess them.

## Verdicts
| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 激増 | CLEAN | CLEAN | CLEAN |
| 下車 | CLEAN | CLEAN | CLEAN |
| 下旬 | CLEAN | CLEAN | CLEAN |
| 下水 | CLEAN | CLEAN | CLEAN |
| 削る | CLEAN | CLEAN | CLEAN |
| 桁 | CLEAN | CLEAN | CLEAN |
| 下駄 | CLEAN | CLEAN | CLEAN |
| 血圧 | CLEAN | CLEAN | CLEAN |
| 血液 | CLEAN | CLEAN | CLEAN |
| 月給 | CLEAN | CLEAN | CLEAN |
| 傑作 | CLEAN | CLEAN | CLEAN |
| 月末 | CLEAN | CLEAN | CLEAN |
| 気配 | UNVERIFIED (B24-C-02) | CLEAN | CLEAN |
| 下品 | CLEAN | CLEAN | CLEAN |
| 煙い | CLEAN | CLEAN | CLEAN |
| 蹴る | CLEAN | CLEAN | CLEAN |
| 険しい | CLEAN | CLEAN | CLEAN |
| 見学 | NEEDS FIX (B24-Q-01) | CLEAN | CLEAN |
| 謙虚 | CLEAN | CLEAN | CLEAN |
| 原稿 | CLEAN | CLEAN | CLEAN |

**Kanji edits: all CLEAN on correctness, coverage and comprehensibility.**
- **圧:** adds the [血圧] common-word line and footer entry 1255110.
- **血:** links 血液 in the ケツ reading row and in Common words, adds 血圧, and adds footer entry 1255110.
- **液:** links 血液 in Common words; footer entry 1255120 was already there.
- Both new words with N2 kanji (血圧, 血液) now have reciprocal links at their actual readings. The other written kanji have no cards, and every component is listed in the article metadata.

**Mappings N2:462–481: all 20 CLEAN on all three facets.**
- Each one matches the TSV exactly in spelling, reading and entry, and every selected or additional sense is taught explicitly.
- Contradictory raw glosses are handled correctly:
  - 削る: "take a percentage" is assigned to はつる (1298100, sense 2), not to けずる.
  - 気配: "worry" is called unestablished, and the article points to 心配.
  - 傑作: "boner/blunder" is limited to the jocular/dated sense 2.
  - 険しい: "inaccessible place, sharp eyes" is interpreted as describing terrain and expressions.
  - 下品: "meanness" is qualified rather than taught as stinginess.
  - 気配's mapping identity is correct; only the article's market example is unverified (B24-C-02).

## Findings
**B24-Q-01. Severity: Minor. Facet: correctness (quiz labels). Confidence: medium.**
- **Location:** words\見学.md:4, 9; also words\訪問.md:4 and words\訪ねる.md:5.
- **Claim:** 見学's title is "study visit; observation". Both 訪問 and 訪ねる are titled "visit; call on", and none of the three cards excludes the others.
- **Learning impact:** "visit" is an ordinary translation of 見学 (工場見学 = factory visit), and 訪問 covers visiting companies and places (会社を訪問). A learner could reasonably accept either title for either word, in both quiz directions.
- **Consistency:** the existing list already excludes words with weaker overlap: 旅行, 旅, 見る and 拝見.
- **Remedy:** add 訪問 and 訪ねる to 見学's quiz_exclusions. Exclusions are not transitive, so both are needed.

**B24-C-02. Severity: Minor. Facet: correctness (UNVERIFIED example). Confidence: low–medium.**
- **Location:** words\気配.md:22–24 and 44.
- **Claim:** the example 市場は強い気配を示しています (read けはい) is an invented collocation that I could not find attested.
- **Evidence:**
  - Daijisen sense 2 (取引で、市場の景気や相場の状態) gives no example sentence and ends with きはい.
  - The attested market forms I found are 買い気配, 売り気配 and 気配値.
  - Line 44 calls きはい rare without noting Daijisen's link between きはい and the market sense.
- **Remedy:** use an attested form, such as a 買い気配/売り気配 sentence, or describe the sense without an example. Mention the market-sense きはい reading.

## Optional
- 見学 (line 18) claims intransitive use without an example. JMdict lists the word as both transitive and intransitive.
- 桁: add an order-of-magnitude example such as 桁が違う.
- 険しい: add an example such as 険しい目つき.
- 下駄:17: the "not floorboards" disclaimer is odd.
- Plain-text mentions of new words on lower-level kanji cards could become links: 険, 末, 給, 気, 下, 車 and 見.

## Limits
- I could not run Git or recompute hashes. Selected evidence is not the whole dictionary.
- For the 桁 senses 1–4 and the 下駄 usage citation, I relied on author receipts. I checked 気配, 下水, 傑作 and 険しい myself on Daijisen.
- Searches to attest the 気配 market example were blocked or found nothing relevant.
- The title-clash check used English keyword searches, so it may miss synonyms.
- This review is not a native-speaker certification.
