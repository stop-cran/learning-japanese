# B114 two-card delta confirmation — run N1-B114-CLAUDE-DELTA-001

## Snapshot

- Revision checked: `1c2b2c6a6658fa968f724657868ccae1eb61b198`
- Predecessor: `ac38b8e4427afc2c10a957871c5ec99e9cb92bda`
- Reviewer model: the runtime declares Claude Opus 5.5 (claude-opus-5.5). I cannot independently verify the execution model.

## Scope

- **Chain read:** b114-delta-claude-v1 segments 1–5, each read once in order. No re-views and no web_fetch.

| Segment | Contents |
| --- | --- |
| 1 | My previous confirm-claude.md |
| 2 | delta-packet/RESPONSE.md, fix.patch, changed-files.txt, and the revised 穀.md and 碁.md in full |
| 3 | The three counterpart cards 穂.md, 盤.md and 板.md in full |
| 4 | content-format.md through Quiz authoring; QuizBuilder.kt |
| 5 | dictionary.xml (JMdict 1270870, 1270890, 1482420); dictionary-provenance.json; checks budget, lint, manifest, manifest-rebuild, quiz-safety and validate |

- **Not reopened:** the other thirteen cards, the remaining exclusion pairs, word articles and strokes. The instruction and the patch bound this pass to two cards.

## Dispositions

**D1 — 穀–穂 removal: DISPUTE ACCEPTED.**
- *Change:* `穀.md:14` drops 穂, leaving `[米, 麦, 稲, 種, 粒, 実]`. The note at `穀.md:68-69` keeps "[穂] is the grain-bearing head, a part of a plant, not a synonym for all grain" and drops the exclusion rationale.
- *Rule:* content-format.md (Quiz authoring) requires a pair to rest on "evidence about the actual displayed labels and ordinary meanings".
- *Labels:* the full displayed labels are "grain; cereals" and "grain-bearing head". The second is explicitly qualified as the plant part that bears grain. 穂.md defines it as "an ear or head of grain … not the entire plant". Neither label is a defensible correct answer for the other prompt.
- *My earlier F1:* it rested on two things.
  - The 粒 precedent. But 粒 shares the bare, unqualified label token "grain", which is a different situation.
  - A part–whole relationship. That is a semantic relation, not synonymy.
- *Verdict:* on the evidence now opened, the withdrawal is justified. Removing the guard only stops withholding a distinct alternative.
- *Side effect:* the change also removes the "Like the rice plant…" sentence that I had flagged as misleading in my previous Optional section.

**D2 — 碁–盤 removal: DISPUTE ACCEPTED.**
- *Change:* `碁.md:14` is now `quiz_exclusions: []`. The new note at `碁.md:59-61` says: "[盤], board/disc, can name the Go board, as in 碁盤 ごばん. 碁 names the game, not its board. [板], plank/board, describes a flat piece of material rather than the game."
- *Dictionary check:*
  - JMdict 1482420 sense 1 is "board (in shogi, go, chess, etc.)" and JMdict 1270890 碁盤 is "Go board". So "can name the Go board" is accurate and suitably non-absolute.
  - JMdict 1270870 碁 is "go (board game)". So "names the game, not its board" is accurate.
- *Title checks:*
  - "board/disc" matches 盤's title "board; disc".
  - "plank/board" matches 板's title "plank; board".
  - 板.md describes "a board, plank, or flat plate of material", so the material wording is accurate. It also avoids the earlier absolute claim that a plank is "not that equipment".
- *Labels:* "Go board game" names the game; "board; disc" names an object. These are different meanings under full-label reading, as the unchanged bullet at `碁.md:63-65` says ("A shared game-related topic alone is not an exclusion rule"). The note is now internally consistent with that bullet.
- *My earlier F2:* it relied on the 盤–乗 precedent. That is a declaration on 盤 for a bare token homograph, and it does not override the displayed-label rule here.
- *Verdict:* the withdrawal is justified.

**D3 — Delta hunks and regressions: RESOLVED (no regression).**
- The patch touches only `quiz_exclusions` (line 14) and one Notes bullet on each card. changed-files.txt lists only 碁.md, 穀.md and manifest.json.
- Unchanged: titles, readings, quizOnyomi/quizKunyomi, distractors (穀 殿 投 段; 碁 目 日 田), Meaning, Readings, Common words and Metadata.
- Links on the changed lines resolve to existing cards: 穂, 盤, 板. Their descriptive phrases match the real titles.
- Neither counterpart lists the batch card:
  - 穂 has no quiz_exclusions, and its distractors are 積 想 息.
  - 盤 has exclusions 板 皿 台 基 岩 乗 and distractors 船 番 晩.
  - So both pairs are now genuinely unguarded, as intended, with no residual one-sided declaration.
- quiz-safety.txt shows unchanged curated meaning options for both cards (3/3): 穀 "palace; lord | throw | step; level"; 碁 "eye | sun, day | rice field". It reports 0 errors.
- Under QuizBuilder.kt lines 26-36, 穂 or 盤 may now appear as fallback wrong options when curated slots are not filled. They remain distinct, wrong alternatives.
- Other checks: lint 0/0, validate 0 errors, manifest and rebuild identical (version 1531e050487c8a64, 8664 files), budget within the earlier envelope.

**Whether this adjudication replaces my earlier approval.** It does. My previous confirmation recorded F1 and F2 as RESOLVED by adding these two guards. On the full-label evidence now opened, those guards were conservative rather than required. Their removal is the better-supported reading of content-format.md, so it supersedes my earlier approval for these two pairs only. My other earlier dispositions are not reopened.

## Verdicts

- **Correctness: CLEAN.** The new 碁 note and the trimmed 穀 note match JMdict 1270870, 1270890 and 1482420 and the counterpart titles.
- **Scoped coverage: CLEAN.** The grain/head and game/board/material distinctions remain in the Notes.
- **Consistency / quiz safety: CLEAN.** The note text and front matter agree, there is no one-sided residue, curated options are unchanged, and the change does not conflict with the displayed-label rule.
- **Comprehensibility: CLEAN.** The new sentences are short and plain.

## Confirmation

CONFIRMED.

## Findings

None.

## Optional

None.

## Limits

- **Pool scope.** Only N1/All pools are modelled, and in them curated options fill all slots. Fallback, custom or caller-built pools and multi-borrow Starter are not modelled. I claim no general custom-pool safety; this change only stops excluding two distinct alternatives.
- **App code.** QuizBuilder.kt is a supplied static copy. There was no Kotlin, JVM, emulator or phone execution, and no native or device evidence.
- **Old client.** Installed APK 5c000bd predates quiz_exclusions, which it ignores.
- **Checks not supplied.** No unittest or reading-exposure/reading-options log was supplied for this delta. Readings were unchanged by the patch, so I carry forward the earlier reading-audit limits rather than re-verifying them.
- **Carried forward unchanged:**
  - Daijisen-only supplementary claims remain unverified, including 碁 キ and 穀 beans/たなつもの.
  - There is still no stroke-geometry, raw-SVG or Joyo-PDF visual verification.
  - The earlier model-scope limits still apply.
- **No hashing.** I hashed nothing myself and relied on the coordinator's verification of the chain inputs.
