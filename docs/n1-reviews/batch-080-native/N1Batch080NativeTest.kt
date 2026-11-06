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

private fun disposable080() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch080GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun clarityLookalikesAndIceWaterFallbacksAcrossFourProductionFamilies() {
        disposable080()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("上 今 優 光 冫 冱 冴 冷 凍 器 字 寒 手 日 明 次 氵 汗 河 澄 牙 用 目 眠", "覚 輝 透 通 鋭 頭", "冴 次 汗 河 冫 氵 冱 牙 冴える 冱える 冴寒 頭 目 眠 冷 凍")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 080: clarity / look-alikes / ice and water fallback")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 30 scoped Han; focused 冴/次/汗/河/牙, 冫/冱/氵. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("上", "今", "優", "光", "冫", "冱", "冴", "冷", "凍", "器", "字", "寒", "手", "日", "明", "次", "氵", "汗", "河", "澄", "牙", "用", "目", "眠", "覚", "輝", "透", "通", "鋭", "頭")) {
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
            for (word in listOf("冴える")) {
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
        assertEquals(124, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-080-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-080-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 120).put("wholeWordRasterProbes", 4).put("panels", 3)
            .put("limits", "30 actual scoped Han including exact 冫/冱/氵 fallback inspection, four production families, three bounded Compose panels and four whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch080ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineClarityOneReciprocalPairCuratedKunDrawingAndSystemBack() {
        disposable080()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-080-${UUID.randomUUID()}", "main")
        val head = "0d2c9aee6de9e4f430935b38e31228db4bd47908"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-080-0d2c9aee-envelope.zip")
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
        assertEquals(1092, updated.kanji)
        assertEquals(5048, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("4572f7b1d0d95059", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(112, n1.size)
        val clarity = n1.single { it.kanji == "冴" }
        assertEquals(listOf("ゴ", "コ"), clarity.onyomi.splitSep())
        assertEquals(listOf("さ.える", "こお.る", "ひ.える"), clarity.kunyomi.splitSep())
        assertNotNull(clarity.quizOnyomi)
        assertNotNull(clarity.quizKunyomi)
        assertEquals(emptyList<String>(), clarity.quizOnyomi?.splitSep())
        assertEquals(listOf("さ.える"), clarity.quizKunyomi?.splitSep())
        assertEquals(emptyList<String>(), clarity.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(listOf("さえる"), clarity.toReadingCard().quizKeys(ReadingKind.Kun))
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
                        if (card.kanji == "冴") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "冴" && kind == ReadingKind.Kun && key == "さえる") now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "冴", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(clarity.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(clarity.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(clarity.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(clarity.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(clarity.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(clarity.quizKunyomi).splitSep()))
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 冴 meaning and sole curated kun key さえる due. Explicit empty on list. Two historical good 冴 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 112 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("冴")
            click("clear; sharp-minded")
            await("冴 — clear; sharp-minded")
            show(articleBullet("Strokes: 7 · Key (radical): 冫 (the two left-hand strokes, no. 15) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("Learn 冴 through 冴える (さえる): to be clear-headed or alert, or vivid and clear in appearance or sound. The verb can also describe deft performance. An older sense concerns intense cold; coldness is not implied whenever someone is clear-headed."), "kanji-03")
            show(articleBullet("Modern-shape mnemonic: imagine the cold 冫 beside the fang-like 牙 (きば) shape as a reminder of a crisp, keen mind. This is an invented memory aid, not a historical derivation or verified phonetic analysis."), "kanji-04")
            section("Readings")
            show(articleBullet("All five source readings remain below in source order. Only さ.える is selected for reading practice; there are no selected on questions."), "kanji-06")
            show(readingExample("ゴ"), "kanji-10")
            show(readingExample("冴寒 (ごかん) — extreme cold; a dictionary-attested rare term, for recognition rather than practice"), "kanji-12")
            show(readingExample("コ"), "kanji-13")
            show(readingExample("source-only lookup information; no exact non-name word example established in the inspected families"), "kanji-15")
            show(readingExample("さ.える"), "kanji-16")
            show(readingExample("冴える さえる — be clear-headed; be vivid"), "kanji-18")
            show(readingExample("こお.る"), "kanji-19")
            show(readingExample("source-only lookup information; do not treat the ordinary spelling 凍る (こおる) as evidence for a word written with 冴"), "kanji-21")
            show(readingExample("ひ.える"), "kanji-22")
            show(readingExample("source-only lookup information; 冷える (ひえる) is a separate spelling and does not establish a 冴 example"), "kanji-24")
            show(articleBullet("The source-only rows preserve character-dictionary information, not recommended spellings to invent in everyday writing. They do not claim that no example exists anywhere."), "kanji-25")
            section("Common words")
            show(articleBullet("冴える さえる — be clear-headed; be vivid"), "kanji-27")
            show(articleBullet("頭が冴える (あたまがさえる) — be clear-headed"), "kanji-28")
            show(articleBullet("目が冴える (めがさえる) — be wide awake; be unable to sleep"), "kanji-29")
            section("Notes")
            show(articleBullet("目が冴える concerns wakefulness, not eyes visibly shining. 冴えない (さえない) can describe something lacklustre, disappointing or unappealing; it is not always a literal absence of visual clarity or a judgement about intelligence."), "kanji-31")
            show(articleBullet("Compare the two left-hand marks with 次, whose right side is different. 汗 and 河 have three left-hand water dots, 氵, rather than 冫. The grade-9 source classification concerns name-use kanji, but 冴える is not a name-only word. Personal-name readings are outside this card's scope."), "kanji-32")
            show(articleBullet("Metadata: KANJIDIC2. Word evidence: JMdict, entries 1297050, 1877830, 1911790, 2576510 and 2679180. Usage: Digital Daijisen: 冴える. Character reading: 字通: 冴."), "kanji-33")
            section("Common words")
            show(articleBullet("冴える さえる — be clear-headed; be vivid"), "word-forward-21")
            inline(await(articleBullet("冴える さえる — be clear-headed; be vivid")), "冴える", 0)
            await("Article contents")
            await("冴える (さえる) — be clear-headed; be vivid")
            section("Meaning")
            show(articleBullet("冴える describes mental clarity or alertness, and a crisp, vivid quality in sights, colours or sounds. Learn the whole expression with its subject: 頭が冴える (あたまがさえる) means to be clear-headed; 目が冴える (めがさえる) means to be wide awake, often when you would rather sleep."), "word-02")
            show(articleBullet("今日は頭が冴えています。 (きょうはあたまがさえています。) — I feel clear-headed today."), "word-03")
            show(articleBullet("目が冴えて眠れません。 (めがさえてねむれません。) — I'm wide awake and can't sleep."), "word-04")
            show(articleBullet("This is an intransitive ichidan verb: the subject takes が. Forms include 冴えます (さえます), 冴えた (さえた), 冴えて (さえて) and 冴えない (さえない). 冴えている can describe an existing alert state. The examples adapt dictionary examples to polite endings."), "word-05")
            section("How the kanji combine")
            show(articleBullet("冴 supplies the clarity meaning in this single-kanji native verb. In the written form 冴える, 冴 represents さ and the following える completes さえる. The conjugation stem is さえ, including the written え. It is not a compound assembled from on readings."), "word-07")
            show(articleBullet("JMdict also records 冱える (さえる) as a rarely used kanji spelling. That spelling flag does not make the pronunciation さえる rare."), "word-08")
            section("Synonyms and antonyms")
            show(articleBullet("覚める (さめる) focuses on waking or regaining awareness: 目が覚める (めがさめる) means \"wake up,\" whereas 目が冴える describes wakefulness. 澄む (すむ) and 透き通る (すきとおる) overlap for clear sound, but physical transparency is not a universal meaning of 冴える."), "word-10")
            show(articleBullet("For an opposite evaluation, 冴えない can mean \"lacklustre\" or \"unsatisfactory,\" depending on what is being described; it is not a single antonym for every sense."), "word-11")
            section("Distinctive meaning")
            show(articleBullet("冴える can describe deft technique or a well-executed performance, not only mental alertness. It does not generally mean a permanent high intelligence score, nor does 目が冴える mean eyes lighting up with happiness."), "word-13")
            show(articleBullet("The negative 冴えない often concerns a disappointing result, an unappealing appearance or a subdued condition rather than literal blur. An older, somewhat old-fashioned sense of 冴える is \"become intensely cold.\" For ordinary cooling, learn 冷える (ひえる); for freezing, 凍る (こおる). Those verbs are not alternative pronunciations of the 冴える taught here."), "word-14")
            show(articleBullet("Dictionary: JMdict, entries 1297050, 1911790, 2576510 and 2679180. Usage and example bases: Digital Daijisen: 冴える, especially sense 5; clarity, performance and negative uses in senses 2–7."), "word-15")
            section("How the kanji combine")
            show(articleBullet("冴 supplies the clarity meaning in this single-kanji native verb. In the written form 冴える, 冴 represents さ and the following える completes さえる. The conjugation stem is さえ, including the written え. It is not a compound assembled from on readings."), "word-reverse-33")
            inline(await(articleBullet("冴 supplies the clarity meaning in this single-kanji native verb. In the written form 冴える, 冴 represents さ and the following える completes さえる. The conjugation stem is さえ, including the written え. It is not a compound assembled from on readings.")), "冴", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("さ.える"), "kanji-backlink")
            back()
            await(articleBullet("冴 supplies the clarity meaning in this single-kanji native verb. In the written form 冴える, 冴 represents さ and the following える completes さえる. The conjugation stem is さえ, including the written え. It is not a compound assembled from on readings.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("system-back-to-word")
            back()
            await(articleBullet("冴える さえる — be clear-headed; be vivid")).assertIsDisplayed()
            section("Common words")
            capture("system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 1).put("directedLinkTransitions", 2)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            assertEquals("冴", (quiz.ui as QuizUi.Question).card.kanji)
            capture("meaning-question")
            click("clear; sharp-minded")
            await("Correct!")
            assertEquals("冴", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKinds = mutableSetOf<ReadingKind>()
            repeat(1) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("冴", question.card.kanji)
                assertTrue("Duplicate target reading kind", answeredKinds.add(question.question.kind))
                assertEquals(ReadingKind.Kun, question.question.kind)
                val key = "さえる"
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "冴" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf(ReadingKind.Kun), answeredKinds)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(1, done.answered)
            assertEquals(1, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "冴" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(1, readingLogs.size)
            assertEquals(setOf("さえる"), readingLogs.map { it.reading }.toSet())
            capture("curated-kun-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("clear; sharp-minded").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "冴") })
            assertEquals(listOf("ゴ", "コ"), card.onyomi.splitSep())
            assertEquals(listOf("さ.える", "こお.る", "ひ.える"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(emptyList<String>(), card.quizOnyomi?.splitSep())
            assertEquals(listOf("さ.える"), card.quizKunyomi?.splitSep())
            evidence.put("fullProjectionOnyomi", JSONArray(card.onyomi.splitSep()))
                .put("fullProjectionKunyomi", JSONArray(card.kunyomi.splitSep()))
                .put("fullProjectionQuizOnyomi", JSONArray(requireNotNull(card.quizOnyomi).splitSep()))
                .put("fullProjectionQuizKunyomi", JSONArray(requireNotNull(card.quizKunyomi).splitSep()))
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(7, strokes.length())
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
            rule.onNode(hasContentDescription("7 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "冴" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "冴" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("soleCuratedKunPersistedGoodAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-080-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-080-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-080-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
