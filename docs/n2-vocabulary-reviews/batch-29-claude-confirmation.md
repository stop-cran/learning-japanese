## Snapshot
The corrected commit is `790d3d1cd94e28f1a06c2aa55ec7d5eea8c8693b`, directly following the authored commit `abb39bbd85d529380cb2506b9ca7f3c2df59c8b3`. The clean state, commit identity and the diff and evidence hashes all come from the author's receipt. I had file, search and web tools but no Git or hash execution, so I verified none of them myself.

## Scope
- **Reviewer:** claude-opus-5.5 (Claude family), working alone and sequentially, with no edits.
- **Changed articles, read in full:** 琴, 言付ける, こないだ, ごめん, 転がす, 転がる, plus their article diffs.
- **Comparison cards, read in full:** 楽器, 近頃, このごろ, 任せる, お待ちどおさま, お待たせしました, 裏返す, 返る, あいにく, 弾く, 久しぶり and 御無沙汰. While checking ごめん's guards I also read 恐縮 and 申し訳, and checked the headers of 届ける, 送る, 伝える, 配達, 預ける, ごめんなさい, すみません and ごめんください.
- **Evidence, read in full:** all eleven appended families (`additionalComparisonEntryFamilies`), all of `correctionEvidence` (including `currentQuizDeclarations` and the adjudication), and the principal families 1241450, 1270670, 1440980, 1441000 and 1593330.
- **Not read:** forbidden ledgers, notes, the canonical batch-29.json and the other family's report.

## Verdicts
| Item | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 琴 | CLEAN | CLEAN | CLEAN |
| 言付ける | CLEAN | CLEAN | CLEAN |
| こないだ | CLEAN | CLEAN | CLEAN |
| ごめん | CLEAN | CLEAN | NEEDS FIX (B29-CL-06; existed before the correction, not a regression) |
| 転がす | CLEAN | CLEAN | CLEAN |
| 転がる | CLEAN | CLEAN | CLEAN |
| Appended evidence | CLEAN | CLEAN | CLEAN |

Supporting checks on the appended evidence:
- There are eleven new families, and the twelfth (久しぶり, 1227370) was already captured.
- The cited senses match the records: 1440980:2 "to turn over / tip over", 1441000:2 "fall over / roll over", 1512150:2 "to turn over" and 1550630:1 "turn (something) over".
- The current declarations match the actual article headers. My own count gives 81 declarations across 18 cards, nine of them new.
- Every new exclusion target exists, with no self-references or duplicates.

## Findings
**My original findings:**
- **B29-CL-01: resolved.** `琴.md:25` now says "variant character form". The 1241450 family lists 筝 with no flags, and the text no longer makes a chronology claim.
- **B29-CL-02: resolved.** `琴.md:9` now excludes 楽器. Its "musical instrument" title (1207340:1) is a broad label that also fits the koto.
- **B29-CL-03: resolved.**
  - `こないだ.md:9` now excludes 近頃 and このごろ; both JMdict senses (1242300:1, 1004710:1) gloss "recently".
  - Line 27 keeps the distinction between one past occasion and a current tendency.
- **B29-CL-04: resolved.**
  - `言付ける.md:9` now excludes 任せる; JMdict 1467150:1 glosses it "entrust (to someone)".
  - Line 31 accurately contrasts passing something onward with leaving the handling or decision to someone.
- **B29-CL-05: resolved.**
  - `ごめん.md:9` directly excludes both waiting formulas (1002360:1, 2149640:1), without relying on transitivity through ごめんなさい.
  - The あいにく guard is supported by the actual labels ("sorry, but" versus "sorry"), and line 38 states its limits.
- **Optional items from my original report:**
  - **Greeting example: resolved.** In my original retrieval of the Weblio raw HTML, I confirmed that Daijisen 御免 sense 5 contains 「―、お邪魔するよ」. The kana and the translation "I'm coming in" are sound.
  - **弾く link: resolved.** The link goes to the ひく article (1419370), and the はじく family (1419360) stays separate.
  - **御無沙汰/久しぶり: I accept the decline and withdraw it as a candidate.** The labels "not having been in touch" and "first time in a long while" don't collide, and 御無沙汰.md already compares the two.
  - **此間 and the instrument taxonomy:** remain optional.
  - **N2:573 wording:** withdrawn.
- **Regressions:** none found.

**B29-CL-06** (new; it existed before the correction and my initial review missed it). Minor; comprehensibility (quiz); `ごめん.md:9`, `恐縮.md:9`.
- **Claim:** ごめん ("sorry; no thanks") is not directly guarded against 恐縮 ("feeling obliged; apologetic gratitude").
- **Learning impact:** "sorry; no thanks" is a defensible-looking wrong answer for 恐縮, and the reverse also holds.
- **Evidence:**
  - JMdict 1270670:1 glosses ごめん as "I'm sorry; my apologies". 恐縮 sense 2 is "feeling sorry (for troubling someone)" per Jisho, and 恐縮.md teaches that sense ("Sorry to trouble you, but…").
  - `恐縮.md:9` already guards ごめんなさい, すみません and あいにく for exactly this sorry-label overlap.
  - Exclusions are not transitive, so ごめん is not covered through ごめんなさい.
- **Minimal remedy:** add 恐縮 to ごめん's `quiz_exclusions`.
- **Confidence:** medium.

## Optional
- **申し訳 ("apology; excuse") versus ごめん:** the precedent is mixed. 恐縮 guards 申し訳, but ごめんなさい and すみません do not, so this is optional only.
- **Pairs across transitivity:** 転がす/返る and 転がる/裏返す are not established collisions. "Roll something along", "return" and "turn inside out" separate the full labels.
- **届ける ("deliver; notify") versus 言付ける:** the "through someone" and "entrust for" qualifiers separate them.
- **Polish at `転がす.md:33`:** state plainly that 裏返す shows the other side and is not knocking something over.

## Limits
- I ran no Git or hash commands. All receipts and hashes are author-executed.
- I did not re-fetch Weblio 御免 in this pass. I rely on my earlier independent retrieval and on the author's reinspection receipt.
- 恐縮 1236740 is not in the evidence packet. I checked it on Jisho's current JMdict, not the pinned snapshot.
- This was a bounded confirmation, not a second review of all twenty articles. I ran no quiz draws in the app and did no corpus or native-speaker check.
- Raw HTML files from my first-pass fetches remain in `%TEMP%`, because I have no delete tool.
