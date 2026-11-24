**Needs fixes before sign-off.** The packet supports the ten selected quiz readings and all 20 required reciprocal link pairs. I found eight missing direct meaning-quiz exclusions and several learner-facing distinctions that need correction.

**Snapshot:** `cbf5c2c5ca52758812aff3e61ae421e72fadd9e7`, based on `ac5304bac6a9352c7e6d98526e932875e6445edf`. Packet only; no uncommitted changes were identified in it, and worktree status was not verified.

**Scope:** One blind reviewer, GPT-6.2 Sol. Read all ten new kanji cards, ten new word cards, ten existing-kanji diffs, and six older comparison articles in full as supplied. Checked `primary.xml`, `sources.json`, all seven `families-*.jsonl` files, `quiz.txt`, and `labels.txt` against the rubric. The older articles were reviewed only for the supplied comparison or changed passage.

**Verdicts:** Each triplet is **correctness / scoped coverage / comprehensibility**. **C** = CLEAN, **F** = NEEDS FIX, **U** = UNVERIFIED. Quiz correctness here means the supplied static evidence, not observed runtime behavior.

| Kanji card | Verdict | Word card | Verdict |
|---|---|---|---|
| 廷 | C/C/C | 法廷 | C/C/C |
| 弊 | C/C/C | 弊害 | F/C/C |
| 弓 | C/C/C | 弓 | C/C/C |
| 弔 | F/C/C | 弔問 | C/C/C |
| 弥 | F/U/C | 弥縫策 | C/C/C |
| 弦 | C/F/C | 弦楽 | F/C/F |
| 彩 | C/C/C | 色彩 | C/C/C |
| 彰 | F/C/C | 表彰 | C/C/C |
| 征 | F/C/C | 征服 | C/C/C |
| 忌 | F/C/C | 回忌 | C/F/C |

**Existing cards:** 問, 回, 害, 服, 楽, 法, 策, 縫, 色, 表 — each C/C/C for the changed excerpt. 克服, 支配, 裁判, 対策, 葬式, 見舞い — each C/C/C in its comparison role.

**Findings**

| Severity / facet | Location | Evidence, impact, and exact remedy |
|---|---|---|
| Moderate / meaning-quiz correctness | `kanji\弔.md:14`, `kanji\忌.md:14`, `kanji\弥.md:14` | Add direct pairs **弔–忌, 弔–悔, 忌–悔, 忌–憎, 弥–継**. `labels.txt` displays *mourn/mourning* on the first three cards, *abhor* versus *hate; detest*, and *patch up* versus *patch*. The existing exclusions through 喪 or 修 do not protect these pairs. **High confidence** in the static gaps. |
| Moderate / meaning-quiz correctness | `kanji\彰.md:14`, `kanji\征.md:14`, `words\弊害.md:8` | Add **彰–賛** (*commend/praise*), **征–克** (*conquer/overcome*), and **弊害–毒** (*harmful influence*). The first two prompts leave the overlapping gloss unqualified; the figurative sense of 征服 and the 克服 comparison show why “conquer” is not reliably military-only. For 弊害–毒, 毒 displays the exact JMdict gloss *harmful influence* (1508270), and both currently exclude 害, not each other. **High confidence** for 弊害–毒; **medium** for the two kanji pairs. |
| Moderate / correctness and comprehensibility | `words\弦楽.md:26–30` | 管弦楽 is **orchestral music**, not the kanji name for the orchestra itself (`families-1.jsonl`, 1214130). Contrast **弦楽** “music for strings,” **管弦楽** “orchestral music,” and **オーケストラ** “orchestra, the ensemble.” Do not define an orchestra by requiring winds and percussion; in the concert example, gloss 弦楽四重奏 as “string quartet” without restricting it to the players. **High confidence** on the music/ensemble error. |
| Minor / correctness | `kanji\弥.md:36` | Keep 弥る as search-only, but replace the blanket “write 渡る.” JMdict 1444680 distinguishes **渡る** “cross” from the usually kana **わたる** “span/extend over,” the sense relevant to the card’s “far-reaching” gloss. Give both choices. **High confidence.** |
| Minor / scoped coverage | `kanji\弦.md:32` | Qualify the pot-handle example: “The same word つる can mean an arched pot handle, especially when written **鉉**.” JMdict 1578400 gives that spelling preference; it does not rule out 弦. **High confidence.** |
| Minor / scoped coverage | `words\回忌.md:14,21–31` | Present **一周忌** as the usual first-anniversary term and **一回忌（いっかいき）** as a recorded alternative, not equal production choices. Frame the numbered terms as Buddhist memorial usage without implying a service is held every year. Keep **三回忌 = second anniversary** and cite its actual JMdict entry, **1814080**, alongside 1199390; 1161330 explicitly says “usu. 一周忌.” **High confidence.** |

**Evidence and counts:** The packet contains **10 mapped source rows → 10 distinct new word articles**, with no baseline reuse in those mappings. I matched all **23 kanji metadata readings** to a reading-table row or qualified source-only explanation, and all **10 offered keys** (nine on, one kun) to the selected word readings. The ten mapped words require **20 reciprocal kanji–word pairs**; both relative link directions and the full backlink reading are present for every pair. I counted **98 family records**, **38 declared kanji exclusions**, and **16 declared word exclusions**. I did not infer pairs transitively. In particular, the displayed qualifiers already distinguish 弓 from a bow of respect and 法廷 from a sports court.

**Optional:** In `words\弦楽.md:30`, call 絃楽 an **alternate spelling** rather than an **older spelling**; the packet attests the variant, not its chronology. In `kanji\表.md`, consolidate the two adjacent JMdict lists without losing 1489670.

**Limits:** `sources.json` records the author’s Daijisen heading checks for all ten words and standard-use row checks for all ten kanji; it is not an independent copy of those pages. The local evidence supports **びほうさく** over irregular **びぼうさく** and its use for **ビ**. The exhaustive claim that no preferred tagged 弥 candidate qualifies remains unverified: the packet does not independently establish the full candidate inventory or all no-card claims. The reported zero drawable reading collisions, including the removals involving **ゆ** and **よ**, are author-side simulation results; actual option pools and any bare-kana **征服／制服** prompt were not verified. No external-page, native-speaker, device, whole-deck, or runtime-manifest verification was performed.
