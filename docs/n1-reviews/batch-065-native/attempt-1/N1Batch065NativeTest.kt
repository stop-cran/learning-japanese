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

private fun disposable065() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch065GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun frugalityLookalikesOlderFormAndRadicalsAcrossFourProductionFamilies() {
        disposable065()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val text = "倹 儉 険 験 値 人 亻 阝 馬 約 糸 勺 倹約 倹しい"
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 065: thrift / look-alikes / older form / radicals")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(text, fontFamily = font.family(), fontSize = 24.sp, lineHeight = 34.sp)
                    }
                    Text("Compare 倹 with 儉, 険, 験 and 値; inspect 人/亻, 阝, 馬 and 約 with 糸/勺. Read 倹約 and 倹しい. Shared fallback need not give four different designs.", fontSize = 18.sp)
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
            for (char in listOf("倹", "儉", "険", "験", "値", "人", "亻", "阝", "馬", "約", "糸", "勺")) {
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
            for (word in listOf("倹約", "倹しい")) {
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
        assertEquals(56, rows.length())
        rule.waitForIdle()
        rule.onAllNodesWithText(text).assertCountEquals(4)
        for (index in fonts.indices) rule.onAllNodesWithText(text)[index].assertIsDisplayed()
        File(context.getExternalFilesDir(null), "n1-065-font-pairs.png").outputStream().use {
            assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        File(context.getExternalFilesDir(null), "n1-065-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 48).put("wholeWordRasterProbes", 8)
            .put("limits", "Forty-eight single-character native Paint probes including older 儉 and actual 人/亻/阝/馬/糸/勺, eight complete-word nonblank raster probes and four production Compose rows; actual 倹/儉/険/験/値/人/亻/阝/馬/約/糸/勺/倹約/倹しい readability requires separate visual inspection. Emulator, not phone. Fallback styles may coincide; actual fallback face not identified.")
            .toString(2))
    }
}

class N1Batch065ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineFrugalityThreePairsBothCuratedReadingsDrawingAndSystemBack() {
        disposable065()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-065-${UUID.randomUUID()}", "main")
        val head = "ee672744235275d321b4bfb33a6efe0286444594"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-065-ee672744-envelope.zip")
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
        assertEquals(1077, updated.kanji)
        assertEquals(5036, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("6a940651167e0e94", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(97, n1.size)
        val frugality = n1.single { it.kanji == "倹" }
        assertEquals(listOf("ケン"), frugality.onyomi.splitSep())
        assertEquals(listOf("つま.しい", "つづまやか"), frugality.kunyomi.splitSep())
        assertNotNull(frugality.quizOnyomi)
        assertNotNull(frugality.quizKunyomi)
        assertEquals(listOf("ケン"), frugality.quizOnyomi?.splitSep())
        assertEquals(listOf("つま.しい"), frugality.quizKunyomi?.splitSep())
        assertEquals(listOf("けん"), frugality.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(listOf("つましい"), frugality.toReadingCard().quizKeys(ReadingKind.Kun))
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
                        if (card.kanji == "倹") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "倹" && ((kind == ReadingKind.On && key == "けん") || (kind == ReadingKind.Kun && key == "つましい"))) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "倹", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(frugality.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(frugality.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(frugality.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(frugality.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 倹 meaning and both curated reading keys due. Full source-only つづまやか retained, not offered. Two historical good 倹 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 97 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("倹")
            click("frugal; thrifty")
            await("Article contents")
            await("as left-hand 亻", substring = true).performScrollTo().assertIsDisplayed()
            capture("kanji-radical")
            section("Meaning and origin")
            show("倹 concerns thrift", "kanji-meaning")
            show("Modern-shape mnemonic, not etymology:", "kanji-mnemonic")
            section("Readings")
            show(readingExample("倹約 けんやく — thrift; frugality"), "kanji-on-reading")
            show(readingExample("倹しい つましい — frugal; modest in one's living; usually written in kana"), "kanji-kun-reading")
            show(readingExample("source-only character-dictionary reading associated with frugality or restraint; no verified practical word spelled with 倹 is supplied here"), "kanji-source-only")
            show("The full source lists and their order are retained.", "kanji-curation-boundary")
            section("Notes")
            show("Compare the similar right-hand shapes", "kanji-lookalikes")
            show("倹しい is つましい, not つつましい.", "kanji-pronunciation-boundary")
            show("The older form of 倹 is 儉", "kanji-older-form")
            section("Common words")
            show(articleBullet("倹約家 (けんやくか) — a thrifty person"), "kanji-frugal-person")
            inline(await(articleBullet("倹約 けんやく — thrift; frugality")), "倹約")
            await("倹約 (けんやく) — thrift; frugality")
            section("Meaning")
            show("倹約 means avoiding wasteful spending", "thrift-meaning")
            show(articleBullet("小遣いを倹約しています。 (こづかいをけんやくしています。) — I am economizing on my spending money."), "thrift-verb-example")
            show(articleBullet("倹約な生活を送っています。 (けんやくなせいかつをおくっています。) — I lead a frugal life."), "thrift-adjective-example")
            show("With する, the expenditure being reduced takes を.", "thrift-attachment")
            section("How the kanji combine")
            show("The on readings combine as ケン + ヤク: けんやく.", "thrift-reading-allocation")
            inline(await("contributes reduction or restraint here.", substring = true), "倹")
            await("Article contents")
            section("Readings")
            show(readingExample("倹約 けんやく — thrift; frugality"), "thrift-person-backlink")
            back()
            await("contributes reduction or restraint here.", substring = true).assertIsDisplayed()
            capture("system-back-thrift-person")
            inline(await("contributes reduction or restraint here.", substring = true), "約")
            await("Article contents")
            await("Key (radical):", substring = true).performScrollTo().assertIsDisplayed()
            capture("agreement-radical")
            section("Meaning and origin")
            show("約 has two particularly useful jobs", "agreement-two-uses")
            show("This recalls the promise meaning only", "agreement-mnemonic")
            section("Readings")
            show(readingExample("約束 やくそく — promise; 予約 よやく — reservation"), "agreement-on-reading")
            show(readingExample("約 やく — approximately"), "agreement-approximate-reading")
            show("The source's kun readings remain", "agreement-source-boundary")
            section("Notes")
            show("約束を守る", "agreement-promise-example")
            show("Identify 約 by its relatively simple 勺", "agreement-lookalikes")
            section("Common words")
            show(articleBullet("約束 やくそく — promise; arrangement"), "agreement-common-promise")
            show(articleBullet("予約 よやく — reservation; booking"), "agreement-common-reservation")
            show(articleBullet("約 やく — about; approximately, before a quantity"), "agreement-common-approximation")
            inline(await(articleBullet("倹約 けんやく — thrift; frugality")), "倹約")
            await("倹約 (けんやく) — thrift; frugality")
            section("How the kanji combine")
            show("The on readings combine as ケン + ヤク: けんやく.", "thrift-agreement-backlink")
            back()
            await(articleBullet("倹約 けんやく — thrift; frugality")).assertIsDisplayed()
            capture("system-back-agreement")
            back()
            await("contributes reduction or restraint here.", substring = true).assertIsDisplayed()
            section("Synonyms and antonyms")
            show("節約 also readily describes saving electricity or time", "thrift-conservation-boundary")
            show("spending less does not guarantee that the difference is saved.", "thrift-saving-boundary")
            section("Distinctive meaning")
            show("倹約 does not inherently call someone a miser.", "thrift-stinginess-boundary")
            show("neither is an unrestricted replacement for the other.", "thrift-economy-boundary")
            inline(await("describes frugal or modest living as an い-adjective.", substring = true), "倹しい")
            await("倹しい (つましい) — frugal; modest in one's living")
            section("Meaning")
            show("つましい describes living without extravagance", "modest-meaning-spelling")
            show(articleBullet("二人はつましい暮らしをしています。 (ふたりはつましいくらしをしています。) — The two of them lead a modest life."), "modest-living-example")
            show(articleBullet("私たちの生活はつましいですが、満足しています。 (わたしたちのせいかつはつましいですが、まんぞくしています。) — Our life is modest, but we are content."), "modest-content-example")
            show("It is an い-adjective:", "modest-attachment")
            section("How the kanji combine")
            show("supplies つま, with しい as the written ending", "modest-reading-boundary")
            show("JMdict also recognizes 約しい", "modest-spelling-flag")
            inline(await("supplies つま, with しい as the written ending", substring = true), "倹")
            await("Article contents")
            section("Common words")
            inline(await(articleBullet("倹しい つましい — frugal; modest in one's living; usually written つましい")), "倹しい")
            await("倹しい (つましい) — frugal; modest in one's living")
            section("How the kanji combine")
            show("supplies つま, with しい as the written ending", "modest-person-backlink")
            back()
            await(articleBullet("倹しい つましい — frugal; modest in one's living; usually written つましい")).assertIsDisplayed()
            capture("system-back-person-modest")
            back()
            await("supplies つま, with しい as the written ending", substring = true).assertIsDisplayed()
            section("Synonyms and antonyms")
            show("Compare 倹約する", "modest-thrift-contrast")
            show("Do not manufacture a strict behavior-versus-lifestyle split", "modest-pronunciation-overlap")
            inline(await("Compare 倹約する", substring = true), "倹約")
            await("倹約 (けんやく) — thrift; frugality")
            section("Meaning")
            show("With する, the expenditure being reduced takes を.", "modest-thrift-backlink")
            back()
            await("Compare 倹約する", substring = true).assertIsDisplayed()
            capture("system-back-modest-thrift")
            section("Distinctive meaning")
            show("つましい does not itself say", "modest-judgment-boundary")
            show("Nor does つましい mean", "modest-simple-boundary")
            back()
            await("describes frugal or modest living as an い-adjective.", substring = true).assertIsDisplayed()
            back()
            await("Common words")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            assertEquals("倹", (quiz.ui as QuizUi.Question).card.kanji)
            capture("meaning-question")
            click("frugal; thrifty")
            await("Correct!")
            assertEquals("倹", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKinds = mutableSetOf<ReadingKind>()
            repeat(2) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("倹", question.card.kanji)
                assertTrue("Duplicate target reading kind", answeredKinds.add(question.question.kind))
                val key = if (question.question.kind == ReadingKind.On) "けん" else "つましい"
                assertFalse(question.question.options.any { it.key.isBlank() })
                assertEquals(key, question.question.correctKey)
                assertEquals(1, question.question.options.count { it.key == key })
                capture("curated-${question.question.kind}-question")
                click(question.question.options.single { it.key == key }.label)
                await(if (question.question.kind == ReadingKind.On) "Correct! — on'yomi" else "Correct! — kun'yomi")
                assertTrue((reading.ui as ReadingUi.Answer).correct)
                capture("curated-${question.question.kind}-feedback")
                click("Next")
                rule.waitUntil(30_000) { runBlocking {
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "倹" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "倹" && it.mode == ReadingKind.Kun.mode.name && it.reading == "つづまやか" }
            })
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("frugal; thrifty").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "倹") })
            assertEquals(listOf("ケン"), card.onyomi.splitSep())
            assertEquals(listOf("つま.しい", "つづまやか"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("ケン"), card.quizOnyomi?.splitSep())
            assertEquals(listOf("つま.しい"), card.quizKunyomi?.splitSep())
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(10, strokes.length())
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
            rule.onNode(hasContentDescription("10 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "倹" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "倹" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("bothCuratedReadingsAndPersistedGrades", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-065-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-065-article-tree.txt").writeText(rule.onRoot().printToString())
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

    private fun inline(node: SemanticsNodeInteraction, label: String) {
        node.performScrollTo().assertIsDisplayed()
        val text = node.fetchSemanticsNode().config[SemanticsProperties.Text].joinToString("") { it.text }
        val layouts = mutableListOf<TextLayoutResult>()
        node.performSemanticsAction(SemanticsActions.GetTextLayoutResult) { it(layouts) }
        val offset = text.indexOf(label)
        assertTrue("Missing $label in $text", offset >= 0)
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
        File(app.getExternalFilesDir(null), "n1-065-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
