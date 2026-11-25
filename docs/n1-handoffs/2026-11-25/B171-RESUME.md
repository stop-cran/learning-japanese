# B171 resume note (paused for app restart, 2026-11-25)

## State at pause
- Batch: B171 = 戒 戯 扉 扶 抄 把 抑 披 抹 + 露 (row 1177, pulled forward for 披露 ロウ); 拐 moves to B172.
- Phase: pre-draft authoring. Evidence gathered and verified; content/render scripts NOT yet written.
  Nothing is committed, signed, pushed or under review. No reviewer sessions, CI runs or shells are running.
- Worktree: C:\Users\romanko\n1-kanji-workspace\b171-wt, branch n1-b171 (local only, no remote branch),
  HEAD = beca991c03d66578b2abccce7f29de1c4a2ab983 = origin/main at the B170 receipt (pushed upstream already).
- Uncommitted (untracked) files in the worktree, all kept:
  - docs/n1-sources/batch-171-membership.json
  - strokes/{戒,戯,扉,扶,抄,把,抑,披,抹,露}.json (verified against pinned stroke inputs)
- Evidence (workspace root C:\Users\romanko\n1-kanji-workspace\): b171-dj.json..b171-dj4.json (Daijisen),
  b171-jm.json..b171-jm8.json (pinned JMdict lookups; jm8 = 戒心 児戯 扶育 抑揚 披見 直披 露店 雨露 掌握
  上演 抑止 露出 抄訳 抄録 扶助 戒律 遊戯 抹消 抹殺 一抹 抑圧 夜露 茶の湯 茶道 抹茶味 警戒心 開店),
  b171-readings.json, b171-joyo.txt, b171_lookup.py, b171_strokes.py. Temporary: b171-tmp.txt, b171-scan\.
- Templates: this folder's b170_content.py / b170_render.py / n1_gates.py / b170_close|panel|publish|followup.py.

## Card plan (unchanged from the session checkpoint)
戒 警戒 1252310 カイ | 戯 戯曲 1225010 ギ (sense 1 only; PARTIAL) | 扉 扉 1483380 とびら (senses 1–2) |
扶 扶養 1496990 フ | 抄 抄本 1349540 ショウ (news2/spec2) | 把 把握 1470910 ハ | 抑 抑制 1547290 ヨク |
披 披露 1483490 ヒ (+ 露 ロウ EXTRA_MAP row) | 抹 抹茶 1525220 マツ (news2/spec2) | 露 暴露 1601280 ロ.
Manual reused row 戯→words/悪戯.md (activated baseline pair; jukujikun, no reading allocation) + link 戯 in 悪戯.md
(file is LF on disk in this checkout; preserve existing line endings byte-for-byte).
Constituent cards edited: 警 握 暴 (link existing mentions) and 曲 養 本 制 茶 (add Common words line).

## New finding during this segment (meta_scan at base)
- meta_scan reads only the first `Metadata:` line. At base, 握's Metadata is a wrapped paragraph (ids not on line 1)
  and 警 has only a `Dictionary:` line, so both already show whole-run gaps (警: 1252330 1252360 1252310;
  握: 1152720 1152730 1152750 1470910 1160970 1349660 1152660 1160980 1153440). Precedent: B167 閉/凡 and
  B168 縫 collapsed such paragraphs into one `Metadata:` line with the merged sorted id list. Do the same for 握 and 警,
  recording before/after in changedReusedPassages. Other expected gaps: 曲 1239730 1239740; 本 15 ids; 制 1374880
  1223010 1409550; 茶 1422720 1002430 1280770 1422770 (append a `Word pairs` Metadata line).

## Exact next step on resume
1. Write files\b171_content.py (copy b170_content.py format; full prose per the plan) and files\b171_render.py
   (b170_render.py + PARTIAL, manual 悪戯 row, 警/握/暴 link edits, collapsed Metadata for 警/握, new-word exclusions).
2. From b171-wt: render → python tools/validate.py → python tools/build_manifest.py → word_quiz_audit (0 problems)
   → python tools/audit_n1_batch.py --batch 171 → n1_gates.py 171 beca991c… "戒 戯 扉 扶 抄 把 抑 披 抹 露"
   "警 握 暴 曲 養 本 制 茶" "警戒 戯曲 扉 扶養 抄本 把握 抑制 披露 抹茶 暴露".
3. Signed draft commit as stop-cran; then serial blind reviews (Claude correctness → GPT consistency/quiz → Grok
   comprehensibility), fixes/confirmations, integration with live origin/main, signed content + receipt commits,
   verify both ZIPs, #60 checkpoint, recount (target 738 delivered / 490 missing). Then B172 (拐 拒 拓 拘 拙 拠 拳 拷 挑 据).
