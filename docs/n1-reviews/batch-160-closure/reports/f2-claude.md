**Daijisen fragment finding: RESOLVED.**

**Snapshot (all confirmed)**
- HEAD is `fdf0df12…`.
- The binary diff SHA-256 is `5d5130a9…f1a999`, which matches the reviewed value.
- The manifest contains content version `25556a8e69ecf82d`.

**What I checked**
- `words/嗣子.md` now ends its Dictionary line with the Daijisen link `…嗣子-73182#E3.83.87.E3.82.B8.E3.82.BF.E3.83.AB.E5.A4.A7.E8.BE.9E.E6.B3.89`.
- `words/画伯.md` uses the identical fragment, `#E3.83.87.E3.82.B8.E3.82.BF.E3.83.AB.E5.A4.A7.E8.BE.9E.E6.B3.89`, after its own page ID (`画伯-465586`).
- The earlier malformed fragment (`#E3.83.87.E3.82.B8.3.82.BF…`, with `.E3` missing) is gone.

**Limits**
- This was a narrow check of the fragment only. I did not re-read the rest of the diff.
- I did not re-fetch the kotobank page to confirm the anchor scrolls correctly. It is the same canonical format as 画伯, and the page itself resolved earlier.
- No files were edited.
