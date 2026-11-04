The finding from my initial review is **resolved** at `ca54f1e`. Both articles are now CLEAN on all three facets, and no new defect or regression turned up.

```text
Snapshot: Revised signed teaching snapshot ca54f1e910522d76f42732fa10ee1a8a6ef1359f; the initial snapshot was
  07b359ca4fb55dbcb7623ee96c71c958385d28b8. The coordinator says the commits were checked in Git; I have no
  shell and could not check them myself. The supplied diff changes only kanji\匁.md (the め row and the first
  Notes bullet) and manifest.json (contentVersion and the 匁.md hash). I did not check the hash values.

Scope: claude-opus-5.5, in the same session as the initial review (b90bb59d-8135-4296-afb4-60732512ce23).
  This is a bounded check that depends on my earlier review, not a fresh blind initial review.
  I read once each:
  - my initial report (1-85)
  - the diff (1-44)
  - the revised kanji\匁.md (1-47)
  - the unchanged words\匁.md (1-34)
  - batch-051-jmdict.xml (1-63)
  - batch-051-me.html (1860-1862 and 1876-1888)
  - the Nikkoku section of batch-051-kotobank-monme.html (1384-1396)
  I checked all three facets in both articles, covering the changed passages and anything they could affect.

Verdicts:
  kanji\匁.md — correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
  words\匁.md — correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.

Findings:
  Original finding 1 (Minor; correctness; kanji\匁.md:31, 41) — RESOLVED.
  - Line 31 now gives both JMdict flags, each at the right level:
    - "archaic" is the sense-level misc tag on the entry's only sense.
    - "irregular kana usage" is the re_inf on the ひゃくめ reading (batch-051-jmdict.xml lines 11-18).
    - The text calls this "an unusual spelling–reading pairing". That is a fair learner-level gloss of the flag
      on this entry.
  - Line 41 now says that Japanese dictionaries write the shortened unit as 目 (め), and that it is a unit use,
    not "eye". The evidence supports this:
    - Nikkoku ① says 「略して、『目(め)』という」.
    - The Daijisen heading め【目／眼】 (line 1860) has 接尾 sense 4: 「数を表す語に付いて、匁(もんめ)の意を表す。
      『百―』『一貫―』」 (line 1888).
  - The revision rightly leaves out my original remedy's word "usually". Neither source gives frequency
    evidence, so I withdraw that wording from the remedy.
  - "Do not assume that shortened め can freely replace もんめ after every number" is still there. It matches
    the evidence, which shows the suffix only in specific listed expressions, not as a free pattern.
  No new findings.

  Regressions checked:
  - Metadata is unchanged: kunyomi [もんめ, め], quizOnyomi [], quizKunyomi [もんめ], and the three wrong
    choices 久/文/包.
  - The もんめ row and its link are unchanged.
  - words\匁.md is unchanged. Its line 32 ("a documented shortening in unit expressions") still agrees with the
    revised card.
  - The links between the kanji card and the word article remain in both directions.

Optional: Every optional item from the initial review stays optional, and none becomes a requirement:
  1. Hedged Shinjigen (文 + katakana メ) and Nipponica (泉) shape-origin accounts: optional; not adopted.
  2. Line 24's "shape differs from the standalone radical" wording: optional; unchanged.
  3. Adding the 目 spelling to words\匁.md:32: optional. My earlier "usually written 目" wording is withdrawn
     because it has no frequency evidence.
  4. The 文目 spelling and its origin: optional.
  5. The type: wago rationale: optional.
  6. 花いちもんめ: optional.

Limits:
  - Corrections to my initial report's process claims:
    - My initial claim of "strictly one tool call per response" was wrong. I issued the content-format 161-180
      and jlpt-levels 1-160 views together in one response. That overlap is a deviation I am recording here.
    - My first me.html read gave complete lines only up to 1875 and cut off partway through 1876. The follow-up
      started at 1877, so the initial review had a gap. This session read all of line 1876.
    - The prompt calls line 1876 sense 13. In the file as I read it, line 1876 is Daijisen 目 sense 11 (saw
      teeth and file grooves), and sense 13 is on line 1878. It is unrelated to the unit sense either way; the
      unit sense is on line 1888, which both sessions read.
  - In this session I made exactly one view call per response.
  - All sources were supplied saved copies, not fresh retrievals. I made no web_fetch calls and did no search.
  - The Japanese dictionary pages show the 目 suffix and the 百― example. I did not separately confirm a
    Japanese dictionary headword spelled 百匁; that pair rests on frozen JMdict 1488550.
  - This is a textual review only. No native-speaker, device, physical-phone, fresh Android or publication
    evidence was supplied, and none is certified here. Compatible Android f9b59a2+ remains required;
    physical-phone and general-release acceptance remain outstanding.
```
