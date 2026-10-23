## Snapshot
- **Revised commit:** `7132eedd62f20b68eb13b08be9d61fb0b1803483`, which directly follows `c53e61946e7229fafbf9401901cfbebe48c2c19e`.
- **What I checked myself:** `.git\HEAD` points to `refs/heads/jlpt-n2-vocabulary`, and that ref file contains `7132eed…`.
- **Provenance limit:** "clean committed content" and every SHA-256 value are claims in the author's receipt. I did not run Git or recompute any hash. I assumed the files on disk and the patch match the commit.

## Scope
- **Model:** claude-opus-5.5 (claude family). No delegation, no edits.
- **Changed articles:** I read all nine in full: 納める, 治める, お辞儀, 教わる, 落ち着く, おとなしい, 落とし物, お出かけ and お手伝いさん.
- **Comparison cards:** I read all 17 in full: 配達, 終える, 済ませる, 支払, 収める, ぺこぺこ, 学習, 就く, 冷静, 合う, しっとり, 利口, そっと, 落す, 遠足, デート and 助手.
- **Patch:** I read all of it.
- **batch-10.json:**
  - The patch adds new sections at lines 14084–15832 and leaves earlier lines unchanged.
  - I read all 22 additional dictionary families in full.
  - I also read the original families 1589090, 1589220, 1589260, 1316820/1316830 and 1338475.
- **My own lookup:** I fetched the Weblio 収める entry myself.

## Verdicts
| Item | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 納める | CLEAN | CLEAN | CLEAN |
| 治める | CLEAN | CLEAN | CLEAN |
| お辞儀 | CLEAN | CLEAN | CLEAN |
| 教わる | CLEAN | CLEAN | CLEAN |
| 落ち着く | CLEAN | CLEAN | CLEAN |
| おとなしい | CLEAN | CLEAN | CLEAN |
| 落とし物 | CLEAN | CLEAN | CLEAN |
| お出かけ | CLEAN | CLEAN | CLEAN |
| お手伝いさん | CLEAN | CLEAN | CLEAN |
| Packet additions | CLEAN | CLEAN | CLEAN |

**Basis for the article verdicts:**
- Each of the 19 new pairs has either overlapping English answer labels or a real sense overlap:
  - 納める: sense 4 (pay, deliver) is spelled 納める only, and sense 9 (finish) is also 納める only. That supports pairing it with 配達, 支払, 終える and 済ませる.
  - 治める: sense 8 of 1589090 ("settle") has no spelling restriction and cross-references 治める sense 2.
  - 落ち着く: senses 1, 5 and 6 match 冷静, 合う and しっとり.
- All targets exist, and no list contains a duplicate or the card itself.
- 治める.md:37 corrects the earlier implication without claiming the spellings are interchangeable:
  - 争いを収める is valid.
  - Governing is distinctive to 治める. JMdict 1589090 has no "govern" sense.
  - Weblio sense 4 (紛争を―・める, 怒りを―・める) confirms this.
- 落とし物.md:25 links to 落す.md, which says 落す is a spelling of 落とす.
- お出かけ.md:34 matches JMdict 1338475 sense 1.

**Basis for the packet verdict:**
- There are 22 new families plus the original 1589260, giving 23 families for 20 word forms. I found no duplicates.
- The extra same-reading entries are kept and correctly set aside:
  - 1551230 is 率土, a literary noun read そっと.
  - 1344450 is 助手 read たすけて.
  - 1000420 is the あの meaning "that".
- The supplied evidence summaries match the full records, including restrictions. For example, 就く sense 4 is limited to the 就く spelling, and 利口 sense 2 notes it is usually used with お-.
- The Weblio receipt's attribution limit is accurate: my fetch also had no dictionary heading.

## Findings
No new regressions. Here is how each of my original findings and weaker hypotheses closes:

| Item | Status | Where it was closed |
|---|---|---|
| B10-01 (収める also settles disputes) | Resolved | 治める.md:37, 39; 落ち着く.md:39 |
| B10-02 (冷静 pair) | Resolved | 落ち着く.md:9 |
| B10-03 (利口 and そっと pairs) | Resolved | おとなしい.md:9; しっとり was also added |
| B10-04 (遠足 and デート pairs) | Resolved | お出かけ.md:9 |
| B10-05 (助手 pair) | Resolved | お手伝いさん.md:9 |
| 教わる/就く | Resolved | 教わる.md:9 |
| Odd wording at お出かけ.md:34 | Resolved | お出かけ.md:34 |
| ぺこぺこ and 支払 (candidates I noted in my working notes but did not report) | Addressed | お辞儀.md:9; 納める.md:9 |
| 落ち着く excluding 納める was "a stretch" | Withdrawn | JMdict sense 8 ("settle") has no spelling restriction, so the pair has a basis |

The three weaker hypotheses, all withdrawn:
- **おどかす vs びっくり/ぎょっと:** "threaten; startle" means causing the shock, while "be surprised; startled" and "taken aback; startled" mean experiencing it. That is a legitimate contrast for a quiz to test.
- **おだいじに vs お見舞い:** a formula wishing someone recovery is not the same thing as a visit or an expression of sympathy.
- **おじゃまします vs あの:** あの is a hesitation or attention-getter ("um; excuse me"), while おじゃまします is specific to intruding.

My earlier optional suggestions are still optional: the 御手洗 additions, links from 御 and 教, and an おさめる row in confusable-words.md.

## Optional
- 落ち着く.md:39 now links to 収める.md, but 収める.md does not itself teach settling a dispute. A one-line 争いを収める note there would help.
- 治める.md:37 could read more smoothly as "These spellings are not exclusive compartments: 収める is also used for…".
- 納める could mention its completion sense (仕事納め, 歌い納める), which is what justifies the 終える and 済ませる pairs.

## Limits
- **Git and hashes:** I did not run Git, the validator, or the app, and did not recompute any hash.
- **Dictionary data:** the JMdict records come from the packet. I could not check the pinned dictionary versions or confirm that the set of same-reading entries is complete.
- **治める lookup:** I did not refetch it; the author's failed fetch is not evidence. That point rests on JMdict 1316830 and my original Kotobank check.
- **Not read:** author notes, the review ledger and other reports.
- **Not a certification:** these verdicts are not native-speaker certified, and I make no claims about how often the app draws any pair.
