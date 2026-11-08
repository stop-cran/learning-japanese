The verdicts I gave still hold at the scale the images were actually delivered, but they rest on downscaled copies, not the original pixels. Every PNG reached me as a 900×2000 rescaled copy of a 1080×2400 original, so nothing I said describes the original pixels.

**Snapshot:** source ba8917b6d35e044bf96d059beb44a7bd7392f2de; teaching unchanged from 08e76c1688ada4898a79e25e13650687dadf65d1; Android build bf30cdead8515739bc0e671d57a54b9a3109dd46. This is a clarification of my own report only. I did no new viewing, reading or editing.

**Scope**
- **Model and session:** Claude Opus 5.5 (claude-opus-5.5), original session eb1a8995-1568-4cd5-b7bb-0a1056233592.
- **Text:** resources 01–09 came back in full, as I reported.
- **Images:** I requested 73 distinct original paths and got 73 successful responses. Each contained the rescaled copy described above, and none was byte-identical to its original. The original file hashes remain intact.
- **What my image observations cover:** they describe those rescaled copies, not the original pixels.
- **Retention:** a successful tool response does not prove the image stayed in every later model request.

**Corrections to my previous report**
- **"word-2-13 is a larger capture of the same scroll state" is withdrawn.** All 73 copies arrived at the same 900×2000 size, so I had no basis for a size difference. All I can say is that word-2-13 looked the same as 09, 10 and 12.
- **Byte hashes and visual states:** the 33 byte-distinct hashes do not show how many distinct visual states exist. My grouping statements only report that the copies looked alike to me.

**Verdicts** (correctness / scoped coverage / comprehensibility, at the delivered scale)
- **The four new articles and three changed passages:** CLEAN / CLEAN / CLEAN still holds. These verdicts come mainly from the text review, which the scaling does not affect, and the rescaled renderings were legible and matched that text.
- **Sampled semantics (128 sets plus the live default):** CLEAN / CLEAN / CLEAN for those samples only. This rests on text evidence, so scaling does not affect it.
- **Four-font rendering and reading/drawing presentation:** CLEAN / CLEAN / CLEAN only within these bounds:
  - In the rescaled copies, 厂 was readable and clearly different from 万, 力, 厚 and 励.
  - All required text was legible and nothing was clipped.
  - The reading keys れい and はげむ and the drawing states could be made out.
  - None of this is approval of the full-resolution images.

**Findings:** none. Automatic scaling alone does not show any glyph or text defect.

**Optional:** unchanged: the three suggestions for `励.md:35`, `激励.md:26` and `励む.md:24`, plus the app-wide wording on the drawing practice screen.

**Limits:** these remain UNVERIFIED:
- original full-resolution pixels, and whether a reader would understand the originals equally well;
- the identity of 厂's fallback font and how readable it is natively;
- physical-phone behaviour, native-speaker review and learning effectiveness;
- arbitrary choice pools, and upstream or Git verification.
