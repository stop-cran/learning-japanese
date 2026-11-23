# Batch 150: textual-review closure

The fifteen cards are textually review-closed. Both families' last
confirmations of the reviewed snapshot are **CONFIRMED**, with no remaining
finding. `origin/main` had not moved from the published base when the review
closed, so publication is a fast-forward and no integration merge is needed.
Publication is **pending** at this closure commit; the later receipt
establishes the remote commit, CI and served ZIP. No JVM, native, device or
phone acceptance is implied.

## Snapshot and scope

- Members: **葬 蒔 蓄 薦 虚 融 衆 街 衝 裁 裂 裸 覆 視 覧**
  (source rows 944, 946, 948, 954, 964, 974, 975, 976, 978, 984, 985, 988,
  994, 996, 997).
- Published base: `c6dbb52e3d64b0af6213aa6ee17eb37db10b6c93` (the B149 receipt).
- Blind-review freeze: `2dd9d46bca2aa4cc2b439d08c2ef36e6d9067a41`.
- Fix commit: `7e3c101b84848bd7a342cb1f44a421cd0f6f73e6`, the reviewed
  snapshot. It changes ten of the fifteen cards (蒔 薦 虚 融 街 衝 裁 裸 視 覧)
  and the derived `manifest.json`. 葬 蓄 衆 裂 覆, the fifteen stroke files and
  the eighteen word articles are unchanged from the freeze.
- After the freeze, six front-matter lists changed and nothing else in front
  matter. `quiz_exclusions`: 蒔 loses 苗, 裁 loses 布, 視 and 覧 lose 捜, 街
  gains 径 and 衝 gains 攻. No title, tag, metadata reading, quizzed reading,
  distractor or stroke file changed.

The batch adds fifteen cards and stroke files. Eighteen existing word
articles each gain one link to a new card (葬式, 蒔く, 蓄える, 推薦, 謙虚,
金融, 公衆, 街角, 衝突, 裁判, 裁縫, 裂く, 裸, 覆う, 無視, 重視, 展覧会 and
御覧), and no other line of them changes. No word article is added and no
existing kanji card changes. `n1_linkplan.py verify --remarks` and the
author's `kanji_remarks.py` confirm that these are the only changes to
existing texts.

Before the freeze, the author checked the quoted glosses and Japanese phrases
against their sources and every mnemonic against its KanjiVG tree. The reason
for excluding 仰 from 覧 lost an unverifiable "revere"; the 裁 mnemonic was
reworded to follow KanjiVG; 薦's こも row takes the existing label "kun,
outside the official table"; 裂's distractors became 縫 編 畳, because the
quiz-safety check found the earlier choice 縫 excluded from both 結 and 織; and
exclusions were added on ten cards (街 区 丁; 衆 団 組 公; 裁 定 絶 布; 衝 争
戦; 虚 穴; 蒔 苗; 覆 殻; 視 and 覧 捜; 裂 断 絶). The exclusions 蒔 苗, 裁 布
and 捜 on 視 and 覧 were removed again after the review (G1, G2).

## Review execution

Two reviewer agents, one Claude and one GPT, worked independently. All four
runs ran one after the other (no two runs overlapped). The two initial runs
reviewed the same frozen packet (`packet/`) without seeing each other's work.
Each confirmation was run by a **fresh agent of the same model family**, not a
later turn of an earlier agent. It received a new packet with the author's
statement answering its family's report (`RESPONSE.md`), the list of changes
(`CHANGES.md`), the revised cards and the exact diff, and was allowed to read
the original packet and its own family's initial report, and never the other
family's report. Models and times come from the runtime session records, not
from the reports.

| Run | Model | Snapshot | Window, 2026-11-20 UTC | API requests | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| initial-claude | claude-opus-5.5 | `2dd9d46b` | 13:17:17-13:31:06 | 93 | 92 | 1 | Cards CLEAN on all four facets; one minor finding on audit evidence (C1) |
| initial-gpt | gpt-6.1-sol | `2dd9d46b` | 13:31:56-13:47:35 | 67 | 66 | 1 | NEEDS FIX (G1, G2) |
| confirm-claude | claude-opus-5.5 | `7e3c101b` | 13:58:36-14:03:05 | 40 | 39 | 1 | CONFIRMED |
| confirm-gpt | gpt-6.1-sol | `7e3c101b` | 14:03:26-14:09:29 | 44 | 43 | 1 | CONFIRMED |

Both families confirmed the same final commit `7e3c101b`, which was written
before either confirmation started. `confirm-packet/` holds the two packets
(`c1claude`, `c1gpt`; shared files are stored once in `common/`). `reports/`
holds the verbatim reports, `prompts/` the exact prompts and `scope-audits/`
each run's read-scope audit. `provenance.json` hashes the files with the
packets. Raw session logs stay local because they may hold private context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| G1: 蒔 excludes 苗 because a "seedling" overlaps "seeds", and 裁 excludes 布 because "cloth" occurs in "cut out cloth"; neither is a real overlap | GPT | Changed in 7e3c101b: both exclusions and their bullets removed; 蒔's separately sourced replanting sense kept. Resolved |
| G2: 視 and 覧 exclude 捜, whose "look for" is searching, not looking at or over | GPT | Changed in 7e3c101b: 捜 removed from both cards; the 仰 bullets restated without relying on the shared word "look". Resolved |
| C1: the reading audits label extra readings passed with `--extra` as "card text" | Claude | Changed in the audit tooling, outside the repository: the label now reads "--extra list", and the second line of each audit names the sources of the extras. Counts unchanged. Resolved |
| O1: 虚 quotes 邪心をもたない for both sources | Claude | Applied: Kanjipedia 邪心をもたない and Digital Daijisen 邪心を持たない, each attributed |
| O2: 薦 puts JMdict's "[see also: 推奨]" in gloss quotes and repunctuates Kanjipedia's mat sense | Claude | Applied: "has a see-also cross-reference to 推奨"; Kanjipedia's こも。敷物。しとね。 in its own punctuation |
| O3 and O4: 街/径 and 衝/攻 not excluded | Claude | Applied: 街 excludes 径 (JMdict 1454080 spells みち 道, 途, 路 or 径) and 衝 excludes 攻 (JMdict 1456890, 衝く "to attack") |
| O10: the 融 and 覧 mnemonics name 鬲 and 𠂉 without describing them | Claude | Applied as shape descriptions only, checked against KanjiVG; no meaning is given, since it would read as etymology |
| O11: the 裸 image mixes clothing and a fruit | Claude | Applied: one image, a fruit whose clothing, its peel, is stripped away |
| O5 (覆/転), O6 (葬/墓), O7 to O9 (衝撃, 衝動, 衝立, 虚偽, 空虚, 一覧 and 破裂 as further words), O12 (normalise the okurigana-scan parses) | Claude | Not applied: 転's title names neither covering nor overturning; a grave is a place; further words would add new sourced claims to a revision whose coverage both reviews judged clean; the scan is mechanical evidence, now labelled. Accepted in the confirmation |
| GO1 (shorten repeated qualifications and mnemonic disclaimers), GO2 (explain Joyo and transitive locally), GO3 (a 虚偽 example) | GPT | Not applied: GO1 and GO2 for consistency with the existing N1 cards, GO3 as for O7 to O9. Accepted in the confirmation |
| Confirmation optional: split the 覧 line 25 mnemonic sentence so that "one more horizontal stroke below it" cannot be read as attached to 臣; the 仰 reasons on 視 and 覧 rest on reasoning, not a source | Claude | Not applied; editorial, recorded here. The reviewer judged reasoning acceptable for a title-to-title overlap |
| GPT confirmation | GPT | No finding and no optional item |

## Limits

- **Fresh confirmers.** Each confirmation ran as a new agent of the same model
  family and had no memory of its own earlier reading. The confirmations of
  the two families are independent of each other.
- **Execution.** Every run started after the previous one ended, and no run
  had more than one tool call in flight. The `initial-gpt` audit flags one
  "recursive shell command over packet directories". This is a false
  positive: the audit's pattern matches `**`, and the matched command
  (13:39:48) used `**` as Python exponentiation to sample Bézier curves of
  the stroke files; no recursive listing ran. The `confirm-gpt` audit flags
  one path outside the packet and report: the parent `review-packets` folder,
  used only as a base variable to build paths into the packet, the
  confirmation packet and the `initial-gpt` report.
- **Prompts.** Every prompt was saved to a file before use.
- **Scope audits.** The audit script does not attribute reads made through
  shell commands or Python, so it lists files as unread that the reports say
  were read: the 15 stroke files in the `initial-claude` audit (parsed in
  Python), all fifteen cards, stroke files and word articles in the
  `initial-gpt` audit (read in `Get-Content` loops and parsed in Python),
  and all fifteen cards in the `confirm-gpt` audit,
  whose report says it read the ten changed cards in full. The confirmations
  read the changed lines and the cumulative change, and could read the
  original packet and their own family's initial report; `confirm-claude`
  did not open the five unchanged cards.
- **Dictionary text.** Several judgments rest partly on live reads of Digital
  Daijisen, Kanjipedia and Jisho pages, not on pinned copies in the packet.
  `initial-claude` checked JMdict through the packet extracts and its own
  knowledge of the public entries.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. At `7e3c101b` they report 0
  production, 0 padded-session and 0 one-holder hits for an ordinary reading
  and four latent collisions, readings that other cards offer but no audited
  pool can draw, all KANJIDIC2 name readings: 蒔 まい (参 舞), 蒔 まき (巻),
  街 また (復) and 視 み (味 未 美 魅). 街 また can be offered by 復 only in a
  Starter practice session that also borrows 復; in the N1 and All pools 街's
  three curated options 橋 庭 池 fill every wrong slot. The older
  reading-options check lists 街 また for information and reports 0 problems.
  Sampled seeds are not exhaustive, and the claim covers the documented
  shipped pool configurations only.
- **Quizzed readings.** Readings with no declaring word article are listed and
  illustrated but not quizzed. Nine cards quiz only their on reading (葬 ソウ,
  薦 セン, 虚 キョ, 融 ユウ, 衆 シュウ, 衝 ショウ, 裁 サイ, 視 シ, 覧 ラン) and six
  only their kun reading (蒔 ま.く, 蓄 たくわ.える, 街 まち, 裂 さ.く, 裸 はだか,
  覆 おお.う).
- **Source-only readings.** Some readings rest on a single dictionary entry or
  a Kanjipedia-only entry and are labelled as such on the cards.
- **Metadata ids.** Four words named on the cards have no JMdict id on the
  Metadata line, because they are cited from the Joyo table, Kanjipedia or
  Digital Daijisen (蓄え, 敷物, じっと見る and 難読); the cards make no JMdict
  claim about them (listed in the ledger).
- **Lint warnings.** Four Dictionary-line warnings on the existing word
  articles 公衆, 葬式, 蓄える and 街角 (no JMdict entry id) are older than the
  batch and out of scope.
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** No published commit is rewritten. The freeze and
  the fix commit remain in the history, and every report is kept.

## Validation and accounting

At the reviewed snapshot `7e3c101b`: 439 host tests pass; validation 0 errors;
lint 0 errors and 4 warnings (above); quiz safety 0/0; reading options 0
problems; manifest rebuild unchanged (version `281edb7d3213283e`, 9,579 files,
SHA-256 `D39FA9702BCDD91099F2CCF247825E0423F6B311F8AF53F3FBFECB2B50F23C68`);
budget 9,602 entries, 55,947,534 retained, 56,306,830 inflated and
36,026,242 local-ZIP bytes; vocabulary 3201/3539; link plan 18 links, 0
remark edits, 0 problems; kanji remarks 15 of 15 present, no existing card
modified.

After publication, delivery becomes **512/1,228**, with **716 remaining**.
Until the receipt it stays 497/1,228.
