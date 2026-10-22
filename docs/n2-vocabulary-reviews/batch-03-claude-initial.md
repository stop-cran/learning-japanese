## Snapshot
Frozen commit: **eabe2e942e8e6fa67cc4dd4093c3e6ea14edaf3c** (parent f8eaca3bef6d3c90b5002e0d3b50b206acc73d5d). I reviewed committed content only. I had file tools but no Git, so I couldn't recompute the file hashes or compare against Git. I read the working tree and relied on the receipt's statement that the content is clean and committed.

## Scope
- **Reviewer:** claude-opus-5.5 (Claude family), working alone and without editing any files.
- **New articles:** all 19 read completely against their mappings (N2:42–61) and the JMdict families in batch-03.json.
- **Related edits:** only the changed passages from the patch, on the 荒, 改, 著, 争, 有, 難, 易, 外, 言, 付, 意 and 生 kanji cards and on 戦う.
- **Reuse claim:** only the 在る/ある coverage in `words\ある.md`, checked against JMdict entry 1296400.
- **Other files read:** existing cards, to check links, comparisons and quiz overlaps.
- **Not read:** the forbidden documents and any unchanged teaching on existing cards.

## Verdicts
| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 荒い | CLEAN | CLEAN | CLEAN |
| 粗い | CLEAN | CLEAN | CLEAN |
| あらすじ | CLEAN | CLEAN | CLEAN |
| 争う | CLEAN | CLEAN | CLEAN |
| 改めて | CLEAN | CLEAN | CLEAN |
| 改める | CLEAN | CLEAN | CLEAN |
| 著す | NEEDS FIX (F1) | CLEAN | CLEAN |
| 有難い | CLEAN | CLEAN | CLEAN |
| あれこれ | CLEAN | CLEAN | CLEAN |
| あわただしい | NEEDS FIX (F2) | CLEAN | NEEDS FIX (F3) |
| あわてる | NEEDS FIX (F2) | CLEAN | CLEAN |
| 安易 | CLEAN | CLEAN | NEEDS FIX (F3) |
| 案外 | CLEAN | CLEAN | CLEAN |
| アンテナ | CLEAN | CLEAN | CLEAN |
| 言い出す | CLEAN | CLEAN | NEEDS FIX (F3) |
| 言い付ける | CLEAN | CLEAN | CLEAN |
| 意義 | CLEAN | CLEAN | CLEAN |
| 生き生き | CLEAN | CLEAN | CLEAN |
| いきなり | CLEAN | NEEDS FIX (F4) | CLEAN |

- **Related edits (changed passages only):** CLEAN on all three facets. Every link resolves and every reading matches the word. The N2 kanji 荒, 改 and 著 gain reciprocal links to their new words.
- **Reuse claim (`ある.md`):** CLEAN on all three facets.
  - Line 20 renders the spelling 在る.
  - Line 12 teaches location with "place に thing が ある", which covers JMdict sense 3.
  - "Usually for things" matches sense 1's note that ある is usually used of inanimate objects.
  - "Kana is usual" matches the dictionary's usually-written-in-kana flag.
  - The card stays at N5 under the same identity.

## Findings
- **F1 — minor; correctness (quiz labels)**
  - **Where:** `words\著す.md:4,9` and `words\著者.md:4,9`.
  - **Problem:** 著す is titled "author; publish a work" and 著者 is titled "author". Neither excludes the other, even though they share 著. English "author" is both a noun and a verb, so whichever of the two is the distractor can look like a correct answer, in either quiz direction.
  - **Fix:** add 著者 to 著す's `quiz_exclusions`, or retitle 著す as something like "write or publish (a work)".
  - **Confidence:** high.
- **F2 — minor; correctness (quiz labels)**
  - **Where:** `words\あわただしい.md:4,9` and `words\あわてる.md:4,9`.
  - **Problem:** the titles are "hectic; hurried" and "become flustered; hurry". Both cards exclude 急ぐ, which shows the author treats the hurry overlap as risky, yet they don't exclude each other. あわただしい.md:39 even contrasts the two words directly.
  - **Fix:** add the exclusion on one of the two cards.
  - **Confidence:** medium, because the different parts of speech partly tell them apart.
- **F3 — minor; comprehensibility**
  - **Where:** `あわただしい.md:30` ("the source's kana form") and `:42–43` ("the source gloss contains English 'confused'"), `安易.md:41` ("The source's 'easy-going'"), and `言い出す.md:40` ("The source gloss 'break the ice'").
  - **Problem:** learners never see "the source", so these sentences are unclear to them.
  - **Fix:** say "some word lists gloss it as…", or state the point directly.
  - **Confidence:** high.
- **F4 — minor; scoped coverage (linking)**
  - **Where:** `いきなり.md:33`.
  - **Problem:** the comparison mentions 徐々に as plain text, but `words\徐々に.md` exists (N3, "gradually; by degrees"). The content-structure guide, lines 20 and 55, says comparisons should link existing cards.
  - **Fix:** change it to `[徐々に](徐々に.md)`.
  - **Confidence:** high.

## Optional
- 改める: consider adding "change" (sense 1) to the title.
- 意義: consider putting "significance" first in the title. Its exact match with 意味 is already deduplicated by the app.
- Borderline quiz exclusions: 粗い with かさかさ, and 有難い with 御礼 or ありがとう.
- あれこれ.md:25: the wording about 彼 not being read かれ is awkward.
- 有/難 kanji lines: "usually ありがたい" would be clearer as "usually written ありがたい".
- 有難い: could mention the 有り難し ("rare") etymology.
- 改めて: could add 改めて感じる ("realize anew").
- 生き生き: could link 生きる.
- ある: could note that the official guidance associates 在る with existence and 有る with possession, while kana is standard.

## Limits
- Without Git, I could not check that the working tree matches the commit or verify file hashes.
- The official spelling extracts (bunka.go.jp, entries 014–016) were supplied by the author. I did not retrieve the PDF myself.
- I did not inspect how the app picks quiz distractors, so the practical impact of F1 and F2 depends on whether the app pairs those words.
- 情勢があわただしく変わる and 情報にアンテナを張る seemed natural to me but were not checked against an outside source. This is not a native-speaker certification.
- The JMdict evidence is a selection from the dictionary, so a missing sense does not prove it doesn't exist.
