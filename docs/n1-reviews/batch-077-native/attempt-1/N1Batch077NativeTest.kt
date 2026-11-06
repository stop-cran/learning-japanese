package io.github.stopcran.kanji.ui

import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.Typeface
import android.net.ConnectivityManager
import android.os.Build
import androidx.activity.ComponentActivity
import androidx.compose.foundation.layout.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.asAndroidBitmap
import androidx.compose.ui.semantics.SemanticsActions
import androidx.compose.ui.semantics.SemanticsProperties
import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.junit4.createEmptyComposeRule
import androidx.compose.ui.text.TextLayoutResult
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.res.ResourcesCompat
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel
import androidx.room.withTransaction
import androidx.test.core.app.ActivityScenario
import androidx.test.platform.app.InstrumentationRegistry
import io.github.stopcran.kanji.KanjiApp
import io.github.stopcran.kanji.MainActivity
import io.github.stopcran.kanji.R
import io.github.stopcran.kanji.core.content.ContentParser
import io.github.stopcran.kanji.core.content.RepoSource
import io.github.stopcran.kanji.core.reading.ReadingKind
import io.github.stopcran.kanji.core.srs.KanjiFont
import io.github.stopcran.kanji.core.srs.StudyMode
import io.github.stopcran.kanji.data.*
import kotlinx.coroutines.runBlocking
import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.*
import org.junit.Rule
import org.junit.Test
import java.io.ByteArrayInputStream
import java.io.File
import java.security.MessageDigest
import java.util.UUID

private fun disposable077() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch077GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun bravingRiskLookalikesAndRadicalFallbacksAcrossFourProductionFamilies() {
        disposable077()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("供 侵 備 冂 冒 危 壊 好 子 官 害 山 店 必 損 攻 旅 日 準 物 犯 病 登 目", "罪 行 被 要 語 道 開 阜 阝 限 院 険 頭 馬 験", "冒 日 目 官 冂 阜 阝 険 犯 侵 冒険 冒す")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 077: braving risk / look-alikes / radical fallback")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 39 scoped Han; focused 冒/日/目/官, 冂 and 阜/阝. Fallback families may coincide.", fontSize = 16.sp)
                }
            }
        }
        val typefaces = listOf(Typeface.DEFAULT,
            requireNotNull(ResourcesCompat.getFont(context, R.font.kanji_mincho)),
            requireNotNull(ResourcesCompat.getFont(context, R.font.kanji_textbook)),
            requireNotNull(ResourcesCompat.getFont(context, R.font.kanji_brush)))
        val rows = JSONArray()
        for ((index, typeface) in typefaces.withIndex()) {
            val hashes = mutableSetOf<String>()
            for (char in listOf("供", "侵", "備", "冂", "冒", "危", "壊", "好", "子", "官", "害", "山", "店", "必", "損", "攻", "旅", "日", "準", "物", "犯", "病", "登", "目", "罪", "行", "被", "要", "語", "道", "開", "阜", "阝", "限", "院", "険", "頭", "馬", "験")) {
                val paint = Paint(Paint.ANTI_ALIAS_FLAG).also {
                    it.typeface = typeface
                    it.textSize = 96f
                    it.textLocale = java.util.Locale.JAPAN
                }
                assertTrue("$char ${fonts[index]}", paint.hasGlyph(char))
                val image = Bitmap.createBitmap(if (char.length > 1) 256 else 128, 128, Bitmap.Config.ARGB_8888)
                Canvas(image).drawText(char, 8f, 104f, paint)
                val pixels = IntArray(image.width * image.height)
                image.getPixels(pixels, 0, image.width, 0, 0, image.width, image.height)
                assertTrue(pixels.any { it != 0 })
                val bytes = java.nio.ByteBuffer.allocate(pixels.size * 4)
                    .also { it.asIntBuffer().put(pixels) }.array()
                val hash = MessageDigest.getInstance("SHA-256").digest(bytes)
                    .joinToString("") { "%02x".format(it) }
                assertTrue("Indistinguishable raster ${fonts[index]}", hashes.add(hash))
                rows.put(JSONObject().put("character", char).put("font", fonts[index].name)
                    .put("hasGlyph", true).put("nativePaintRasterSha256", hash))
                image.recycle()
            }
            for (word in listOf("冒険", "冒す")) {
                val paint = Paint(Paint.ANTI_ALIAS_FLAG).also {
                    it.typeface = typeface
                    it.textSize = 96f
                    it.textLocale = java.util.Locale.JAPAN
                }
                // hasGlyph tests multi-character ligatures, not ordinary word coverage.
                val image = Bitmap.createBitmap(kotlin.math.ceil(paint.measureText(word)).toInt() + 16, 128, Bitmap.Config.ARGB_8888)
                Canvas(image).drawText(word, 8f, 104f, paint)
                val pixels = IntArray(image.width * image.height)
                image.getPixels(pixels, 0, image.width, 0, 0, image.width, image.height)
                for (position in word.indices) {
                    val left = (8f + paint.measureText(word, 0, position)).toInt()
                    val right = kotlin.math.ceil(8f + paint.measureText(word, 0, position + 1)).toInt()
                    assertTrue("Word raster bounds $word ${fonts[index]}", left >= 0 && right <= image.width && left < right)
                    assertTrue("Blank word character ${word[position]} ${fonts[index]}",
                        (0 until image.height).any { y -> (left until right).any { x -> pixels[y * image.width + x] != 0 } })
                }
                val bytes = java.nio.ByteBuffer.allocate(pixels.size * 4)
                    .also { it.asIntBuffer().put(pixels) }.array()
                val hash = MessageDigest.getInstance("SHA-256").digest(bytes)
                    .joinToString("") { "%02x".format(it) }
                rows.put(JSONObject().put("word", word).put("font", fonts[index].name)
                    .put("renderedCharactersNonblank", word.length).put("nativePaintRasterSha256", hash))
                image.recycle()
            }
        }
        assertEquals(164, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-077-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-077-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 156).put("wholeWordRasterProbes", 8).put("panels", 3)
            .put("limits", "39 scoped Han including metadata-only 攻 and pending 冂/阝 fallback inspection, four production families, three bounded Compose panels and eight whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch077ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineBravingRiskThreeReciprocalPairsBothReadingsDrawingAndSystemBack() {
        disposable077()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-077-${UUID.randomUUID()}", "main")
        val head = "46dff1466ac9f3cf64b54e197c05088414939896"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-077-46dff146-envelope.zip")
                }
                else -> error("Unexpected fixture request: $url")
            }
            object : ContentResponse {
                override val code = 200
                override val body = input
                override fun header(name: String): String? = null
                override fun close() = input.close()
            }
        }
        val result = runBlocking { ContentSync(app.db, app.settings.sync, http).sync(source, force = true) }
        assertTrue(result.toString(), result is SyncResult.Updated)
        val updated = result as SyncResult.Updated
        assertEquals(1, archiveRequests)
        assertEquals(1089, updated.kanji)
        assertEquals(5046, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("2944928c13e2165a", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(109, n1.size)
        val bravingRisk = n1.single { it.kanji == "冒" }
        assertEquals(listOf("ボウ"), bravingRisk.onyomi.splitSep())
        assertEquals(listOf("おか.す"), bravingRisk.kunyomi.splitSep())
        assertNotNull(bravingRisk.quizOnyomi)
        assertNotNull(bravingRisk.quizKunyomi)
        assertEquals(listOf("ボウ"), bravingRisk.quizOnyomi?.splitSep())
        assertEquals(listOf("おか.す"), bravingRisk.quizKunyomi?.splitSep())
        assertEquals(listOf("ぼう"), bravingRisk.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(listOf("おかす"), bravingRisk.toReadingCard().quizKeys(ReadingKind.Kun))
        val now = System.currentTimeMillis()
        app.settings.sync.lastCheckMs = now
        app.settings.setStartingGuideVisible(false)
        app.settings.setDailyNewCards(50)
        app.settings.setWeekPlan("FFFFFFF")
        app.settings.setTraceNew(true)
        app.settings.setVaryFonts(true)
        app.settings.setStack("jlpt-n5")
        runBlocking {
            app.db.withTransaction {
                n1.forEach { card ->
                    app.db.reviews().putState(ReviewStateEntity(
                        source.id, "jlpt-n1", card.kanji, StudyMode.Quiz.name, "Review", 30.0, 5.0,
                        if (card.kanji == "冒") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "冒" && ((kind == ReadingKind.On && key == "ぼう") || (kind == ReadingKind.Kun && key == "おかす"))) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "冒", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(bravingRisk.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(bravingRisk.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(bravingRisk.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(bravingRisk.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(bravingRisk.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(bravingRisk.quizKunyomi).splitSep()))
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 冒 meaning and both complete curated readings due. Two historical good 冒 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 109 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("冒")
            click("brave danger; venture")
            await("冒 — brave danger; venture")
            show(articleBullet("Strokes: 9 · Key (radical): 冂 (the outer outline of the upper part, no. 13) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("冒 expresses braving danger or venturing despite difficulty in 冒す (おかす) and 冒険 (ぼうけん), \"adventure; risky venture.\" It is not a general label for anything dangerous: 危険 (きけん) names danger, while 危険を冒す (きけんをおかす) means taking a risk."), "kanji-03")
            show(articleBullet("Modern-shape mnemonic: picture an eye, 目, beneath a boxlike upper outline, looking ahead despite danger. This is a memory aid, not a historical sun-plus-eye explanation. The classical indexing radical is 冂, not 日, even though the upper shape can resemble 日."), "kanji-04")
            section("Readings")
            show(articleBullet("Both complete source readings are retained and selected for reading practice."), "kanji-06")
            show(readingExample("ボウ"), "kanji-10")
            show(readingExample("冒険 ぼうけん — adventure; risky venture"), "kanji-12")
            show(readingExample("おか.す"), "kanji-13")
            show(readingExample("冒す おかす — brave danger; 危険を冒す きけんをおかす — take a risk"), "kanji-15")
            section("Common words")
            show(articleBullet("冒険 ぼうけん — adventure; risky venture"), "kanji-17")
            show(articleBullet("冒す おかす — brave danger; venture despite difficulty"), "kanji-18")
            show(articleBullet("冒頭 (ぼうとう) — beginning; opening"), "kanji-19")
            section("Notes")
            show(articleBullet("Do not force the risk-taking gloss into every compound: 冒頭 names an opening, not an adventure. 冒す also has a harm/affliction sense: 病に冒される (やまいにおかされる), \"be afflicted by a disease,\" is passive, not someone choosing to take a risk."), "kanji-21")
            show(articleBullet("犯 also has the reading おか.す, but 犯す is used for committing an offense, as in 罪を犯す (つみをおかす), \"commit a crime.\" 侵す (おかす) concerns invading or infringing and can overlap with 冒す in harm/affliction uses. These are useful spelling distinctions, not perfectly separate meaning compartments. For shape comparison, 官 has a roof and a different connected lower outline; neither 官 nor 目 means braving danger."), "kanji-22")
            show(articleBullet("Metadata: KANJIDIC2. Dictionary: JMdict, entries 1519820, 1519830, 1519860, 1855070, 1868850, 1359800 and 1481550. Reading and meaning branches: Digital Daijisen: 冒; spelling overlap: Digital Daijisen: 冒す."), "kanji-23")
            section("Common words")
            show(articleBullet("冒す おかす — brave danger; venture despite difficulty"), "冒す-forward-14")
            inline(await(articleBullet("冒す おかす — brave danger; venture despite difficulty")), "冒す", 0)
            await("Article contents")
            await("冒す (おかす) — brave danger; take a risk")
            section("Meaning")
            show(articleBullet("冒す means braving danger or proceeding despite a known difficulty. In 危険を冒す (きけんをおかす), \"take a risk,\" を marks the danger being faced. It is a transitive verb, not a noun meaning an adventure."), "冒す-02")
            show(articleBullet("危険を冒して山に登りました。 (きけんをおかしてやまにのぼりました。) — I climbed the mountain despite the danger."), "冒す-03")
            show(articleBullet("危険を冒す必要はありません。 (きけんをおかすひつようはありません。) — There is no need to take a risk."), "冒す-04")
            show(articleBullet("The second sentence says that taking the risk is unnecessary; it does not say that the situation is safe."), "冒す-05")
            section("How the kanji combine")
            show(articleBullet("冒 writes おか, with す as okurigana. There is no second kanji to read as a compound. This is a godan verb: 冒します (おかします), 冒して (おかして), 冒さない (おかさない)."), "冒す-07")
            section("Synonyms and antonyms")
            show(articleBullet("冒険 (ぼうけん) is the related noun \"adventure; risky venture\"; 冒険する means to venture or have an adventure. 危険 (きけん) names danger, whether or not anyone chooses to face it. Avoiding danger contrasts with braving it, but 冒す has other senses too, so no single opposite covers every use."), "冒す-09")
            section("Distinctive meaning")
            show(articleBullet("Do not translate every occurrence as voluntarily taking a risk. 病に冒される (やまいにおかされる), \"be afflicted by a disease,\" uses the passive of the harm/affliction sense. Here the person is affected by the illness, not choosing to brave it. This sense can also concern harmful chemicals. The dictionary also records desecrating something sacred and assuming someone else's surname; these are separate senses, not explanations of 危険を冒す."), "冒す-11")
            show(articleBullet("Two other verbs share the reading おかす. 犯す, written with 犯, is used in 罪を犯す (つみをおかす), \"commit a crime.\" 侵す concerns invading or infringing and also has a harm/affliction use overlapping with 冒す. Choose the spelling from the expression and meaning, not from the sound alone; this comparison is not an absolute division of every use."), "冒す-12")
            show(articleBullet("Dictionary: JMdict, entries 1519820 (senses 1–4), 1868850, 1855070, 1519830, 1218560, 1359800 and 1481550. Spelling and usage: Digital Daijisen: 冒す."), "冒す-13")
            section("How the kanji combine")
            show(articleBullet("冒 writes おか, with す as okurigana. There is no second kanji to read as a compound. This is a godan verb: 冒します (おかします), 冒して (おかして), 冒さない (おかさない)."), "冒す-reverse-24")
            inline(await(articleBullet("冒 writes おか, with す as okurigana. There is no second kanji to read as a compound. This is a godan verb: 冒します (おかします), 冒して (おかして), 冒さない (おかさない).")), "冒", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("ボウ"), "冒す-kanji-backlink")
            back()
            await(articleBullet("冒 writes おか, with す as okurigana. There is no second kanji to read as a compound. This is a godan verb: 冒します (おかします), 冒して (おかして), 冒さない (おかさない).")).assertIsDisplayed()
            section("How the kanji combine")
            capture("冒す-system-back-to-word")
            back()
            await(articleBullet("冒す おかす — brave danger; venture despite difficulty")).assertIsDisplayed()
            section("Common words")
            capture("冒す-system-back-to-kanji")
            section("Common words")
            show(articleBullet("冒険 ぼうけん — adventure; risky venture"), "冒険-forward-25")
            inline(await(articleBullet("冒険 ぼうけん — adventure; risky venture")), "冒険", 0)
            await("Article contents")
            await("冒険 (ぼうけん) - adventure; risky venture")
            section("How the kanji combine")
            show(articleBullet("冒 contributes braving or venturing, while 険 contributes danger or difficulty. The relationship is roughly venturing into danger. The on readings are ボウ + ケン."), "冒険-07")
            section("How the kanji combine")
            show(articleBullet("冒 contributes braving or venturing, while 険 contributes danger or difficulty. The relationship is roughly venturing into danger. The on readings are ボウ + ケン."), "冒険-reverse-27")
            inline(await(articleBullet("冒 contributes braving or venturing, while 険 contributes danger or difficulty. The relationship is roughly venturing into danger. The on readings are ボウ + ケン.")), "冒", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("ボウ"), "冒険-kanji-backlink")
            back()
            await(articleBullet("冒 contributes braving or venturing, while 険 contributes danger or difficulty. The relationship is roughly venturing into danger. The on readings are ボウ + ケン.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("冒険-system-back-to-word")
            section("How the kanji combine")
            show(articleBullet("冒 contributes braving or venturing, while 険 contributes danger or difficulty. The relationship is roughly venturing into danger. The on readings are ボウ + ケン."), "冒険-険-28")
            inline(await(articleBullet("冒 contributes braving or venturing, while 険 contributes danger or difficulty. The relationship is roughly venturing into danger. The on readings are ボウ + ケン.")), "険", 42)
            await("Article contents")
            show(articleBullet("Strokes: 11 · Key (radical): 阜 (as left-hand 阝, no. 170) · JLPT: N3 (community list)"), "険-fallback-01")
            section("Meaning and origin")
            show(articleBullet("険 occurs in steep or difficult terrain and in danger-related words. 険しい けわしい can describe a steep, rugged route; 危険 きけん means danger or dangerous. 冒険 ぼうけん names an adventure or venture."), "険-counterpart-30")
            inline(await(articleBullet("険 occurs in steep or difficult terrain and in danger-related words. 険しい けわしい can describe a steep, rugged route; 危険 きけん means danger or dangerous. 冒険 ぼうけん names an adventure or venture.")), "冒険", 147)
            await("Article contents")
            section("How the kanji combine")
            show(articleBullet("冒 contributes braving or venturing, while 険 contributes danger or difficulty. The relationship is roughly venturing into danger. The on readings are ボウ + ケン."), "冒険-険-component-backlink")
            back()
            await(articleBullet("険 occurs in steep or difficult terrain and in danger-related words. 険しい けわしい can describe a steep, rugged route; 危険 きけん means danger or dangerous. 冒険 ぼうけん names an adventure or venture.")).assertIsDisplayed()
            section("Meaning and origin")
            capture("冒険-険-system-back-to-component")
            back()
            await(articleBullet("冒 contributes braving or venturing, while 険 contributes danger or difficulty. The relationship is roughly venturing into danger. The on readings are ボウ + ケン.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("冒険-険-system-back-from-component")
            back()
            await(articleBullet("冒険 ぼうけん — adventure; risky venture")).assertIsDisplayed()
            section("Common words")
            capture("冒険-system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 3).put("directedLinkTransitions", 6)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            assertEquals("冒", (quiz.ui as QuizUi.Question).card.kanji)
            capture("meaning-question")
            click("brave danger; venture")
            await("Correct!")
            assertEquals("冒", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKinds = mutableSetOf<ReadingKind>()
            repeat(2) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("冒", question.card.kanji)
                assertTrue("Duplicate target reading kind", answeredKinds.add(question.question.kind))
                val key = if (question.question.kind == ReadingKind.On) "ぼう" else "おかす"
                assertEquals(key, question.question.correctKey)
                assertFalse(question.question.options.any { it.key.isBlank() })
                assertEquals(1, question.question.options.count { it.key == key })
                capture("curated-${question.question.kind}-question")
                click(question.question.options.single { it.key == key }.label)
                await(if (question.question.kind == ReadingKind.On) "Correct! — on'yomi" else "Correct! — kun'yomi")
                assertTrue((reading.ui as ReadingUi.Answer).correct)
                capture("curated-${question.question.kind}-feedback")
                click("Next")
                rule.waitUntil(30_000) { runBlocking {
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "冒" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(2, done.answered)
            assertEquals(2, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "冒" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(2, readingLogs.size)
            assertEquals(setOf("ぼう", "おかす"), readingLogs.map { it.reading }.toSet())
            capture("curated-both-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("brave danger; venture").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "冒") })
            assertEquals(listOf("ボウ"), card.onyomi.splitSep())
            assertEquals(listOf("おか.す"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("ボウ"), card.quizOnyomi?.splitSep())
            assertEquals(listOf("おか.す"), card.quizKunyomi?.splitSep())
            evidence.put("fullProjectionOnyomi", JSONArray(card.onyomi.splitSep()))
                .put("fullProjectionKunyomi", JSONArray(card.kunyomi.splitSep()))
                .put("fullProjectionQuizOnyomi", JSONArray(requireNotNull(card.quizOnyomi).splitSep()))
                .put("fullProjectionQuizKunyomi", JSONArray(requireNotNull(card.quizKunyomi).splitSep()))
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(9, strokes.length())
            capture("drawing-trace")
            val pad = rule.onNode(hasContentDescription("Drawing area for the kanji", substring = true))
            pad.performScrollTo()
            for (index in 0 until strokes.length()) {
                val points = strokes.getJSONObject(index).getJSONArray("points")
                pad.performTouchInput {
                    fun point(i: Int): Offset {
                        val pair = points.getJSONArray(i)
                        return Offset(pair.getDouble(0).toFloat() * width / 109f,
                            pair.getDouble(1).toFloat() * height / 109f)
                    }
                    down(point(0))
                    for (i in 1 until points.length()) moveTo(point(i), delayMillis = 16)
                    up()
                }
            }
            rule.onNode(hasContentDescription("9 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "冒" && it.mode == StudyMode.Draw.name }
            })
            await("Correct strokes").performScrollTo().assertIsDisplayed()
            capture("drawing-feedback")
            click("Next")
            await("Draw the kanji for")
            click("I don't remember")
            await("Here is the kanji")
            capture("drawing-recall-feedback")
            click("Next")
            rule.waitUntil(30_000) { runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "冒" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("bothCuratedKindsPersistedGoodAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-077-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-077-article-tree.txt").writeText(rule.onRoot().printToString())
            scenario.close()
        }
    }

    private fun model(prefix: String): ViewModel? {
        var result: ViewModel? = null
        scenario.onActivity { activity ->
            result = activity.viewModelStore.keys().lastOrNull { it.startsWith(prefix) }?.let { activity.viewModelStore[it] }
        }
        return result
    }

    private fun await(text: String, substring: Boolean = false): SemanticsNodeInteraction {
        return await(hasText(text, substring = substring))
    }

    private fun await(matcher: SemanticsMatcher): SemanticsNodeInteraction {
        rule.waitUntil(30_000) { rule.onAllNodes(matcher).fetchSemanticsNodes().isNotEmpty() }
        rule.onAllNodes(matcher).assertCountEquals(1)
        return rule.onNode(matcher)
    }

    private fun readingExample(text: String): SemanticsMatcher {
        return hasText(text) and hasAnyAncestor(hasTestTag("article-body")) and
            hasAnyAncestor(SemanticsMatcher.keyIsDefined(SemanticsProperties.HorizontalScrollAxisRange))
    }

    private fun articleBullet(text: String): SemanticsMatcher {
        return hasText(text) and hasAnyAncestor(hasTestTag("article-body")) and
            !hasAnyAncestor(SemanticsMatcher.keyIsDefined(SemanticsProperties.HorizontalScrollAxisRange))
    }

    private fun click(text: String) = click(await(text))

    private fun click(node: SemanticsNodeInteraction) {
        rule.waitUntil(30_000) { !node.fetchSemanticsNode().config.contains(SemanticsProperties.Disabled) }
        if (node.onAncestors().filter(hasScrollAction()).fetchSemanticsNodes().isNotEmpty()) node.performScrollTo()
        node.assertIsDisplayed().assertIsEnabled().performClick()
    }

    private fun section(title: String) {
        rule.onNodeWithTag("article-body").performScrollToIndex(0)
        click("Article contents")
        rule.onNode(hasText(title, substring = true) and hasClickAction()).performScrollTo().performClick()
        rule.waitForIdle()
    }

    private fun show(selector: String, step: String) {
        show(hasText(selector, substring = true), step)
    }

    private fun show(matcher: SemanticsMatcher, step: String) {
        val body = rule.onNodeWithTag("article-body")
        body.performScrollToNode(matcher)
        val target = await(matcher)
        target.performScrollTo()
        val viewport = body.fetchSemanticsNode()
        val cell = target.fetchSemanticsNode()
        val top = viewport.positionInRoot.y
        val bottom = top + viewport.size.height
        if (cell.positionInRoot.y < top || cell.positionInRoot.y + cell.size.height > bottom) {
            body.performSemanticsAction(SemanticsActions.ScrollBy) {
                it(0f, cell.positionInRoot.y - top - 16f)
            }
            rule.waitForIdle()
        }
        target.assertIsDisplayed()
        capture(step)
    }

    private fun inline(node: SemanticsNodeInteraction, label: String, offset: Int) {
        node.performScrollTo().assertIsDisplayed()
        val text = node.fetchSemanticsNode().config[SemanticsProperties.Text].joinToString("") { it.text }
        val layouts = mutableListOf<TextLayoutResult>()
        node.performSemanticsAction(SemanticsActions.GetTextLayoutResult) { it(layouts) }
        assertTrue("Wrong linked offset $offset for $label in $text", offset >= 0 && text.substring(offset).startsWith(label))
        node.performTouchInput { click(layouts.single().getBoundingBox(offset).center) }
    }

    private fun back() {
        InstrumentationRegistry.getInstrumentation().uiAutomation.performGlobalAction(
            android.accessibilityservice.AccessibilityService.GLOBAL_ACTION_BACK)
        rule.waitForIdle()
    }

    private fun capture(step: String) {
        rule.waitForIdle()
        val automation = InstrumentationRegistry.getInstrumentation().uiAutomation
        automation.waitForIdle(500, 5_000)
        android.os.SystemClock.sleep(1_000)
        rule.waitForIdle()
        val bitmap = requireNotNull(automation.takeScreenshot())
        File(app.getExternalFilesDir(null), "n1-077-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
