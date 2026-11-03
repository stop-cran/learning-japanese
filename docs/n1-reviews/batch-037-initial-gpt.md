**Snapshot:** `0e725a59afec03a258b4b78998c4a385c7fe3081`, as identified by the task; no uncommitted teaching included. Commit/worktree correspondence was not independently checked. Read-only initial review; no edits, delegation, commits or issues.

**Scope:** GPT-6.1 Sol (`gpt-6.1-sol`). Reviewed every sentence and metadata field in `kanji\蛇.md`, `words\蛇.md`, `words\蛇行.md` and the entire reused `words\蛇口.md` for correctness, scoped coverage and textual phone comprehensibility.

Read the assigned instructions and format/level guidance, all six raw KANJIDIC2 character elements, and all **3,218 XML lines / 139 distinct complete JMdict families**: 108 lexical, eight comparison and 23 draft-comparison families. Inspected spellings, readings, restrictions, senses and local flags. The eight core families overlapping the lexical packet were not counted again.

Read all five comparison kanji—虫, 蚊, 蛍, 口, 行—and all fourteen comparison words—曲る, カーブ, 曲線, 曲げる, うろうろ, ふらふら, ぐるぐる, 動物, 生き物, 生物, 獣, 酔っ払い, コック, 水道. Inspected every specified supplied external-dictionary range. All tool calls were serial.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Textual comprehensibility |
| --- | --- | --- | --- |
| `kanji\蛇.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\蛇.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\蛇行.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\蛇口.md` | **CLEAN** | **CLEAN** | **CLEAN** |

CLEAN means no actionable defect established within this bounded textual review, not exhaustive certification or native-rendering acceptance.

**Findings:** None.

The complete source reading order **ジャ / ダ / イ / ヤ / へび** is preserved. Explicit selections `[ジャ, ダ]` and `[へび]` each have their own linked example. Digital Daijisen’s character entry independently supports the ジャ allocation in 蛇口 and ダ allocation in 蛇行; Kanjipedia corroborates both. 委蛇’s いい/いだ readings and と・たる/classical たり construction are supported, and its obsolete flag is correctly attributed to the frozen word dictionary. ヤ remains explicitly source-only; Kanjipedia’s タ is disclosed as a differing inventory rather than silently substituted.

The animal examples correctly distinguish existence-location に with いる from sighting-location で. The 蛇行 examples, intransitive する treatment, translations and alternative じゃこう reading agree with the inspected entries. River, road and driving uses have actual Japanese dictionary support; the article does not infer intoxication or intention from a winding course. The heavy-drinker **じゃ** entry is properly separated from animal **へび**, present drunkenness and medical diagnosis.

All three required reciprocal pairs are present: 蛇–蛇, 蛇–蛇行 and 蛇–蛇口. The six direct new exclusions are explicitly declared: 蛇 with 動物, 生き物, 生物 and 酔っ払い; 蛇行 with 曲る and カーブ. Their justification comes from actual displayed labels and applicable senses, not transitive exclusion assumptions. No additional required pair was established among the assigned comparisons. The kanji distractor titles “insect; bug,” “mosquito” and “firefly” do not identify a snake.

The reused faucet article retains the requested identity, N2 field, reading, title and コック exclusion in the inspected snapshot. Its ジャ + voiced native ぐち explanation is sound. A fresh raw-HTML lookup of [Digital Daijisen’s 蛇口 entry](https://www.weblio.jp/content/蛇口) verified both the faucet じゃぐち heading/body and the separate へびくち meanings. The modern-shape mnemonic accurately separates visible components from etymology.

**Optional:** None required.

**Limits:** All required local/XML ranges returned completely; no assigned teaching or evidence packet remained truncated. The confusable-word inventory was inspected only through the scoped search, not exhaustively. Frozen XML and supplied HTML are supplied evidence, not independent upstream retrieval; their stated hashes were not recomputed. Fresh Weblio Markdown retrievals omitted the relevant Daijisen bodies; the subsequent targeted raw-HTML retrieval supplied them. Other unrequested dictionary families, examples’ corpus frequencies and historical reconstruction were not independently audited.

Native/phone acceptance remains **UNVERIFIED**. The supplied 31-Han/30-cmap coverage figures were not reproduced. In particular, new **它** has no inherited baseline occurrence and still needs fresh supported-native fallback, readability and viewport acceptance; cmap presence alone cannot establish those outcomes. Earlier pilot/all-40/160 acceptance applies only to unchanged production scope. Fresh batch-037 Android, combined-main, CI and exact public-ZIP checks remain pending; batch-036 XML cannot substitute. Compatible Android `f9b59a2+` is required, and physical-phone/general-release acceptance remains outstanding—not a blanket veto on bounded owner testing.

No other reviewer reports or prohibited author/process records were opened. Historical preservation beyond the inspected fields, other sessions’ execution behavior and publication status were not independently verified.
