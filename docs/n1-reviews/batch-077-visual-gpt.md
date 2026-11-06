**Snapshot:** Supplied evidence HEAD `45191e3dcdee657fd872a8c416227480b95cbc3e`; reviewed teaching `02877a257d6b265625e637e6a304fc8440ddd337`; native archive `46dff1466ac9f3cf64b54e197c05088414939896`. No teaching changes since my textual confirmation are reported. Actual exposed model: **GPT-6.1 Sol (`gpt-6.1-sol`)**.

**Scope:** Read the complete source packet once, then **all 33 assigned original PNGs in the specified order**, each through a separate serial `view` call. No failures, truncation, repeated image reads or other resources. Read complete article sources, the complete 567-line fixture, both terminal test results, route JSON and final article tree. The 54-capture alias inventory does not constitute 54 independently inspected pixel groups.

Fresh visual scope covers complete new 冒/冒す and only `words\冒険.md:24` and `kanji\険.md:22`, with older passages as context. Lexical conclusions carry forward my own prior review; **40 families were not freshly reread**.

**Verdicts:**

| Item | Correctness | Scoped coverage | Bounded visual comprehensibility |
|---|---|---|---|
| New `kanji\冒.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| New `words\冒す.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| Changed `words\冒険.md:24` paragraph | **CLEAN** | **CLEAN** | **CLEAN** |
| Changed `kanji\険.md:22` paragraph | **CLEAN** | **CLEAN** | **CLEAN** |

CLEAN means no demonstrated actionable scoped defect, not exhaustive correctness or physical-phone certification.

**Findings:** None demonstrated.

- **Actual article pixels:** Japanese, kana, English examples/translations, godan forms, polarity explanation and passive-affliction distinctions remain legible and consistent with source (`kanji\冒.md:18–54`; `words\冒す.md:15–45`). Both reading labels and linked examples are visible across complementary captures. The sideways-scroll instruction and shifted table captures establish that initially clipped columns are not absent teaching. Both changed reused paragraphs visibly retain their component/meaning explanations and links.
- **Fonts:** Inspected all **39 scoped Han** across Gothic/Mincho/Textbook/Brush in panels 1–2, plus focused 冒/日/目/官/冂/阜/阝/険/犯/侵 and whole words 冒険/冒す in panel 3. No blank, replacement box or misleading collapsed look-alike was observed. 冂 and 阝 are visibly rendered, including article facts lines. Main-font cmap absence therefore does not demonstrate glyph failure here. This conclusion comes from pixels—not the 156 single-character and eight word-raster probes—and identifies no particular fallback face. **Confidence: high within these captures.**
- **Actual quiz pixels:** N1 selection shows **109 cards**. The meaning question offers “mulberry,” “pavilion; restaurant building,” “brave danger; venture,” and “combine; concurrent roles”; feedback correctly selects the target. These are the observed choices, **not** the authored 日/目/官 set. On options are オウ／ボウ／コウ／ジュウ; kun options おかす／とら／おか／くす. Correct feedback identifies ボウ/on and おかす/kun, and completion shows **2 of 2 correct**. No ambiguity is established in those actual configurations.
- **Supplied execution evidence:** `N1Batch077NativeTest.kt:180–205,410–420` asserts one production ContentSync archive import, **1089 kanji / 5046 words / 109 N1**, version `2944928c13e2165a`, problems 0, parser epoch 1, and matching Full/Lite raw and curated readings with keys **ぼう／おかす**. Lines **281–358** exercise all six directions of 冒↔冒す, 冒↔冒険 and 険↔冒険, with destination assertions and System Back. Representative pixels agree. Offline assertions occur at **236–237,459–461**; route JSON records success, and `instrumentation.txt:1–38` reports **OK (2 tests)**. These are coordinator-executed results, not my execution.
- **Drawing evidence:** Pixels show a recognizable nine-stroke trace/reference and feedback, followed by blank recall input and “Here is the kanji.” Fixture **421–456** injects nine reference-derived touch strokes, asserts trace is ungraded with no drawing log, then selects “I don’t remember” and checks a newly persisted **grade 1** after Next. Reading grade-3 logs are newly exercised at **388–403**. Earlier meaning states and two historical good logs were seeded at **214–234** to unlock drawing; they are not fresh demonstrated mastery. Model-download messaging is visible, followed by model-unavailable feedback—not successful download or MLKit recognition.

**Optional:** None remaining. My prior position is retained: the implemented 冒す/攻める exclusion (`words\冒す.md:8`) is a prudent direct safeguard, **not proof of unrestricted equivalence** or proof that its earlier absence was necessarily defective. Frozen community membership remains **resolved** from the previous confirmation; the corrected original family split remains **29 lexical / 11 comparison**.

**Limits:** Earlier limitations reconcile as follows:

| Earlier limit | Status and exact boundary |
|---|---|
| 冂/阝 rendering and scoped glyph legibility | **Resolved for supplied emulator captures**; physical-device rendering remains unverified. |
| Actual reading questions, keys and completion | **Resolved for this bounded supplied run**; arbitrary/random configurations remain unverified. |
| Reciprocal routes, System Back and offline operation | **Partially resolved** by inspected fixture, successful terminal results and representative pixels; stills alone do not prove transitions or offline state. |
| Native drawing behavior | **Partially resolved** for injected tracing, feedback and recall-Again persistence only—not human handwriting, successful recall or recognition. |
| Git/signature/hash/upstream verification | **Unresolved**; supplied provenance was not independently verified. |
| Physical phone, native-speaker, general-release, whole-set and final integrated publication acceptance | **Unresolved**. |

The supplied final article tree (`n1-077-article-tree.txt:16–61`) records a transient loading screen; it does not independently prove a settled final UI or contradict the earlier targeted assertions. Persistence evidence is an in-run database check, not a restart/relaunch durability test.

This confirmation is limited to the supplied **API 35 emulator-5580** evidence. Prior prerequisite acceptance is inherited, not freshly repeated. No edits, independent native execution, process certification or exhaustive quiz-safety claim occurred.
