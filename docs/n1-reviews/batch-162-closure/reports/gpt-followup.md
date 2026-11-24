**All four original findings are resolved. No remaining blocker in the corrected passages.** I reviewed `corrections.diff` from `4dcff959` to `338e7b20`; the batch articles are reported unchanged at integrated commit `32ed450b37b8158f5a01bc5cee57d18c8f2aa155`.

| Original finding | Disposition |
|---|---|
| 壮 ↔ 健 quiz overlap | **Resolved.** `kanji/壮.md` adds 健 directly and preserves the existing exclusions. Under the symmetric, non-transitive contract, this protects both directions without a duplicate declaration on 健. |
| 壇 ↔ プラットホーム quiz overlap | **Resolved.** `words/壇.md` adds direct exclusions for both プラットホーム and ステージ, preserving 台 and 舞台. Each pair is protected independently. |
| 塁 reading guidance | **Resolved.** `kanji/塁.md` now teaches both “base” and “fortress” under ルイ, identifies 塁 as a rare spelling of とりで, and uses 塁を守る to show how context distinguishes the two るい senses. |
| 土 and 彫 citations | **Resolved.** `kanji/土.md` adds `1445270` for standalone 土 つち. `kanji/彫.md` removes the unrelated `1497380` and retains `1428070` for 彫塑. |

No consequential regression found in the other edited passages. The 墜ちる/落ちる links and spelling guidance still agree, and 壇 still has a standalone example alongside the new 壇上 example. 彫塑 no longer makes the unsupported “model for a sculpture” claim. The author confirmed that Digital Daijisen explicitly gives classical おつ; I did not independently reopen that entry.

**Limits:** Diff-only follow-up. I did not reread the initial packet, verify the integrated tree, or test quiz behavior on a device.
