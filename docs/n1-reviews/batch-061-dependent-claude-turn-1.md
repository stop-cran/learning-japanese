The first slice of the lexical XML (lines 1–140) supports the original conclusions. It shows nothing that bears on the teaching, and I have no new findings. This is turn 1 of 4: one tool call, no other resources.

**Snapshot:** The frozen teaching snapshot is `2567f5e7b3888f2df3ed560f618341266b471902`. You reported an empty runtime teaching/manifest diff against HEAD `928a12f3796714edd74116fe5ac49b06f31d839c`. I can't check Git myself.

**Scope:** Claude Opus 5.5 (`claude-opus-5.5`), same session as the original review. This is a dependent confirmation, not a new blind review. I made exactly one call this turn: `docs\n1-sources\batch-061-jmdict.xml`, lines 1–140.

**Entries seen in this slice:**
- **Complete (8):**
  - 1471890 俳画/はいが — "briefly drawn picture; haiku picture".
  - 1471900 俳句/はいく — common-word markers ichi1/news1/nf05. One sense: "haiku", explained as a "17-mora poem, usu. in 3 lines of 5, 7 and 5 morae".
  - 1471910 俳号/はいごう — haiku poet's pseudonym.
  - 1471920 俳人/はいじん — haiku poet.
  - 1471930 俳聖/はいせい — famous haiku poet; Basho.
  - 1471940 俳壇/はいだん — the world of haiku.
  - 1471950 俳文/はいぶん — prose with a haiku flavour.
  - 1471960 俳味/はいみ — refined taste; haiku flavour.
- **Pending (1):** 1471970 俳優/はいゆう. Lines 1–140 show the spelling and reading with markers ichi1/news1/nf03 and stop at the opening `<sense>` tag. Its senses need confirming next turn.
- **Restrictions and labels:** none of the complete entries has a reading restriction, a sense limited to one spelling, or a usage label. Each has one spelling and one reading.

**Verdicts (this slice only):**
- **Lexical identity and reading of 俳句:** consistent with `kanji\俳.md` and `words\俳句.md`. The articles teach the morae with stated exceptions and qualify the three-line layout as a convention ("usu." in the source), so they don't treat it as a fixed rule.
- **Identity, spelling and reading of 俳優:** consistent with `kanji\俳.md`, `words\俳優.md` and `kanji\優.md`. Its senses remain pending.
- **Other complete entries:** not taught as examples, which is acceptable.

I'm not closing the whole packet yet: that waits for turn 4.

**Findings:** None in this slice.

**Optional:** None new. The original four optional suggestions stay nonblocking and are not reopened.

**Limits:**
- **Earlier process violations still stand (audit 061-P1/P2):**
  - 061-P1: one original response sent three view calls at once, with two overlapping starts, reading lexical lines 150–300, 300–450 and 450–487.
  - 061-P2: fourteen calls each returned 151 lines, over the 150-line limit.

  The initial review did not strictly comply with the read rules.
- **Packet coverage:** 22 of the 30 lexical families and lines 141–487 are not confirmed in this sequence.
- **Lookup limits:** the original public-lookup limits still apply. No Daijisen definition text was returned, and the haiku and actor pages came through as truncated or encyclopedia material. Modern 俳優 identity rests on frozen JMdict entry 1471970.
- **Nothing else retrieved or tested:** no new upstream retrieval, and no native-speaker, phone, rendering, drawing or runtime acceptance.
