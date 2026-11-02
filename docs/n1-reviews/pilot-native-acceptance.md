# N1 pilot native gate: partial evidence, not acceptance

Teaching snapshot: `6855b42fa2c4e4cae6fd01a2697d10ee42011abb`.
Android production snapshot: `2bc0234bffcb3c4a0cbafde80367d24d2638a93a`.
No teaching, production app code, algorithms or saved owner-device state changed.
The [two-family textual review](pilot-reconciliation.json) is unchanged.

## What actually ran

A dedicated `emulator-5580` was booted from the existing
`N3_Acceptance_20261029` AVD with `-read-only -no-snapshot -no-window`.
No phone or other emulator was connected at the initial check. All installs
and instrumentation commands explicitly selected this serial. The saved AVD
was not reset, wiped or snapshot-saved.

The emulator was Android 15/API 35, fingerprint
`google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.036/12592187:user/release-keys`,
1080 x 2400, 420 dpi, font scale 1.0, hardware `ranchu`. Host SDK emulator
37.2.12.0/build 16428233 used WHPX. Both initial SwiftShader/Vulkan and the
subsequent SwiftShader GLES run with Vulkan disabled booted and responded.

`N1FallbackInspectionTest.allFortyFallbacksAndPilotRadicals` actually passed
on each API-35 run, each with raw per-test status **0**, not an assumption
skip. The retained evidence is from the second run. It mounts the production
`KanjiFont.family()` choices in native Compose: Gothic, Mincho, Textbook and
Brush. All **40** frozen missing-cmap targets were shown in each family.
Native Paint `hasGlyph` and unique per-character rasters also passed for
all **160** character/family combinations; this alone is not visual acceptance.

The coordinator visually inspected all seven retained screenshots:

| Page | Inspected characters |
| --- | --- |
| [1](pilot-native/n1-font-page-1.png) | 侑 凜 勁 奎 崚 彗 昴 晏 |
| [2](pilot-native/n1-font-page-2.png) | 晟 晨 暉 栞 椰 毬 洵 洸 |
| [3](pilot-native/n1-font-page-3.png) | 滉 漱 澪 熙 燎 燿 瑶 皓 |
| [4](pilot-native/n1-font-page-4.png) | 眸 笙 綸 綺 翔 脩 茉 莉 |
| [5](pilot-native/n1-font-page-5.png) | 菫 詢 諄 赳 迪 頌 颯 黎 |
| [6](pilot-native/n1-font-page-6.png) | 干 氏 手 凵 丿 矛 鳥 彐 |
| [7](pilot-native/n1-font-page-7.png) | 水 木 艸 扌 氵 艹; 凜/凛 and 瑶/瑤 |

No blank, replacement box or materially misleading shape was established
in these renderings. The four bundled/default choices correctly converge
to a system face for the missing subset; that typeface change is not a
defect. The displayed radical/component variants remain recognizable.
The two explicit variant pairs retain visible distinctions. This is bounded
coordinator inspection, not native-speaker certification, exhaustive look-alike
testing, small-phone usability, or coverage of every supported OS/device/font scale.
The immutable cmap inventory remains historical and unmodified;
[per-target native dispositions](pilot-native/native-inspection.json) are separate.

## Navigation and drawing remain unverified

The [external native fixture](pilot-native/N1PilotAcceptanceTest.kt) bundles
the exact committed full Git archive as an instrumentation asset, serves it
through production `ContentSync` using a synthetic source/HEAD, and attempts
the real MainActivity N1 chip, meaning session, linked support article, system
Back and 24-stroke 鷹 drawing/trace-to-recall path. This is not a public-sync test.
The fixture discloses all due-state/meaning-log seeding and never changes
production scheduling. It is an attempted acceptance harness, **not a passing
navigation/drawing receipt**.

The first API-35 navigation execution lost its emulator host process with
Windows exit `-1073741819` (`0xC0000005`). The second environment, with Vulkan
disabled, returned a normal test failure after successful complete import:
the fixture unconditionally requested a scroll action for an already visible
Home node. Its click helper was corrected using the existing native test
pattern. The corrected attempt again lost the emulator host process with the
same exit. Neither truncated instrumentation stream contains a terminal
per-test pass. Host crashes are not attributed to a particular content/app
defect without evidence.

A final bounded alternative used the existing `Grammar_API29` AVD, again
read-only/no-snapshot on the same dedicated port after the earlier process
had exited, with host GLES and Vulkan disabled. Its fingerprint was
`google/sdk_gphone_x86_64/generic_x86_64:10/QSR1.211112.011/13135432:userdebug/dev-keys`,
1080 x 1920, physical 420 dpi/override 480 dpi. The full-archive preflight
failed with an actual `OutOfMemoryError`: reported growth limit **16,777,216
bytes**, before MainActivity launched. `dalvik.vm.heapgrowthlimit` was empty;
`dalvik.vm.heapsize` reported 512m. The discrepancy was not silently repaired
or used to claim a production app memory defect. No heap/manifest/archive
guard was increased, owner AVD configuration edited, or rooting attempted.
The coordinator stopped this own emulator process after recording the result.
Further repeated attempts were not made.

Original raw instrumentation results, including the failures and truncated
attempts, are retained under [pilot-native](pilot-native). A temporary exporter
first failed class discovery because it had accidentally been declared locally;
it was moved to its own file and successfully exported the existing font
artifacts through supported instrumentation status output. Export success
does not convert any navigation failure into a pass.

Some compound host/AVD inspection and adb device-filesystem transfer commands
were permission-denied before execution. No permissions were escalated.
Ordinary explicit-serial APK installation worked. Packaging the exact archive
in test assets and exporting bounded evidence via the test runner avoided the
need for device-filesystem transfer commands. No token, private service
reasoning or raw emulator authentication material is included in these records.

## Recalibration and disposition

The [measured recalibration](../n1-sources/pilot-recalibration.json) records
12 drafted kanji, 5 new and 8 reused support articles, 56 complete dictionary
families, 47 reading dispositions, and a 67,911-byte retained runtime increase.
The local candidate remains **8,097 ZIP entries / 43,383,873 retained /
43,649,907 inflated / 29,774,269 estimated compressed bytes**. The exact local
Git archive used in native testing is separately hashed; neither archive is
an accepted immutable GitHub publication.

Using current pilot mean card/stroke/manifest bytes for the remaining 1,216
undrafted characters gives these **capacity sensitivities, not lexical forecasts**:

| Total new support words | Estimated final entries | Estimated retained MiB |
| --- | --- | --- |
| 5, assuming no further words | 10,529 | 47.014 |
| 512, rounded pilot-ratio sensitivity | 11,036 | 47.908 |
| 1,228, one per character sensitivity | 11,752 | 49.171 |

Unknown future reused-passage changes, larger cards and further support
articles are not bounded by these scenarios. No future compressed/inflated
size promise is inferred from this small sample. Existing 18,000-entry /
42-MiB compressed / 80-MiB inflated / 56-MiB retained guards stay unchanged.

With the 12-card pilot and later batches capped at 15, the floor is **83
batches / 166 initial reviewer assignments**. Caps of 10 or 8 would mean
123/246 or 153/306 respectively; split for actual evidence complexity, not
to meet a quota. The two observed initial processes took 301.177 and
123.732 seconds, with a 39.26-second confirmation. These exclude authoring,
source discovery, native failures, signing, integration and publication.
Five coordinator executions have covered preparation through this partial
native gate. No defensible elapsed-time, AI-credit or exact support-count
forecast follows from these observations. The pilot's unusually many readings
also make a straight full-set effort extrapolation misleading.

**Blocked at the pilot gate.** The shared reading prerequisite remains
unresolved under [content issue #1](https://github.com/stop-cran/learning-japanese/issues/1#issuecomment-6579222017):
12 source-only keys among 41 are still offered across seven pilot cards,
and 漱 loses supported すすぐ to the first-three cap. Metadata/order are
preserved; no companion feature was implemented here.
Native selection/session/article/Back and drawing still need a stable,
supported environment and terminal passing evidence. Real-phone acceptance
remains outstanding. No card is review-closed or published; all 1,228 additions
remain undelivered. Full rollout and any push of this draft branch remain
prohibited at this gate. The accepted-pilot README update and publication
checks must wait for actual acceptance, not be represented as completed.
