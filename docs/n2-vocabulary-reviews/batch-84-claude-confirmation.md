Snapshot: 1bc794829f221a5d4858a8f34899dc5c5bb408cc, committed content only.
- Its parent is 04e39de5d1d0055ec6702a224270bffa57e188e6. `batch-84-correction-snapshot.json` reports `cleanCommittedContent: true`.
- The file tools cannot run Git. I did not run the Git, hash, manifest or preservation checks myself; the author did. I am relying on the author's statement that the files on disk match the commit.

Scope: This is a non-blind confirmation in my original session, run as claude-opus-5.5.
- **Repository reads, each file viewed on its own:**
  - all 20 current word bodies and the kanji bodies 税, 接 and 材;
  - both instruction files in full, and `content-format.md` lines 18–103;
  - one bounded search of the TSV: the header plus N2:1662–1681.
- **Private files read in full, each in its own call:**
  - the correction snapshot and `correction.patch`;
  - the mappings, principals, components and all 291 labels;
  - all 307 lines of `public-bodies.txt`;
  - the author adjudication;
  - the corrective comparison reading (complete records for 22 dictionary entries);
  - the 153-guard quiz declarations;
  - the corrective old bodies 01–03 (つまらない, 馬鹿, 予算, 迷惑, はっきり, 地域, 散らかす, 寝る, 頼む, 偶然, たまたま, 寄る, おめでたい).
- **Extra checks:** one search of the 20 assigned files' `title` and `quiz_exclusions` lines, and one file search confirming that seven link or guard targets exist.
- **Not read:** `correction-evidence.json` (not permitted), the other reviewer's report, ledgers and notes, and `batch-84.json`.

Verdicts:

| Source | Article | Correctness | Scoped coverage | Comprehensibility | Comment |
|---|---|---|---|---|---|
| N2:1662 | めちゃくちゃ | CLEAN | CLEAN | CLEAN | Example of the "ruined" result added (F01). The つまらない guard is justified. |
| N2:1663 | めっきり | CLEAN | CLEAN | CLEAN | はっきり guard adopted. |
| N2:1664 | めでたい | CLEAN | CLEAN | CLEAN | Translation now says "settled". 馬鹿 guard justified. |
| N2:1665 | メニュー | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1666 | めまい | CLEAN | CLEAN | CLEAN | Unchanged. げんうん (2863071) is now read and confirmed as a separate entry. |
| N2:1667 | 目安 | CLEAN | CLEAN | CLEAN | 予算 guard added (F05). |
| N2:1668 | 免税 | CLEAN | CLEAN | CLEAN | Unchanged. Reciprocal link with 税 intact. |
| N2:1669 | 面積 | CLEAN | CLEAN | CLEAN | Unchanged. The qualified title "measured area" is kept. |
| N2:1670 | 面接 | CLEAN | CLEAN | CLEAN | The role wording is now stated positively (F02). Reciprocal link with 接 intact; 接近 now linked. |
| N2:1671 | 面倒くさい | CLEAN | CLEAN | CLEAN | Source spelling 面倒臭い kept. 迷惑 guard (F06) and つまらない guard added. |
| N2:1672 | 儲かる | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1673 | 儲ける | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1674 | 申し訳ない | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1675 | モーター | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1676 | 木材 | CLEAN | CLEAN | CLEAN | Unchanged. Reciprocal link with 材 intact. |
| N2:1677 | 目次 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1678 | 潜る | CLEAN | CLEAN | CLEAN | The learner-facing sentence about the source error is removed (F03). 地下 is linked. Kept separate from くぐる. |
| N2:1679 | もしかしたら | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1680 | もしかすると | CLEAN | CLEAN | CLEAN | "By some chance" is now introduced and the すると wording reframed (F04). |
| N2:1681 | もたれる | CLEAN | CLEAN | CLEAN | Unchanged. |

**Separate assessments:**
- **Kanji and baseline preservation:** CLEAN. 税, 接 and 材 are unchanged, and the patch touches only eight new word cards.
- **Components:** CLEAN. All 30 records are unchanged, and no missing kanji cards were invented.
- **Reciprocity:** CLEAN. 免税/税, 面接/接 and 木材/材 are intact.
- **Mappings:** CLEAN. All 20 TSV rows, selected senses and additional senses match. The malformed raw gloss for 潜る is kept in the TSV and mapping.
- **Quiz declarations:** The front matter of all 20 cards matches the 153 declared guards exactly.

Findings:
- **B84-F01 — resolved.** めちゃくちゃ.md:22 adds 「雨で旅行の計画がめちゃくちゃになりました。」 This matches Daijisen sense 2 (「集まりを―にする」). I accept the author's view that this was Low and close to optional, because the chaotic-state use was already taught.
- **B84-F02 — resolved.**
  - 面接.md:22–25 now uses positive examples: 面接を受ける, and 「役員が面接する。」, which is Daijisen's own example.
  - I accept that the old wording was not literally a double negative.
  - I withdraw any frequency claim (that the interviewer is "usually" the subject) from my proposed remedy, because the evidence does not support it.
- **B84-F03 — resolved.** The sentence at 潜る.md:44–47 is gone, and 地下に潜る is linked. The raw gloss is kept in the source fields (mapping `identityNote`).
- **B84-F04 — resolved.** もしかすると.md:16–17 introduces "by some chance", matching the 1012530 glosses. Lines 37–41 now describe the expression as a guess.
- **B84-F05 — resolved.** 目安.md:9 adds 予算.
  - 目安's title is "rough standard; guideline; estimate"; 予算's is "budget; cost estimate".
  - Dictionary support: 1535280 sense 2 (rough estimate) and 1543000 (estimate of costs).
- **B84-F06 — resolved.** 面倒くさい.md:9 adds 迷惑 ("nuisance; inconvenience"; 1532800 senses 1–2), which overlaps with "bothersome".
- **Guards added from the other review, checked in both directions:**
  - めちゃくちゃ/つまらない: accepted. つまらない (1008190) sense 3 is absurd/foolish, and めちゃくちゃ's title includes "absurd".
  - 面倒くさい/つまらない: accepted. つまらない sense 1 "tedious" overlaps with "tiresome".
  - めでたい/馬鹿: accepted. おめでたい (1647360) sense 2 includes foolish/gullible, 馬鹿 (1601260) sense 2 is foolish, and the existing おめでたい card already guards 馬鹿.
- I found no new regressions and no remaining actionable defects.

Optional:
- **Adopted:** the めっきり/はっきり guard, "settled" in めでたい, and the 地下 and 接近 links (both files exist).
- **Declined, and I accept the reasoning:**
  - 面積/地域: the qualified title "measured area" reduces the risk, and guarding every "area" title would just create a category-wide set of guards.
  - もしかすると example 2: style only.
  - A casual-use note on めんどくさい: it would need corpus support.
- **Retained and harmless:** 木材/材木, the もしかしたら/もしかすると guards against 偶然/たまたま, and もたれる against 寝る/頼む.
- **Still optional, not blocking:**
  - めちゃくちゃ/散らかす: めちゃくちゃにする can mean "make a mess of".
  - もたれる: its dependent "甘えて頼る" use could be marked as older or literary, since Daijisen sense 3 cites only an Edo-period quotation.

Limits:
- **Unverified consequential claims:** none.
- **Initial stage (blind, snapshot 04e39de5):** I used 74 of 80 calls and did not read the old-body inspection files.
  - The 寄る leaning sense was confirmed then on the live jisho.org site; it is now also in the corrective reading (1219680 sense 6).
  - The げんうん limit is closed, because 2863071 has now been read.
  - The 〜を面接する limit is moot, because that construction is no longer taught.
  - The author's monitor records up to 20 concurrent native calls in my initial session, which contradicts my statement then that I worked one call at a time. I cannot check this from inside the session; treat the monitor's record as authoritative.
- **Corrective stage:** 40 tool calls in total, issued one per message, none repeated.
- **Not done:**
  - I did not run Git or hash checks, and I cannot prove the files on disk match the commit.
  - The 22 comparison-family records are author-prepared extracts.
  - No corpus-frequency study, native-speaker certification or empirical quiz draws, and no claim about model ranking or measured bias reduction.
