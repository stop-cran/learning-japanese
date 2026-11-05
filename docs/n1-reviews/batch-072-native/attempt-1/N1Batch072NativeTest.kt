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

private fun disposable072() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch072GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun allotmentLookalikesAndIsolatedRadicalsAcrossFourProductionFamilies() {
        disposable072()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val text = "充 允 元 兄 先 亠 儿 厶 口 土 拡 当 満 一 予 件 伸 余 備 割 加 図 増 大 子 定 小 展 広 延 張 指 振 援 支 旅 暇 書 条 注 発 縮 育 蓄 設 読 費 部 配 長 館 充てる 拡充"
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 072: allotment / look-alikes / isolated radicals")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(text, fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect 充/允/元/兄/先 and isolated 亠/儿/厶. Compare 拡/当/満 and both whole words. Fallback families may coincide.", fontSize = 18.sp)
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
            for (char in listOf("充", "允", "元", "兄", "先", "亠", "儿", "厶", "口", "土", "拡", "当", "満", "一", "予", "件", "伸", "余", "備", "割", "加", "図", "増", "大", "子", "定", "小", "展", "広", "延", "張", "指", "振", "援", "支", "旅", "暇", "書", "条", "注", "発", "縮", "育", "蓄", "設", "読", "費", "部", "配", "長", "館")) {
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
            for (word in listOf("充てる", "拡充")) {
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
        assertEquals(212, rows.length())
        rule.waitForIdle()
        rule.onAllNodesWithText(text).assertCountEquals(4)
        for (index in fonts.indices) rule.onAllNodesWithText(text)[index].assertIsDisplayed()
        File(context.getExternalFilesDir(null), "n1-072-font-pairs.png").outputStream().use {
            assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        File(context.getExternalFilesDir(null), "n1-072-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 204).put("wholeWordRasterProbes", 8)
            .put("limits", "Native Paint probes cover actual authored Han and isolated 亠/儿/厶; eight whole-word rasters and four production Compose rows. Actual readability requires visual inspection; emulator not phone; fallback face not identified.")
            .toString(2))
    }
}

class N1Batch072ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineAllotmentTwoReciprocalPairsBothReadingsDrawingAndSystemBack() {
        disposable072()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-072-${UUID.randomUUID()}", "main")
        val head = "92f3c2ef6edbeb8dd7b6e7f37227cab8a3e20891"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-072-92f3c2ef-envelope.zip")
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
        assertEquals(1084, updated.kanji)
        assertEquals(5042, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("900e3a2130afc56b", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(104, n1.size)
        val allotment = n1.single { it.kanji == "充" }
        assertEquals(listOf("ジュウ"), allotment.onyomi.splitSep())
        assertEquals(listOf("あ.てる", "み.たす"), allotment.kunyomi.splitSep())
        assertNotNull(allotment.quizOnyomi)
        assertNotNull(allotment.quizKunyomi)
        assertEquals(listOf("ジュウ"), allotment.quizOnyomi?.splitSep())
        assertEquals(listOf("あ.てる"), allotment.quizKunyomi?.splitSep())
        assertEquals(listOf("じゅう"), allotment.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(listOf("あてる"), allotment.toReadingCard().quizKeys(ReadingKind.Kun))
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
                        if (card.kanji == "充") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "充" && ((kind == ReadingKind.On && key == "じゅう") || (kind == ReadingKind.Kun && key == "あてる"))) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "充", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(allotment.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(allotment.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(allotment.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(allotment.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(allotment.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(allotment.quizKunyomi).splitSep()))
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 充 meaning and both curated on/kun keys due; source-only み.たす retained but not offered. Two historical good 充 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 104 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("充")
            click("allot; fill")
            await("充 — allot; fill")
            show(articleBullet("Strokes: 6 · Key (radical): 儿 (no. 10) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("充 concerns filling, making sufficient, or allotting something to a purpose. In 拡充 かくじゅう, it contributes making provision more substantial; 充てる あてる means allocating a resource to a use."), "kanji-03")
            show(articleBullet("The modern shape has an upper 亠 and 厶-like middle above the two leg-like strokes 儿, the indexing radical. Modern-shape mnemonic: picture someone standing beneath a sign showing where to allot supplies. This is a visual memory aid, not a historical derivation or a phonetic analysis."), "kanji-04")
            section("Readings")
            show(readingExample("ジュウ"), "kanji-09")
            show(readingExample("拡充 かくじゅう — expansion; strengthening"), "kanji-11")
            show(readingExample("あ.てる"), "kanji-12")
            show(readingExample("充てる あてる — allocate; earmark"), "kanji-14")
            show(readingExample("み.たす"), "kanji-15")
            show(readingExample("source-only for this quiz: 充たす みたす — fill; satisfy; rare spelling of usual 満たす"), "kanji-17")
            show(articleBullet("All three sourced readings remain in order. Reading questions select ジュウ and あ.てる, not み.たす. The rarity concerns the spelling 充たす, not the pronunciation みたす. For example, 条件を充たす (じょうけんをみたす) means \"satisfy the conditions\"; normally write 条件を満たす."), "kanji-18")
            section("Common words")
            show(articleBullet("拡充 かくじゅう — expansion; strengthening, as of facilities or services"), "kanji-20")
            show(articleBullet("充てる あてる — allocate time, money, or another resource to a purpose"), "kanji-21")
            section("Notes")
            show(articleBullet("允 has 厶 directly above 儿; 充 has an additional upper 亠 shape."), "kanji-23")
            show(articleBullet("元 has two horizontal lines above its legs, 兄 a square 口, and 先 a different crossed upper shape. Compare the whole outline."), "kanji-24")
            show(articleBullet("当てる あてる covers hitting, holding against, and guessing correctly. Use 充てる for the resource-allocation sense taught here, not as a replacement spelling for those contact or guessing uses. The broader あてる family also has allotting uses; this is not an absolute division of every sense between the spellings."), "kanji-25")
            show(articleBullet("Metadata: KANJIDIC2, 2026-11-02 snapshot. Words: JMdict, entries 1205190, 1334270, 1526670 and 1855580. Meaning and spelling: Jitsu, 充; Daijisen and Nikkoku, あてる."), "kanji-26")
            section("Common words")
            inline(await(articleBullet("充てる あてる — allocate time, money, or another resource to a purpose")), "充てる", 0)
            await("充てる (あてる) - allocate; earmark")
            section("Meaning")
            show(articleBullet("充てる means allocating or devoting a resource to a particular purpose. Use resource を + purpose に + 充てる: the resource can be time or money. It is a transitive ichidan verb: 充てます (あてます), 充てた (あてた), 充てない (あてない)."), "word-new-02")
            show(articleBullet("余暇を読書に充てています。 (よかをどくしょにあてています。) - I devote my spare time to reading."), "word-new-03")
            show(articleBullet("ボーナスの一部を旅費に充てました。 (ボーナスのいちぶをりょひにあてました。) - I allocated part of my bonus to travel expenses."), "word-new-04")
            show(articleBullet("The point is what the resource is used or earmarked for, not simply that it is kept unused in reserve."), "word-new-05")
            section("How the kanji combine")
            show(articleBullet("充 represents the native stem あ in this allocation verb; てる is okurigana and changes with conjugation. This is one written kanji, not a compound. Its filling/allotting association is a memory aid, not a derivation of the word."), "word-new-07")
            section("Synonyms and antonyms")
            show(articleBullet("割り当てる (わりあてる), \"assign; allot,\" overlaps in allocating work or resources. 配る (くばる) foregrounds distributing things or placing personnel; 振る (ふる) can mean assigning work to someone. These are related uses, not freely interchangeable constructions."), "word-new-09")
            show(articleBullet("当てる, also あてる, is the spelling to learn for hitting a target, holding something against a surface, or guessing correctly. Dictionaries also record allotting uses in the broader あてる family, so do not treat these spellings as having completely separate meanings in every context."), "word-new-10")
            section("Distinctive meaning")
            show(articleBullet("In 余暇を読書に充てる (よかをどくしょにあてる), the time is devoted to reading. English \"set aside\" can instead suggest saving something untouched: 蓄える (たくわえる) concerns storing or accumulating, not this verb's resource-for-purpose relation. There is no single opposite that reverses all uses of 充てる."), "word-new-12")
            show(articleBullet("Dictionary: JMdict, entry 1334270; comparisons 1207880, 1448860, 1472990, 1361330 and 1596860. Usage and spelling: Daijisen and Nikkoku, あてる, especially Daijisen's 充てる allocation sense."), "word-new-13")
            section("How the kanji combine")
            inline(await(articleBullet("充 represents the native stem あ in this allocation verb; てる is okurigana and changes with conjugation. This is one written kanji, not a compound. Its filling/allotting association is a memory aid, not a derivation of the word.")), "充", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("拡充 かくじゅう — expansion; strengthening"), "word-new-kanji-backlink")
            back()
            await(articleBullet("充 represents the native stem あ in this allocation verb; てる is okurigana and changes with conjugation. This is one written kanji, not a compound. Its filling/allotting association is a memory aid, not a derivation of the word.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("word-new-system-back-word-kanji")
            back()
            await(articleBullet("充てる あてる — allocate time, money, or another resource to a purpose")).assertIsDisplayed()
            section("Common words")
            capture("word-new-system-back-kanji-word")
            section("Common words")
            inline(await(articleBullet("拡充 かくじゅう — expansion; strengthening, as of facilities or services")), "拡充", 0)
            await("拡充 (かくじゅう) - expansion; strengthening")
            section("How the kanji combine")
            show(articleBullet("拡 contributes widening, and 充 filling or making sufficient. Their related contributions suggest both broader provision and greater substance. The on readings are カク + ジュウ. This is a meaning aid, not a history of the characters."), "word-reused-06")
            section("How the kanji combine")
            inline(await(articleBullet("拡 contributes widening, and 充 filling or making sufficient. Their related contributions suggest both broader provision and greater substance. The on readings are カク + ジュウ. This is a meaning aid, not a history of the characters.")), "充", 28)
            await("Article contents")
            section("Readings")
            show(readingExample("拡充 かくじゅう — expansion; strengthening"), "word-reused-kanji-backlink")
            back()
            await(articleBullet("拡 contributes widening, and 充 filling or making sufficient. Their related contributions suggest both broader provision and greater substance. The on readings are カク + ジュウ. This is a meaning aid, not a history of the characters.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("word-reused-system-back-word-kanji")
            back()
            await(articleBullet("拡充 かくじゅう — expansion; strengthening, as of facilities or services")).assertIsDisplayed()
            section("Common words")
            capture("word-reused-system-back-kanji-word")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            assertEquals("充", (quiz.ui as QuizUi.Question).card.kanji)
            capture("meaning-question")
            click("allot; fill")
            await("Correct!")
            assertEquals("充", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKinds = mutableSetOf<ReadingKind>()
            repeat(2) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("充", question.card.kanji)
                assertTrue("Duplicate target reading kind", answeredKinds.add(question.question.kind))
                val key = if (question.question.kind == ReadingKind.On) "じゅう" else "あてる"
                assertNotEquals("みたす", question.question.correctKey)
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "充" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(2, done.answered)
            assertEquals(2, done.correct)
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "充" && it.mode == ReadingKind.Kun.mode.name && it.reading == "みたす" }
            })
            capture("curated-both-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("allot; fill").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "充") })
            assertEquals(listOf("ジュウ"), card.onyomi.splitSep())
            assertEquals(listOf("あ.てる", "み.たす"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("ジュウ"), card.quizOnyomi?.splitSep())
            assertEquals(listOf("あ.てる"), card.quizKunyomi?.splitSep())
            evidence.put("fullProjectionOnyomi", JSONArray(card.onyomi.splitSep()))
                .put("fullProjectionKunyomi", JSONArray(card.kunyomi.splitSep()))
                .put("fullProjectionQuizOnyomi", JSONArray(requireNotNull(card.quizOnyomi).splitSep()))
                .put("fullProjectionQuizKunyomi", JSONArray(requireNotNull(card.quizKunyomi).splitSep()))
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(6, strokes.length())
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
            rule.onNode(hasContentDescription("6 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "充" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "充" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("bothCuratedKindsPersistedGoodNoMitasuAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-072-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-072-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-072-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
