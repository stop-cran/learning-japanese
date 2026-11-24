Snapshot: 6ad1fedc1e3a50228ca9ccae45de50e05ac16f7a on base 6121ea9e6593497b4a93fb1e9597868bc92a5e6e. Packet `snapshot.txt` still names 027e5581; the new hash is the user’s and is only echoed in `line-endings.txt`. Not a new whole-batch review.

Scope: My prior comprehensibility and scoped-coverage findings only. Read `changes-1..4.txt`, `revision-1..5.txt`, `dictionary-check.txt`, `additional-families.xml`, and `line-endings.txt`. Reviewer: Grok 4.7 (grok-4.7).

Finding 1 — partially resolved; remainder still actionable. Titles, the 嫡 reading row, common-word gloss, and the `子` addition now say “legitimate child,” matching JMdict 1422910 sense 2. The heir example and the modern-rights warning remain. The parentage example still does not teach that sense: `revision-5.txt` translates 嫡子 only as *chakushi* and shows “children of the principal wife.” Unchanged contrasts still say 嗣子 need not specify who the mother was and that 継 is “not who a child’s mother was.” “Parentage within marriage” is attached to 嫡子, while `additional-families.xml` gives that English gloss to both 嫡子 and 嫡出子, and `dictionary-check.txt` separates Daijisen’s principal-wife sense from the 嫡出子 legal-marriage entry. That check is an author paraphrase, not a quotation. Remedy: in the example, gloss 嫡子 as “legitimate child”; label any principal-wife wording as the cited Daijisen sense, not the whole JMdict sense; name 嫡出子 if “within marriage” stays; qualify or replace the two mother-identity sentences. Confidence: high on the label fix and the example gap; medium on Daijisen wording.

Finding 2 — resolved. `revision-3.txt` flags 孔・あな as outside the standard-use table and says to write 穴 for ordinary あな. `revision-5.txt` says the same and keeps the flaw example as usage, not a sense ban. Matches `sources.json` and the Kanjipedia note in `dictionary-check.txt`.

Finding 3 — resolved. `revision-1.txt` gives お祖母さん (also おばあさん).

Finding 4 — resolved. `revision-4.txt` gives 婚約 (こんやく), matching family 1289710.

Optional: ばば outside-table flag, ひめ- as small rather than princess, and おうじょ / おうひ are in. 媒体 no longer says “or something else.” Still optional, not done: a tale/play label or attested non-royal 姫 example, a literary note on 才媛, and an advanced marker for 嫡子 on the N5 子 card. None of these is now a defect.

Regressions: none consequential. 妊娠 still contrasts the person in Synonyms; the new した / している lines have readings and do not contradict 1467350. 婿’s “both uses” is slightly stale after the added “husband” gloss, but 1531160 supports that gloss. 旋 and 嬢 notes match `labels.txt`. EOL-only noise in `子.md` is not a content change; the substantive line is the corrected gloss.

Limits: No git-object, device, native, or external-page check. Daijisen prose is still not in the packet. Untouched articles were not reread.
