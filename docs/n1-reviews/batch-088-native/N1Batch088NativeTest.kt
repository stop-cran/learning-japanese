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

private fun disposable088() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch088GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun triumphLookalikesAndRadicalFallbacksAcrossFourProductionFamilies() {
        disposable088()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("会 優 公 几 凡 凱 凸 凹 勝 和 国 大 宅 山", "帰 戻 手 故 旋 歌 演 祝 豆 豈 選 風 鬨", "凱 几 豈 山 豆 鬨 凡 凸 凹 勝 歌 旋 凱旋")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 088: triumph / look-alikes / radical fallback")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 27 scoped Han; focused 凱/凡/凸/凹 and 几/豈/鬨. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("会", "優", "公", "几", "凡", "凱", "凸", "凹", "勝", "和", "国", "大", "宅", "山", "帰", "戻", "手", "故", "旋", "歌", "演", "祝", "豆", "豈", "選", "風", "鬨")) {
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
            for (word in listOf("凱旋")) {
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
        assertEquals(112, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-088-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-088-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 108).put("wholeWordRasterProbes", 4).put("panels", 3)
            .put("limits", "27 actual scoped Han including exact 几/豈/鬨 fallback inspection, four production families, three bounded Compose panels and four whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch088ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineTriumphOneReciprocalPairOneOnKeyNoKunDrawingAndSystemBack() {
        disposable088()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-088-${UUID.randomUUID()}", "main")
        val head = "e445d826118681e1df9687eb53d144eed7d66139"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-088-e445d826-envelope.zip")
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
        assertEquals(1111, updated.kanji)
        assertEquals(5067, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("afff40af0e155dbe", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(120, n1.size)
        val triumph = n1.single { it.kanji == "凱" }
        assertEquals(listOf("凡", "凸", "凹"), triumph.distractors.splitSep())
        assertEquals(listOf("ガイ", "カイ"), triumph.onyomi.splitSep())
        assertEquals(listOf("かちどき", "やわらぐ"), triumph.kunyomi.splitSep())
        assertNotNull(triumph.quizOnyomi)
        assertNotNull(triumph.quizKunyomi)
        assertEquals(listOf("ガイ"), triumph.quizOnyomi?.splitSep())
        assertEquals(emptyList<String>(), triumph.quizKunyomi?.splitSep())
        assertEquals(listOf("がい"), triumph.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(emptyList<String>(), triumph.toReadingCard().quizKeys(ReadingKind.Kun))
        val expectedMeanings = mapOf(
            "凱" to "victory song; triumph", "凸" to "convex; protruding",
            "凡" to "commonplace; mediocre", "凹" to "concave; sunken",
        )
        val all = runBlocking { app.db.content().kanjiLite(source.id) }
        val checkedPools = JSONObject()
        for ((poolName, pool) in listOf("N1" to n1, "All" to all)) {
            val cards = pool.map { QuizCard(it.kanji, it.title, it.tags.splitSep(), it.distractors.splitSep()) }
            val target = cards.single { it.kanji == "凱" }
            assertEquals(listOf("凡", "凸", "凹"), target.distractors)
            val options = QuizBuilder.options(target, cards, kotlin.random.Random(622))
            assertEquals(4, options.size)
            assertEquals(expectedMeanings, options.associate { it.kanji to it.title })
            assertEquals(3, cards.count { it.kanji in target.distractors })
            checkedPools.put(poolName, JSONObject().put("poolSize", pool.size)
                .put("options", JSONArray().also { rows ->
                    options.forEach { rows.put(JSONObject().put("kanji", it.kanji).put("title", it.title)) }
                }).put("availableCuratedCount", cards.count { it.kanji in target.distractors })
                .put("fallbackOptions", options.count { it.kanji !in expectedMeanings }))
        }
        val importedReturn = requireNotNull(runBlocking { app.db.content().word(source.id, "凱旋") })
        assertEquals(listOf("帰る", "帰宅", "帰り", "戻る"), importedReturn.quizExclusions.splitSep())
        assertEquals("がいせん", importedReturn.reading)
        assertNull(importedReturn.jlpt)
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
                        if (card.kanji == "凱") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "凱" && kind == ReadingKind.On && key in setOf("がい")) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "凱", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("directWordGuardCount", importedReturn.quizExclusions.splitSep().size)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(triumph.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(triumph.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(triumph.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(triumph.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(triumph.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(triumph.quizKunyomi).splitSep()))
            .put("productionBuilderN1AndAllExactChoices", checkedPools)
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 凱 meaning and exactly onがい due; explicit kun[] and unselectedカイ give no questions. Two historical good 凱 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 120 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("凱")
            click("victory song; triumph")
            await("凱 — victory song; triumph")
            show(articleBullet("Strokes: 12 · Key (radical): 几 (no. 16) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("凱 concerns the celebration of victory: a victory song or cry, and triumph. Learn it in 凱旋 がいせん, \"triumphant return.\" The character also has a separate dictionary sense of becoming gentle or calm, seen in 凱風 (がいふう), \"southerly wind\"; do not force the victory meaning into that compound."), "kanji-03")
            show(articleBullet("Modern-shape mnemonic, not etymology: the left side 豈 resembles 山, \"mountain,\" above 豆 (まめ), \"bean.\" Imagine a victory celebration beside that stacked shape. The right-hand 几 is the indexing radical. This is a memory aid, not a historical or phonetic derivation."), "kanji-04")
            section("Readings")
            show(readingExample("ガイ"), "kanji-09")
            show(readingExample("凱旋 がいせん — triumphant return"), "kanji-11")
            show(readingExample("カイ"), "kanji-12")
            show(readingExample("Preserved from the character dictionaries; no verified modern word example is supplied here."), "kanji-14")
            show(readingExample("かちどき"), "kanji-15")
            show(readingExample("Character-dictionary reading/gloss: a victory cry. The noun is written 勝どき or 勝鬨 (かちどき) in the inspected word dictionary, not 凱."), "kanji-17")
            show(readingExample("やわらぐ"), "kanji-18")
            show(readingExample("Character-dictionary reading/gloss: become gentle or calm. This is not a verified ordinary verb spelling with 凱."), "kanji-20")
            show(articleBullet("Only ガイ is selected for reading practice. The other three readings remain lookup information, not proposed everyday word spellings. In particular, 凱風 is read がいふう, not やわらぐ. The native verb 和らぐ (やわらぐ), \"soften; subside,\" is a separate spelling; do not construct an example such as 凱ぐ from this metadata."), "kanji-21")
            section("Common words")
            show(articleBullet("凱旋 がいせん — triumphant return"), "kanji-23")
            show(articleBullet("凱歌 (がいか) — victory song; victory"), "kanji-24")
            show(articleBullet("The second word can concern victory itself, not necessarily an actual song."), "kanji-25")
            section("Notes")
            show(articleBullet("勝 concerns winning; 凱 emphasizes victory celebration in the compounds above. 歌 means a song or singing more generally."), "kanji-27")
            show(articleBullet("凡 concerns the commonplace or general, while 凸 and 凹 concern projecting and sunken shapes, not triumph."), "kanji-28")
            show(articleBullet("Grade 9 is the source's name-use classification, not a claim that 凱 occurs only in names. 凱旋 is a non-name example; personal-name readings are outside this card's scope."), "kanji-29")
            show(articleBullet("Metadata: KANJIDIC2, 2026-11-02 snapshot. Word pairs: JMdict, entries 1203190, 1203200, 1791660, 1706780 and 1561950. Character readings and senses: Digital Daijisen and Jitsu, 凱."), "kanji-30")
            section("Common words")
            show(articleBullet("凱旋 がいせん — triumphant return"), "return-forward")
            inline(await(articleBullet("凱旋 がいせん — triumphant return")), "凱旋", 0)
            await("Article contents")
            await("凱旋 (がいせん) — triumphant return")
            section("Meaning")
            show(articleBullet("凱旋 is a triumphant return after victory or success. It is a noun and forms the intransitive verb 凱旋する: the person or team returns. Although associated with returning after victory in battle, it also describes returns after sporting or performing success."), "return-02")
            show(articleBullet("大会で優勝した選手が故国に凱旋した。 (たいかいでゆうしょうしたせんしゅがここくにがいせんした。) — The athlete who won the championship returned to their homeland in triumph."), "return-03")
            show(articleBullet("選手の凱旋を祝った。 (せんしゅのがいせんをいわった。) — We celebrated the athlete's triumphant return."), "return-04")
            show(articleBullet("In the first example, the returning athlete is marked with が and the destination with に. A destination can also take へ. 凱旋する is not a verb for returning an object to its owner. In the second example, 凱旋 is a noun: the return is what people celebrated."), "return-05")
            section("How the kanji combine")
            show(articleBullet("凱 contributes victory celebration or victory music; 旋 (せん) contributes returning in this compound. Together, they describe a return characterized by triumph, not just an ordinary trip back. The on-readings are ガイ + セン. This explanation does not make \"return\" the only meaning of 旋 in other words."), "return-07")
            section("Synonyms and antonyms")
            show(articleBullet("帰る (かえる), \"return home,\" and 戻る (もどる), \"go back,\" can describe the same movement without expressing triumph. 帰宅 (きたく), \"returning home,\" likewise does not imply success."), "return-09")
            show(articleBullet("優勝 (ゆうしょう), \"championship victory,\" names the winning, not the subsequent return. A person can win without having returned yet. There is no need to treat every unsuccessful return as a fixed opposite word of 凱旋."), "return-10")
            section("Distinctive meaning")
            show(articleBullet("Use 凱旋 when the return is presented as a success worth celebrating, not merely for coming home after work. The word does not require that the person won a championship: success in a performance can also motivate a triumphant homecoming."), "return-12")
            show(articleBullet("For recognition, 凱旋公演 (がいせんこうえん) is a performance given after a successful tour abroad. This is not a label for every local concert or every performance after a journey."), "return-13")
            show(articleBullet("Dictionary: JMdict, entries 1203200 and 2042620. Meaning, component explanation and extended usage: Digital Daijisen, 凱旋."), "return-14")
            section("How the kanji combine")
            show(articleBullet("凱 contributes victory celebration or victory music; 旋 (せん) contributes returning in this compound. Together, they describe a return characterized by triumph, not just an ordinary trip back. The on-readings are ガイ + セン. This explanation does not make \"return\" the only meaning of 旋 in other words."), "return-reverse")
            inline(await(articleBullet("凱 contributes victory celebration or victory music; 旋 (せん) contributes returning in this compound. Together, they describe a return characterized by triumph, not just an ordinary trip back. The on-readings are ガイ + セン. This explanation does not make \"return\" the only meaning of 旋 in other words.")), "凱", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("ガイ"), "return-kanji-backlink")
            back()
            await(articleBullet("凱 contributes victory celebration or victory music; 旋 (せん) contributes returning in this compound. Together, they describe a return characterized by triumph, not just an ordinary trip back. The on-readings are ガイ + セン. This explanation does not make \"return\" the only meaning of 旋 in other words.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("return-system-back-to-word")
            back()
            await(articleBullet("凱旋 がいせん — triumphant return")).assertIsDisplayed()
            section("Common words")
            capture("return-system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 1).put("directedLinkTransitions", 2)
                .put("completeArticleProjections", 2).put("changedReusedArticles", 0)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            val meaning = quiz.ui as QuizUi.Question
            assertEquals("凱", meaning.card.kanji)
            val expectedMeanings = mapOf(
                "凱" to "victory song; triumph",
                "凸" to "convex; protruding",
                "凡" to "commonplace; mediocre",
                "凹" to "concave; sunken",
            )
            assertEquals(4, meaning.options.size)
            assertTrue(meaning.options.all { option -> n1.any { it.kanji == option.kanji && it.title == option.title } })
            assertTrue(meaning.options.any { it.kanji == "凹" })
            assertEquals(0, meaning.options.count { it.kanji !in expectedMeanings })
            assertEquals("victory song; triumph", meaning.options.single { it.kanji == "凱" }.title)
            assertEquals(listOf("凡", "凸", "凹"), meaning.card.distractors.splitSep())
            for (option in meaning.options) await(option.title).assertIsDisplayed()
            evidence.put("exactDefaultMeaningOptions", JSONArray().also { options ->
                meaning.options.forEach { option ->
                    options.put(JSONObject().put("kanji", option.kanji).put("title", option.title))
                }
            }).put("actualN1CuratedAvailable", 3).put("actualN1FallbackOptions", 0)
                .put("meaningChoiceVisualAdjudicationRequired", true)
            capture("meaning-question")
            click("victory song; triumph")
            await("Correct!")
            assertEquals("凱", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKeys = mutableSetOf<String>()
            repeat(1) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("凱", question.card.kanji)
                assertEquals(ReadingKind.On, question.question.kind)
                val key = question.question.correctKey
                assertTrue(key in setOf("がい"))
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "凱" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf("がい"), answeredKeys)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(1, done.answered)
            assertEquals(1, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "凱" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(1, readingLogs.size)
            assertEquals(setOf("がい"), readingLogs.map { it.reading }.toSet())
            assertTrue(readingLogs.all { it.mode == ReadingKind.On.mode.name })
            capture("curated-one-on-no-kun-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("victory song; triumph").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "凱") })
            assertEquals(listOf("凡", "凸", "凹"), card.distractors.splitSep())
            assertEquals(listOf("ガイ", "カイ"), card.onyomi.splitSep())
            assertEquals(listOf("かちどき", "やわらぐ"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("ガイ"), card.quizOnyomi?.splitSep())
            assertEquals(emptyList<String>(), card.quizKunyomi?.splitSep())
            evidence.put("fullProjectionOnyomi", JSONArray(card.onyomi.splitSep()))
                .put("fullProjectionKunyomi", JSONArray(card.kunyomi.splitSep()))
                .put("fullProjectionQuizOnyomi", JSONArray(requireNotNull(card.quizOnyomi).splitSep()))
                .put("fullProjectionQuizKunyomi", JSONArray(requireNotNull(card.quizKunyomi).splitSep()))
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(12, strokes.length())
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
            rule.onNode(hasContentDescription("12 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "凱" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "凱" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("singleCuratedOnKeyPersistedGoodAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-088-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-088-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-088-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
