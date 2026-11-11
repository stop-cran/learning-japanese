# Mechanical checks (automatic output, not a review verdict)

## lint

```text
kanji checked: 15, words checked: 18
WARN  words/撮る.md: no Dictionary: line
0 error(s), 1 warning(s)
```

## unit tests

```text
----------------------------------------------------------------------
Ran 431 tests in 57.005s
OK
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 8518, 'entries': 8533, 'retainedBytes': 45035085, 'inflatedBytes': 45306395, 'localZipBytes': 30511270, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot
```

## manifest

```text
manifest.json: 8511 files incl. 400 images, 202 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version a4c36b5e19e5e105
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
BUILD SUCCESSFUL in 16s
43 actionable tasks: 4 executed, 39 up-to-date
gradle exit: 0
TEST-io.github.stopcran.kanji.core.RealContentTest.xml: tests=3 failures=0 errors=0 skipped=0
TEST-io.github.stopcran.kanji.core.RareHanTest.xml: tests=1 failures=0 errors=0 skipped=0
```

## quiz safety simulation

```text
催 (host an event; sponsor)  options: employ; hire | tilt; incline | gather
    reading サイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
    reading もよお.す  (kun): wrong options from distractors 3/3 (rest filled from other cards)
促 (urge; prompt)  options: foot, leg | fast | side
    reading ソク     (on): wrong options from distractors 0/3 (rest filled from other cards)
摩 (rub; chafe)  options: horse | seat; place | grove; woodland
    reading マ      (on): wrong options from distractors 3/3 (rest filled from other cards)
擦 (scrape; scrub)  options: observe; infer | edge; occasion | festival; ritual; worship
    reading サツ     (on): wrong options from distractors 2/3 (rest filled from other cards)
    reading こす.る   (kun): wrong options from distractors 2/3 (rest filled from other cards)
括 (tie together; enclose)  options: lively | talk, speak | extract
    reading カツ     (on): wrong options from distractors 2/3 (rest filled from other cards)
弧 (arc; curved line)  options: pull; draw | weak; frail | strong
    reading コ      (on): wrong options from distractors 3/3 (rest filled from other cards)
抵 (resist; collide)  options: low; lower in height | bottom; base | embrace
    reading テイ     (on): wrong options from distractors 1/3 (rest filled from other cards)
抗 (defy; oppose)  options: navigate; sail; fly | extract | skill; technique
    reading コウ     (on): wrong options from distractors 2/3 (rest filled from other cards)
撮 (photograph; film)  options: most | touch; join | throw
    reading サツ     (on): wrong options from distractors 3/3 (rest filled from other cards)
    reading と.る    (kun): wrong options from distractors 3/3 (rest filled from other cards)
影 (shadow; silhouette)  options: scenery | shape; form | capital
    reading エイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
    reading かげ     (kun): wrong options from distractors 2/3 (rest filled from other cards)
攻 (attack; go on the offensive)  options: merit; achievement | release | failure; defeat
    reading コウ     (on): wrong options from distractors 2/3 (rest filled from other cards)
    reading せ.める   (kun): wrong options from distractors 2/3 (rest filled from other cards)
撃 (shoot; strike)  options: throw | kill | establish; provide
    reading ゲキ     (on): wrong options from distractors 3/3 (rest filled from other cards)
掲 (put up; display; publish)  options: scenery | loss; damage | dig; excavate
    reading ケイ     (on): wrong options from distractors 2/3 (rest filled from other cards)
批 (criticize; critique)  options: sadness | grow tired | cover; incur
    reading ヒ      (on): wrong options from distractors 0/3 (rest filled from other cards)
択 (select; opt for)  options: station | translate; explanation | residence
    reading タク     (on): wrong options from distractors 2/3 (rest filled from other cards)
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
