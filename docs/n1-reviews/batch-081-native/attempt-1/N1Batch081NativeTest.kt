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

private fun disposable081() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch081GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun smeltingLookalikesAndIceWaterFallbacksAcrossFourProductionFamilies() {
        disposable081()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("世 事 典 冫 冶 台 大 女 始 字 学 属 氵 治 溶 界 百 研 科 究 精 術 製 通", "金 鋳 錬 鍛 陶", "冶 治 台 始 冫 氵 冶金 金 鋳 錬 鍛 陶 溶")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 081: smelting / look-alikes / ice and water fallback")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 29 scoped Han; focused 冶/治/台/始, 冫/氵. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("世", "事", "典", "冫", "冶", "台", "大", "女", "始", "字", "学", "属", "氵", "治", "溶", "界", "百", "研", "科", "究", "精", "術", "製", "通", "金", "鋳", "錬", "鍛", "陶")) {
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
            for (word in listOf("冶金")) {
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
            File(context.getExternalFilesDir(null), "n1-081-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-081-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 116).put("wholeWordRasterProbes", 4).put("panels", 3)
            .put("limits", "29 actual scoped Han including exact 冫/氵 fallback inspection, four production families, three bounded Compose panels and four whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch081ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineSmeltingTwoReciprocalPairsCuratedOnDrawingAndSystemBack() {
        disposable081()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-081-${UUID.randomUUID()}", "main")
        val head = "95a87783e4be501c4b2b788d6906f6cc76b3c751"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-081-95a87783-envelope.zip")
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
        assertEquals(1093, updated.kanji)
        assertEquals(5049, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("f1dd5d8b9d2ff535", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(113, n1.size)
        val smelting = n1.single { it.kanji == "冶" }
        assertEquals(listOf("ヤ"), smelting.onyomi.splitSep())
        assertEquals(listOf("い.る"), smelting.kunyomi.splitSep())
        assertNotNull(smelting.quizOnyomi)
        assertNotNull(smelting.quizKunyomi)
        assertEquals(listOf("ヤ"), smelting.quizOnyomi?.splitSep())
        assertEquals(emptyList<String>(), smelting.quizKunyomi?.splitSep())
        assertEquals(listOf("や"), smelting.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(emptyList<String>(), smelting.toReadingCard().quizKeys(ReadingKind.Kun))
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
                        if (card.kanji == "冶") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "冶" && kind == ReadingKind.On && key == "や") now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "冶", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(smelting.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(smelting.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(smelting.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(smelting.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(smelting.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(smelting.quizKunyomi).splitSep()))
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 冶 meaning and sole curated on key や due. Explicit empty kun list. Two historical good 冶 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 113 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("冶")
            click("smelt; work metals")
            await("冶 — smelt; work metals")
            show(articleBullet("Strokes: 7 · Key (radical): 冫 (the two left-hand strokes, no. 15) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("冶 concerns smelting and working metals. Learn it through 冶金 (やきん), metallurgy: the science and technology of obtaining and working metals. Not every use is literal metalworking: 陶冶 (とうや) can mean cultivation or training, for example of character or abilities."), "kanji-03")
            show(articleBullet("Modern-shape mnemonic: imagine the two cold 冫 marks beside a 台-shaped work stand where metal is being shaped. This is an invented memory aid, not a historical derivation or a verified explanation of the sound."), "kanji-04")
            section("Readings")
            show(articleBullet("Both source readings remain below. Only ヤ is selected for reading practice."), "kanji-06")
            show(readingExample("ヤ"), "kanji-10")
            show(readingExample("冶金 やきん — metallurgy"), "kanji-12")
            show(readingExample("い.る"), "kanji-13")
            show(readingExample("source-only character-dictionary lookup information; no exact modern word example written 冶る was established in the inspected families"), "kanji-15")
            show(articleBullet("The source-only row is not a recommendation to invent everyday spellings. 鋳る (いる), \"cast metal,\" is a separately documented spelling, not proof of a word written 冶る. Keeping this reading for lookup does not claim that no such example exists anywhere."), "kanji-16")
            section("Common words")
            show(articleBullet("冶金 やきん — metallurgy"), "kanji-18")
            show(articleBullet("冶金学 (やきんがく) — metallurgy as a science"), "kanji-19")
            section("Notes")
            show(articleBullet("Compare 治, \"govern; heal\": its left side has three water strokes, 氵, rather than 冶's two strokes, 冫. 始, \"begin,\" has 女 on the left. Sharing the 台-shaped right side does not make these characters interchangeable."), "kanji-21")
            show(articleBullet("鍛冶 (かじ), \"blacksmithing; blacksmith,\" has a special whole-word reading. Do not extract ジ from its final kana and add it to 冶's on readings. The dictionaries also document the separate reading たんや for 鍛冶."), "kanji-22")
            show(articleBullet("For general melting or dissolving, compare 溶 and 溶かす (とかす). 冶 is not the ordinary spelling to substitute into a sentence about melting butter or dissolving sugar."), "kanji-23")
            show(articleBullet("Metadata: KANJIDIC2. Word evidence: JMdict, entries 1536310, 1536320, 1655600, 1419150 and 1587780. Character readings and senses: Digital Daijisen and 字通: 冶."), "kanji-24")
            section("Common words")
            show(articleBullet("冶金 やきん — metallurgy"), "word-forward-15")
            inline(await(articleBullet("冶金 やきん — metallurgy")), "冶金", 0)
            await("Article contents")
            await("冶金 (やきん) — metallurgy")
            section("Meaning")
            show(articleBullet("冶金 is metallurgy: the science and technology of extracting metals from raw materials and working them into useful materials and forms. It includes more than simply melting something. It is a technical noun."), "word-02")
            show(articleBullet("大学で冶金を学んでいます。 (だいがくでやきんをまなんでいます。) — I am studying metallurgy at university."), "word-03")
            show(articleBullet("冶金について研究しています。 (やきんについてけんきゅうしています。) — I am doing research on metallurgy."), "word-04")
            show(articleBullet("冶金を学ぶ (やきんをまなぶ) means \"study metallurgy\"; 冶金について (やきんについて) means \"about metallurgy.\""), "word-05")
            section("How the kanji combine")
            show(articleBullet("冶 (ヤ) contributes smelting or working metal. 金 (キン) means metal here, not money or gold alone. The relationship is action plus object: working metal. The whole noun names the technical field, not just one operation. This is a meaning aid, not an account of the word's historical formation."), "word-07")
            section("Synonyms and antonyms")
            show(articleBullet("冶金学 (やきんがく) specifically names metallurgy as a science. 金属 (きんぞく) means the material \"metal,\" not the field that studies and processes it. 製錬 and 精錬 (both せいれん) concern smelting or refining: related processes rather than the whole discipline. There is no useful everyday opposite of the field's name."), "word-09")
            section("Distinctive meaning")
            show(articleBullet("冶金 belongs in scientific, educational and industrial contexts. It does not mean making money, and it is not limited to gold. 錬金術 (れんきんじゅつ), \"alchemy,\" is a different term, not a synonym for modern metallurgy."), "word-11")
            show(articleBullet("Use 溶かす (とかす) when describing an action such as melting butter or dissolving sugar; 冶金 names the metalworking field and its technology, not any act of making something liquid."), "word-12")
            show(articleBullet("Dictionary: JMdict, entry 1536310; related entries 1536320, 1243040, 1380250 and 1559970. Scope: 世界大百科事典: 冶金."), "word-13")
            section("How the kanji combine")
            show(articleBullet("冶 (ヤ) contributes smelting or working metal. 金 (キン) means metal here, not money or gold alone. The relationship is action plus object: working metal. The whole noun names the technical field, not just one operation. This is a meaning aid, not an account of the word's historical formation."), "word-reverse-25")
            inline(await(articleBullet("冶 (ヤ) contributes smelting or working metal. 金 (キン) means metal here, not money or gold alone. The relationship is action plus object: working metal. The whole noun names the technical field, not just one operation. This is a meaning aid, not an account of the word's historical formation.")), "冶", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("ヤ"), "kanji-backlink")
            back()
            await(articleBullet("冶 (ヤ) contributes smelting or working metal. 金 (キン) means metal here, not money or gold alone. The relationship is action plus object: working metal. The whole noun names the technical field, not just one operation. This is a meaning aid, not an account of the word's historical formation.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("system-back-to-word")
            section("How the kanji combine")
            show(articleBullet("冶 (ヤ) contributes smelting or working metal. 金 (キン) means metal here, not money or gold alone. The relationship is action plus object: working metal. The whole noun names the technical field, not just one operation. This is a meaning aid, not an account of the word's historical formation."), "gold-forward-26")
            inline(await(articleBullet("冶 (ヤ) contributes smelting or working metal. 金 (キン) means metal here, not money or gold alone. The relationship is action plus object: working metal. The whole noun names the technical field, not just one operation. This is a meaning aid, not an account of the word's historical formation.")), "金", 45)
            await("Article contents")
            await("金 — gold, money")
            section("Common words")
            show(articleBullet("冶金 やきん — metallurgy"), "gold-reverse-27")
            inline(await(articleBullet("冶金 やきん — metallurgy")), "冶金", 0)
            await("Article contents")
            await("冶金 (やきん) — metallurgy")
            back()
            await(articleBullet("冶金 やきん — metallurgy")).assertIsDisplayed()
            section("Common words")
            capture("system-back-to-gold")
            back()
            await(articleBullet("冶 (ヤ) contributes smelting or working metal. 金 (キン) means metal here, not money or gold alone. The relationship is action plus object: working metal. The whole noun names the technical field, not just one operation. This is a meaning aid, not an account of the word's historical formation.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("system-back-to-word-from-gold")
            back()
            await(articleBullet("冶金 やきん — metallurgy")).assertIsDisplayed()
            section("Common words")
            capture("system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 2).put("directedLinkTransitions", 4)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            assertEquals("冶", (quiz.ui as QuizUi.Question).card.kanji)
            capture("meaning-question")
            click("smelt; work metals")
            await("Correct!")
            assertEquals("冶", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKinds = mutableSetOf<ReadingKind>()
            repeat(1) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("冶", question.card.kanji)
                assertTrue("Duplicate target reading kind", answeredKinds.add(question.question.kind))
                assertEquals(ReadingKind.On, question.question.kind)
                val key = "や"
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "冶" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf(ReadingKind.On), answeredKinds)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(1, done.answered)
            assertEquals(1, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "冶" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(1, readingLogs.size)
            assertEquals(setOf("や"), readingLogs.map { it.reading }.toSet())
            capture("curated-on-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("smelt; work metals").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "冶") })
            assertEquals(listOf("ヤ"), card.onyomi.splitSep())
            assertEquals(listOf("い.る"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("ヤ"), card.quizOnyomi?.splitSep())
            assertEquals(emptyList<String>(), card.quizKunyomi?.splitSep())
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
                    it.kanji == "冶" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "冶" && it.mode == StudyMode.Draw.name && it.grade == 1 }
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
            File(app.getExternalFilesDir(null), "n1-081-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-081-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-081-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
