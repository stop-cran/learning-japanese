# B162: review and integration

All three initial reviewers saw the same 19 new articles at `4dcff959`, the full reused 落ちる article, the seven reused-article diffs and the same source packet. They ran one at a time, without access to one another's findings. Each resumed their own session to check [the corrections](https://github.com/stop-cran/learning-japanese/compare/4dcff959aaa5394e35342e11b9f2c48d846f395e...338e7b203854e34c786a365d75083a4696952a92). See the [report index](provenance.json) for response models, hashes and scope. Follow-ups confirmed the changes; they were not fresh readings of the entire deck.

| Finding | Disposition |
|---|---|
| 塁: fortification presented only through the uncommon spelling of とりで | Resolved. The ルイ row gives both senses of 塁 (1555910); the kun row gives 砦 first and marks 塁 rare for とりで (1295240). Daijisen's 塁 entry gives `―を守る` in its fortification sense. |
| 墜 and 落ちる: implied restriction and unclear use of outside-table reading | Resolved. 墜ちる is another spelling, not a separate verb or a spelling restricted by JMdict to aircraft. The ordinary model remains 落ちる. The on-reading is illustrated with 墜落, not offered without a corresponding mapped article. Daijisen's おちる entry identifies classical おつ. |
| 彫塑: unsupported or unclear scope of “model for a sculpture” | Resolved by narrowing the teaching to a clay model vs. the field of sculpture. No claim about relative everyday frequency was added on the strength of priority tags. |
| Outside-table readings, 塚 scope, 開墾 gloss and 壮大 grammar | Resolved. 塁, 墜, 墾 and 壮 identify the relevant kun-readings. The 塚 word card limits the mound explanation to the examples and mentions the stone marker sense. 開墾 introduces the dictionary gloss before explaining it. 壮大 distinguishes attributive な from predicative だ. |
| 壇 examples and overlapping labels | Resolved. The word now illustrates 壇上 and stepping down from the platform; Daijisen explicitly exemplifies the latter. 壇 excludes プラットホーム and ステージ as direct pairs. 壮 excludes 健, whose displayed title also says “robust.” |
| Conditional concern over exclusions being declared on one side only | Withdrawn: the [format contract](../../content-format.md#quiz-authoring) protects both directions of a declared pair but does not make exclusions transitive. No blanket reverse declarations were added. |
| 土 and 彫 citation identities | Resolved. 土 cites the standalone つち family 1445270; 彫 describes the part of 浮き彫り within that word and cites its full family without attributing it to the standalone noun 浮き. |

Optional extensions (such as another baseball position, a full clay-model sentence or Kofun-period background) were not necessary to teach the chosen senses. No consequential finding remains open. The reports distinguish external entries the author inspected from evidence the reviewers inspected themselves.

Selection used `2eb37d43`. Upstream then changed 入, 出入り, 取り出す and 回り道. The merge at `32ed450b` preserved their upstream Git blobs and all 38 corrected batch article/stroke/tool blobs; only the generated manifest overlapped. The auditor compares the integrated runtime with `491ecfd9`, not with the obsolete selection base. This establishes source and package consistency, not native-speaker, Android or phone acceptance.
