**Both findings are resolved.** No regression was found in the two checks.

1. `kanji/嘆.md:14` directly excludes `悔`, preserves `悲` and `哀`, and exactly matches the ledger at `docs/n1-sources/batch-160-progress.json:490–495`.
2. `words/嗣子.md:34` uses the same canonical Daijisen fragment as `words/画伯.md:34`. The fragment also resolves to the live Daijisen section for 嗣子.

**Verified snapshot:** HEAD `fdf0df122332d39b18c4d36c04e9cde98f591baf`; base `e946e840fcf6fc5f530758d861390af77936cd1e`; binary diff SHA-256 `5d5130a948aa6ec3fc1b51e70b60cea10e77d7afeac4be8a59c2085030f1a999`; manifest content version `25556a8e69ecf82d`.

**Limits:** No broader review or Android runtime testing. No files edited; the diff hash was unchanged.
