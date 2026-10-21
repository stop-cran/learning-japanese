## Snapshot
`ae79da1aa5ea5b20c91d356f3490e1bababa46de`, clean committed files only. My tools cannot run Git, so I could not check the commit, the worktree status, or that this diff is the full change since `d9f323abaec692983e6ca2d31f419edb644974f5`. I relied on the author's authentication. Every added line in the diff matches the current file contents.

## Scope
**Model:** claude-opus-5.5 (claude family).

**Read in full:**
- The 59-line, four-hunk diff: two hunks in `城.md`, one in `姓.md`, one in `埋める.md`.
- The three revised files: `kanji\城.md`, `kanji\姓.md`, `words\埋める.md`.
- My initial report.
- The linked pages `words\記入.md` and `words\詰める.md`.

**Evidence checked:**
- `batch-05.json`: the 城 external source (lines 484-503) and the JMdict records 傾城 1249540, 名字/苗字 1604730, 姓 1375190 and 姓名 1375210.
- The relevant rules in `content-structure.instructions.md`.
- The live Kotobank page.

**Not covered:**
- The other 15 pages and the legacy passages, which keep their initial verdicts.
- Stroke files.
- The forbidden reports and authoring inputs, which I did not open.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji\城.md | CLEAN | CLEAN | CLEAN |
| kanji\姓.md | CLEAN | CLEAN | CLEAN |
| words\埋める.md | CLEAN | CLEAN | CLEAN |

## Findings
None of the changes introduces an actionable defect or a regression.

**城.md (lines 29, 39, 45)**
- The fetched Kotobank page shows the Nipponica heading 傾城（花魁、娼妓） けいせい, defined as an alternative name for 花魁 and 娼妓. It ends with 「明治以後はほとんど使われなくなった。」 That heading covers the courtesan sense, so limiting "historical" to that sense is accurate.
- The けいせん heading and the separate dance (kabuki) entry on the same page are not cited.
- セイ stays in the metadata and in the readings table.
- No JMdict rarity flag is claimed. The 傾城 record has news2/nf41 priority and no archaic label.
- The external link uses HTTPS, as the external-source rule requires.

**姓.md (line 39)**
- Entry 1604730 lists 苗字 and 名字 with the glosses "surname, family name, last name."
- Entry 1375210 姓名 is "(full) name; family name and given name."
- The note makes no claim about register or frequency, and it adds a kana reading for 姓名.

**埋める.md (lines 29-31)**
- 空欄に名前を記入してください is natural, and its kana and translation are correct.
- The に/を contrast is correct and matches example 3 (空欄を埋めてください, line 19), line 15, and the pattern in `記入.md`.

**My earlier observations:**
- B05-O-04 (unused citation 1604730) is resolved.
- B05-O-08 (abstract 記入 pattern) is resolved.
- B05-O-06 (register note on `words\姓.md`) was correctly not turned into an unsourced claim.
- B05-O-01, O-02, O-03, O-05 and O-07 concern unchanged passages and remain optional.

## Optional
- **R05-O-01** `城.md:39`: 明治以後 means "from Meiji onward." "From the Meiji period onward" would be more exact than "after the Meiji period." The packet claim on line 498 uses the same wording.
- **R05-O-02** `姓.md:39`: "名字 (also written 苗字), both みょうじ" would show that this is one word with two spellings.
- **R05-O-03** `埋める.md:31,37`: line 37's "the form-filling example" now has two candidates; "the 空欄を埋める example" would remove the ambiguity. "記入 is not a verb" could also be phrased with 記入する, since 記入 itself is a noun.

## Limits
- Without Git, I could not confirm the snapshot or the diff's provenance.
- I checked the Nipponica text only as rendered on Kotobank, not against the print edition.
- Whether the "beauty" sense of 傾城 is still current is unverified. The card makes no claim about it.
- Naturalness is my judgement, not native-speaker certification.
