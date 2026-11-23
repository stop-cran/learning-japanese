# Author's statement for the reviewer of `b159-review-claude.md`

This statement answers only the points in YOUR initial report. C1-C3 are your report's Findings 1-3, O1-O3 are your three Optional bullets in order, and L1-L5 are the first five of your six Limits in order. Your sixth Limit (example naturalness as your own judgement) describes your method and needs no answer.

The statement is the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and independent sources; do not rely on this text as evidence. Line numbers refer to the revised files in this packet.

What changed, in brief (see `CHANGES.md` for every line):
- five batch kanji cards (厘 又 叔 吟 呈) and all nine remaining new word articles;
- the new word 又聞き is deleted, and the frozen line added to 聞 is removed;
- the frozen one-line additions to 太 and 官 changed;
- two existing kana-headed articles, また and または, now link the 又 card;
- the repository audit `tools/audit_n1_batch.py` and its tests;
- the ledger `docs\n1-sources\batch-159-progress.json`;
- the batch's pinned JMdict extract (two entries removed);
- the generated `manifest.json`.

Every stroke file and every other kanji card and word article is unchanged. Give a disposition for each of C1-C3, O1-O3 and L1-L5, and judge the other reviews' changes described below.

## Findings

### C1: 又's untagged-route reason ("usually written in kana") is not a rule exclusion

Author action: **changed**. 又 no longer uses the untagged route. Its support words are now the two existing kana-headed articles `words\または.md` and `words\また.md`, under point 2 of the rule (`evidence\rule-7058679348.md`): "I first check whether an existing article, including a kana-headed one, already teaches a suitable word … if so, it is linked instead of adding one."

- **The two supports.**
  - または (entry 1524990) carries ichi1/news1 on both the spelling 又は and the reading または. `words\または.md:24` says 又は is another spelling. 又は is the Joyo table's example for 又 (`evidence\joyo\p145.txt`).
  - また (entry 1524930) carries ichi1/news1 only on the reading. The spelling 又 has no tag, so the ledger records that mapping as untagged, with a note (ledger lines 45-67). `words\また.md:24` says 又 is a recognized spelling.
- **The 又 card.**
  - `kanji\又.md:23` links [又](../words/また.md) and [又は](../words/または.md). It says that the linked articles are headed in kana and show 又 and 又は as other spellings.
  - Line 30 (the また row) links both. `quizKunyomi` is now [また] (line 12) instead of [また-].
  - The prefix sense stays as information. Line 23 mentions it, and line 31 (the また- row) keeps 又聞き and 又貸し as unlinked examples marked "Not selected for questions here."
- **Removed from the frozen draft.**
  - The article `words\又聞き.md` and its line on `kanji\聞.md`.
  - 又聞き's ledger mapping and its exclusion row.
  - JMdict entries 1442420 (伝聞) and 2025400 (又ね), which only the removed text cited.
  - Ledger line 29 (`selectionReason`) now names the kana-headed support.
- **Repository audit.** The audit had to learn the kana-headed case. `tools\audit_n1_batch.py:60-67` adds `support_spelling()`, which accepts a mapping's `spelling` field only when:
  - the article is kana-headed;
  - the spelling contains the kanji;
  - the article text shows that spelling.

  Five new tests are at `tools\test_audit_n1_batch.py:129-153`.
- **Lint.** It reports two new warnings on `kanji\又.md`, because または and また do not list 又 in `kanji:`. `tools\validate.py:504-508` rejects a `kanji:` entry that is not in the headword, so a kana-headed article cannot list it.

Please judge whether linking the two existing articles satisfies point 2 of the rule.

### C2: the 叔 reason says the tags "belong to the readings おじ and おば"

Author action: **wording changed**; the untagged route with 伯叔 is **kept**.

- Ledger line 78 (`exceptionReason`) now says that the spellings 叔父 (1607070) and 叔母 (1607100) carry ichi1/news1, but their tagged readings are the whole-word readings おじ and おば. The Joyo table lists those as special readings of 叔父 and 叔母 (`evidence\joyo\p75.txt`; the appendix of whole-word readings, 付表, on `p162.txt`). しゅくふ and しゅくぼ are restricted to those spellings and carry no priority tag. An article headed 叔父 or 叔母 would teach おじ or おば as its primary reading.
- This is your suggested wording, with one addition: the reason why the route is kept. The 叔 card has no kun reading (`kunyomi: []`), and おじ and おば are not readings of 叔 alone.
- `kanji\叔.md:39` adds the same point for learners: the Joyo table gives 伯叔 as its only example word for シュク, and おじ and おば are whole-word special readings, not readings of 叔 alone.
- The same choice was accepted in B156 for 伯, where 伯父 and 伯母 were passed over for 伯仲.

### C3: the 后 and 吏 exceptions

Author action: **none**; you found both acceptable. Two related wording changes from the other reviews are listed below (items 5 and 6).

## Optional notes

### O1: 吏員 or 能吏 instead of 官吏

Author action: **not changed**; the support word is still 官吏.

- 官吏, 吏員 and 能吏 are all Joyo examples for 吏 (`evidence\joyo\p154.txt`). All are untagged under the rule; 官吏 has only news2/nf34/spec2 (`evidence\jmdict-scan-c1.txt`).
- The author kept 官吏 because it shows 吏's main meaning through 官, which has the same meaning. Digital Daijisen defines 官吏 as 国家公務員, with 役人 and 官員 as equivalents (`evidence\daijisen-kotobank.json`). 能吏 adds a judgement ("able official"), and 吏員 (1549700) is glossed only "official".
- The dated mark is now shown to learners:
  - `kanji\官.md:37` adds "(dated)";
  - `words\官吏.md:18` replaces the undated corruption example with one framed as history ("I read about a corrupt government official in a history book.");
  - `words\官吏.md:28` already names 公務員 as the modern word.

### O2: 太后 is obscure for N5-N4 learners

Author action: **not changed** (the support word is still 太后), **explanation added**.

- 母后 ぼこう (1783060, "empress dowager") and 王后 おうこう (2014540, "queen") are also untagged, and are no less obscure. The Joyo examples 皇后 and 皇太后 (`evidence\joyo\p52.txt`) need 皇, which has no card.
- `words\太后.md:15` now explains the title in plain terms from Digital Daijisen: 皇太后 is the empress of the previous emperor, or one who is also the current emperor's birth mother, and 太皇太后 is the empress of the emperor two reigns back.
- `kanji\太.md:38` adds that in 太后, 太 is added to an honored person's title and does not mean "thick".

### O3: JMdict's "one's father's brothers" is narrower than Daijisen's "parent's brothers"

Author action: **changed**.

- `words\伯叔.md:15` gives Digital Daijisen's two numbered senses: (1) older and younger brothers; (2) the older and younger brothers of one's father or mother, that is, 伯父 and 叔父. It then quotes JMdict's gloss "brothers; one's father's brothers", and says both examples use sense 2.
- Line 24 explains the combination for both senses.
- Line 32 adds that neither sense covers aunts.
- The title is unchanged: it is JMdict's gloss, which the app uses for quiz options.

## Limits answered

### L1: Digital Daijisen checked only through Weblio

Author action: **evidence added**. `evidence\daijisen-kotobank.json` holds the Digital Daijisen sections from kotobank.jp, a second online reproduction (fetched 2026-11-23), for:
- the nine words;
- the kanji 又 吏 太 吟 叙 呈;
- 皇太后 and 太皇太后.

The nine word articles now link these kotobank entries on line 34. The author has no access to the printed edition.

### L2: 太's sense "added to titles of honored persons"

Author action: **evidence added**. Entry 太 in `evidence\daijisen-kotobank.json` (https://kotobank.jp/word/太-556043) has sense 4: 「尊い者に添える語。「太公・太后・太閤」」.

### L3: the Joyo table notes

Author action: **evidence added**. `evidence\joyo\` has the text of each cited page of the official PDF, with its sha256:
- p34: 吉, 「吉日」は，「キツジツ」とも;
- p145: 又, with the examples 又 and 又は;
- p51: 呉, with 呉服 and 呉越同舟;
- also the pages for 厘 (with 分), 叔, 叙, 后, 吏, 吟 and 呈.

### L4: KANJIDIC2 raw records

Author action: **none needed**. The raw records are in the original packet, `evidence\kanjidic2-records.xml`. The revision changes no `onyomi` or `kunyomi` field. The only reading-metadata change is 又's `quizKunyomi`: from また- to また, which is listed in the 又 record.

### L5: the 叙 claim about ついず and ついで, and 厘's "分 = next larger"

- **叙: evidence added.** `evidence\jmdict-scan-c1.txt` lists every pinned entry read ついず or ついで. There are two, 1316390 (次いで) and 1345470 (序で, 序), and neither has a 叙 spelling. The same file lists all 46 entries with a spelling containing 叙; none is read ついず or ついで.
- **厘: changed.**
  - `kanji\厘.md:42` now says that 分 ぶ "is the fractional unit ten times larger". It follows JMdict's gloss of 分 ぶ as one-tenth, including 3 mm as one-tenth of a sun (entry 1502850). 厘 is one-hundredth, including 0.3 mm as one-hundredth of a sun.
  - `words\厘.md:28` says one 分 equals ten 厘.
  - 一分一厘 is the Joyo example for 厘 (`evidence\joyo\p157.txt`).

## Changes made for the other reviews

The other two reviews asked for the changes below. Please judge each change as a reviewer of the revised text, not only as an answer to your own notes.

1. **吟味 excludes 試験 and 確認** (`words\吟味.md:8`). JMdict 1243390 sense 1 includes "testing", and 吟味 was drawable in 試験's quiz. 確認 was added for consistency with the existing exclusion 確かめる. `CHANGES.md` lists the 12 quizzes in which 吟味 can still be drawn and why none is a second defensible answer.
2. **吟 excludes 検 審 査 調 究 研** (`kanji\吟.md:14`; the reason, with their titles, is at line 42). Their titles overlap with examining something closely, Digital Daijisen's sense 4 of 吟 (内容を探り確かめる). `CHANGES.md` explains why 診 偵 試 験 察 鑑 覧 are not excluded.
3. **Digital Daijisen links** on line 34 of all nine new word articles, as point 4 of the rule requires.
4. **又's sense list** (`kanji\又.md:23`) quotes the senses one by one: "again," "also," "on the other hand," "and; in addition" and "or; otherwise". The distractor note (line 48) says none means "again," "also" or "or." This replaces the frozen "and, or or".
5. **太后 and 太**: the plain explanation and the bridge clause described under O2.
6. **官吏 and 官**: the historical example and "(dated)" described under O1.
7. **吟味's "How the kanji combine"** (`words\吟味.md:24`): here 吟 has its sense of examining contents closely, and Digital Daijisen lists 吟味 under that sense. Reciting a poem and savoring its flavor is the original meaning: JMdict sense 4 (archaic) and Daijisen sense 3.
8. **伯叔**: the two senses and the example labels described under O3.
9. **Optional wording:**
   - `words\呉服.md:18` explains obi ("the long sash tied around the waist over a kimono") and calls 呉服売り場 the department store's kimono-fabric counter;
   - `kanji\呈.md:40` quotes 呈する's JMdict glosses in full (entry 2012430): "to present; to offer," "to show; to display; to exhibit" and "to assume (e.g. a shape)".

Every other changed line is a ledger line that records the same changes, or the regenerated `manifest.json`. `CHANGES.md` lists every changed line by file.
