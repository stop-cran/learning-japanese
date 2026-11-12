# Mechanical checks (automatic output, not a review verdict)

## lint

```text
kanji checked: 15, words checked: 93
WARN  words/一応.md: Dictionary: line cites no JMdict entry id
WARN  words/威張る.md: Dictionary: line cites no JMdict entry id
WARN  words/嫌い.md: no Dictionary: line
WARN  words/嫌がる.md: Dictionary: line cites no JMdict entry id
WARN  words/平仮名.md: Dictionary: line cites no JMdict entry id
WARN  words/応ずる.md: Dictionary: line cites no JMdict entry id
WARN  words/応対.md: Dictionary: line cites no JMdict entry id
WARN  words/応接.md: Dictionary: line cites no JMdict entry id
WARN  words/応援.md: Dictionary: line cites no JMdict entry id
WARN  words/応用.md: Dictionary: line cites no JMdict entry id
WARN  words/感激.md: Dictionary: line cites no JMdict entry id
WARN  words/振り仮名.md: Dictionary: line cites no JMdict entry id
WARN  words/整う.md: Dictionary: line cites no JMdict entry id
WARN  words/整備.md: Dictionary: line cites no JMdict entry id
WARN  words/整数.md: Dictionary: line cites no JMdict entry id
WARN  words/調整.md: Dictionary: line cites no JMdict entry id
WARN  words/騒々しい.md: Dictionary: line cites no JMdict entry id
0 error(s), 17 warning(s)
```

## unit tests

```text
Exported approved packages only. Validate content, rebuild the manifest and check archive budgets before publishing.
Exported approved packages only. Validate content, rebuild the manifest and check archive budgets before publishing.
Exported approved packages only. Validate content, rebuild the manifest and check archive budgets before publishing.
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 8548, 'entries': 8563, 'retainedBytes': 45175070, 'inflatedBytes': 45446380, 'localZipBytes': 30574492, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot
```

## manifest

```text
manifest.json: 8541 files incl. 400 images, 202 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version 3f0f13d8a00f4fd5
warning: in the working copy of 'manifest.json', LF will be replaced by CRLF the next time Git touches it
```

## android JVM content tests

```text
> Task :core:cleanTest
> Task :core:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :core:compileKotlin UP-TO-DATE
> Task :core:compileJava NO-SOURCE
> Task :core:processResources NO-SOURCE
> Task :core:classes UP-TO-DATE
> Task :core:jar UP-TO-DATE
> Task :core:compileTestFixturesKotlin UP-TO-DATE
> Task :core:compileTestFixturesJava NO-SOURCE
> Task :core:processTestFixturesResources UP-TO-DATE
> Task :core:testFixturesClasses UP-TO-DATE
> Task :core:testFixturesJar UP-TO-DATE
> Task :core:compileTestKotlin UP-TO-DATE
> Task :core:compileTestJava NO-SOURCE
> Task :core:processTestResources UP-TO-DATE
> Task :core:testClasses UP-TO-DATE
> Task :core:test
> Task :app:cleanTestDebugUnitTest
> Task :app:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :app:preBuild UP-TO-DATE
> Task :app:preDebugBuild UP-TO-DATE
> Task :app:generateDebugBuildConfig UP-TO-DATE
> Task :app:checkDebugAarMetadata UP-TO-DATE
> Task :app:processDebugNavigationResources UP-TO-DATE
> Task :app:compileDebugNavigationResources UP-TO-DATE
> Task :app:generateDebugResValues UP-TO-DATE
> Task :app:mapDebugSourceSetPaths UP-TO-DATE
> Task :app:generateDebugResources UP-TO-DATE
> Task :app:mergeDebugResources UP-TO-DATE
> Task :app:packageDebugResources UP-TO-DATE
> Task :app:parseDebugLocalResources UP-TO-DATE
> Task :app:createDebugCompatibleScreenManifests UP-TO-DATE
> Task :app:extractDeepLinksDebug UP-TO-DATE
> Task :app:processDebugMainManifest UP-TO-DATE
> Task :app:processDebugManifest UP-TO-DATE
> Task :app:processDebugManifestForPackage UP-TO-DATE
> Task :app:processDebugResources UP-TO-DATE
> Task :app:kspDebugKotlin UP-TO-DATE
> Task :app:compileDebugKotlin UP-TO-DATE
> Task :app:javaPreCompileDebug UP-TO-DATE
> Task :app:compileDebugJavaWithJavac UP-TO-DATE
> Task :app:bundleDebugClassesToRuntimeJar UP-TO-DATE
> Task :app:bundleDebugClassesToCompileJar UP-TO-DATE
> Task :app:kspDebugUnitTestKotlin UP-TO-DATE
> Task :app:compileDebugUnitTestKotlin UP-TO-DATE
> Task :app:preDebugUnitTestBuild UP-TO-DATE
> Task :app:javaPreCompileDebugUnitTest UP-TO-DATE
> Task :app:compileDebugUnitTestJavaWithJavac NO-SOURCE
> Task :app:mergeDebugShaders UP-TO-DATE
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:mergeDebugAssets UP-TO-DATE
> Task :app:packageDebugUnitTestForUnitTest UP-TO-DATE
> Task :app:processDebugUnitTestManifest UP-TO-DATE
> Task :app:generateDebugUnitTestConfig UP-TO-DATE
> Task :app:processDebugJavaRes UP-TO-DATE
> Task :app:processDebugUnitTestJavaRes UP-TO-DATE
> Task :app:testDebugUnitTest
BUILD SUCCESSFUL in 20s
43 actionable tasks: 4 executed, 39 up-to-date
gradle exit: 0
TEST-io.github.stopcran.kanji.core.RealContentTest.xml: tests=3 failures=0 errors=0 skipped=0
TEST-io.github.stopcran.kanji.core.RareHanTest.xml: tests=1 failures=0 errors=0 skipped=0
```

## quiz safety simulation

```text
ptions from distractors 2/3 (rest filled from other cards)
    reading もと     (kun): wrong options from distractors 2/3 (rest filled from other cards)
応 (respond; comply)  options: wide, spacious | government agency | Europe (abbreviation)
    reading オウ     (on): wrong options from distractors 2/3 (rest filled from other cards)
仮 (temporary; assumed)  options: plank; board | slope; incline | give back; repay
    reading カ      (on): wrong options from distractors 3/3 (rest filled from other cards)
基 (foundation; basis)  options: period; term | mold; type | intuition; hunch
    reading キ      (on): wrong options from distractors 3/3 (rest filled from other cards)
    reading もと     (kun): wrong options from distractors 1/3 (rest filled from other cards)
価 (worth; price)  options: temporary; assumed | west | transform
    reading カ      (on): wrong options from distractors 1/3 (rest filled from other cards)
激 (intense; excite)  options: shoot; strike | drip; drop | rinse the mouth; gargle
    reading ゲキ     (on): wrong options from distractors 1/3 (rest filled from other cards)
    reading はげ.しい  (kun): wrong options from distractors 2/3 (rest filled from other cards)
嫌 (dislike; suspicion)  options: combine; concurrent roles | test; verify | liking; favorable
    reading ゲン     (on): wrong options from distractors 1/3 (rest filled from other cards)
    reading きら.う   (kun): wrong options from distractors 3/3 (rest filled from other cards)
    reading きら.い   (kun): wrong options from distractors 3/3 (rest filled from other cards)
    reading いや     (kun): wrong options from distractors 3/3 (rest filled from other cards)
縮 (shrink; contract)  options: lodging | achievements; results | group; assemble
    reading シュク    (on): wrong options from distractors 2/3 (rest filled from other cards)
    reading ちぢ.む   (kun): wrong options from distractors 2/3 (rest filled from other cards)
    reading ちぢ.める  (kun): wrong options from distractors 2/3 (rest filled from other cards)
    reading ちぢ.れる  (kun): wrong options from distractors 2/3 (rest filled from other cards)
騒 (make noise; uproar)  options: test; verify | station; remain | sweep; brush
    reading ソウ     (on): wrong options from distractors 3/3 (rest filled from other cards)
    reading さわ.ぐ   (kun): wrong options from distractors 2/3 (rest filled from other cards)
    reading さわ.がしい (kun): wrong options from distractors 2/3 (rest filled from other cards)
統 (unify; lineage)  options: allot; fill | practice; refine | paper
    reading トウ     (on): wrong options from distractors 3/3 (rest filled from other cards)
級 (grade; school class)  options: inhale; suck in | handle; deal with | pay; bestow
    reading キュウ    (on): wrong options from distractors 0/3 (rest filled from other cards)
整 (put in order; adjust)  options: politics | respect; honor | failure; defeat
    reading セイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
    reading ととの.う  (kun): wrong options from distractors 3/3 (rest filled from other cards)
暖 (warm; warm up)  options: dark | step; level | converse; consult
    reading ダン     (on): wrong options from distractors 2/3 (rest filled from other cards)
    reading あたた.かい (kun): wrong options from distractors 1/3 (rest filled from other cards)
    reading あたた.まる (kun): wrong options from distractors 1/3 (rest filled from other cards)
    reading あたた.める (kun): wrong options from distractors 1/3 (rest filled from other cards)
existing cards that fall back to tag-similar options: 11
    人 (person) curated slots used 2/3
    休 (rest) curated slots used 2/3
    何 (what) curated slots used 2/3
    入 (enter, put in) curated slots used 2/3
    出 (go out, exit) curated slots used 2/3
    口 (mouth) curated slots used 2/3
    女 (woman, female) curated slots used 2/3
    日 (sun, day) curated slots used 2/3
    月 (moon, month) curated slots used 2/3
    男 (man, male) curated slots used 2/3
    買 (buy) curated slots used 2/3
0 error(s), 0 warning(s)
```
