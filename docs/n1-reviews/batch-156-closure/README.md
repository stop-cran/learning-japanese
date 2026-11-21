# Batch 156: textual-review closure

The ten cards and ten new word articles are textually review-closed.
Reviewers of three model families, Claude, GPT and Grok, reviewed the frozen
draft blind, and each family's last confirmation of the reviewed snapshot
`ba44b280` is **CONFIRMED**, with no remaining actionable finding (each
raised one optional point, recorded below). `origin/main` moved twice during
the review, and the batch was merged with it in two signed integration merges
(see "Integration with current main"). Publication is **pending** at this
closure commit, because main's own CI is red on a stale vocabulary review
outside the batch (`onoma-c7-nechinechi-criticism`); the later receipt records
the pushed commit, a green CI run on it and the served ZIP. No Android JVM
test, Kotlin cross-check, native, device or phone check was run.

## Snapshot and scope

- Members: **丹 乙 亜 仁 仙 伎 伏 伐 伯 伴** (source rows 7, 11, 16, 23, 24,
  30, 31, 32, 33, 34).
- Published base: `0638544ce1967ccec58ca7f9208c51ce8eaf4f8d`, the owner's
  commit after the B155 receipt.
- Blind-review freeze: `c6afa16315d5a88b5045eeb85d429b8f7fd90b1f`.
- Fix commits, in order:
  - `7eaf5c24612c3581e723d992453753ef49de932d` applies the initial findings
    (C1, G1-G3, X1) and the optional wording points marked "Changed" below;
  - `2c206d8f033110605971d4a5f2165aa20985868d` gives 乙, 伏, 伐 and 伴
    distractors from the domain of the card's meaning, replaces 仙's 父 and
    伎's 行 and 達 with other Starter cards (JMdict gives 父 the sense "God;
    Father", and the 達 card teaches "attain skill"; both are near the cards'
    own meanings), and changes two lines of the 甲乙 article;
  - `395f53643988ba24f444a376187c803aa6794654` cites KANJIDIC2's 甲 record
    in the 甲乙 article;
  - `3c5ef8450e38051682dab2bea5fce320b992e5ea` drops an unsourced
    contract-parties sense from the 甲乙 article;
  - `a7cc61e27261c62e84c3bd1f28e8a9254d9dcb04` adds the JMdict ids of six
    words named on the cards to the Metadata lines of 乙, 亜, 仁, 仙 and 伯
    (item A0 below);
  - `ba44b2809e6f46a6532ad58a016cb9d639ad2afc` replaces 甲乙 with 乙種 as
    the 乙 word (item A1 below). This is the reviewed snapshot.
- Merges: `e37ad00b796ed16dc752f5e60f0fd119f14dfa5e` (first parent
  `3c5ef845`, second `origin/main` at `9766dbd5`) and
  `eafee44b5129b283cd0e62d07303fd49d842204a` (first parent `a7cc61e2`,
  second `origin/main` at `0697b768`). `ba44b280` is one commit on top of the
  second merge (see "Integration with current main").
- After the freeze, card front matter changed only in six `distractors`
  lists (乙 箱 卵 鳩 → 王 硬 粗; 仙 麦 皿 筒 → 下 供 生; 伎 梅 蛇 炭 → 供 食 自;
  伏 糸 杯 象 → 起 座 伸; 伐 絹 鶏 缶 → 保 耕 育; 伴 塩 羊 墨 → 迎 離 他). The
  word article 仁 gained the quiz exclusions 人物, 個人, 芯 and 中心. The 乙
  word changed twice: the frozen article 乙 おつ was replaced by 甲乙 こうおつ
  in `7eaf5c24`, and 甲乙 by 乙種 おつしゅ in `ba44b280`. No kanji card's
  title, exclusion list, metadata reading, quizzed reading or stroke file
  changed.

The batch adds ten cards, ten stroke files and ten word articles: 丹念,
乙種, 亜熱帯, 仁, 仙人, 歌舞伎, 降伏, 伐採, 伯仲 and 同伴, one per kanji. Each
article's other kanji already have cards. Two existing files change in one
line each: `words/伯母さん.md:24` links the 伯 card, and the 潜 card's line
57 links 伏 in 潜伏 せんぷく, with a pointer to the compound-sound-changes
article for ぷく. `n1_linkplan.py verify --remarks` checks the links (one
added to an existing article, 0 problems), and the author's
`kanji_remarks.py` finds ten new cards and one changed existing card, 潜,
whose change is a remark only. Every card quizzes exactly one on reading, the
one its new article uses (丹 タン, 乙 オツ, 亜 ア, 仁 ジン, 仙 セン, 伎 キ,
伏 フク, 伐 バツ, 伯 ハク, 伴 ハン); every quizzed kun list is empty. 伯母さん
is a whole-word reading (jukujikun), so it supports no 伯 reading; 伯 selects
ハク through 伯仲.

Selection follows the proposal posted on
[issue 60](https://github.com/stop-cran/learning-japanese/issues/60#issuecomment-7058679348),
which governs the remaining rows from this batch on: one supporting word
article per kanji, Joyo rows first in source-row order, up to ten kanji per
batch. The ten members are the first ten remaining Joyo rows. The article's
word should have one of JMdict's common-word tags news1, ichi1, spec1 or
gai1; an untagged word needs a justification reviewed for its row, and the
word's other kanji must already have cards or join the batch. At the freeze
the author also counted news2 and spec2 as qualifying, so no row was flagged;
仙人 and 伯仲 carry only those two tags. The fix `7eaf5c24` then chose 甲乙 as
the 乙 word, which also carries only news2 and spec2, without checking its
other kanji 甲, which has no card and is not in the batch. Rechecked against
the list, seven words carry a listed tag (丹念, 亜熱帯, 仁, 歌舞伎, 降伏, 伐採,
同伴). No reviewer had raised either error. The author disclosed both to the
reviewers in the last confirmation round (`confirm4-claude`, `confirm3-gpt`
and `confirm2-grok`); those statements date both errors to the freeze,
although 甲乙 entered in `7eaf5c24`. In `ba44b280` and those statements the
author:

- replaced 甲乙 with 乙種 (JMdict 1862630, untagged). 乙 alone (JMdict
  1182940, news1) was the frozen article that C1, G1 and X1 rejected, because
  JMdict also reads 乙 as おと (entry 2837087). 早乙女 (news1) and the
  untagged 乙女 are whole-word readings in the Joyo table's appendix (PDF p.
  162) and do not use オツ. 乙種 is the first Joyo example for 乙 (PDF p. 19),
  and Digital Daijisen and Kanjipedia give it for the sense "second rank"; 種
  has a card;
- kept 仙人: the only candidate with a listed tag is 仙台 (spec1), a city
  name;
- kept 伯仲: 伯父 and 伯母 are tagged only for their whole-word readings おじ
  and おば, 伯爵 needs 爵, which has no card, and 画伯 is the alternative.

All three families accepted the three row decisions (items A1-A3).

## Review execution

Reviewers of three model families, Claude, GPT and Grok, worked
independently. The issue 60 proposal named the two-family review of earlier
batches; because this batch adds new word articles, the repository's review
rule for new word cards and learner articles calls for three reviewers of
different families, so the author added a Grok reviewer; no reply to the
proposal has been posted on issue 60 yet. The three initial runs reviewed
the same frozen packet (`packet/`, manifest SHA-256 `b378c4a9…`) without
seeing each other's work. Each covered all four facets (correctness,
scoped coverage, consistency and quiz safety, comprehensibility), with an
assigned emphasis: Claude on correctness and scoped coverage, GPT on
consistency, quiz safety and comprehensibility, Grok on comprehensibility.
The rule assigns one facet to each reviewer instead (see "Facet assignment"
under Limits).

Each confirmation was run by a **fresh agent of the same model family**, not a
later turn of an earlier agent. It received a new packet with the author's
statement answering its family's last report (`RESPONSE.md`), the list of
changes (`CHANGES.md`), the revised files, the exact diff and the check
outputs, and was allowed to read the original packet and its own family's
earlier reports. Later commits were confirmed in further rounds, and the last
round confirmed `ba44b280` in all three families. All twelve runs ran one
after the other (no two runs overlapped). Models and times come from the
runtime session records, not from the reports; every run's actual model
equals the requested one.

| Run | Model | Snapshot | Window, 2026-11-21 UTC | API requests | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| initial-claude | claude-opus-5.5 | `c6afa163` | 13:13:35-13:21:55 | 78 | 78 | 2 | NEEDS FIX (consistency and quiz safety): one minor finding (C1); three optional suggestions (O1-O3) |
| initial-gpt | gpt-6.1-sol | `c6afa163` | 13:22:17-13:35:13 | 67 | 66 | 1 | NEEDS FIX (consistency and quiz safety): two major findings (G1, G2) and one minor (G3); three optional suggestions (O1-O3) |
| initial-grok | grok-4.7 | `c6afa163` | 13:36:16-14:00:03 | 182 | 181 | 1 | NEEDS FIX (consistency and quiz safety): one minor finding (X1); three optional suggestions (O1-O3) |
| confirm-claude | claude-opus-5.5 | `395f5364` | 16:26:46-16:33:16 | 48 | 48 | 2 | CONFIRMED initial-claude's items; three optional points |
| confirm-gpt | gpt-6.1-sol | `3c5ef845` | 16:45:50-16:54:42 | 57 | 56 | 1 | CONFIRMED initial-gpt's items; one optional point |
| confirm-grok | grok-4.7 | `3c5ef845` | 16:55:32-17:04:42 | 74 | 73 | 1 | CONFIRMED initial-grok's items; two optional points (P1, P2) |
| confirm2-claude | claude-opus-5.5 | `3c5ef845` | 17:05:16-17:07:13 | 20 | 19 | 1 | CONFIRMED confirm-claude's items; one optional point |
| confirm3-claude | claude-opus-5.5 | `a7cc61e2` | 17:51:25-17:53:36 | 23 | 23 | 2 | CONFIRMED confirm2-claude's point and the Metadata ids; one optional point |
| confirm2-gpt | gpt-6.1-sol | `a7cc61e2` | 17:55:01-18:00:03 | 44 | 43 | 1 | CONFIRMED confirm-gpt's point and the Metadata ids |
| confirm4-claude | claude-opus-5.5 | `ba44b280` | 20:55:12-20:58:44 | 32 | 32 | 2 | CONFIRMED confirm3-claude's point and A1-A3; one optional point |
| confirm3-gpt | gpt-6.1-sol | `ba44b280` | 21:00:16-21:11:04 | 96 | 95 | 1 | CONFIRMED A1-A3; one optional point |
| confirm2-grok | grok-4.7 | `ba44b280` | 21:12:15-21:26:39 | 123 | 122 | 1 | CONFIRMED P1, P2 and A0-A3; one optional point |

All three families' last confirmations are of the same final commit
`ba44b280`, which was committed (19:54:11 UTC) before any of them started.
`confirm-packet/` holds the nine confirmation packets (`c1claude`, `c1gpt`,
`c1grok`, `c2claude`, `c2gpt`, `c2grok`, `c3claude`, `c3gpt`, `c4claude`,
numbered by each family's round; shared files are stored once in `common/`).
`reports/` holds the verbatim reports, `prompts/` the exact prompts and the
three wrappers that delivered the initial prompts, `scope-audits/` each run's
read-scope audit and `integration/` the two merge proofs. `provenance.json`
hashes the files with the packets. Raw session logs stay local because they
may hold private context.

## Findings and dispositions

The confirmation statements number a family's earlier optional points P1-P3
and the author's own items A0-A3. The items below use the numbering of the
last round. A0, the Metadata ids, was numbered A1 in the statements to
`confirm3-claude` and `confirm2-gpt`; the last statements to Claude and GPT,
which had already confirmed it, omit it and start at A1.

| Item | Raised by | Disposition |
|---|---|---|
| C1, G1, X1: the reading quiz of the frozen word article 乙 おつ could offer おと, which 音 provides, as a wrong option, although JMdict also reads the spelling 乙 as おと (entry 2837087) | Claude (minor), GPT (major), Grok (minor) | Changed in 7eaf5c24: `words/乙.md` is deleted and 甲乙 こうおつ becomes the 乙 word; the 乙 card keeps 乙 おつ (JMdict 1182940) as an unlinked word in its オツ row. 甲乙 was later replaced by 乙種 (A1). Resolved, confirmed by all three families |
| G2: the meaning quiz of the word 仁 could offer 人物 as a wrong option, although JMdict gives 仁 the sense "human" | GPT | Changed in 7eaf5c24: `words/仁.md` excludes 人物, and also 個人, 芯 and 中心, for the senses "human" and "kernel". Resolved |
| G3: the distractors of 仙 (麦, 皿, 筒) and 伎 (梅, 蛇, 炭) are concrete things unrelated to the card's meaning, so a learner can rule them out without knowing the card | GPT | Changed in 7eaf5c24 for 仙 and 伎, which took Starter cards, and in 2c206d8f, which gave 乙, 伏, 伐 and 伴 same-domain sets and replaced 仙's 父 and 伎's 行 and 達. Final sets are listed under "Snapshot and scope"; in the N1 and All stacks every reading question takes all three wrong options from them, while in a Starter practice session 乙, 伏, 伐 and 伴 take all three from the fallback, as at the freeze. Resolved |
| Claude O1, GPT O3, Grok O1: `words/仁.md:22` "writes about" is unidiomatic | Claude, GPT, Grok | Changed in 7eaf5c24 to "discusses". Resolved |
| Claude O2: the 仁 article omits JMdict's sense "nucleolus" | Claude | Changed in 7eaf5c24 (`words/仁.md:38`). Resolved |
| Claude O3: `reading_options.py` over-reports 伯 は | Claude | Not changed: a tooling limit, not a card defect. Recorded as a follow-up. Accepted in the confirmation |
| GPT O1: shorten the audit-style text on the cards | GPT | Not changed: the cards follow the layout adopted for batch 149. Accepted in the confirmation |
| GPT O2: explain "epigone" and "ateji" | GPT | Changed in 7eaf5c24: "epigone" is dropped from the 亜流 gloss on 亜, and 仙's セント row explains ateji. Resolved |
| Grok O2: `words/亜熱帯.md:29` says "either character" of a three-character word | Grok | Changed in 7eaf5c24 to "any of the three characters". Resolved |
| Grok O3: the ateji gloss on 仙 (line 32) | Grok | Changed in 7eaf5c24, with GPT O2. Resolved |
| Points the initial reports could not verify (Claude: that JMdict has no entry read わざおぎ, and eight glosses outside the packet's families file; GPT and Grok: the compound-sound-changes article and JMdict 1002570, which Grok checked only through jpdb because the EDRDG page asks for a password) | Claude, GPT, Grok | Evidence supplied in the confirmation packets. 1002570 (お疲れ様) was cited only by the deleted `words/乙.md`. Accepted in the confirmations |
| confirm-claude 1, confirm-gpt optional, Grok P1: add an example of /p/ after ん, such as 先輩 せんぱい, to the compound-sound-changes article, which the 潜 card now links for 潜伏 | Claude, GPT, Grok | Not changed: the article is outside the batch and its h-row to p-row explanation is correct. Recorded as a follow-up. DECLINE ACCEPTED by confirm2-claude, confirm2-gpt and confirm2-grok |
| confirm-claude 2: 中心 is the weakest of the four new 仁 exclusions, while 中央 remains drawable | Claude | Not changed: JMdict gives 中心 the sense "core", and excluding it only removes an option. DECLINE ACCEPTED by confirm2-claude. Recorded as a follow-up |
| confirm-claude 3: the 甲乙 exclusions 対照 and 差 are loose | Claude | Not changed. DECLINE ACCEPTED by confirm2-claude; moot since the 甲乙 article was deleted (A1) |
| confirm-claude Limits: other readings of 甲乙, and the source of its contract-parties sense | Claude | A scan of the readings was supplied; the unsourced sense was removed in 3c5ef845. RESOLVED by confirm2-claude |
| Grok P2: a point on the gloss of a 甲乙 example | Grok | RESOLVED by confirm2-grok: the 甲乙 article was deleted (A1) |
| confirm2-claude: 甲乙 also has the reading かんおつ, a music term | Claude | Not changed: the article said the music term is a different word not in JMdict. DECLINE ACCEPTED by confirm3-claude; moot since the article was deleted. Recorded for any later 甲乙 article |
| confirm3-claude: `CHANGES.md` said `quiz-safety.txt` differs from the earlier copy "apart from line 1", but the file is byte-identical and has no command line | Claude | Corrected in the `CHANGES.md` of the last round. RESOLVED by confirm4-claude |
| A0: six words named on the cards lacked JMdict ids on their Metadata lines: 乙種 1862630, 亜麻 1149860, 仁術 1369740, 仙骨 1387150, 酒仙 1329130 and 伯母さん 2261500 | Author | Changed in a7cc61e2. RESOLVED by confirm3-claude, confirm2-gpt and confirm2-grok |
| A1: the selection errors (news2 and spec2 counted as qualifying tags at the freeze; `7eaf5c24` chose 甲乙 without checking 甲) and the replacement of 甲乙 by 乙種 | Author | Changed in ba44b280 (`乙.md` lines 23, 31 and 38; `words/乙種.md` added; `words/甲乙.md` deleted). RESOLVED by all three families |
| A2: keep 仙人, whose only tagged alternative is the city name 仙台 | Author | DECLINE ACCEPTED by all three families |
| A3: keep 伯仲 | Author | DECLINE ACCEPTED by all three families. confirm4-claude and confirm3-gpt would prefer 画伯 if the row is revisited (Claude: its frequency rank; GPT: its transparent current meaning). Recorded as a follow-up |
| confirm2-grok: 乙種's exclusions 位, 級, 段 and 次ぐ are topic neighbours rather than synonyms | Grok | No change requested. Recorded for awareness |

## Integration with current main

`origin/main` moved twice after the published base. First, the owner's
commits `a6a40ef7` ("Add next-100 onomatopoeia companion guides", 15:52 UTC)
and `9766dbd5` ("Address independent onomatopoeia guide reviews", 16:22 UTC)
changed 102 paths: onomatopoeia articles, word articles and grammar files,
docs, `README.md`, `REVIEW.md` and `manifest.json`. The signed merge
`e37ad00b` has `3c5ef845` as its first parent and `9766dbd5` as its second.
Then `32f8b991` (18:01 UTC) and `0697b768` ("Illustrate dotto and
butsubutsu", 18:06 UTC) changed 11 paths: `REVIEW.md`,
`docs/onomatopoeia.md`, `docs/onomatopoeia-scene-images.json`,
`grammar/onomatopoeia-next-100-cohort-7.json`, `words/ねちねち.md`, two scene
files, three images and `manifest.json`. The signed merge `eafee44b` has
`a7cc61e2` as its first parent and `0697b768` as its second. In both merges
the only conflict was the derived `manifest.json`, which was regenerated with
`tools/build_manifest.py`.

`integration/merge_proof.py` writes `integration/merge-proof.json` for
`e37ad00b` and `integration/merge2-proof.json` for `eafee44b`. Both pass: every
non-derived path equals one parent byte for byte (49,043 and 49,048 paths
compared, none unmatched); none of the 32 batch runtime paths or 171 link
targets was changed by main, and the batch runtime files equal those of the
first parent; no main-changed line mentions a batch kanji or word; and the
manifest lists every batch file. In the first merge, `docs/confusable-words.md`
mentions 伯 only on lines that main did not change. The second merge's three
images were not scanned, because they are binary. Neither merge changed
reviewed batch text or resolved a substantive conflict, so, as for batches 144
and 155, no integration review was needed under the issue 60 contract. The
confirmations of `a7cc61e2` and `ba44b280` also received the author's merge
scope check (`evidence/merge-scope.txt`).

Main's own CI is red. The Validate content runs on `32f8b991` (44933285897)
and `0697b768` (44933684389) fail at `python tools/grammar_vocabulary.py
check`, because the vocabulary review of
`onoma-c7-nechinechi-criticism` in main's
`grammar/onomatopoeia-next-100-cohort-7.json` is stale; the run on
`9766dbd5` (44924260700) passed. No batch file is involved, and the batch does
not fix it. The batch's vocabulary check reports the same stale line, so CI on
this closure commit will fail in the same way until the owner fixes main. The
publication receipt needs a green run on the exact published commit.

## Limits

- **Fresh confirmers.** Each confirmation ran as a new agent of the same model
  family and had no memory of its own earlier reading. The confirmations of
  the three families are independent of each other. Grok was not asked to
  confirm `a7cc61e2` on its own; `confirm2-grok` reviewed A0 at `ba44b280`.
  Issue 60 asks for corrections to be confirmed with the original reviewers
  where possible; as in batches 150-155, each confirmation ran as a new agent
  instead.
- **Facet assignment.** The repository's review rule for new word articles
  asks for three reviewers of different families, one each for correctness,
  consistency and quiz safety, and comprehensibility. Here each reviewer
  covered all four facets with an assigned emphasis (Claude: correctness and
  scoped coverage; GPT: consistency, quiz safety and comprehensibility; Grok:
  comprehensibility). The review meets the three-family requirement but not
  the one-facet-per-reviewer split.
- **Execution.** Every run started after the previous one ended. Four Claude
  runs each once issued two read-only `view` calls at the same time:
  `initial-claude` at 13:17:46 UTC (two ranges of `mechanical-checks.md`),
  `confirm-claude` at 16:28:09 (the rubric and `QuizBuilder.kt`),
  `confirm3-claude` at 17:51:51 (`meta-scan-before.txt` and
  `meta-scan-after.txt`) and `confirm4-claude` at 20:56:05
  (`weblio-乙種.txt` and `weblio-乙種合格.txt`); the times come from the
  local session logs. Their reports wrongly say that each response
  made one tool call. The other runs had at most one tool call in flight.
  From the `confirm2-*` prompts on, the prompts also forbade combining several
  commands in one call: `confirm3-claude` disclosed three single PowerShell
  commands that looped over or printed several files, and `confirm4-claude`
  two single pipelines over several files (a `Compare-Object` of two reads
  and a `Get-FileHash` over six paths). `confirm-claude` reports "51 reverse
  targets", but the range it cites has 50 lines.
- **Grok's initial scope.** The prompt forbade recursive listings and
  corpus scans. `initial-grok` disclosed one recursive listing, but its audit
  shows eleven recursive commands over the packet or the repository snapshot,
  and a recursive grep of the packet. One `grep` with no path ran in the
  agent's working folder outside the packet and found nothing. It used
  `read_powershell` and `stop_powershell` on one shell, and wrote its report
  through a PowerShell here-string.
- **Other runs.** `confirm3-gpt` left one oversized comparison output, which
  the tool runtime saved to a temporary file, unopened; its report says so.
  Three of `confirm2-grok`'s GitHub contents-API requests, for `kanji/甲.md`,
  `kanji/爵.md` and `kanji/種.md` at the unpublished `ba44b280`, failed; its
  report takes the absence of the 甲 and 爵 cards from the author. Its report
  names only its family; the session records show grok-4.7.
- **Scope-audit flags.** The audits flag some paths outside the allowed
  folders that are false positives: base paths such as the parent
  `review-packets` folder, under which every built path lies in an allowed
  packet; the reports folder; and strings parsed out of JSON arrays. The
  audit script does not attribute reads made through shell commands or
  Python, so it can list files as unread that the reports say were read.
- **Context compaction.** The runtime compacted the context once in
  `initial-claude`, `initial-gpt`, `confirm-claude`, `confirm-grok` and
  `confirm2-grok`, and twice in `initial-grok`; those runs continued from a
  summary of their earlier reading. The other six runs were not compacted.
  These counts come from the local session logs; `provenance.json` does not
  record compaction.
- **Prompts.** Every prompt was saved to a file before use. The initial
  prompts were delivered by a short wrapper message naming the prompt file
  and its SHA-256 (`prompts/initial-*-wrapper.txt`). Compared with the
  delivered text in the local session logs, `confirm2-claude.txt` ends with
  CRLF where the delivered text ends with LF, and seven of the other eight
  confirmation prompts (all but `confirm2-gpt.txt`) end with one more line
  feed; otherwise the saved prompts match the delivered text.
- **Packet record.** `packet/` keeps 48 files: 44 files of the initial packet
  (its instructions, mechanical checks, diffs and most evidence), its three
  largest evidence files compressed, and a compressed copy of its manifest in
  which the hashes of its 6,772 copies of the repository's kanji and word
  files are folded into one aggregate. It does not keep the packet's copies of
  repository files, its rubric or its title lists; the recorded commits
  reproduce them.
  The manifest file the reviewers read (SHA-256 `b378c4a9…`) is not stored;
  `provenance.json` records the SHA-256 of its canonical JSON form. 32 of the
  stored files have LF line ends where the reviewers' copies had CRLF, so
  `provenance.json` also records the hashes of the stored files. The
  confirmation packets omit only their snapshot copies of the batch files.
- **Packet builder.** Before the last confirmation round the builder's list
  of batch paths was changed to come from the batch's own first-parent
  commits, with merges of main excluded, as that round's `CHANGES.md` files
  describe; one wording fix was also made in the text it generates.
- **Dictionary text.** Several judgments rest partly on live reads of
  Kanjipedia, Digital Daijisen (Weblio), Kotobank, Jisho, Takoboto and jpdb
  pages, not on pinned copies in the packets. EDRDG's JMdictDB pages ask for a
  password, so the reviewers checked JMdict ids against the packets' extracts
  and third-party mirrors.
- **Confirmation evidence.** The confirmers did not rerun the gates; they
  judged the check outputs that the author ran on each revised snapshot and
  included in their packets.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. At `ba44b280` they report 0
  production, 0 padded-session and 0 one-holder hits, and 10 latent
  collisions that no audited pool can draw: 丹 た; 亜 や; 仁 く, じ and と; 伯
  いき, えき, か, き and は. `reading_options.py` reports one problem, its
  known over-report of 伯 は (Claude O3). The meaning-quiz check reports 0
  errors and 0 warnings. In the N1 and All stacks all ten reading questions
  take three of three wrong options from their curated distractors; in a
  Starter practice session 乙, 伏, 伐 and 伴, whose curated cards are not
  Starter cards, take all three from the fallback, as at the freeze. Eleven
  existing cards (人 休 何 入 出 口 女 日 月 男 買) still fill one slot each
  from the fallback, as before. The word-quiz audit of the ten articles
  finds no attested reading among the wrong options and no question with
  too few candidates. The author reported 112 existing words whose reading
  quiz can offer a reading that JMdict attests for the same spelling,
  because word-reading exclusions do not cover alternative readings; this
  predates the batch and is recorded as an app follow-up. Sampled seeds are
  not exhaustive.
- **Selection.** The freeze counted news2 and spec2 as qualifying tags, and
  `7eaf5c24` chose 甲乙 without checking 甲 (see "Snapshot and scope"). 乙種
  is untagged, and 仙人 and 伯仲 carry only news2 and spec2; all three rows
  rely on per-row justifications that the reviewers accepted. 甲 still has
  no card.
- **Exclusions.** The ten cards declare 86 exclusions. The only exclusion
  between two new cards is 亜/乙, declared on 亜; the app applies an
  exclusion in both directions.
- **Metadata ids.** Every word named on the cards as a whole run outside a
  quotation has its JMdict entry id on the card's Metadata line. Four shorter
  words occur only inside longer ones and are not listed: 熱帯 in 亜熱帯, 歌舞
  in 歌舞伎, 伏せ in 伏せる and 母さん in 伯母さん.
- **Lint warning.** One warning, on `words/潜る.md`, whose Dictionary line
  cites no JMdict entry id, is older than the batch and out of scope.
- **Content budget.** Retained bytes at `ba44b280` are 56,679,021, under the
  56 MiB guard. No choice between raising the guard and a reduced set for
  the remaining rows has been posted on issue 60 yet.
- **CI.** Main's CI is red on a stale vocabulary review outside the batch
  (see "Integration with current main"). CI on this closure commit will fail
  in the same way until the owner fixes main, and the receipt waits for a
  green run on the exact published commit.
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance. Phone acceptance is
  outstanding, not inferred.
- **Superseded material.** No published commit is rewritten. `2c206d8f` was
  amended three times (`2e64b649`, `fe6cfb06`, `e62f1f13`) after the initial
  packet was built from the freeze and before any confirmation packet was
  built; no reviewer saw the earlier versions. The deleted articles 乙 and
  甲乙 remain in the history, and their reviewed text is in the confirmation
  packets. Every report is kept.

## Validation and accounting

At `ba44b280`: 439 host tests pass; validation 0 errors; lint 0 errors and 1
warning (above); quiz safety 0/0; reading options 1 problem (伯 は, above);
manifest rebuild unchanged (version `3cff2a550b6cbc3d`, 9,753 files,
SHA-256 `DC8128855B7B41CCAB6E74CAB14937FDDC733CF6526A9310B553666D38081BD5`);
budget 9,776 entries, 56,679,021 retained, 57,114,625 inflated and
36,425,719 local-ZIP bytes; vocabulary 3201/3539 with main's one stale line;
link plan 10 new articles and 1 added link, 0 problems; kanji remarks 10 of
10 new cards present, one existing card (潜) changed in a remark only, 0
problems; the Metadata scan finds no whole-run gap outside a quotation.

After publication, delivery becomes **588/1,228**, with **640 remaining**.
Until the receipt it stays 578/1,228.

Follow-ups recorded for a later pass: whether news2 and spec2 should count in
the tag list; the 伯 は over-report in `reading_options.py`; word-reading
exclusions that do not cover attested alternative readings; an example of /p/
after ん in the compound-sound-changes article; かんおつ for any later 甲乙
article; 画伯 instead of 伯仲; the 中心 exclusion on 仁; and a 甲 card.
