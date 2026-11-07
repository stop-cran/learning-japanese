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
import io.github.stopcran.kanji.core.quiz.QuizBuilder
import io.github.stopcran.kanji.core.quiz.QuizCard
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

private fun disposable092() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch092GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun mowLookalikesAndScopedHanAcrossFourProductionFamilies() {
        disposable092()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("乃 凸 凹 刀 刂 切 刈 収 夏 庭 短 稲", "穫 草 除 髪", "刈 切 刀 刂 乃 凹 凸 草 髪 稲 刈除")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 092: mow / look-alikes / scoped Han")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 16 scoped Han; focused 刈/切/刀/刂/乃/凹/凸. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("乃", "凸", "凹", "刀", "刂", "切", "刈", "収", "夏", "庭", "短", "稲", "穫", "草", "除", "髪")) {
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
            for (word in listOf("刈除")) {
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
        assertEquals(68, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-092-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-092-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 64).put("wholeWordRasterProbes", 4).put("panels", 3)
            .put("limits", "16 actual scoped Han; 刂 absent from all three bundled cmaps requires actual system fallback inspection, four production families, three bounded Compose panels and four whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch092ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineMowReusedN3ReciprocalPairOneKunNoOnFourStrokesAndSystemBack() {
        disposable092()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-092-${UUID.randomUUID()}", "main")
        val head = "62c6d3e29b87d89a2027bcb3d063081de23c4320"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-092-62c6d3e2-envelope.zip")
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
        assertEquals(1115, updated.kanji)
        assertEquals(5070, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("8445a5717d080dcc", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(124, n1.size)
        val mow = n1.single { it.kanji == "刈" }
        assertEquals(listOf("乃", "凹", "凸"), mow.distractors.splitSep())
        assertEquals(listOf("ガイ", "カイ"), mow.onyomi.splitSep())
        assertEquals(listOf("か.る"), mow.kunyomi.splitSep())
        assertNotNull(mow.quizOnyomi)
        assertNotNull(mow.quizKunyomi)
        assertEquals(emptyList<String>(), mow.quizOnyomi?.splitSep())
        assertEquals(listOf("か.る"), mow.quizKunyomi?.splitSep())
        assertEquals(emptyList<String>(), mow.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(listOf("かる"), mow.toReadingCard().quizKeys(ReadingKind.Kun))
        val expectedMeanings = mapOf(
            "刈" to "mow; reap", "凸" to "convex; protruding",
            "乃" to "thereupon; possessive no", "凹" to "concave; sunken",
        )
        val all = runBlocking { app.db.content().kanjiLite(source.id) }
        val checkedPools = JSONObject()
        for ((poolName, pool) in listOf("N1" to n1, "All" to all)) {
            val cards = pool.map { QuizCard(it.kanji, it.title, it.tags.splitSep(), it.distractors.splitSep()) }
            val target = cards.single { it.kanji == "刈" }
            assertEquals(listOf("乃", "凹", "凸"), target.distractors)
            val options = QuizBuilder.options(target, cards, kotlin.random.Random(662))
            assertEquals(4, options.size)
            assertEquals(expectedMeanings, options.associate { it.kanji to it.title })
            assertEquals(3, cards.count { it.kanji in target.distractors })
            checkedPools.put(poolName, JSONObject().put("poolSize", pool.size)
                .put("options", JSONArray().also { rows ->
                    options.forEach { rows.put(JSONObject().put("kanji", it.kanji).put("title", it.title)) }
                }).put("availableCuratedCount", cards.count { it.kanji in target.distractors })
                .put("fallbackOptions", options.count { it.kanji !in expectedMeanings }))
        }
        val importedMow = requireNotNull(runBlocking { app.db.content().word(source.id, "刈る") })
        assertEquals(listOf("切る", "収穫"), importedMow.quizExclusions.splitSep())
        assertEquals("かる", importedMow.reading)
        assertEquals(3, importedMow.jlpt)
        assertEquals("mow; clip; reap", importedMow.title)
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
                        if (card.kanji == "刈") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "刈" && (kind == ReadingKind.Kun && key == "かる")) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "刈", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("directWordGuardCount", importedMow.quizExclusions.splitSep().size)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(mow.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(mow.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(mow.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(mow.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(mow.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(mow.quizKunyomi).splitSep()))
            .put("productionBuilderN1AndAllExactChoices", checkedPools)
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; only 刈 meaning and kunかる due, no on keys. All three raw readings retained. Two historical good 刈 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 124 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("刈")
            click("mow; reap")
            await("刈 — mow; reap")
            show(articleBullet("Strokes: 4 · Key (radical): 刀 (no. 18), appearing as 刂 on the right · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("刈 concerns cutting growing things: mowing grass, clipping hair, or reaping crops. The native verb 刈る かる retains a cutting action; it is not a general word for every method of harvesting."), "kanji-03")
            show(articleBullet("Modern-shape mnemonic, not etymology: Picture the two crossed strokes on the left as growth to be clipped beside the upright knife form 刂 on the right. The indexing radical is 刀; 刂 is its right-hand form. This shape association is a memory aid, not a reconstruction of the character's history."), "kanji-04")
            section("Readings")
            show(readingExample("ガイ"), "kanji-09")
            show(readingExample("刈除 がいじょ — removal; cutting off; mowing"), "kanji-11")
            show(readingExample("カイ"), "kanji-12")
            show(readingExample("刈除 かいじょ — an alternative reading of the same word"), "kanji-14")
            show(readingExample("か.る"), "kanji-15")
            show(readingExample("刈る かる — mow; clip; reap"), "kanji-17")
            show(articleBullet("Focus practice on かる. The two on readings are retained for recognition: JMdict records both がいじょ and かいじょ for 刈除, without a spelling or sense restriction separating them. This does not establish how often either is used. In 刈る, 刈 supplies か and る is the written verb ending."), "kanji-18")
            section("Common words")
            show(articleBullet("刈る かる — mow; clip; reap"), "kanji-20")
            show(articleBullet("稲刈り いねかり — rice reaping; rice harvesting"), "kanji-21")
            show(articleBullet("The object helps with the English translation: 草を刈る (くさをかる) is mowing grass, 髪を刈る (かみをかる) is clipping hair, and 稲を刈る (いねをかる) is reaping rice plants. See the linked verb article for complete examples."), "kanji-22")
            section("Notes")
            show(articleBullet("切, \"cut,\" has a broader range. Compare 刈's crossed left strokes and separate upright 刂 with 切's left part and bent 刀 on the right."), "kanji-24")
            show(articleBullet("乃, \"thereupon; possessive no,\" 凹, \"concave; sunken,\" and 凸, \"convex; protruding,\" do not mean mowing or reaping."), "kanji-25")
            show(articleBullet("Learn 刈る as a godan verb: 刈ります (かります), 刈った (かった), 刈らない (からない). These inflections do not add new dictionary readings."), "kanji-26")
            show(articleBullet("Metadata: KANJIDIC2, 2026-11-02 snapshot. Word families: JMdict, entries 1209540, 1209550 and 1167840. Native verb usage: Digital Daijisen and Nikkoku, 刈る. The ガイ compound is also recorded by Jitsu, 刈除; that heading does not independently verify カイ."), "kanji-27")
            section("Common words")
            show(articleBullet("刈る かる — mow; clip; reap"), "karu-forward")
            inline(await(articleBullet("刈る かる — mow; clip; reap")), "刈る", 0)
            await("Article contents")
            await("刈る (かる) - mow; clip; reap")
            section("Meaning")
            show(articleBullet("刈る means to cut grass, hair, crops, or similar growth: to mow, clip, shear, or reap according to the object. It is a transitive godan verb. The thing cut takes を; the polite form is 刈ります (かります), the past 刈った, and the negative 刈らない."), "karu-02")
            show(articleBullet("庭の草を刈りました。 (にわのくさをかりました。) - I cut the grass in the garden."), "karu-03")
            show(articleBullet("夏なので、髪を短く刈りました。 (なつなので、かみをみじかくかりました。) - Since it is summer, I had my hair cropped short."), "karu-04")
            show(articleBullet("短く describes the resulting short length in the second example."), "karu-05")
            section("How the kanji combine")
            show(articleBullet("刈 represents cutting or reaping. It supplies the native stem か, followed by the kana ending る. There is no multi-kanji compound to decompose."), "karu-07")
            section("Synonyms and antonyms")
            show(articleBullet("切る (きる) is the broader verb for cutting. It works with many objects that do not suit 刈る, such as a sheet of paper. 髪を切る, \"cut one's hair,\" does not specifically present the haircut as cropping or clipping."), "karu-09")
            section("Distinctive meaning")
            show(articleBullet("The object helps determine the English verb: 草を刈る is mowing or cutting grass, while 稲を刈る (いねをかる) is reaping rice plants. Do not extend the English gloss \"harvest\" to every crop or method of gathering food. 刈る retains a cutting action, rather than simply collecting something that has grown."), "karu-11")
            show(articleBullet("Dictionary: JMdict, entry 1209540, sense 1."), "karu-12")
            section("How the kanji combine")
            show(articleBullet("刈 represents cutting or reaping. It supplies the native stem か, followed by the kana ending る. There is no multi-kanji compound to decompose."), "karu-reverse")
            inline(await(articleBullet("刈 represents cutting or reaping. It supplies the native stem か, followed by the kana ending る. There is no multi-kanji compound to decompose.")), "刈", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("か.る"), "karu-kanji-backlink")
            back()
            await(articleBullet("刈 represents cutting or reaping. It supplies the native stem か, followed by the kana ending る. There is no multi-kanji compound to decompose.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("karu-system-back-to-word")
            back()
            await(articleBullet("刈る かる — mow; clip; reap")).assertIsDisplayed()
            section("Common words")
            capture("karu-system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 1).put("directedLinkTransitions", 2).put("activatedBaselinePairs", 1)
                .put("completeArticleProjections", 2).put("changedReusedArticles", 1)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            val meaning = quiz.ui as QuizUi.Question
            assertEquals("刈", meaning.card.kanji)
            val expectedMeanings = mapOf(
                "刈" to "mow; reap",
                "凸" to "convex; protruding",
                "乃" to "thereupon; possessive no",
                "凹" to "concave; sunken",
            )
            assertEquals(4, meaning.options.size)
            assertEquals(expectedMeanings, meaning.options.associate { it.kanji to it.title })
            assertTrue(meaning.options.all { option -> n1.any { it.kanji == option.kanji && it.title == option.title } })
            assertTrue(meaning.options.any { it.kanji == "凹" })
            assertEquals(0, meaning.options.count { it.kanji !in expectedMeanings })
            assertEquals("mow; reap", meaning.options.single { it.kanji == "刈" }.title)
            assertEquals(listOf("乃", "凹", "凸"), meaning.card.distractors.splitSep())
            for (option in meaning.options) await(option.title).assertIsDisplayed()
            evidence.put("exactDefaultMeaningOptions", JSONArray().also { options ->
                meaning.options.forEach { option ->
                    options.put(JSONObject().put("kanji", option.kanji).put("title", option.title))
                }
            }).put("actualN1CuratedAvailable", 3).put("actualN1FallbackOptions", 0)
                .put("meaningChoiceVisualAdjudicationRequired", true)
            capture("meaning-question")
            click("mow; reap")
            await("Correct!")
            assertEquals("刈", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKeys = mutableSetOf<String>()
            repeat(1) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("刈", question.card.kanji)
                assertEquals(ReadingKind.Kun, question.question.kind)
                val key = question.question.correctKey
                assertTrue(key in setOf("かる"))
                assertTrue("Duplicate target reading key", answeredKeys.add(key))
                assertEquals(key, question.question.correctKey)
                assertFalse(question.question.options.any { it.key.isBlank() })
                assertEquals(1, question.question.options.count { it.key == key })
                capture("curated-${key}-question")
                click(question.question.options.single { it.key == key }.label)
                await(if (question.question.kind == ReadingKind.On) "Correct! — on'yomi" else "Correct! — kun'yomi")
                assertTrue((reading.ui as ReadingUi.Answer).correct)
                capture("curated-${key}-feedback")
                click("Next")
                rule.waitUntil(30_000) { runBlocking {
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "刈" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf("かる"), answeredKeys)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(1, done.answered)
            assertEquals(1, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "刈" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(1, readingLogs.size)
            assertEquals(setOf("かる"), readingLogs.map { it.reading }.toSet())
            assertTrue(readingLogs.all { it.mode == ReadingKind.Kun.mode.name })
            capture("curated-one-kun-no-on-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("mow; reap").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "刈") })
            assertEquals(listOf("乃", "凹", "凸"), card.distractors.splitSep())
            assertEquals(listOf("ガイ", "カイ"), card.onyomi.splitSep())
            assertEquals(listOf("か.る"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(emptyList<String>(), card.quizOnyomi?.splitSep())
            assertEquals(listOf("か.る"), card.quizKunyomi?.splitSep())
            evidence.put("fullProjectionOnyomi", JSONArray(card.onyomi.splitSep()))
                .put("fullProjectionKunyomi", JSONArray(card.kunyomi.splitSep()))
                .put("fullProjectionQuizOnyomi", JSONArray(requireNotNull(card.quizOnyomi).splitSep()))
                .put("fullProjectionQuizKunyomi", JSONArray(requireNotNull(card.quizKunyomi).splitSep()))
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(4, strokes.length())
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
            rule.onNode(hasContentDescription("4 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "刈" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "刈" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("onlyKunKaruNoOnPersistedGoodAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-092-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-092-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-092-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
