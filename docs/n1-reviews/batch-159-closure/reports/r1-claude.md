**Snapshot:** 1a9bb910d1bbff162f4e3920e64e8821f635a58d. Reviewer: Claude (exact model version not identifiable from inside the session). Shared snapshot only.

**Scope:** 10 new kanji cards (厘 又 叔 叙 吉 后 吏 吟 呈 呉), 10 new word cards (不吉 伯叔 厘 又聞き 叙情 吟味 呉服 太后 官吏 贈呈), and the one-line additions to the 9 edited existing files (不 伯 味 太 官 情 服 聞 贈). Evidence: the packet, plus live Weblio Digital Daijisen pages.

**Verdicts:**
- correctness: NEEDS FIX (two policy-level support-word findings; no factual blocker)
- scoped coverage: CLEAN
- consistency and quiz safety: CLEAN
- comprehensibility: CLEAN

**Findings:**

1. **major (policy)** | correctness/coverage | `snapshot\kanji\又.md`, `snapshot\words\又聞き.md`, `evidence\selection\support-selection.json`
   - **Claim and impact:** the 又 untagged-route reason is that the tagged 又 and 又は "are usually written in kana". JMdict confirms 又 (1524930: ichi1/news1/nf19) and 又は (1524990: ichi1/news1/nf15) carry `word usually written using kana alone`.
     - The rule excludes only irregular, rare, outdated, ateji and gikun marks. "Usually kana" is not one of them.
     - 又は is the Joyo table's own example, and また is a KANJIDIC2 reading.
     - So a qualifying tagged word existed, and the documented reason does not satisfy the rule as written.
     - Learning impact is low: 又聞き is a reasonable article, and its prefix sense is real (JMdict `prefix: indirect`, xref 又聞き; Daijisen ［接頭］ また-).
   - **Remedy:** either re-justify as a usefulness choice with an explicit rule exception, or switch to 又は.
   - **Evidence and confidence:** `jmdict-families.xml` entries 1524930 and 1524990; the rule file. Confidence medium-high.

2. **minor to major (policy)** | correctness | `snapshot\words\伯叔.md`, `support-selection.json`
   - **Claim and impact:** the reason says the tags on 叔父 and 叔母 "belong to the readings おじ and おば". In JMdict 1607070 and 1607100, ichi1/news1 are `ke_pri` on the spellings 叔父 and 叔母.
     - The restricted readings しゅくふ and しゅくぼ have no `re_pri`.
     - So the reason is imprecise. The tags are on the spelling, but the usual and tagged reading is おじ or おば, which is not a KANJIDIC2 on-reading.
     - The しゅくふ and しゅくぼ readings use シュク, but they are the untagged readings.
     - 伯叔 (untagged) is therefore defensible, but the recorded wording should be corrected.
   - **Remedy:** reword the reason to "the tagged readings are おじ and おば (kun); しゅくふ and しゅくぼ carry no re_pri".
   - **Evidence and confidence:** `jmdict-families.xml` entries 1607070 and 1607100. Confidence medium.

3. **Other exceptions checked**
   - **后 (太后): acceptable.** JMdict 1787360 has no tags and no marks. The tagged 皇后 (ichi1/news1) and 皇太后 (news1) need 皇, which has no card. I found no better-qualified word. The sibling readings of 后 (きさき, 1277320) are news2 only.
   - **吏 (官吏): acceptable.** JMdict 1211850 has only news2, nf34 and spec2, which count as untagged. Its `dated term` mark is at sense level and is not an irregular, rare, outdated or ateji mark. No 吏 word carries a qualifying tag (吏 itself is archaic; 公吏 is obsolete).

**Confirmed correct**
- Every Digital Daijisen claim matches the live Weblio entries, for all 10 kanji and the word entries I fetched:
  - 伯叔 (2 senses)
  - 吟味 (the 罪状 sense and the 原義 sense)
  - 不吉
  - 又聞き (example うわさを―する)
  - 叙情 (→叙事 cross-reference, 「抒」代用字)
  - 呉服 (3 senses)
  - 太后 (太皇太后 or 皇太后)
  - 官吏
  - 贈呈 (進呈)
  - 厘 (原字 釐)
  - 皇太后
- The JMdict tags and senses cited in the cards match the packet. I checked 吟味 (ichi1/news2, plus the dated and orig-meaning senses), 呉服, 贈呈, 叙情 (news1), 不吉, 厘 (news1; 釐 an out-dated kanji form) and 分 (ぶ).
- All relative links resolve. All quiz_exclusions and distractor targets exist. The 官吏/役人 and 叔/伯 exclusions are symmetric or covered by the app rule.
- Mechanical checks: validate exits 0. The 4 lint errors are on reused files and are identical at base.
- Word-quiz audits show no answer clash. The 呉 reading audit shows a latent ぐ collision (供 具 工 求) that is not drawable in production pools; informational only.
- The one-line additions to the nine edited files are correct. 贈 turns 贈呈 into a link.
- The 厘 example (打率 三割二分五厘 = .325) is correct. The original example sentences' grammar, kana and translations show no defects.

**Optional:**
- 官吏: 吏員 or 能吏 would also be untagged and are not marked dated.
- 太后 is obscure for an N5–N4 audience (comprehensibility only; 母后 or 王后 are alternatives).
- 伯叔: JMdict says "one's father's brothers", narrower than Daijisen's "parent's brothers". Consider wording.

**Limits (unverifiable or not checked):**
- Daijisen was verified through Weblio's reproduction, not the publisher's original.
- The 太 card's claim that 太后 sits under a 太 sense "added to titles of honored persons" was not verified (Weblio 太 not fetched).
- The Joyo table notes were not checked: 吉日 also read キツジツ, the 又 examples 又 and 又は, and 呉服 and 呉越同舟. Fetching the Joyo table PDF and Wikipedia list was inconclusive.
- KANJIDIC2 raw records were not re-read line by line. Readings were checked via card tables, the reading audits and Kanjipedia text.
- The 叙 Notes claim about no 叙 spelling for ついず or ついで, and the 厘 kanji-card "分 = next larger" claim, were not independently verified. The 分 ぶ entry itself was seen.
- Example naturalness is my own judgement as a non-native reviewer.
