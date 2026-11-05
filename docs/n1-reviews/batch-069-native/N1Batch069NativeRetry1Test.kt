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

private fun disposable069() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch069Retry1GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun confucianLookalikesAndRadicalVariantsAcrossFourProductionFamilies() {
        disposable069()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val text = "儒 需 儀 僧 優 人 亻 教 攴 攵 子 考 校 木 儒教"
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 069: Confucian / look-alikes / radical variants")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(text, fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect 儒 versus 需/儀/僧/優, 人 versus standalone 亻, 儒教 and 教 with 子/攴/攵 plus 考/校/木. Fallback families may coincide.", fontSize = 18.sp)
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
            for (char in listOf("儒", "需", "儀", "僧", "優", "人", "亻", "教", "攴", "攵", "子", "考", "校", "木")) {
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
            for (word in listOf("儒教")) {
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
        assertEquals(60, rows.length())
        rule.waitForIdle()
        rule.onAllNodesWithText(text).assertCountEquals(4)
        for (index in fonts.indices) rule.onAllNodesWithText(text)[index].assertIsDisplayed()
        File(context.getExternalFilesDir(null), "n1-069-font-pairs.png").outputStream().use {
            assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        File(context.getExternalFilesDir(null), "n1-069-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 56).put("wholeWordRasterProbes", 4)
            .put("limits", "Fifty-six single-character native Paint probes including 人/standalone亻 and actual 攴/攵, four whole-word nonblank raster probes and four production Compose rows. Actual readability requires visual inspection; emulator not phone; fallback face not identified.")
            .toString(2))
    }
}

class N1Batch069Retry1ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineConfucianTwoReciprocalPairsOnOnlyDrawingAndSystemBack() {
        disposable069()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-069-${UUID.randomUUID()}", "main")
        val head = "e245739783dbc2ebe33ee164b8cfa718d670551b"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-069-e2457397-envelope.zip")
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
        assertEquals(1081, updated.kanji)
        assertEquals(5038, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("83ed94552dd1a9ce", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(101, n1.size)
        val confucian = n1.single { it.kanji == "儒" }
        assertEquals(listOf("ジュ"), confucian.onyomi.splitSep())
        assertEquals(emptyList<String>(), confucian.kunyomi.splitSep())
        assertNotNull(confucian.quizOnyomi)
        assertNotNull(confucian.quizKunyomi)
        assertEquals(listOf("ジュ"), confucian.quizOnyomi?.splitSep())
        assertEquals(emptyList<String>(), confucian.quizKunyomi?.splitSep())
        assertEquals(listOf("じゅ"), confucian.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(emptyList<String>(), confucian.toReadingCard().quizKeys(ReadingKind.Kun))
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
                        if (card.kanji == "儒") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "儒" && (kind == ReadingKind.On && key == "じゅ")) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "儒", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(confucian.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(confucian.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(confucian.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(confucian.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 儒 meaning and sole curated on key due; explicit no-kun. Two historical good 儒 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 101 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("儒")
            click("Confucian; Confucian scholar")
            await("儒 — Confucian; Confucian scholar")
            show(articleBullet("Strokes: 16 · Key (radical): 人 (as 亻, no. 9) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("儒 concerns Confucian thought and its scholars. 儒教 じゅきょう means Confucianism, the tradition of teachings associated with 孔子（こうし）, Confucius. 儒 is not a general label for every teacher or religious believer."), "kanji-03")
            show(articleBullet("The visible parts are 亻, the side form of 人, and 需 on the right. Modern-shape mnemonic: picture a person beside layers of study notes. This is an invented visual memory aid, not a historical or phonetic explanation."), "kanji-04")
            section("Readings")
            show(readingExample("儒教 じゅきょう — Confucianism"), "kanji-11")
            show(articleBullet("The frozen character dictionary gives ジュ and no kun reading."), "kanji-12")
            section("Common words")
            show(articleBullet("儒教 じゅきょう — Confucianism"), "kanji-14")
            section("Notes")
            show(articleBullet("儒学（じゅがく）also means Confucianism, with emphasis on its scholarly aspect. It often overlaps with 儒教; do not impose an absolute religion-versus-philosophy divide."), "kanji-16")
            show(articleBullet("In older scholarly usage, 儒 can extend to a learned person more generally. Learn the whole word and context rather than treating \"Confucian\" as an exceptionless translation in every compound."), "kanji-17")
            show(articleBullet("儀, \"ceremony; formal conduct,\" 僧, \"Buddhist monk; priest,\" and 優, \"gentle; superior,\" also have 亻 but different right-hand shapes. A shared component does not make their meanings interchangeable."), "kanji-18")
            show(articleBullet("Metadata: KANJIDIC2. Word pairs: JMdict, entries 1329450, 1329470 and 1329510. Usage: Daijisen and Nikkoku, 儒; Nipponica, 儒学."), "kanji-19")
            section("Common words")
            inline(await(articleBullet("儒教 じゅきょう — Confucianism")), "儒教", 0)
            await("儒教 (じゅきょう) — Confucianism")
            section("Meaning")
            show(articleBullet("儒教 is Confucianism, the tradition of teachings associated with 孔子（こうし）, Confucius. It is a noun naming that particular tradition, not religion or education in general."), "word1-02")
            show(articleBullet("歴史の授業で儒教について学びました。 (れきしのじゅぎょうでじゅきょうについてまなびました。) — I learned about Confucianism in history class."), "word1-03")
            show(articleBullet("この本は儒教の考え方を紹介しています。 (このほんはじゅきょうのかんがえかたをしょうかいしています。) — This book introduces Confucian ideas."), "word1-04")
            show(articleBullet("儒教について学ぶ（じゅきょうについてまなぶ）means \"learn about Confucianism\"; studying a tradition does not itself mean following it."), "word1-05")
            section("How the kanji combine")
            show(articleBullet("儒 contributes Confucian thought or its scholars, and 教 contributes teaching or doctrine. This is a modifier + head compound: Confucian teachings. The on readings combine as ジュ + キョウ → じゅきょう."), "word1-07")
            section("Synonyms and antonyms")
            show(articleBullet("儒学（じゅがく）also means Confucianism, often emphasizing its scholarly aspect. The words overlap; they are not an absolute division between religion and secular philosophy. 宗教 しゅうきょう means religion more broadly, and 思想 しそう means thought or ideology, not specifically Confucianism. There is no simple everyday antonym for the name of this tradition."), "word1-09")
            section("Distinctive meaning")
            show(articleBullet("教 does not make 儒教 a word for school teaching in general. Use 儒教の思想（じゅきょうのしそう）, \"Confucian thought,\" when describing its ideas. The word names a tradition; it does not by itself state a person's nationality, beliefs or degree of commitment."), "word1-11")
            show(articleBullet("Dictionary: JMdict, entry 1329510. Usage: World Encyclopedia, 儒教; Nipponica, 儒学."), "word1-12")
            section("How the kanji combine")
            inline(await(articleBullet("儒 contributes Confucian thought or its scholars, and 教 contributes teaching or doctrine. This is a modifier + head compound: Confucian teachings. The on readings combine as ジュ + キョウ → じゅきょう.")), "儒", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("儒教 じゅきょう — Confucianism"), "word1-new-kanji-backlink")
            back()
            await("儒教  Confucianism")
            section("How the kanji combine")
            inline(await(articleBullet("儒 contributes Confucian thought or its scholars, and 教 contributes teaching or doctrine. This is a modifier + head compound: Confucian teachings. The on readings combine as ジュ + キョウ → じゅきょう.")), "教", 53)
            await("教 — teach, instruct")
            show(articleBullet("Strokes: 11 · Key (radical): 攴 (right-side shape 攵, no. 66) · JLPT: N4 (community list)"), "component1-01")
            section("Meaning and origin")
            show(articleBullet("教 concerns teaching and instruction; in some compounds it also concerns a doctrine or faith. The everyday verb 教える includes telling someone information, not just teaching a lesson."), "component1-03")
            show(articleBullet("Modern-shape mnemonic: notice 子 within the left side and picture a child following a teacher's pointing gesture on the right. This is an invented memory scene, not a claim about the origin of 攵."), "component1-04")
            section("Readings")
            show(readingExample("教室 きょうしつ (classroom), 教科書 きょうかしょ (textbook)"), "component1-11")
            show(readingExample("教える おしえる (teach; tell)"), "component1-14")
            show(readingExample("教わる おそわる (be taught; learn from someone)"), "component1-17")
            section("Common words")
            show(articleBullet("教える おしえる — teach; tell someone information"), "component1-19")
            show(articleBullet("教わる おそわる — be taught, learn from someone"), "component1-20")
            show(articleBullet("教室 きょうしつ — classroom"), "component1-21")
            show(articleBullet("教科書 きょうかしょ — textbook"), "component1-22")
            show(articleBullet("儒教 じゅきょう — Confucianism"), "component1-23")
            section("Notes")
            show(articleBullet("教える views the exchange from the instructor's side; 教わる views it from the learner's side. The verb is not limited to school: a person can 教える a name or an address."), "component1-25")
            show(articleBullet("考 has a similar upper-left outline, but lacks 子 and 攵. 校 is another school-related character with a different left-hand component, 木."), "component1-26")
            show(articleBullet("Metadata: KANJIDIC2, 2026-10-08 (EDRDG; CC BY-SA 4.0)."), "component1-27")
            section("Common words")
            inline(await(articleBullet("儒教 じゅきょう — Confucianism")), "儒教", 0)
            await("儒教 (じゅきょう) — Confucianism")
            section("How the kanji combine")
            show(articleBullet("儒 contributes Confucian thought or its scholars, and 教 contributes teaching or doctrine. This is a modifier + head compound: Confucian teachings. The on readings combine as ジュ + キョウ → じゅきょう."), "word1-legacy-backlink")
            back()
            await("Common words")
            capture("system-back-component1")
            back()
            await("How the kanji combine")
            capture("system-back-word1-component")
            back()
            await("Common words")
            capture("system-back-kanji-word1")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            assertEquals("儒", (quiz.ui as QuizUi.Question).card.kanji)
            capture("meaning-question")
            click("Confucian; Confucian scholar")
            await("Correct!")
            assertEquals("儒", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKinds = mutableSetOf<ReadingKind>()
            repeat(1) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("儒", question.card.kanji)
                assertTrue("Duplicate target reading kind", answeredKinds.add(question.question.kind))
                assertEquals(ReadingKind.On, question.question.kind)
                val key = "じゅ"
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "儒" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf(ReadingKind.On), answeredKinds)
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "儒" && it.mode == ReadingKind.Kun.mode.name }
            })
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("Confucian; Confucian scholar").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "儒") })
            assertEquals(listOf("ジュ"), card.onyomi.splitSep())
            assertEquals(emptyList<String>(), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("ジュ"), card.quizOnyomi?.splitSep())
            assertEquals(emptyList<String>(), card.quizKunyomi?.splitSep())
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(16, strokes.length())
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
            rule.onNode(hasContentDescription("16 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "儒" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "儒" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("soleCuratedOnQuestionAndPersistedGradeNoKun", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-069-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-069-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-069-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
