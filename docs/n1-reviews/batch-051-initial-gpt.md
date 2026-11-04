**Snapshot:** `07b359ca4fb55dbcb7623ee96c71c958385d28b8`, supplied as the frozen signed snapshot. Reviewed the exposed files; no uncommitted teaching was declared or intentionally included. Git identity, signature and worktree cleanliness could not be independently verified with the permitted tools.

**Scope:** Independent read-only initial review by GPT-6.1 Sol (`gpt-6.1-sol`). Reviewed both complete new teaching files, `kanji\匁.md:1–47` and `words\匁.md:1–34`, for correctness, scoped coverage and comprehensibility. No changed reused teaching passages were assigned.

Read all assigned guidance ranges, the complete raw-character packet, the supplied KanjiVG SVG, and every assigned Japanese dictionary-page section. Reviewed all **21 complete frozen JMdict families**: 匁, 百匁, 花いちもんめ; グラム, 円（えん）, 丸／円（まる）, 久しい, 斤, 升（ます）, 文（ふみ）, 文（ぶん）, 包む（つつむ）, 目（め）, 貫（かん）, 紋／文（もん）, 目（もく）, 綾／文（あや）, 文（もん）, 升（しょう）, 貫（ぬき）, and 包む（くるむ）.

Read all nine unchanged comparison cards completely: kanji 久・文・目・包 and words グラム・目・文・包む・円. Checked the confusable-word inventory through scoped searches and its interpretive guidance, plus incoming direct exclusion references involving 匁.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\匁.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\匁.md` | **CLEAN** | **CLEAN** | **CLEAN** |

CLEAN means no actionable defect established within this bounded review, not exhaustive correctness.

**Findings:** None.

Supporting checks:
- Full reading metadata preserves the supplied KANJIDIC2 order, `もんめ, め`, with no on’yomi. Selecting only `もんめ` is supported by its own reading row and linked word article. The shortened reading remains explicitly recognition-only.
- JMdict 1536280 supports 匁／もんめ and restricts its mass sense to 匁. The article respects that restriction rather than teaching 文目 as an unrestricted mass spelling.
- JMdict 1488550 records both 百匁 readings, marks the sense archaic, and flags `ひゃくめ` for irregular kana usage. The card presents a documented whole expression, labels its archaic status and warns against unrestricted substitution. The supplied Japanese sources independently support shortened め; it is not inferred merely from a kana substring.
- The **3.75 g** conversion and continued pearl-trading use are supported by the supplied Nipponica and Daijisen sections. The conversion sentence, `いちもんめ` and `さんてんななごグラム`, and English translation are appropriate. Historical silver-money use is distinguished from mass and modern monetary conversion.
- Four strokes, classical radical 勹／20 and the described modern outline agree with the raw metadata and SVG. The mnemonic is explicitly not etymology; it does not misleadingly reconcile the different historical explanations supplied by Kanjipedia and Nipponica.
- The actual distractor titles—“a long time,” “sentence, writing,” and “wrap; enclose”—are defensible wrong answers for “monme (3.75 g).” The comparison families’ additional senses do not establish another correct answer to this target.
- No direct word exclusion involving 匁 was found or established as necessary among the reviewed comparisons. Grams and monme are different-sized units, not synonymous answer labels. Both directions of the required 匁 kanji–word link are present, with the correct word reading. The supporting word has no vocabulary JLPT level inferred from its kanji.

**Optional:** None.

**Limits:** All evidence was inspected locally from the supplied frozen packets and saved HTML; no fresh upstream retrieval was performed, and their provenance/hashes were not independently authenticated. One HTML response truncated the final requested line, `batch-051-me.html:1888`; that line was recovered separately. All assigned ranges were ultimately read completely; no lookup failed.

The comparison inventory and targeted exclusion search do not certify every possible automatic fallback choice across the repository. Unchanged comparison cards were reviewed as context, not reopened for unrelated corrections.

This is textual review, not native-speaker acceptance, glyph-rendering certification, Android integration testing or physical-phone evidence. Compatible Android `f9b59a2` or later remains required; physical-phone/general-release acceptance remains outstanding, without constituting a blanket veto on bounded owner testing.

Tool calls were observed to be serial, one per response, awaiting each result. No parallel tools, shell commands, delegation, edits, commits or issues were used; no external execution audit is claimed.
