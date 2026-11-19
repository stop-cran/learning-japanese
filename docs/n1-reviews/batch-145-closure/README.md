# Batch 145: textual-review closure

The fifteen cards are textually review-closed. Both final confirmations are
**CONFIRMED**, with no remaining finding. Publication is **pending** at this
closure commit; the later receipt establishes the remote commit, CI and served
ZIP. No JVM, native, device or phone acceptance is implied.

## Snapshot and scope

- Members: **湧 源 滅 滑 滞 漫 漬 潔 潜 澄 濁 瀬 災 炎 為**
  (source rows 636, 637, 639, 642, 644, 649, 650, 653, 654, 658, 661, 663,
  664, 667, 668).
- Published base: `305763eab81430f26c51446ed0532cc03910ffbb`.
- Blind-review freeze: `845aefbb37e40aeb737f32de8066959968cc2cf6`.
- First fix: `e07ab3127d6ea3d9daa507b519fc993bd968f08c` (the cards 漫 漬 潜 濁
  瀬 災 炎 為, the existing card 暑, the existing word article 湧く and the
  generated `manifest.json`).
- Second fix: `97168e795cfc47698d2445ec1886be503494b415` (two lines of 為, the
  progress record and the manifest), the reviewed snapshot. 湧, 源, 滅, 滑, 滞,
  潔 and 澄 are unchanged from the freeze.
- `origin/main` did not move during the batch (still the B144 receipt
  `305763ea` at closure), so there is no merge and no integration proof.
- No front matter changed in any card; no title, tag, metadata reading,
  curated distractor, quiz exclusion or stroke file changed after the freeze.

The freeze adds fifteen cards and stroke files. Twenty existing word articles
each gain one link to a new card, and no word article is added. Three existing
texts change in one remark each: the 渋 card said 滞 had no card here and now
links 滞; the 暑 card said there was no card for 炎 to exclude and now links 炎
(the fix reworded it, see C2); and the 湧く article said neither 湧 nor 涌 had
a card and now says 湧 has one (added by the fix, see G1). The checkers
`kanji_remarks.py` and `n1_linkplan.py verify` confirm that these are the only
changes to existing texts besides the twenty links.

There were two confirmation rounds on the Claude side. The first Claude
confirmer (`confirm-claude-1`) reviewed `e07ab312` and found one new minor
point (the 為 paraphrase of Daijisen's fourth ため sense), so a second fix
commit `97168e79` was added on top of it (not an amend, because `e07ab312` had
been reviewed). A fresh Claude agent (`confirm-claude`) then confirmed
`97168e79`. GPT confirmed `97168e79` once, against the cumulative change from
the freeze. `confirm-packet/` holds three packets: the round-1 packet for
`e07ab312` (`claude`), the round-2 packet for `97168e79` (`claude2`) and the
GPT packet for `97168e79` (`gpt`); shared files are stored once in `common/`.

## Review execution

Two reviewer agents, one Claude and one GPT, worked independently. All five
runs ran one after the other (no two runs overlapped). The two initial runs
reviewed the same frozen packet (`packet/`) without seeing each other's work.
Each confirmation was run by a **fresh agent of the same model family**, not a
later turn of an earlier agent. It received a new packet with the author's
statement answering its family's latest report (`RESPONSE.md`), the list of
changes (`CHANGES.md`), the revised cards and the exact diff, and was allowed
to read the original packet and its own family's earlier reports, and never the
other family's reports. The revised cards are not stored again, because they
are the blobs at `97168e79` (and `e07ab312` for the round-1 packet). Models and
times come from the runtime session records, not from the reports.

| Run | Model | Snapshot | Window, 2026-11-19 UTC | API requests | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| initial-claude | claude-opus-5.5 | `845aefbb` | 12:32:46–12:44:22 | 69 | 68 | 1 | NEEDS FIX (C1 to C10, all minor) |
| initial-gpt | gpt-6.1-sol | `845aefbb` | 12:45:19–12:58:36 | 65 | 64 | 1 | NEEDS FIX (G1 to G6, all minor) |
| confirm-claude-1 | claude-opus-5.5 | `e07ab312` | 13:43:42–13:48:33 | 33 | 33 | 2 | NEEDS FIX (C10, the 為 part, and one new minor finding F1) |
| confirm-claude | claude-opus-5.5 | `97168e79` | 13:58:21–14:00:13 | 12 | 11 | 1 | CONFIRMED (two optional notes) |
| confirm-gpt | gpt-6.1-sol | `97168e79` | 14:00:27–14:07:28 | 41 | 40 | 1 | CONFIRMED (no finding; one optional polish note) |

`confirm-claude-1` confirms `initial-claude`; `confirm-claude` is the fresh
agent that confirms `confirm-claude-1`'s result; `confirm-gpt` confirms
`initial-gpt`. `reports/` holds the verbatim reports, `prompts/` the exact
prompts and `scope-audits/` each run's read-scope audit.
`provenance.json` hashes the files with the packets. Raw session logs stay
local because they may hold private context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| C1: 漫 lists すず where Daijisen prints すずろ | Claude, initial (minor); GPT, initial (G2) | Changed: 漫.md:46 says Daijisen also lists すずろ and そぞろ; the reading audits' `--extra` input had the same truncation and was corrected before the audits were rerun. Resolved by both |
| C2: 暑 says 炎 names fire rather than weather heat | Claude, initial (minor); GPT, initial (G5) | Changed: 暑.md:49 (the declared remark edit) says 炎 mainly names fire but in 炎天 and 炎暑 also means blazing heat, so the 炎 card keeps 暑 out of its meaning choices; 炎.md:57 says the 暑 card notes that 炎 mainly names fire. Resolved by both |
| C3: 浪漫 should be given as ロマン | Claude, initial (minor) | Changed: 漫.md:30 gives ロマン as a JMdict ateji spelling whose reading ろうまん is only a rarely used kana form (JMdict 1147940). Resolved |
| C4: 濁 implies ジョク is a table reading | Claude, initial (minor) | Changed: 濁.md:46 says the table does not list ジョク, KANJIDIC2 lists it and Kanjipedia marks it as outside the table. Resolved |
| C5: 為 "first sense" and "for the same doing" | Claude, initial (minor) | Changed: 為.md:23 says JMdict glosses it (2861111 has one sense); 為.md:25 no longer says "for the same doing". Resolved |
| C6: 為 never says the table gives no kun reading | Claude, initial (minor) | Changed: 為.md:44 says the table lists no kun reading for 為 and that な.す and the other kun readings are outside it. The suggested "usually written in kana" was not added because the packet does not cite it. Resolved |
| C7: 防災 gloss | Claude, initial (minor) | Changed: 災.md:25 quotes "protection against disaster" (JMdict 1520360). Resolved |
| C8: 漬物 headword | Claude, initial (minor) | Changed: 漬.md:41 names 漬物 (JMdict 1433700), with 漬け物 as another spelling and 漬けもの as "search-only kanji form". Resolved |
| C9: 原潜 gloss with the tag inside the quotes | Claude, initial (minor) | Changed: 潜.md:30 reads JMdict "nuclear submarine," tagged "abbreviation" (1262040). Resolved |
| C10: Daijisen paraphrases in double quotes (災, 為) | Claude, initial (minor) | Changed: 災.md:25 and 為.md:25 give the わざわい and ため descriptions as unquoted paraphrases. 災 resolved at the first confirmation; the 為 part found F1 |
| F1: 為.md:25 paraphrases Daijisen's fourth ため sense as "acting for someone" | Claude, first confirmation (minor, introduced by the fix) | Changed in the second fix: 為.md:25 says the sense is a relation to someone, as in Daijisen's example 私のためには叔父にあたる, meaning he is an uncle to me (unquoted; the English is the author's paraphrase). Both final confirmers checked it live against Weblio: resolved |
| G1: 湧く says neither character has a kanji card | GPT, initial (minor) | Changed: words/湧く.md:31–32 says 湧 has a card, the rare alternate 涌 has none and this word's kanji metadata lists only 湧 (declared word remark edit, checked by `n1_linkplan.py verify` and declared in the evidence `word-remarks.json`). Resolved |
| G3: 漫 "small ん" | GPT, initial (minor) | Changed: the clause is gone from 漫.md:44. Resolved |
| G4: 瀬 right-hand part | GPT, initial (minor) | Changed: 瀬.md:27 says the whole right-hand part is the kanji 頼 and keeps the modern-shape, not-etymology label; GPT checked it against the pinned KanjiVG decomposition. Resolved |
| G6: raw codes and checker wording in learner prose | GPT, initial (minor); Claude O2 and O3 | Changed: `spec1` is gone from 漫.md:44 and 漬.md:39, `stagk=漬ける` in 漬.md:23 is a plain restriction sentence, and 為.md:42 no longer mentions the reading checker. After the first confirmation 為.md:42 reads "な.る and な.す share the stem な; 為す uses な.す, so this card claims only what the linked word supports:" (Claude's optional wording). Resolved by both |
| O1: 炎 missing "and" | Claude, initial (optional) | Applied (炎.md:57). Resolved |
| O4: 瀬 年の瀬; O5: 漫 漫才 | Claude, initial (optional) | Not applied; extra examples, and coverage is complete without them. Declines accepted |
| O6: 滑 Kanjipedia wording; O7: 滞 Notes wording; O9: 瀬戸物 link wrap | Claude, initial (optional) | Not applied; accurate as written or following the one-link rule. Declines accepted |
| O8: 為 exclusions 業 and 理 | Claude, initial (optional) | No change; exclusions only remove options. Accepted |
| O-A (GPT): density of 潜, 濁 and 炎 | GPT, initial (optional) | Not applied; no sourced content may be dropped and no new defect was shown. Decline accepted; the final confirmation notes shorter paragraphs in 漬 and 為 as optional polish only |
| O-B (GPT): the conservative 滑–滞 and 為–幕 exclusions | GPT, initial (optional) | No change; they remove candidates and create no second correct answer. Accepted |
| O-C (GPT): keep the 為替, ぬめる and source-only treatment | GPT, initial (optional) | Kept. Resolved |
| O-P: the connective "so" in 為.md:42 | Claude, first confirmation (optional) | Applied with Claude's wording in the second fix. Resolved |
| O-Q: the 湧く remark edit listed under `kanjiCardEdits` in the progress record | Claude, first confirmation (optional) | Applied: it is listed under `otherArticleEdits`. Resolved |
| O-R: 暑 Metadata lacks 1177140 and 1177090 | Claude, first confirmation (optional) | Not applied: the 暑 change is a declared remark-only edit and `kanji_remarks.py` rejects any other change to an existing card, and the two ids are named in the remark itself. Decline accepted |
| Optional: no readings given for the 叔父 example (わたし, おじ) in 為.md:25 | Claude, second confirmation (optional) | Not applied; the Japanese phrase is quoted as Daijisen's own example and the English follows it. Recorded |
| Optional: the progress record said 29 meta-scan matches are part of a longer run; the rerun says 30 | Claude, second confirmation (optional) | Applied in the closure commit: the progress record now says 30 (the extra match is 叔父 in the 為 example) |
| Optional: shorter paragraphs in 漬 and 為 | GPT, final confirmation (optional) | Not applied; not a finding |

Claude raised all ten initial findings and nine optional points; GPT
independently raised the 暑 and 漫 すずろ points and alone raised the stale 湧く
remark, the 漫 "small ん", the 瀬 component and the reviewer-facing wording
of the 漫 and 為 cards (Claude's O2 and O3 touched the same wording from the
other side), and Claude's first confirmer alone found the 為 ため paraphrase. These are
contributions to this sample, not model rankings.

## Limits

- **Fresh confirmers.** Each confirmation ran as a new agent of the same model
  family, so it had no memory of its own earlier reading. The two Claude
  confirmers are different agents: `confirm-claude` did not see
  `confirm-claude-1`'s reasoning, only its report and the author's answer. The
  confirmations of the two families are independent of each other.
- **Execution.** Every run started after the previous one ended. Four runs had
  one tool call in flight at a time; the audit of `confirm-claude-1` shows one
  moment with two read-only `view` calls in flight, although its report says
  one call per response. No GPT report names the exact model; the runtime
  records gpt-6.1-sol. Four audits flag one recursive shell command inside the
  run's own packet; `confirm-gpt`'s audit reports one path outside the packet
  and report, a false positive from the `review-packets` folder used as a base
  path variable in its shell commands (the paths it then read were its own
  packets and report). All five reports equal the runs' final messages.
- **Scope audits.** The audit script does not attribute reads made through
  shell commands or Python, so it lists cards and other files as unread that the
  reports say were read. The second Claude confirmation covered only the two
  changed lines, and the GPT confirmation the cumulative change; neither
  re-read the unchanged cards or any word article beyond 湧く.
- **Reviewers' own limits.** Neither reviewer ran a JVM or Android build or
  could certify the pool construction beyond the supplied audits; the first
  Claude confirmer took the 瀬 component from its own knowledge (GPT later
  checked it against KanjiVG), checked Joyo claims against the packet extract
  (GPT later checked the official PDF pages) and took the JMdict claims from
  the pinned XML, not the online dictionary.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. At `97168e79` they report 0
  production, 0 padded-session and 0 one-holder hits and ten latent
  collisions: 滅 べつ (別); 滑 かり (権, a KANJIDIC2 name reading); 漫 ばん (万
  判 晩 板 満 番 盤); 澄 すみ (墨 炭 隅) and み (三 実 巳 御 深 身); 瀬 せい (背);
  炎 ぬく (抜 温) and もえる (燃); 為 す (州 巣) and た (手 田). The older
  reading-options check still labels 滅 べつ and 漫 ばん as HITs and reports
  "2 problem(s)" (exit 1), because it ignores filled slots; the curated
  distractors 海 水 火 and 海 水 日 are Starter cards that fill every slot, so
  they cannot be drawn, and the exposure audit is authoritative (the same
  precedent as batches 135, 138 and 139 to 144). The first gate runs showed べつ
  of 滅 offered by 別 and one-holder padded hits for 滅, 漫, 為 and a name-only
  hit for 澄, because the original distractors were not Starter cards; they
  were replaced before review. No quiz-option or reading-exposure line changed
  between the freeze and the fixes apart from the command lines. Sampled seeds
  are not exhaustive.
- **Source-only readings.** Some readings rest on a single dictionary entry or
  a Kanjipedia-only entry and are labelled as source-only on the cards where
  they appear, for example 滅 ベツ (Kanjipedia only, shared with 別) and 濁
  ジョク (KANJIDIC2 and Kanjipedia, not in the table). Readings with no
  declaring word article are listed and illustrated but not quizzed.
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** No published commit is rewritten. The freeze and
  both fix commits remain in the history; the reports of both Claude
  confirmers are kept.

## Validation and accounting

At the reviewed snapshot `97168e79`: 439 host tests pass; validation 0 errors;
lint 0 errors and 5 warnings, all on untouched, wrapped Dictionary lines (不潔,
湧く, 潜る, 澄む and 蒸し暑い, the last linted only because the modified 暑 card
declares it); quiz safety 0/0; manifest rebuild unchanged (version
`de1d575cfb20ec49`); vocabulary 3201/3336; link plan 20 links and 1 declared
word remark edit, 0 problems; kanji remarks 15 of 15 present, 渋 and 暑 the
only modified cards, 0 problems; budget 9,140 entries, 51,778,814 retained,
52,137,905 inflated and 32,403,210 local-ZIP bytes; the Metadata scan finds no
whole-run gap.

After publication, delivery becomes **437/1,228**, with **791 remaining**.
Until the receipt it stays 422/1,228.
