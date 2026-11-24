**No actionable issues remain in the checked revision.** The five requested meaning-quiz exclusions are present, the 駐屯 label now matches its intransitive construction, and the revised text preserves the required navigation and reading keys. I withdraw my earlier claim that the normalized dictionary record dropped the intransitive tag.

**Snapshot and scope:** `f5a9c5e8c8ae139398910cec196754efe7c033ab` against the blind candidate `aca8b242dcad188c7927dac74e708cc668de6995`. Same reviewer: GPT-6.2 Sol. I read all five revision files and all five diff files in full, covering 15 revised cards. I checked `followup-facts.txt`, `correction-evidence.txt`, `correction-families.xml`, and the relevant original packet evidence. I checked unchanged link endpoints against the original packet, not a fresh full-deck read.

| Original finding | Confirmation |
|---|---|
| **上手い–上手** | **Resolved.** `words\上手い.md` has the direct exclusion and still distinguishes the *i*-adjective from the *na*-adjective. JMdict `1310460` and `1353320` support the shared skill meaning. |
| **崇–尚, 崇–貴, 巧–芸, 崇拝–憧れる** | **Resolved.** All four direct exclusions are in the revised card metadata and the audit. The revised comparisons explain the overlap without teaching the terms as interchangeable. |
| **駐屯 gloss and source tag** | **Gloss resolved; tag finding withdrawn.** `words\駐屯.md`, `kanji\屯.md`, and `kanji\駐.md` now use “being stationed (of troops).” Both the original `primary.xml` and `families-3.jsonl:9` already mark `1426940` intransitive. |
| **峡 and 峰 evidence** | **Card fixes resolved.** `kanji\峡.md` drops the unnecessary Daijisen claim and uses the supplied Kanjipedia record for はざま. `kanji\峰.md` names and links the exact ね【峰／嶺】 heading and drops the literary-example claim. The mountaintop sense and the unchanged 岬 lake-shore wording are supported by the author’s named-heading checks, not by my own page inspection. |

**Regression and counts:** The diff preserves all **17 required reciprocal pairs** and the separate **尾↔しっぽ** kanji comparison. The new `しっぽ` → word `尾` link completes a separate word-to-word pair. The **28 metadata readings** and **11 offered keys** are unchanged. The declared exclusion lists now total **30 kanji pairs** and **25 word pairs**, including the additional 屯–拾 guard. 崎 replaces 岸 with 岩 (“rock; boulder”), which does not duplicate “cape; promontory.” The new compound citations match the supplied dictionary families. The progress figures reconcile internally: **1,228 = 678 published + 550 undelivered**; **678 = 672 N1 + 6 N2**; **550 = 10 local drafts + 540 not started**. That is an arithmetic check, not publication verification.

**Optional:** Retain short Daijisen excerpts for 峰 and 岬 so future reviewers can check those senses directly from the packet.

**Limits:** No external page, native-speaker, device, or fresh whole-deck review. Symmetric exclusion handling and reading-option filtering are reported in the packet; I checked the static declarations and reading projection, not runtime behavior.
