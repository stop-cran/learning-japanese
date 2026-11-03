Batch 017 confirmation: I withdraw my original Daijisen limitation. The Daijisen text is in the static HTML, and it supports the cards' reading allocation, the older form 螢 and the insect-family scope. Verdicts stay CLEAN with no findings. This is a dependent confirmation by my original session, not a new independent review.

**Snapshot:** b751248ea6f9f3d2cd2084e7e744d9de4d7ff30d, with the teaching unchanged. No uncommitted content is included, and no files were written.

**Scope:**
- **Model:** Claude Opus 5.5 (claude-opus-5.5), my original batch 017 review session.
- **Fresh reads this pass, one call per response:**
  - my original report `docs\n1-reviews\batch-017-initial-claude.md`;
  - `kanji\蛍.md` and `words\蛍.md`, read once each;
  - one raw fetch of https://kotobank.jp/word/%E8%9B%8D-488089 at start_index 60000, max_length 12000.
- **Kept from the original review, not re-read:** the guidance documents, `words\蛍光灯.md`, the KANJIDIC2 metadata, all four JMdict packets (72 families), the comparison kanji and words, the `confusable-words.md` searches and the Seisenban body text.
- I make no claim of fresh 72-family coverage.
- **Facets:** correctness, scoped coverage and textual comprehensibility, limited to the Daijisen and optional points below.

**Daijisen check**

The Daijisen article is in the static HTML (`article class="dictype cf daijisen"`). It is followed by the 精選版 日本国語大辞典 (Seisenban) article.

- **Noun entry, ほたる【蛍】:**
  - It says 甲虫目ホタル科の昆虫の総称 ("general term for insects of the firefly family, order Coleoptera"), and names ゲンジボタル・ヘイケボタル・ヒメボタル as examples.
  - On light, it says 暗い所では青白い光を放つことで知られるが、ほとんど光らない種も多い ("known for giving off pale light in the dark, but many species hardly glow").
  - Its second numbered sense is the title of chapter 25 of 源氏物語 (The Tale of Genji).
- **Character entry, けい【蛍〔螢〕】［漢字項目］:**
  - It marks the character 常用漢字 and gives ［音］ケイ（漢） and ［訓］ほたる.
  - The 〈ケイ〉 examples are 蛍火・蛍光・蛍雪・蛍窓.
  - The 〈ほたる（ぼたる）〉 examples are 蛍石・蛍火／源氏蛍.
  - The bracketed 〔螢〕 shows the older form.
- **Gaiji:** the gaiji images are only numbered sense markers. All the surrounding wording was readable.

How this bears on the teaching:
- **Reading allocation:** ケイ is Daijisen's own on-reading, shown with 蛍光; ほたる is its kun-reading. This comes from the dictionary's labelled character entry, not from splitting whole-word kana.
- **Standalone noun:** the noun entry's heading is ほたる. This supports "use ほたる, not ケイ, for the standalone noun".
- **蛍石:** Daijisen lists 蛍石 under ほたる. The card's ほたるいし / けいせき matches JMdict 1794750, and Daijisen does not contradict it.
- **Older form:** 〔螢〕 directly supports "the older character form is 螢".
- **Family scope:** both dictionaries give "general term for the firefly family" (ホタル科…総称). "Insects of the firefly family, not just one particular species" is supported.
- **Glow wording:** Daijisen's ほとんど光らない種も多い is close to "some species do not glow conspicuously". Seisenban's stronger wording (発光する種はわずか, "few species luminesce") is consistent with it.
- **Source lines:** both cards attribute their claims to "Digital Daijisen and Seisenban". Each claim is now traced to the dictionary that supports it:
  - reading allocation and older form: Daijisen;
  - insect scope: both;
  - historical ember and Gion senses: Seisenban only, which is how `words\蛍.md` attributes them.

**Verdicts:**
- **`kanji\蛍.md`:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **`words\蛍.md`:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **`words\蛍光灯.md`:** not re-read and unchanged. The original CLEAN verdicts on all three facets carry over without a fresh check.

**Findings:** none, either originally or in this pass.

**Reconciliation of the original limitation:**
- **Daijisen not read, body appeared to load dynamically: withdrawn.** My statement that the body loaded dynamically was wrong; my earlier raw fetches simply landed at CSS/JS offsets (40000, 90000 and 200000). The Daijisen attribution for reading allocation, the older form and insect scope is now confirmed. No consequential uncertainty remains about the family scope, the light qualification, ケイ versus standalone ほたる, or the source attribution.

**Optional dispositions (all optional, none blocking):**
- **蛍/火 quiz exclusion: optional, retain.** It is a conservative guard based on Seisenban's documented historical leftover-fire sense (②, 小さく消え残った火, "a small fire left smouldering"). It does not claim the words are interchangeable today, and no rule requires removing it. I withdraw the "weak reason" framing as a concern, though the observation stays on record.
- **Expanding "Seisenban" once to 精選版 日本国語大辞典: optional polish.**
- **Glow wording: optional, no change needed.** Daijisen's wording now directly supports the current text, and exhaustive taxonomy is not required.
- **Kanji quiz fallback: optional.** Larger quizzes filling choices by shared tags could show 虫 "insect; bug"; this is a known app limitation. The default four-choice quiz uses the three curated wrong answers 学, 栄 and 営. I claim no larger-quiz behaviour, native behaviour or new exclusion algorithm.

**Limits:**
- **Original process overlap, still disclosed:** in the initial review, one response issued six parallel `view` calls (kanji 光, 灯, 火, 学, 栄, 営), against the one-call rule. This serial confirmation does not make the initial review compliant after the fact.
- **Not read:** the 字通 and 動植物名よみかた辞典 bodies (not needed) and `n1-source-snapshot.json`.
- **Frozen sources:** the dictionary packets are frozen supplied copies, not a fresh upstream retrieval. The Kotobank page is a live fetch from 2026-11-03.
- **Partial inventory:** `confusable-words.md` was searched, not read in full. Cited line numbers are my manual counts.
- **Still outstanding before publication:** actual supported-native acceptance of 螢 versus 蛍 across all four production font families and in the articles. Physical-phone and general-release acceptance also remain outstanding. None of this can be certified from a text review.
