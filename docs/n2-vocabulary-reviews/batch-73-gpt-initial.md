## Snapshot: 4abf8105090403e90d2a950b90a733cd538d1424 — committed content only

**Result: NEEDS FIX.** One pronunciation instruction is incorrect, and three groups of direct quiz exclusions are missing.

Parent: `303da3a4017ebf0405e76c88add06c490beaab6e`. I read `frozen-snapshot.json` first. The commit and committed-content status are supplied snapshot assertions: file tools cannot execute Git, so I could not independently verify checkout identity, parent-tree equality, hashes, or worktree cleanliness. No edits or delegation were performed.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

Complete reads covered all twenty assigned articles, all eight edited kanji bodies, `related.patch`, twenty mappings, twenty complete principal families—including all 29 senses, restrictions, flags, inherited POS and raw source fields—and all 31 component records. I read the required instructions, `docs\content-format.md:18–103`, both source-snapshot documents, and only the TSV header and physical lines **1442–1461**.

Comparison evidence comprised all nine family renderings and the supplemental two-family rendering: the supplied **234-family/515-sense union**. The unrelated Puku Puku character-name family `5744803` was not used as lexical evidence. I also read all eleven older-body renderings, all eighteen additionally named older articles, and the complete articles 流行る and 宣伝: **125 distinct word bodies overall**, accounting for the duplicated 増える. The 129 navigation-label records were read separately and were not counted as complete article reads.

I read `public-bodies.txt` completely and the complete corresponding JSON. Those twenty frozen captures represent **one authority, Digital Daijisen via Weblio**, not twenty independent dictionaries. Additional applicable live evidence was the **精選版 日本国語大辞典** entry for 流行る on Kotobank. The monolithic `review-evidence.json` was not opened; its permitted compact equivalents were used. No prohibited rationale, ledger, script, or other reviewer report was read.

## Verdicts:

**CLEAN** means no actionable defect established within these reads. Scoped coverage includes quiz safeguards; it does not require exhaustive dictionary expansion.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1442 | ピンク — ピンク | CLEAN | CLEAN | CLEAN | `1107140`, selected s1; adult attributive s2 is bounded recognition. Blank source spelling preserved. |
| N2:1443 | 便箋 — びんせん | CLEAN | CLEAN | CLEAN | `1512640`, s1; writing-paper use and 便せん recognition are clear. 箋 remains metadata, not a fabricated link. |
| N2:1444 | 瓶詰 — びんづめ | NEEDS FIX | CLEAN | CLEAN | `1491130`, ss1–2; stable spelling and qualified mixed formation are correct. False “long vowel” instruction: N273-01. |
| N2:1445 | ファスナー — ファスナー | CLEAN | CLEAN | CLEAN | `1108160`, s1; Japanese zipper meaning distinguished from broader English *fastener*. Blank source spelling preserved. |
| N2:1446 | 風船 — ふうせん | CLEAN | CLEAN | CLEAN | `1499940`, selected s1; dated/original aircraft usage is separate recognition, not an unrestricted modern substitute. |
| N2:1447 | 不運 — ふうん | CLEAN | CLEAN | CLEAN | `1491290`, s1; noun/na-adjective patterns, unfavorable luck and vowel morae are handled correctly. |
| N2:1448 | 殖える → 増える — ふえる | CLEAN | CLEAN | CLEAN | `1602440`, s1; same-family spelling explicitly taught. Existing **N4** identity, title, `[増]` and absence of a local exclusion declaration retained. |
| N2:1449 | 深まる — ふかまる | CLEAN | NEEDS FIX | CLEAN | `1362660`, s1; intransitivity, conjugation and seasonal example are sound. Missing direct guards: N273-02. |
| N2:1450 | 不規則 — ふきそく | CLEAN | CLEAN | CLEAN | `1491840`, s1; irregularity is not equated with dishonesty; な/に attachment is supplied. |
| N2:1451 | 普及 — ふきゅう | CLEAN | NEEDS FIX | CLEAN | `1497110`, s1; both transitive and intransitive uses are supported. Missing direct guards: N273-04. |
| N2:1452 | 付近 — ふきん | CLEAN | CLEAN | CLEAN | `1496240`, s1; landmark attachment, の constructions and rare 附近 recognition are appropriately bounded. |
| N2:1453 | 拭く — ふく | CLEAN | CLEAN | CLEAN | `1357240`, s1; wiping, particles and godan forms are correct; washing and homophones are distinguished. |
| N2:1454 | 副詞 — ふくし | CLEAN | CLEAN | CLEAN | `1500440`, s1; the term itself is a noun, and adverbs are not incorrectly limited to modifying verbs. |
| N2:1455 | 複写 — ふくしゃ | CLEAN | CLEAN | CLEAN | `1501390`, s1; copying is not restricted to photocopiers. Document-copy counting is explained. |
| N2:1456 | 複数 — ふくすう | CLEAN | CLEAN | CLEAN | `1501400`, ss1–2; multiple versus numerous, noun＋の, grammatical plural and search-only 復数 are distinguished. |
| N2:1457 | 含める — ふくめる | CLEAN | CLEAN | CLEAN | `1216890`, selected ss1–2; ss3–5 remain contextual recognition. The idiom and both verbs’ transitivity are explained correctly. |
| N2:1458 | 膨らます — ふくらます | CLEAN | NEEDS FIX | CLEAN | `1519970`, s1; source form, godan conjugation and transitive construction are preserved. Missing direct guards: N273-03. |
| N2:1459 | 膨らむ — ふくらむ | CLEAN | NEEDS FIX | CLEAN | `1519990`, s1; intransitive forms, figurative growth and rare spelling are sound. Missing direct guards: N273-03. |
| N2:1460 | 不潔 — ふけつ | CLEAN | CLEAN | CLEAN | `1492160`, ss1–2; hygiene and morally dirty/indecent uses are distinguished without treating the word as a diagnosis. |
| N2:1461 | 更ける — ふける | CLEAN | CLEAN | CLEAN | `1279290`, selected s1; 夜が更ける and ichidan forms are correct. Seasonal use is additional public-dictionary evidence, not an invented pinned sense. |

**Eight kanji edits:** all three facets are CLEAN for each edited body. The nine tracked reciprocal pairs use the actual whole-word readings and matching dictionary footer IDs.

| Kanji | Correctness | Scoped coverage | Comprehensibility | Reciprocal word and reading | JMdict ID |
|---|---|---|---|---|---|
| 瓶 | CLEAN | CLEAN | CLEAN | 瓶詰 びんづめ | `1491130` |
| 詰 | CLEAN | CLEAN | CLEAN | 瓶詰 びんづめ, appropriately under the voiced native component | `1491130` |
| 則 | CLEAN | CLEAN | CLEAN | 不規則 ふきそく | `1491840` |
| 普 | CLEAN | CLEAN | CLEAN | 普及 ふきゅう | `1497110` |
| 副 | CLEAN | CLEAN | CLEAN | 副詞 ふくし | `1500440` |
| 詞 | CLEAN | CLEAN | CLEAN | 副詞 ふくし | `1500440` |
| 複 | CLEAN | CLEAN | CLEAN | 複写 ふくしゃ; 複数 ふくすう | `1501390`; `1501400` |
| 含 | CLEAN | CLEAN | CLEAN | 含める ふくめる | `1216890` |

**Baseline preservation:** the supplied patch preserves existing kanji headers and examples. The observed 増える article retains its required N4 identity, reading, title, body teaching, exclusions and `[増]` metadata. Independent parent-versus-commit byte equality remains **UNVERIFIED**, rather than being inferred from author receipts.

**Mappings:** all twenty were individually checked; **correctness CLEAN, scoped coverage CLEAN, comprehensibility CLEAN**. Source row identities and selected one-based senses match the table. The blank source spellings, 瓶詰 identity, and 殖える→増える reuse are preserved. Additional recognition was assessed separately, without assigning N2 independently to every recognition sense. Required primary Han metadata and substantive existing component links are present; missing 箋/殖/及/拭/膨/潔 cards were not invented.

## Findings:

**N273-01 — Medium; correctness — `words\瓶詰.md:49–50`**

The instruction “Learn the long vowel and voiced ending” incorrectly teaches vowel length in **びんづめ**. Its morae are **び・ん・づ・め**; ん is a nasal mora, not a long vowel. This can induce a wrong pronunciation despite the correctly written reading.

**Minimal remedy:** remove “long vowel and,” retaining the useful **びんづめ, not びんつめ** guidance.

**Exact evidence:** article lines 49–50; unrestricted reading びんづめ in complete principal family `1491130`; applicable frozen Daijisen heading びん‐づめ.

**Confidence:** high.

**N273-02 — Medium; scoped coverage — `words\深まる.md:4–9`**

The displayed **“deepen; intensify”** label is defensible for ordinary meanings of **進む, 強化 and 加わる**, but none has a direct exclusion with 深まる. Existing guards through 増す or other neighbors do not protect these pairs.

**Minimal remedy:** add `[進む, 強化, 加わる]` to 深まる’s existing exclusions; reverse declarations are unnecessary.

**Exact evidence:** complete family `1365980`, s4 explicitly includes *intensify* and *deepen*, without a rare/archaic restriction; `1236200`, s1 includes *intensifying*, corroborated by `words\強化.md:16`; `1189980`, s3 covers increasing heat/degree, with **暑さが加わる — “the heat intensifies”** explicitly taught at `words\加わる.md:21–23`. Complete older bodies and both endpoints’ declarations were read.

**Confidence:** high. The noun/する construction of 強化 does not eliminate this displayed-label overlap.

**N273-03 — Medium; scoped coverage — `words\膨らます.md:4–9`; `words\膨らむ.md:4–9`**

The **“expand”** half of both new titles remains a reasonable answer for **広がる, 広げる and 広める** in their extent/enlargement senses. Neither new article nor those older endpoints declares the required direct pairs. Guards involving 拡大 or another expansion word are nontransitive.

**Minimal remedy:** add `[広がる, 広げる, 広める]` to **each** new article’s exclusions: six direct pairs, not a blanket expansion-category clique.

**Exact evidence:** complete family `1602370`, s1 explicitly includes *expand*; `1278460`, s2 includes *broaden, extend, widen, enlarge*. Actual older teaching supplies **範囲が広がる / 範囲を広げる**, “the range expands / expand the range,” at `words\広げる.md:36–38`, and knowledge broadening at `words\広める.md:16–23`. `words\広がる.md:15–32` covers wider reach and abstract expansion. All three complete older bodies and complete applicable families were read. This is a quiz-label safeguard, not a claim that balloon, knowledge and range constructions freely substitute.

**Confidence:** high.

**N273-04 — Medium; scoped coverage — `words\普及.md:4–9`**

The broad **“spread”** label also fits ordinary spreading senses of **拡大, 展開 and 流行る**, but the direct exclusions are absent. In particular, protecting 普及/流行 and 流行/流行る does not protect 普及/流行る.

**Minimal remedy:** add `[拡大, 展開, 流行る]` to 普及’s exclusions.

**Exact evidence:** complete family `1205200`, s3 explicitly includes *spread*, with **被害が拡大する**, “damage spreads,” taught at `words\拡大.md:38`; complete family `1440600`, s2 includes *spreading out*, corroborated by `words\展開.md:16`. The complete 流行る article teaches disease prevalence at lines 16–21; the applicable [精選版 日本国語大辞典 entry](https://kotobank.jp/word/%E6%B5%81%E8%A1%8C%E3%82%8B-604763), sense ③, independently records spreading through society. Both endpoints’ declarations were checked.

**Confidence:** high for the unguarded spreading overlap; these are not claims of unrestricted Japanese synonymy.

Existing exclusions were also assessed for excess independently of these omissions. **No actionable excess was established** from the complete bodies read. Homophony, category membership and neighboring exclusion cliques were not treated as sufficient evidence.

## Optional:

None.

## Limits:

Git provenance, hash/equivalence verification and byte-for-byte baseline preservation were **not independently executed**. The supplied receipts remain author-executed evidence.

Not every navigation-label article was read completely; no absence claim rests on those unread bodies. The initial live Weblio 流行る extraction returned an encyclopedia article about 流行, and its raw response was not fully inspected; neither was counted as applicable dictionary verification. The usable live corroboration was the explicitly identified **精選版 日本国語大辞典** body on Kotobank, not the empty Digital Daijisen section there.

This review does not establish corpus frequency, independently date historical derivations, certify every sentence with native-speaker testing, or prove whole-repository quiz uniqueness. CLEAN verdicts are limited to the actual linguistic and structural evidence described above.
