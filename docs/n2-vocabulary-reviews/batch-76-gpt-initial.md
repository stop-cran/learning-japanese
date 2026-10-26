## Snapshot: c1563f9c47fa9af139ef149893b4c5e4e9be3317; committed content only

Parent: `4047358f535321e7e4373a408258586cd7cd4e43`.

The frozen receipt was read first. Snapshot identity and committed-only status are supported by that supplied receipt, **not independently verified with Git**: the available file tools cannot execute Git or recompute the author’s hash/equivalence checks.

## Scope: gpt-6.1-sol; gpt family

This was a serial, read-only review, without agents, delegation, edits or concurrent work.

Completely read:

- All twenty assigned articles; all five related kanji bodies; `related.patch`; and the five complete supplied parent-state kanji bodies.
- The required repository instructions and `docs\content-format.md:18–103`; both source snapshot JSON files; the TSV header and exactly physical rows 1502–1521.
- All twenty mappings, twenty complete principal families/36 senses, thirty-one complete component records and 248 complete comparison labels/exclusions, using the bounded JSONL ranges.
- All eight family-inspection renderings and the complete eight-family supplement. Including three further complete packet families—しまう, 仕舞い and 損害—actual pinned dictionary coverage was **204 distinct families/502 senses**, including the twenty principals. This is not inspection of all 429 prepared families.
- All fifteen older-body renderings: 117 complete articles. Twelve additional complete current bodies—がっかり, 失望, しんみり, 良い, 軍, 武士, 終える, 仕舞い, しまう, 一度に, 損害 and 不利—bring older-body coverage to **129 distinct articles**.
- The complete `public-bodies.txt` through EOF. Its twenty frozen captures represent **one authority, Digital Daijisen via Weblio**, not twenty independent dictionaries.

Supplementary public reads included complete live Jisho entries for 終える and 一度に, applicable Kotobank dictionary headings for 一度に, 倒れる and へこむ, and Bunpro’s によって／による explanation. Existing component-card filenames and lower-level metadata were checked directly. The fourteen lower-level kanji bodies were not completely reviewed; their existence, levels and substantive article links were checked.

No prohibited ledger, author-rationale source or other reviewer’s report was read. The large evidence packet was read selectively beyond its complete compact equivalents.

## Verdicts:

**Five localized fixes are identified below.** Source identities, selected meanings, additional recognition and the five reciprocal kanji additions otherwise passed within the inspected scope.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1502 | 文芸 | CLEAN | CLEAN | CLEAN | Literary art and broader arts recognition distinguished; 文藝 treated as an older spelling. |
| N2:1503 | 文献 | CLEAN | CLEAN | CLEAN | Research/reference literature and written sources taught without literalizing 献. |
| N2:1504 | 噴水 | CLEAN | CLEAN | CLEAN | Fountain/water-jet sense distinguished from drinking fountains and natural springs. |
| N2:1505 | 分数 | CLEAN | CLEAN | CLEAN | Fraction reading order and denominator–numerator construction explained correctly. |
| N2:1506 | 文体 | CLEAN | CLEAN | CLEAN | Writing style and written-language form distinguished from typography. |
| N2:1507 | 分布 | CLEAN | CLEAN | CLEAN | Distribution and usual intransitive participant marking appropriately qualified. |
| N2:1508 | 文房具 | NEEDS FIX | CLEAN | CLEAN | F01: exclusions extend from stationery to generic tool categories. |
| N2:1509 | 文脈 | CLEAN | CLEAN | CLEAN | Discourse context and broader contextual recognition are both supported. |
| N2:1510 | 分量 | CLEAN | CLEAN | CLEAN | Everyday quantity teaching separated from additional measuring-verb recognition. |
| N2:1511 | 分類 | NEEDS FIX | CLEAN | NEEDS FIX | F02: によって and noun-modifying による need separate attachment guidance. |
| N2:1512 | 閉会 | NEEDS FIX | CLEAN | CLEAN | F03: three unguarded end/finish labels can overlap its taught meeting-closing use. |
| N2:1513 | 平気 | CLEAN | CLEAN | CLEAN | Composure, indifference and colloquial “all right” usages appropriately distinguished. |
| N2:1514 | 並行 | NEEDS FIX | CLEAN | CLEAN | F04: missing direct exclusion with 一度に’s simultaneous reading. |
| N2:1515 | 平日 | CLEAN | CLEAN | CLEAN | Calendar use and variable Saturday treatment explained; unrelated reading kept separate. |
| N2:1516 | 兵隊 | CLEAN | CLEAN | CLEAN | Individual soldier, troops and colloquial subordinate recognition distinguished. |
| N2:1517 | 平凡 | CLEAN | CLEAN | CLEAN | Ordinary/unremarkable meaning presented without making it invariably insulting. |
| N2:1518 | 平野 | CLEAN | CLEAN | CLEAN | Geographical plain distinguished from activity fields and the reading ひらの. |
| N2:1519 | 凹む | NEEDS FIX | CLEAN | CLEAN | F05: the explicitly taught loss sense leaves 損害 unguarded. |
| N2:1520 | 臍 | CLEAN | CLEAN | CLEAN | Stable identity, usual kana and へそ／ほぞ restrictions preserved. |
| N2:1521 | 隔てる | CLEAN | CLEAN | CLEAN | Transitive ichidan constructions, barriers and intervening intervals explained correctly. |

**Five kanji changes and baseline preservation — CLEAN.** Manual comparison of complete current bodies, the patch and supplied parent bodies found precisely one reciprocal word link and its JMdict footer ID added to each card. Metadata and all other body text were preserved:

- `kanji\芸.md:40,53`: 文芸／ぶんげい; added entry **1505290**.
- `kanji\布.md:38,53`: 分布／ぶんぷ; added entry **1504160**.
- `kanji\量.md:35,46`: 分量／ぶんりょう; added entry **1504430**.
- `kanji\並.md:40,51`: 並行／へいこう; added entry **1508480**.
- `kanji\兵.md:36,45`: 兵隊／へいたい; added entry **1506590**.

Correctness, scoped coverage and comprehensibility of those five additions are CLEAN. This preservation judgment is a supplied-baseline text comparison, not an independently executed parent-commit diff.

**Component metadata and links — CLEAN.** All 28 distinct primary written Han appear in the appropriate word metadata. All nineteen existing component cards receive substantive links, including the fourteen lower-level cards: 文、水、分、数、体、具、類、閉、会、平、気、行、日、野. No current cards were found for 献、噴、房、脈、隊、凡、凹、臍、隔; their plain-text treatment is appropriate. All five required N2 reciprocal pairs are present in both directions.

**Mappings — all twenty CLEAN.** Physical source-row associations, raw source spelling/readings, stable filenames, selected one-based senses and principal-family restrictions match the teaching. In particular, 凹む and 臍 retain their stable identities; 分量’s additional measuring sense is separately qualified recognition, not silently promoted to another N2 source row. Restrictions belonging to other readings of 平日, 凹む, 臍, 軍 or 武士 were not transferred.

## Findings:

**F01 — LOW; correctness, quiz-exclusion excess — `words\文房具.md:9,16–17,31–33`.**

The exclusions with 道具 and 器具 are supported only by a specific-to-general tool-category relationship. Their actual titles are **“tool; implement”** (`words\道具.md:5`) and **“utensil; tool; apparatus”** (`words\器具.md:4`), versus 文房具’s **“stationery; writing supplies.”** The complete older bodies teach general implements, including cooking utensils and experimental apparatus; they do not establish a stationery meaning. The new body itself correctly calls them *broader* terms. Under the requested prohibition on category proximity alone establishing a pair, these suppress usable distinctions rather than guard equivalent meanings. **Minimal remedy:** remove these two IDs from 文房具’s exclusions; retain the useful body comparisons. **Evidence:** complete families 1505620, 1454180 and 1218920, plus the three complete articles and displayed titles. **Confidence: medium.**

**F02 — MEDIUM; correctness/comprehensibility, attachment guidance — `words\分類.md:16–21`.**

Immediately after teaching `things を分類する`, the article says that the criterion can take “によって or による,” without distinguishing their attachment. In this use, **種類によって分類する** modifies the classification action, whereas **種類による分類** has による modifying the following noun. The current presentation invites the erroneous construction `*種類による分類する`; its correct によって example does not resolve the unexplained alternative. **Minimal remedy:** give the two contrasting patterns explicitly, or omit による from this introductory rule. **Evidence:** the article’s quoted rule and example; [Bunpro’s によって／による explanation](https://bunpro.jp/grammar_points/によって-による), including its noun-modification guidance. **Confidence: high.**

**F03 — MEDIUM; correctness, quiz-exclusion omissions — `words\閉会.md:4,9`.**

閉会 can still coexist with 終える, 仕舞い and しまう. Their complete titles are respectively **“finish; complete something,” “end; finish,”** and **“put away; finish; end up doing.”** The relevant ordinary meanings are finishing an activity or bringing it to a close—not merely auxiliary completion or closing a shop. Those meanings overlap the expressly taught transitive closing of a meeting. None of the three older cards declares the reverse edge. Guards through 終わる or 終わり do not propagate, and these titles are not identical to 閉会’s title. **Minimal remedy:** add `[終える, 仕舞い, しまう]` to 閉会’s exclusions. **Evidence:** complete `words\終える.md:4,9,16–21`, `words\仕舞い.md:4,9,16–21`, `words\しまう.md:4,9,16–21`; pinned 1508600:1, 1305380:1 and 1594530:1; the [complete live 終える entry](https://jisho.org/api/v1/search/words?keyword=終える) corroborates its ordinary transitive meaning. **Confidence: high.**

**F04 — MEDIUM; correctness, quiz-exclusion omission — `words\並行.md:4,9,16–21`.**

一度に, titled **“all at once,”** remains eligible beside 並行’s **“moving side by side; concurrency.”** 一度に can describe a batch completed in one occasion without strict simultaneity, but that does not eliminate its ordinary simultaneous use. Carrying out two investigations concurrently can also be described as doing them “at once.” This is a direct overlap, not an inference through the existing 同時 or 一斉 guards. **Minimal remedy:** add 一度に to 並行’s exclusions. **Evidence:** pinned 1508480:2; complete `words\一度に.md:4,16–28`; [精選版日本国語大辞典’s applicable いちどに heading](https://kotobank.jp/word/一度に-433489), which explicitly gives 同時に. The separate ひとたびに heading was not imported. **Confidence: high.**

**F05 — MEDIUM; correctness, quiz-exclusion omission — `words\凹む.md:9,16–17,34–43`.**

The article explicitly teaches “suffer a loss,” but 損害, titled **“damage; loss,”** remains unguarded. Its complete body includes financial loss and a monetary-loss example, so this is not merely an association between physical dents and damage. The shared loss meaning can produce an acceptable alternative in a context-free meaning quiz; the nominal/verbal difference does not by itself remove that ambiguity. 損害’s reverse exclusions also omit 凹む. **Minimal remedy:** add 損害 to 凹む’s exclusions, without changing either word’s grammar or implying that their other senses substitute freely. **Evidence:** pinned 1179200:4 and complete 1406710:1; complete `words\損害.md:4,9,16–24`; [Digital Daijisen’s applicable へこむ heading](https://kotobank.jp/word/凹む-484881), whose public sense 3 gives 損をする. That public numbering is not the pinned JMdict index. **Confidence: medium.**

## Optional:

None.

## Limits:

Git identity, worktree cleanliness, hashes and lossless-rendering equivalence were not independently executed checks. The committed-only assessment relies on the frozen receipt and supplied snapshot representations.

The 248 labels were all read, but they are not 248 full-body inspections. Actual older-body coverage was 129 articles, and pinned family coverage was 204/502—not all 429/976 prepared records. Unread comparison bodies and uninspected families remain outside any exhaustive ambiguity claim.

The frozen public captures establish applicable lexical headings, not every usage or frequency claim. Two supplementary Weblio fetches returned no applicable dictionary body and were not used as verification; later successful sources are identified above. Live public evidence is unpinned and does not replace the frozen JMdict sense indices.

CLEAN means no actionable defect established within this actual scope, not exhaustive correctness or native-speaker certification.
