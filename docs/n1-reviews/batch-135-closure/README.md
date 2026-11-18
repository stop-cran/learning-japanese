# Batch 135: textual-review closure

The fifteen cards are textually review-closed. Both final confirmations are
**CONFIRMED**, with four CLEAN facets and no remaining finding. Publication is
**pending** at this closure commit; the later receipt establishes the remote
commit, CI and served ZIP. No JVM, native, device or phone acceptance is implied.

## Snapshot and scope

- Members: **博 厳 及 姿 履 巡 弾 彫 恵 憶 我 揚 救 暇 模**
  (source rows 129, 136, 138, 229, 278, 296, 331, 336, 363, 395, 401, 446,
  469, 506, 577).
- Published base: `afed6694957e850d516c754f034044e801cc30a4`.
- Blind-review freeze: `163b384e6cb8f75c06fe395f7b144cdd8b105673`.
- Fix 1: `2ef25d33` (博 履 巡 弾 恵 憶 揚 救 模).
- Fix 2: `fb236071b6355b28423581c96a35a8ca1084a193` (履 巡 彫 救), the reviewed snapshot.

The freeze adds fifteen cards and stroke files. Thirty-two existing word articles
each gain one link to a new card; no other article text changes and no word
article is added. Both fixes change only the named cards and `manifest.json`.

## Review execution

Two reviewer agents, one Claude and one GPT, ran one at a time, Claude before
GPT. Both initial runs reviewed the same frozen packet (`packet/`) without seeing
each other's work. Each confirmation was a later turn of the same agent. It
received a new packet (`confirm-packet/`) with the author's statement answering
its own previous report (`RESPONSE.md`), the revised cards and the exact diff,
and never the other family's reports. Models and times come from the runtime
session records, not from the reports.

| Run | Model | Snapshot | Window, 2026-11-17 UTC | API requests | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| initial-claude | claude-opus-5.5 | `163b384e` | 20:36:50–20:49:07 | 72 | 71 | 1 | NEEDS FIX (minor) |
| initial-gpt | gpt-6.1-sol | `163b384e` | 20:50:53–21:09:31 | 76 | 75 | 1 | NEEDS FIX |
| confirm-claude | claude-opus-5.5 | `2ef25d33` | 22:16:57–22:21:34 | 34 | 34 | 2 | CONFIRMED |
| confirm-gpt | gpt-6.1-sol | `2ef25d33` | 22:24:08–22:43:00 | 59 | 58 | 1 | NEEDS FIX (G5) |
| confirm2-claude | claude-opus-5.5 | `fb236071` | 23:28:26–23:31:17 | 17 | 16 | 1 | CONFIRMED |
| confirm2-gpt | gpt-6.1-sol | `fb236071` | 23:33:09–23:40:13 | 40 | 39 | 1 | CONFIRMED |

`reports/` holds the verbatim reports, `prompts/` the exact prompts and
`scope-audits/` each run's read-scope audit. `provenance.json` hashes them with
the packets. Raw session logs stay local because they may hold private context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| C1 / G3: 博 mnemonic added a dot that 甫 already has | both, initial | Changed (`2ef25d33`) |
| C2: 憶 misdescribed 臆測 against the Joyo table | Claude, initial | Changed: 臆 Joyo row and JMdict 1182790 added |
| G1 (major): 救 could offer グ as a wrong answer to キュウ | GPT, initial | Changed: distractors `[敬, 球, 教]` |
| G2 (major): 巡's fallback could offer まわる to めぐる | GPT, initial | Changed: curated providers fill every slot |
| G4 / O4 / OA: dense sense paragraphs | both, initial | 弾 changed to bullets; 博 厳 履 恵 我 揚 模 kept |
| GR: add a regression test for G1–G2 | GPT, initial | Declined: no reading-quiz builder in this repository and no JDK; the exposure audit is the check |
| O1, O2, OB: wording of 履, 模, 巡 恵 揚 | initial | Changed |
| OC: add Kanjipedia outside-table readings to the audits | GPT, initial | Changed: passed with `--extra` |
| O3, O5: weaker exclusions; 及 look-alikes | Claude, initial | Declined with reasons |
| CO1: 巡's kun question always offered かわ, みち, -たち | Claude, confirm | Changed: `[川, 道, 見]` |
| CO2, CO3: 履 wording; card text described quiz output | Claude, confirm | Changed |
| G5 (major): 彫 could offer える in a padded Starter session | GPT, confirm | Changed: `[円, 高, 見]` plus a sourced える/えり note |
| Claude confirm2 Optional 1–2: cite JMdict 1427950 on 彫:41; the -だか option | Claude, confirm2 | Not applied; the text is correct and -だか is one possible option |

Both families found the 博 defect. Claude also found the 憶 source defect and
most wording points; GPT found all three quiz-reachability defects (G1, G2, G5),
each from an attested reading the supplied audits did not yet include. These are
contributions to this sample, not model rankings.

## Limits

- **Execution.** confirm-claude had two `view` calls in flight once (on ranges of
  `fix.patch`), which it disclosed itself; every other run was strictly serial.
  confirm2-gpt's single "outside path" flag is the review-packet root, used as a
  base variable in its scripts, which opened only allowed folders. The audits'
  packet coverage undercounts reads made through shell or Python; the author
  checked such scope claims against the session events.
- **Partial confirmation reads.** confirm2-claude read only the 巡, 弾 and 彫
  blocks of the exposure audit and relied on the summary lines for the rest.
  Neither the author nor a reviewer searched Daijisen for ▽ headwords of the 14
  kanji other than 彫.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder. At `fb236071` they report 0 production, 0 padded-session and
  0 one-holder hits, and 26 latent collisions. Three one-holder cases are
  KANJIDIC2 name-only readings (恵 へい, 恵 み, 我 か), disclosed, not fixed.
  `reading-options.txt` still labels 巡–まわる a hit because that older check
  ignores filled slots; GPT verified from the builder that it cannot be drawn.
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- Reviewers also read public web pages, such as Kanjipedia, jisho.org and the
  Joyo PDF; their reports list those reads.

## Validation and accounting

At `fb236071`: 436 host tests pass; validation 0 errors; lint 0 errors and 7
warnings, all on untouched Dictionary lines of existing word articles; quiz
safety 0/0; manifest rebuild unchanged; vocabulary 3201/3336; budget 8,838
entries, 50,502,721 retained and 31,780,725 local-ZIP bytes. `origin/main` is
still `afed6694`, an ancestor, so no integration merge is needed.

After publication, delivery becomes **287/1,228**, with **941 remaining**.
Until the receipt it stays 272/1,228.
