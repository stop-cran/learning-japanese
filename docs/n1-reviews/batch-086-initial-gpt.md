## Snapshot

`f59c65fde644ed36958d74495da59a66c1d82570`, identified by the packet as the signed teaching snapshot; signature and Git state were **not independently verified**.

Reviewer: **GPT-6.1 Sol**, model ID `gpt-6.1-sol`. Independent initial read-only review; no edits, delegation, other reports or author adjudication.

## Scope

Read the entire returned `C:\Users\stop-\n1-kanji-workspace\control\batch-086-initial-packet.txt` using one `view` call with `forceReadLargeFiles=true`, without ranges or parallel calls. No truncation was indicated. The stated **215,474 bytes / 4,300 lines** are supplied counts, not independently measured.

Reviewed both complete new articles, all six exact reused diffs, and the supplied comparison passages. Inspected **71 distinct complete JMdict families**—49 primary, 12 comparison and 10 draft-comparison families—including restrictions, spelling/reading flags, sense qualifications and priority fields; **seven raw character records**; supplied public-dictionary extractions; and the included metadata, format and compatibility evidence. This was not a fresh full-baseline review.

## Verdicts

**CLEAN** means no established actionable defect within this bounded review, not exhaustive correctness.

| New article | Correctness | Scoped coverage | Phone-text comprehensibility |
|---|---|---|---|
| `kanji\凡.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\凡例.md` | **CLEAN** | **CLEAN** | **CLEAN** |

| Reused article—exact diff only | Correctness | Scoped coverage | Text comprehensibility |
|---|---|---|---|
| `words\平凡.md`:25—凡 navigation link | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\およそ.md`:25—凡そ navigation link | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\全て.md`:27–28—rare 凡て recognition alias | **CLEAN** | **CLEAN** | **CLEAN** |
| `kanji\平.md`:43—平凡 bullet | **CLEAN** | **CLEAN** | **CLEAN** |
| `kanji\例.md`:38—凡例 bullet | **CLEAN** | **CLEAN** | **CLEAN** |
| `kanji\全.md`:39—existing 全て made a link | **CLEAN** | **CLEAN** | **CLEAN** |

**Meaning and constructions.** `words\凡例.md`:15–24 correctly teaches dictionary/book usage conventions and map/diagram legends, not legendary stories. Both complete examples are natural neutral-polite constructions, with matching kana and English: reading the dictionary’s usage notes, and checking symbol meanings through the map legend. Lines 28–32 appropriately associate 例 with conventions/established usage rather than exclusively an individual example. Lines 36–51 distinguish broader 説明/解説, passage-level 注, introductions and personal memos without asserting absolute semantic compartments. はんれい, the warning against ぼんれい, and the distinction from 判例 agree with the supplied evidence.

**Readings and character claims.** `kanji\凡.md`:9–12,35–44 preserves all five source entries and their order: ボン, ハン; およ.そ, おうよ.そ, すべ.て. The two exact selected on-strings each have their own linked example. JMdict verifies the whole words; supplied Daijisen allocates ボン to 平凡 and ハン to 凡例. Explicit `quizKunyomi: []` excludes all native-reading questions on compatible clients while retaining metadata.

The unusual おうよ.そ remains explicitly source-only; its modern lexical use is **UNVERIFIED**, not silently normalized or claimed impossible. JMdict 1523450 supports 凡そ／およそ with usually-kana qualifications. Entry 1595730 supports exact 凡て／すべて as a **rare kanji spelling**, without a conflicting reading or sense restriction. Neither establishes rare pronunciation. Existing stable articles are reused without new identities or inferred vocabulary levels.

The three strokes and radical 几/no. 16 match the raw record and supplied stroke text. The modern-shape mnemonic is clearly not historical derivation. N1 is labelled a community classification; omission of `phonetic` is not presented as denying a phonetic component.

**Quiz safety.** The actual wrong labels are **丸 “round; circle,” 九 “nine,” 凹 “concave; sunken.”** Checked against supplied ordinary secondary meanings as well as titles, none is a defensible displayed answer for 凡. 丸’s whole/full sense does not turn its displayed round/circle label into an equivalent answer. Three curated choices fill the default four-choice question without random supplementation. Supplied affected legacy neighbors 常/般/全/毎/各/皆/総/平 likewise have three slots; this does not establish safety for larger or arbitrary live pools.

All eight direct word guards were checked against displayed titles and complete families: 注, 説明, 解説, メモ, 筆記, はじめに, 概論 and 鍵. Relevant overlaps include explanatory notes, 説明’s legend sense, resulting notes under 筆記, introductory remarks, and English “key.” These guards do **not** assert unrestricted substitution, and they are not transitive cliques. No additional necessary direct guard was established.

**Links and preservation.** All seven mapped reciprocal pairs are present in both directions:

`凡↔平凡`, `凡↔凡例`, `凡↔およそ`, `凡↔全て`, `平↔平凡`, `例↔凡例`, `全↔全て`.

This includes both recognition aliases, reused constituent cards and the newly activated baseline 凡/平凡 pair: **14 directions**. Exact diffs preserve stable identities, readings, easier existing levels—平凡 N2; およそ/全て N3—and original exclusions. No incidental backlink quota or baseline rewrite is warranted.

## Findings

**None established.** No proved defect or additional consequential hypothesis requires a remedy within scope. The expressly qualified source-only reading uncertainty is not an asserted modern-use claim.

## Optional

None.

## Limits

All dictionary and provenance evidence was supplied inside this one packet. Public-page text is coordinator extraction, **not independent upstream retrieval**; archive hashes, snapshot membership and signatures were not recomputed or independently authenticated.

Textual clarity does not establish native-speaker certification, rendered phone layout, native-font/system-fallback acceptance, drawing quality, route behavior or measured learning effectiveness. SVG/JSON inspection is textual evidence only. Compatible Android reading-curation/exclusion behavior is a supplied prerequisite; older clients can ignore those fields. No exhaustive N1/All/custom-pool, device or general-release safety claim is made.
