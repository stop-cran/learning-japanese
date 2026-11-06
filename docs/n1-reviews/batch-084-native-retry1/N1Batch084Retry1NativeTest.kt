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

private fun disposable084() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch084Retry1GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun dignifiedLookalikesAndRadicalFallbacksAcrossFourProductionFamilies() {
        disposable084()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("冗 冫 冴 冷 准 凍 凛 凜 凹 厳 声 寒 揚 明 朗 朝 気 澄 激 確 示 禾 稟 透", "通 険 静 鷹", "凜 凛 冫 稟 禾 示 准 冗 凹 凜とした 凛とした")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 084: dignified / look-alikes / radical fallback")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 28 scoped Han; focused 凜/凛/冫/稟 and 禾/示, 准/冗/凹. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("冗", "冫", "冴", "冷", "准", "凍", "凛", "凜", "凹", "厳", "声", "寒", "揚", "明", "朗", "朝", "気", "澄", "激", "確", "示", "禾", "稟", "透", "通", "険", "静", "鷹")) {
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
            for (word in listOf("凜とした", "凛とした")) {
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
        assertEquals(120, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-084-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-084-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 112).put("wholeWordRasterProbes", 8).put("panels", 3)
            .put("limits", "28 actual scoped Han including exact 凜/凛/冫/稟 fallback inspection, four production families, three bounded Compose panels and eight whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch084Retry1ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineDignifiedReciprocalPairSoleOnDrawingAndSystemBack() {
        disposable084()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-084-${UUID.randomUUID()}", "main")
        val head = "53b6819b22787a2517cd0ad14aa855d357cbc70a"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-084-53b6819b-envelope.zip")
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
        assertEquals(1096, updated.kanji)
        assertEquals(5053, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("74b87b47347b78c1", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(116, n1.size)
        val dignified = n1.single { it.kanji == "凜" }
        assertEquals(listOf("准", "冗", "凹"), dignified.distractors.splitSep())
        assertEquals(listOf("リン"), dignified.onyomi.splitSep())
        assertEquals(listOf("きびし.い"), dignified.kunyomi.splitSep())
        assertNotNull(dignified.quizOnyomi)
        assertNotNull(dignified.quizKunyomi)
        assertEquals(listOf("リン"), dignified.quizOnyomi?.splitSep())
        assertEquals(emptyList<String>(), dignified.quizKunyomi?.splitSep())
        assertEquals(listOf("りん"), dignified.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(emptyList<String>(), dignified.toReadingCard().quizKeys(ReadingKind.Kun))
        val expectedMeanings = mapOf(
            "凜" to "dignified; bracing cold", "准" to "quasi-; associate rank",
            "冗" to "superfluous; redundant", "凹" to "concave; sunken",
        )
        val all = runBlocking { app.db.content().kanjiLite(source.id) }
        val checkedPools = JSONObject()
        for ((poolName, pool) in listOf("N1" to n1, "All" to all)) {
            val cards = pool.map { QuizCard(it.kanji, it.title, it.tags.splitSep(), it.distractors.splitSep()) }
            val target = cards.single { it.kanji == "凜" }
            assertEquals(listOf("准", "冗", "凹"), target.distractors)
            assertEquals(expectedMeanings, cards.filter { it.kanji in expectedMeanings }.associate { it.kanji to it.title })
            val options = QuizBuilder.options(target, cards, kotlin.random.Random(586))
            assertEquals(4, options.size)
            assertEquals(expectedMeanings, options.associate { it.kanji to it.title })
            checkedPools.put(poolName, JSONObject().put("poolSize", pool.size)
                .put("options", JSONArray().also { rows ->
                    options.forEach { rows.put(JSONObject().put("kanji", it.kanji).put("title", it.title)) }
                }).put("allThreeCuratedAvailable", true).put("defaultFourNoPadding", true))
        }
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
                        if (card.kanji == "凜") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "凜" && kind == ReadingKind.On && key == "りん") now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "凜", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(dignified.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(dignified.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(dignified.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(dignified.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(dignified.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(dignified.quizKunyomi).splitSep()))
            .put("productionBuilderN1AndAllExactChoices", checkedPools)
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 凜 meaning and sole curated onりん due, kun[] source-onlyきびし.い not queued. Two historical good 凜 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 116 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("凜")
            click("dignified; bracing cold")
            await("凜 — dignified; bracing cold")
            show(articleBullet("Strokes: 15 · Key (radical): 冫 (the two left-hand marks, no. 15) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("凜 can describe a dignified, tightly composed bearing or bracing, severe cold. Learn it through 凜 (りん), especially 凜とした before a noun. The word also has a clear, ringing sound sense; these meanings are not interchangeable descriptions of everything that is \"strict.\""), "kanji-03")
            show(articleBullet("Modern-shape mnemonic, not etymology: imagine the two icy 冫 marks beside the tall right-hand 稟 (りん) block as someone standing straight in bracing air. The bottom of that block has the 禾 shape. This is an invented memory aid, not a verified historical or phonetic explanation."), "kanji-04")
            section("Readings")
            show(articleBullet("Both source readings are preserved in source order. Only リン is selected for reading practice; there are no selected kun questions."), "kanji-06")
            show(readingExample("リン"), "kanji-10")
            show(readingExample("凜 りん — dignified; bracing cold, as in 凜とした"), "kanji-12")
            show(readingExample("きびし.い"), "kanji-13")
            show(readingExample("source-only character-dictionary lookup information; no exact non-name example established in the inspected families"), "kanji-15")
            show(articleBullet("Do not invent a spelling such as 凜しい from the source-only row. The ordinary adjective 厳しい (きびしい) is a different spelling, not evidence for an example written with 凜. This is a bounded evidence limit, not a claim that no dictionary could record such a form."), "kanji-16")
            section("Common words")
            show(articleBullet("凜 りん — dignified; bracing cold"), "kanji-18")
            show(articleBullet("凜とした声 (りんとしたこえ) — a clear, firm voice"), "kanji-19")
            show(articleBullet("凜とした朝の寒気 (りんとしたあさのかんき) — the bracing chill of the morning"), "kanji-20")
            section("Notes")
            show(articleBullet("凛 is a recognized variant of 凜, with the same りん reading in the linked word's dictionary family. Compare the lowest right-hand part: 凜 has 禾, while 凛 has a 示-shaped bottom. They are different characters for typing and this card's identity; practice writing the displayed 凜. No separate variant card or personal-name reading course is supplied here. The grade-9 source classification concerns name-use kanji, not name-only usage."), "kanji-22")
            show(articleBullet("For other visual contrasts, 准 has a bird-shaped right side, 冗 has a cover-like top, and 凹 has a sunken outline. Their meanings are not dignified bearing or bracing cold."), "kanji-23")
            show(articleBullet("Metadata: KANJIDIC2, database 2026-306, 2026-11-02. Word: JMdict, entry 1564320. Meaning, variant and example phrases: Digital Daijisen: 凜."), "kanji-24")
            section("Common words")
            show(articleBullet("凜 りん — dignified; bracing cold"), "word-forward")
            inline(await(articleBullet("凜 りん — dignified; bracing cold")), "凜", 0)
            await("Article contents")
            await("凜 (りん) — dignified; bracing cold")
            section("Meaning")
            show(articleBullet("凜 describes a dignified, firmly composed bearing, or cold that feels sharp and bracing. It can also describe a clear, ringing voice or sound. Learn the constructions 凜と and 凜とした + noun, rather than adding な as if this were an ordinary な-adjective."), "word-02")
            show(articleBullet("凜とした声がひびく。 (りんとしたこえがひびく。) — A clear, firm voice rings out."), "word-03")
            show(articleBullet("凜とした朝の寒気 (りんとしたあさのかんき) — The bracing chill of the morning."), "word-04")
            show(articleBullet("These short examples come from Daijisen. The second is a noun phrase, not a complete sentence. In both, とした describes the following noun; it does not necessarily report an earlier change into that state. 凜と can modify an action. JMdict labels the word a taru adjective and an adverb taking と; that classification does not make 凜 an い-adjective."), "word-05")
            section("How the kanji combine")
            show(articleBullet("This is a single-character Sino-Japanese word, not a compound. 凜 supplies the whole on reading リン and the dignity/coldness meaning. JMdict also recognizes 凛 (りん) in the same lexical family. The variant spelling does not introduce another pronunciation or word."), "word-07")
            section("Synonyms and antonyms")
            show(articleBullet("寒い (さむい) is the broader everyday adjective for cold weather or surroundings. 凜とした adds the sharp, bracing quality in the morning example; it is not a neutral substitute for every occurrence of 寒い. 厳しい (きびしい) can describe severe cold, but also strict standards and harsh circumstances; do not transfer all those uses to 凜."), "word-09")
            show(articleBullet("澄む (すむ) overlaps for a clear, resonant voice. 冷静 (れいせい) emphasizes mental composure and clear-headedness, not necessarily the dignified outward bearing conveyed by 凜とした. Warmth contrasts with the cold sense, but is not an opposite of dignity."), "word-10")
            section("Distinctive meaning")
            show(articleBullet("A 凜とした声 can sound clear and firm without being loud, angry or cruel. Likewise, a dignified manner does not establish someone's social rank or moral superiority. Select the translation from what is being described."), "word-12")
            show(articleBullet("The full dictionary family also records a tense atmosphere sense. This article focuses on bearing, sound and bracing cold; it is not an exhaustive account of every literary or historical construction. Neither dictionary inclusion nor the variant spelling establishes a frequency ranking. Personal-name usage is outside this article's scope."), "word-13")
            show(articleBullet("Dictionary: JMdict, entry 1564320, all four senses. Constructions and short example bases: Digital Daijisen: 凜; adverbial senses: Seisen: 凜と."), "word-14")
            section("How the kanji combine")
            show(articleBullet("This is a single-character Sino-Japanese word, not a compound. 凜 supplies the whole on reading リン and the dignity/coldness meaning. JMdict also recognizes 凛 (りん) in the same lexical family. The variant spelling does not introduce another pronunciation or word."), "word-reverse")
            inline(await(articleBullet("This is a single-character Sino-Japanese word, not a compound. 凜 supplies the whole on reading リン and the dignity/coldness meaning. JMdict also recognizes 凛 (りん) in the same lexical family. The variant spelling does not introduce another pronunciation or word.")), "凜", 63)
            await("Article contents")
            section("Readings")
            show(readingExample("リン"), "word-kanji-backlink")
            back()
            await(articleBullet("This is a single-character Sino-Japanese word, not a compound. 凜 supplies the whole on reading リン and the dignity/coldness meaning. JMdict also recognizes 凛 (りん) in the same lexical family. The variant spelling does not introduce another pronunciation or word.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("word-system-back-to-word")
            back()
            await(articleBullet("凜 りん — dignified; bracing cold")).assertIsDisplayed()
            section("Common words")
            capture("word-system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 1).put("directedLinkTransitions", 2)
                .put("completeArticleProjections", 2)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            val meaning = quiz.ui as QuizUi.Question
            assertEquals("凜", meaning.card.kanji)
            val expectedMeanings = mapOf(
                "凜" to "dignified; bracing cold",
                "准" to "quasi-; associate rank",
                "冗" to "superfluous; redundant",
                "凹" to "concave; sunken",
            )
            assertEquals(4, meaning.options.size)
            assertEquals(expectedMeanings, meaning.options.associate { it.kanji to it.title })
            assertEquals(listOf("准", "冗", "凹"), meaning.card.distractors.splitSep())
            for (option in meaning.options) await(option.title).assertIsDisplayed()
            evidence.put("exactDefaultMeaningOptions", JSONArray().also { options ->
                meaning.options.forEach { option ->
                    options.put(JSONObject().put("kanji", option.kanji).put("title", option.title))
                }
            }).put("exactCuratedChoicesWithoutFallback", true)
            capture("meaning-question")
            click("dignified; bracing cold")
            await("Correct!")
            assertEquals("凜", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKinds = mutableSetOf<ReadingKind>()
            repeat(1) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("凜", question.card.kanji)
                assertTrue("Duplicate target reading kind", answeredKinds.add(question.question.kind))
                assertEquals(ReadingKind.On, question.question.kind)
                val key = "りん"
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "凜" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf(ReadingKind.On), answeredKinds)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(1, done.answered)
            assertEquals(1, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "凜" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(1, readingLogs.size)
            assertEquals(setOf("りん"), readingLogs.map { it.reading }.toSet())
            capture("curated-on-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("dignified; bracing cold").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "凜") })
            assertEquals(listOf("准", "冗", "凹"), card.distractors.splitSep())
            assertEquals(listOf("リン"), card.onyomi.splitSep())
            assertEquals(listOf("きびし.い"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("リン"), card.quizOnyomi?.splitSep())
            assertEquals(emptyList<String>(), card.quizKunyomi?.splitSep())
            evidence.put("fullProjectionOnyomi", JSONArray(card.onyomi.splitSep()))
                .put("fullProjectionKunyomi", JSONArray(card.kunyomi.splitSep()))
                .put("fullProjectionQuizOnyomi", JSONArray(requireNotNull(card.quizOnyomi).splitSep()))
                .put("fullProjectionQuizKunyomi", JSONArray(requireNotNull(card.quizKunyomi).splitSep()))
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(15, strokes.length())
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
            rule.onNode(hasContentDescription("15 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "凜" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "凜" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("soleCuratedOnPersistedGoodAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-084-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-084-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-084-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
