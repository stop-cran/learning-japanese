## Snapshot: 7ffb9fef77051410d247dfde7de6c8315ccb8e6f — committed content only

Parent: `bab4b8118ca8674554ea1ffc9cae443f166089ef`.

This is the snapshot identified by the frozen receipt, which I read first. **I used file tools, not Git execution.** The receipt’s clean-worktree, hash and derivative-equivalence checks are author-executed assertions, not independent Git checks by this reviewer.

## Scope

Reviewer: **GPT-6.1 Sol**, model ID `gpt-6.1-sol`, family `gpt`. Read-only; no delegation, agents or file changes.

I read all twenty new articles completely, the complete related patch, and all six changed kanji cards and eight changed old-word cards in context. I reviewed the twenty assigned TSV mappings, all twenty principal families/38 sense records, 37 component records, 210 supplied label/exclusion records, complete relevant comparison-family records, supplemental 応接, and all 27 supplied public-entry captures. I also read 50 additional comparison articles completely and made targeted title searches within `words\`.

The required repository instructions and format passages were read. Provenance review included the vocabulary/component snapshots and JLPT policy. Fresh supplementary dictionary definitions were successfully inspected for 当たる, 苦心, 機会 and 結論. Supplied public captures are distinguished from those fresh retrievals.

**Result: four new cards need quiz-label/exclusion fixes.** No actionable defect was established in the source identities, selected teaching coverage, six kanji edits or eight bounded old-word edits.

## Verdicts

`CLEAN` means no actionable defect established in the reviewed scope—not exhaustive correctness or native-speaker certification. Correctness below includes quiz-answer safety.

| Source row | Article | Status | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:882 | `words\青少年.md` | New | CLEAN | CLEAN | CLEAN |
| N2:883 | `words\整数.md` | New | CLEAN | CLEAN | CLEAN |
| N2:884 | `words\清掃.md` | New | CLEAN | CLEAN | CLEAN |
| N2:885 | `words\生存.md` | New | CLEAN | CLEAN | CLEAN |
| N2:886 | `words\生長.md` | New | CLEAN | CLEAN | CLEAN |
| N2:887 | `words\政党.md` | New | CLEAN | CLEAN | CLEAN |
| N2:888 | `words\生年月日.md` | New | CLEAN | CLEAN | CLEAN |
| N2:889 | `words\性能.md` | New | CLEAN | CLEAN | CLEAN |
| N2:890 | `words\整備.md` | New | CLEAN | CLEAN | CLEAN |
| N2:891 | `words\成分.md` | New | CLEAN | CLEAN | CLEAN |
| N2:892 | `words\性別.md` | New | CLEAN | CLEAN | CLEAN |
| N2:893 | `words\正方形.md` | New | CLEAN | CLEAN | CLEAN |
| N2:894 | `words\正門.md` | New | CLEAN | CLEAN | CLEAN |
| N2:895 | `words\成立.md` | New | NEEDS FIX — GPT45-02 | CLEAN | CLEAN |
| N2:896 | `words\西暦.md` | New | NEEDS FIX — GPT45-04 | CLEAN | CLEAN |
| N2:897 | `words\背負う.md` | New | CLEAN | CLEAN | CLEAN |
| N2:898 | `words\赤道.md` | New | CLEAN | CLEAN | CLEAN |
| N2:899 | `words\せっかく.md` | New | NEEDS FIX — GPT45-01 | CLEAN | CLEAN |
| N2:900 | `words\接近.md` | New | CLEAN | CLEAN | CLEAN |
| N2:901 | `words\接する.md` | New | NEEDS FIX — GPT45-03 | CLEAN | CLEAN |

**Six kanji edits — assessed individually**

| Card | Correctness / coverage / comprehensibility | Assessment |
|---|---|---|
| 清 | CLEAN / CLEAN / CLEAN | 清掃 appears at セイ in the reading row and Common words. |
| 掃 | CLEAN / CLEAN / CLEAN | 清掃 appears at ソウ in both required locations. |
| 党 | CLEAN / CLEAN / CLEAN | 政党 appears at トウ in both locations. |
| 門 | CLEAN / CLEAN / CLEAN | 正門 appears at モン in both locations. |
| 接 | CLEAN / CLEAN / CLEAN | Both 接近 and 接する appear at セツ in both locations; the small っ is explained. |
| 角 | CLEAN / CLEAN / CLEAN | 折角 correctly navigates to kana-primary せっかく; it is not counted as another primary-spelling pair. |

The supplied patch contains no kanji metadata or stroke-data changes.

**Eight bounded old-word edits — assessed individually**

| Card and changed passage | Correctness / coverage / comprehensibility |
|---|---|
| 青年 → 青少年, line 31 | CLEAN / CLEAN / CLEAN |
| 小数 → 整数, line 28 | CLEAN / CLEAN / CLEAN |
| 誕生日 → 生年月日, line 28 | CLEAN / CLEAN / CLEAN |
| 性 → 性別, line 28 | CLEAN / CLEAN / CLEAN |
| 四角 → 正方形, line 27 | CLEAN / CLEAN / CLEAN |
| 四角い → 正方形, line 35 | CLEAN / CLEAN / CLEAN |
| 門 → 正門, line 29 | CLEAN / CLEAN / CLEAN |
| 成長 comparison/source additions, lines 42–44 and 54–55 | CLEAN / CLEAN / CLEAN |

The 成長 comparison properly acknowledges plant overlap and broader/older 生長 uses rather than imposing an absolute spelling partition. Existing easier levels and identities are preserved.

**Twenty mappings — separate verdict**

Each mapping **N2:882 through N2:901 is CLEAN / CLEAN / CLEAN** for correctness, scoped coverage and comprehensibility, independently of the quiz defects above. The assigned TSV rows agree with the blind mapping derivative and the taught source identities.

In particular, 政党 correctly teaches the organization rather than copying the raw “member of” parenthesis; 整備 follows the pinned maintenance/equipping senses rather than treating every loose raw gloss as an unrestricted synonym. 背負う preserves primary せおう senses 1–3 and separately recognizes しょう/しょってる-restricted sense 4. 折角 maps explicitly to usual-kana せっかく with appropriate written-kanji metadata. Public extensions do not acquire invented pinned indices or independent N2 status.

## Findings

**GPT45-01 — Medium severity — Correctness: missing direct safeguards for せっかく**

**Location:** `words\せっかく.md:4–9`; comparison headers/exclusions at `words\苦心.md:4–9`, `words\機会.md:4–9`, `words\チャンス.md:4–9` and `words\きっかけ.md:4–9`.

The effort side of the title overlaps 苦心’s “painstaking effort; taking pains.” The opportunity side, **“a valuable opportunity,”** also permits defensible competing labels from 機会 (“opportunity”), チャンス (“chance; opportunity”) and きっかけ (“trigger; opening; opportunity”). None has a direct exclusion with せっかく. Existing guards through 努力, 手間, 苦労 or between the opportunity cards are nontransitive.

**Impact:** These distinct titles remain eligible to coexist despite overlapping English answers. This does not imply unrestricted Japanese substitution or that せっかく is an ordinary countable noun meaning “opportunity.”

**Minimal remedy:** Add direct safeguards for 苦心 and the three opportunity-label pairs. Alternatively, revise the opportunity portion to describe せっかく’s qualifying function, then reassess those three pairs; preserve the accurate constructions in the body.

**Evidence:** Complete JMdict 1596090, senses 1–3 (`batch-45-principal-reading.txt:53`); complete 苦心 1244530 (`batch-45-selected-families-03.txt:77–81`); the actual comparison articles and headers. Fresh Seisenban Nihon Kokugo Daijiten entries for [苦心](https://kotobank.jp/word/苦心) and [機会](https://kotobank.jp/word/機会) corroborate the effort and occasion meanings.

**Confidence:** High for 苦心; medium-high for the opportunity-label safeguards.

**GPT45-02 — Medium severity — Correctness: 成立’s establishment and conclusion labels remain insufficiently guarded**

**Location:** `words\成立.md:4–9,16–23`; `words\誕生.md:4–9,16–21`; `words\建設.md:4–9,16–18`; `words\結論.md:4,15–18`; `words\終わり.md:4–9,16`.

Missing direct pairs include:

| Other card | Established overlap or label ambiguity |
|---|---|
| 誕生 | “Coming into existence” directly overlaps 成立’s selected formation sense, including new entities. |
| 建設 | Its displayed “establishment” is also an ordinary translation of 成立. |
| 結論 | Its unqualified “conclusion” competes with 成立’s displayed, likewise unqualified “conclusion.” |
| 終わり | “End; conclusion” creates a further collision with 成立’s agreement/process-completion sense. |

The last two are English-label ambiguities, not claims that 結論 or 終わり freely replaces 成立 in Japanese.

**Impact:** The completion-oriented exclusions already present do not protect these additional pairs.

**Minimal remedy:** Add the four direct exclusions under the current labels. Qualifying “conclusion” as agreement-conclusion could instead resolve the reasoning-conclusion ambiguity, but would not eliminate the 誕生/建設 overlap.

**Evidence:** Complete 成立 1375880, senses 1–3 (`batch-45-principal-reading.txt:41`); complete 誕生 1419080 (`batch-45-selected-families-10.txt:51–57`) and 建設 1257420 (`batch-45-selected-families-04.txt:3–7`); complete actual comparison articles. Fresh [結論](https://kotobank.jp/word/結論) definitions confirm its reasoning/judgment identity, distinct from concluding an agreement.

**Confidence:** High for 誕生/建設; medium-high for the conclusion-label collisions.

**GPT45-03 — Medium severity — Correctness: 接する misses contact and secondary-sense label collisions**

**Location:** `words\接する.md:4–9,16–27`; `words\当たる.md:4–9,16–22`; `words\連絡.md:4,15–20`; `words\片付ける.md:4–9`.

当たる’s displayed **“make contact”** is defensible for physical 接する. Both cards exclude 触る/触れる, but that does not exclude them from each other.

Two further English-label collisions remain: 連絡’s unqualified **“contact”**, and 接する’s unqualified **“deal with”** against the ordinary matter-settling sense of 片付ける. The latter must not be dismissed merely because the existing 片付ける article selects tidying for its examples.

**Impact:** These pairs can still supply competing acceptable English answers. The different Japanese objects and constructions are not visible in the broad answer labels.

**Minimal remedy:** Add direct guards for 当たる and 連絡. Either guard 片付ける directly or qualify 接する’s “deal with” as dealing with/treating people, then reassess that pair.

**Evidence:** Complete 接する 1385350, especially senses 1–2 (`batch-45-principal-reading.txt:59`); complete 当たる 1448810, especially sense 2 (`batch-45-selected-families-11.txt:61–83`); complete 連絡 1559900 (`batch-45-selected-families-14.txt:8–14`); complete 片付ける 1511790, ordinary sense 2 (`batch-45-selected-families-12.txt:88–96`). Fresh [Daijisen 当たる](https://www.weblio.jp/content/当たる), sense 1, explicitly includes touching/contact.

**Confidence:** High for 当たる; medium-high for the remaining English-label collisions.

**GPT45-04 — Low severity — Correctness: 西暦 has unsupported period-word exclusions**

**Location:** `words\西暦.md:4–9,16–20,39–43`; `words\時代.md:5,15–19`; `words\年代.md:4–9,16–24`.

The exclusions with 時代 and 年代 are overbroad under the actual titles. 西暦’s label explicitly says **“Common Era year numbering; Western calendar,”** not generic “era.” 時代 and 年代 identify periods, not that numbering/calendar system. Sharing the English substring *Era* or the topic of time does not establish an acceptable alternative answer.

The body correctly explains this distinction; the exclusions do not reflect it.

**Impact:** Two semantically distinct choices are unnecessarily removed from the pool.

**Minimal remedy:** Remove 時代 and 年代 from 西暦’s exclusions; retain カレンダー.

**Evidence:** Complete 西暦 1381140, senses 1–2 (`batch-45-principal-reading.txt:44`) and its supplied public definition; complete 時代 1316300 (`batch-45-selected-families-05.txt:35–42`) and 年代 1468950 (`batch-45-selected-families-11.txt:150–154`), together with the actual articles and qualified titles.

**Confidence:** Medium-high.

## Optional

None. The findings concern existing quiz behavior, not optional dictionary expansion or unrelated baseline redesign.

## Limits

I did **not** read the entire 346-family/891-sense evidence union, every captured old body, or the author’s claimed 131-body inspection scope. Selected-family files were consulted for complete relevant records, not treated as an exhaustive dictionary. The full large evidence JSON and full confusable-word inventory were not read end-to-end.

Several fresh lookups failed, returned unrelated material, or exposed no usable definitions—including attempts for きっかけ and 終わり. Those results supply no semantic evidence; the corresponding label findings rely on complete actual app articles and independently inspected principal senses, without inventing additional pinned indices.

No app-generated question was executed. Findings identify eligibility/ambiguity under the documented pairwise quiz contract, not a claim that a particular question was observed. Git state, hashes and frozen-derivative equivalence remain receipt-backed rather than independently verified.
