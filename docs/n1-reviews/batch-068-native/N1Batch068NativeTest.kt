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

private fun disposable068() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch068GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun ceremonyLookalikesAndRadicalVariantsAcrossFourProductionFamilies() {
        disposable068()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val text = "儀 義 億 優 倍 人 亻 式 礼 辞 行 亍 弋 彳 礻 儀式 礼儀 行儀 お辞儀"
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 068: ceremony / look-alikes / radical variants")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(text, fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect 儀 versus 義/億/優/倍, 人 versus 亻, all four mapped words and actual fallback components 亍/弋/彳/礻. Fallback families may coincide.", fontSize = 18.sp)
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
            for (char in listOf("儀", "義", "億", "優", "倍", "人", "亻", "式", "礼", "辞", "行", "亍", "弋", "彳", "礻")) {
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
            for (word in listOf("儀式", "礼儀", "行儀", "お辞儀")) {
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
        assertEquals(76, rows.length())
        rule.waitForIdle()
        rule.onAllNodesWithText(text).assertCountEquals(4)
        for (index in fonts.indices) rule.onAllNodesWithText(text)[index].assertIsDisplayed()
        File(context.getExternalFilesDir(null), "n1-068-font-pairs.png").outputStream().use {
            assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        File(context.getExternalFilesDir(null), "n1-068-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 60).put("wholeWordRasterProbes", 16)
            .put("limits", "Sixty single-character native Paint probes including 人/亻 and actual fallback components 亍/弋/彳/礻, sixteen whole-word nonblank raster probes and four production Compose rows. Actual readability requires visual inspection; emulator not phone; fallback face not identified.")
            .toString(2))
    }
}

class N1Batch068ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineCeremonyEightReciprocalPairsOnOnlyDrawingAndSystemBack() {
        disposable068()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-068-${UUID.randomUUID()}", "main")
        val head = "7ca40a695d8e01f4176f4afcca91b1e4d2d6c0b0"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-068-7ca40a69-envelope.zip")
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
        assertEquals(1080, updated.kanji)
        assertEquals(5037, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("ddef65b637fe2f85", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(100, n1.size)
        val ceremony = n1.single { it.kanji == "儀" }
        assertEquals(listOf("ギ"), ceremony.onyomi.splitSep())
        assertEquals(emptyList<String>(), ceremony.kunyomi.splitSep())
        assertNotNull(ceremony.quizOnyomi)
        assertNotNull(ceremony.quizKunyomi)
        assertEquals(listOf("ギ"), ceremony.quizOnyomi?.splitSep())
        assertEquals(emptyList<String>(), ceremony.quizKunyomi?.splitSep())
        assertEquals(listOf("ぎ"), ceremony.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(emptyList<String>(), ceremony.toReadingCard().quizKeys(ReadingKind.Kun))
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
                        if (card.kanji == "儀") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "儀" && (kind == ReadingKind.On && key == "ぎ")) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "儀", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(ceremony.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(ceremony.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(ceremony.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(ceremony.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 儀 meaning and sole curated on key due; explicit no-kun. Two historical good 儀 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 100 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("儀")
            click("ceremony; formal conduct")
            await("儀 — ceremony; formal conduct")
            show(articleBullet("Strokes: 15 · Key (radical): 人 (as 亻, no. 9) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("儀 appears in words for ceremonies and formal conduct: 儀式 ぎしき is a ceremony or ritual, while 礼儀 れいぎ concerns manners or etiquette. Learn the whole word rather than translating every 儀 as \"ceremony.\""), "kanji-03")
            show(articleBullet("The visible parts are 亻, the side form of 人, and 義 on the right. Modern-shape mnemonic: picture a person standing beside an elaborate ceremonial pattern. This is a visual memory aid, not a historical explanation of the character."), "kanji-04")
            section("Readings")
            show(readingExample("儀式 ぎしき — ceremony; 礼儀 れいぎ — manners; etiquette"), "kanji-11")
            show(articleBullet("The frozen character dictionary gives ギ and no kun reading. The same ギ occurs in 行儀 ぎょうぎ, \"manners; behavior,\" and お辞儀 おじぎ, \"bow; bowing.\""), "kanji-12")
            section("Common words")
            show(articleBullet("儀式 ぎしき — ceremony; rite; ritual"), "kanji-14")
            show(articleBullet("礼儀 れいぎ — manners; etiquette"), "kanji-15")
            show(articleBullet("行儀 ぎょうぎ — manners; behavior"), "kanji-16")
            show(articleBullet("お辞儀 おじぎ — bow; bowing"), "kanji-17")
            section("Notes")
            show(articleBullet("儀 also has a \"matter; affair; case\" branch. In formal letters and notices, this suffix typically follows a noun referring to oneself or one's own side, adding a humble nuance: 私儀（わたくしぎ）, \"as for me.\" This is a formal written use, not an ordinary conversational suffix."), "kanji-19")
            show(articleBullet("Not all compounds concern conduct: 地球儀（ちきゅうぎ）is an Earth globe, a model of the Earth, not a ceremony."), "kanji-20")
            show(articleBullet("式 overlaps in the ceremony sense; 礼 overlaps in manners and also names a bow. These are useful comparisons, not interchangeable characters."), "kanji-21")
            show(articleBullet("義 alone lacks the left-hand 亻. It also has the reading ギ, but its meanings include righteousness and meaning; a shared sound does not make the spellings interchangeable."), "kanji-22")
            show(articleBullet("億, \"hundred million,\" 優, \"gentle; superior,\" and 倍, \"multiple; double,\" share 亻 but have different right-hand shapes."), "kanji-23")
            show(articleBullet("Metadata: KANJIDIC2. Word pairs: JMdict, entries 1224690, 1224700, 1557470, 1281890, 1002030, 1311150, 1421000 and 1956040. Usage: Nikkoku, 儀; Nikkoku, 地球儀."), "kanji-24")
            section("Common words")
            inline(await(articleBullet("儀式 ぎしき — ceremony; rite; ritual")), "儀式", 0)
            await("儀式 (ぎしき) - ceremony; rite; ritual")
            section("Meaning")
            show(articleBullet("儀式 is a ceremony or ritual carried out according to an established form. It is a noun and can describe religious observances or other ceremonial acts."), "word1-02")
            show(articleBullet("神社で伝統的な儀式を見ました。 (じんじゃででんとうてきなぎしきをみました。) - I watched a traditional ceremony at a Shinto shrine."), "word1-03")
            show(articleBullet("儀式は静かに始まりました。 (ぎしきはしずかにはじまりました。) - The ceremony began quietly."), "word1-04")
            section("How the kanji combine")
            show(articleBullet("儀 concerns ceremony or formal observance; 式 concerns a form, method, or ceremony. Their on readings combine as ギ + シキ. The two characters reinforce the idea of a prescribed ceremonial form."), "word1-06")
            section("Synonyms and antonyms")
            show(articleBullet("式 (しき) also names a ceremony, as well as a formula or style in other contexts. 勤め (つとめ) has a religious-service sense in addition to work or duty. Its ordinary employment meaning is not a synonym of 儀式."), "word1-08")
            section("Distinctive meaning")
            show(articleBullet("English \"service\" can describe a religious ceremony, but it can also mean customer service or help. 儀式 covers the ceremonial use, not every サービス. Context, rather than the English spelling alone, establishes which sense is intended."), "word1-10")
            show(articleBullet("Dictionary: JMdict, entry 1224700, sense 1; compare 1240810."), "word1-11")
            section("How the kanji combine")
            inline(await(articleBullet("儀 concerns ceremony or formal observance; 式 concerns a form, method, or ceremony. Their on readings combine as ギ + シキ. The two characters reinforce the idea of a prescribed ceremonial form.")), "儀", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("儀式 ぎしき — ceremony; 礼儀 れいぎ — manners; etiquette"), "word1-new-kanji-backlink")
            back()
            section("How the kanji combine")
            inline(await(articleBullet("儀 concerns ceremony or formal observance; 式 concerns a form, method, or ceremony. Their on readings combine as ギ + シキ. The two characters reinforce the idea of a prescribed ceremonial form.")), "式", 42)
            await("式 — ceremony; formula")
            show(articleBullet("Strokes: 6 · Key (radical): 弋 (no. 56) · JLPT: N3 (community list)"), "component1-01")
            section("Meaning and origin")
            show(articleBullet("式 can name a ceremony, a formula, or an established form or method. An 入学式 にゅうがくしき is a school entrance ceremony; a 数式 すうしき is a mathematical expression. In 形式 けいしき, the focus is form or format. These are word-specific meanings, not one English translation that fits everywhere."), "component1-03")
            show(articleBullet("Modern-shape mnemonic: picture 工 fitted inside the long slanting, hooked 弋 shape, like a small pattern held in place. This is a way to remember the modern layout, not a verified account of its origin."), "component1-04")
            section("Readings")
            show(readingExample("形式 けいしき — format; 入学式 にゅうがくしき — school entrance ceremony"), "component1-11")
            section("Common words")
            show(articleBullet("形式 けいしき — form; format"), "component1-13")
            show(articleBullet("入学式 にゅうがくしき — school entrance ceremony"), "component1-14")
            show(articleBullet("数式 すうしき — mathematical expression; formula"), "component1-15")
            show(articleBullet("儀式 ぎしき — ceremony; rite; ritual"), "component1-16")
            section("Notes")
            show(articleBullet("試 contains the entire 式 shape beside 言, but means testing or trying. 代 contains 弋 beside a person component, without 工. 工 alone lacks the surrounding strokes. These comparisons help recognition; they do not establish phonetic relationships."), "component1-18")
            show(articleBullet("Sources: KANJIDIC2; JMdict, entries 1319060, 1250310, 1465910, 1373070."), "component1-19")
            section("Common words")
            inline(await(articleBullet("儀式 ぎしき — ceremony; rite; ritual")), "儀式", 0)
            await("儀式 (ぎしき) - ceremony; rite; ritual")
            section("How the kanji combine")
            show(articleBullet("儀 concerns ceremony or formal observance; 式 concerns a form, method, or ceremony. Their on readings combine as ギ + シキ. The two characters reinforce the idea of a prescribed ceremonial form."), "word1-legacy-backlink")
            back()
            await("Common words")
            capture("system-back-component1")
            back()
            await("How the kanji combine")
            capture("system-back-word1-component")
            back()
            await("Common words")
            capture("system-back-kanji-word1")
            section("Common words")
            inline(await(articleBullet("礼儀 れいぎ — manners; etiquette")), "礼儀", 0)
            await("礼儀 (れいぎ) - manners; etiquette")
            section("Meaning")
            show(articleBullet("礼儀 is a noun for manners, courtesy, or etiquette: conduct that shows appropriate consideration or respect in a social setting."), "word2-02")
            show(articleBullet("子どもに食事の礼儀を教えます。 (こどもにしょくじのれいぎをおしえます。) - I teach children table manners."), "word2-03")
            show(articleBullet("人の家では礼儀を守りましょう。 (ひとのいえではれいぎをまもりましょう。) - Let's observe good manners in other people's homes."), "word2-04")
            show(articleBullet("礼儀を守る means observing etiquette. 礼儀正しい (れいぎただしい) means well-mannered or courteous; use the full expression rather than assuming the noun alone is an い-adjective."), "word2-05")
            section("How the kanji combine")
            show(articleBullet("礼 contributes courtesy or respectful conduct, and 儀 contributes ceremony or form. Together they express the forms of considerate, socially appropriate behavior. The on readings are レイ + ギ."), "word2-07")
            section("Synonyms and antonyms")
            show(articleBullet("マナー overlaps with manners or etiquette. 丁寧 (ていねい) describes politeness or care and can also apply to how work is done. 失礼 (しつれい), discourtesy or rudeness, provides a useful contrast in social conduct."), "word2-09")
            section("Distinctive meaning")
            show(articleBullet("礼儀 is not merely grammar or a collection of polite verb endings. It can concern greetings, eating, listening, or conduct as a guest. What counts as appropriate depends on the people and situation; the word itself does not establish one universal rule. In a sentence about 礼儀, identify the specific behavior rather than assuming an unexplained cultural requirement."), "word2-11")
            show(articleBullet("Dictionary: JMdict, entry 1557470, sense 1."), "word2-12")
            section("How the kanji combine")
            inline(await(articleBullet("礼 contributes courtesy or respectful conduct, and 儀 contributes ceremony or form. Together they express the forms of considerate, socially appropriate behavior. The on readings are レイ + ギ.")), "儀", 50)
            await("Article contents")
            section("Readings")
            show(readingExample("儀式 ぎしき — ceremony; 礼儀 れいぎ — manners; etiquette"), "word2-new-kanji-backlink")
            back()
            section("How the kanji combine")
            inline(await(articleBullet("礼 contributes courtesy or respectful conduct, and 儀 contributes ceremony or form. Together they express the forms of considerate, socially appropriate behavior. The on readings are レイ + ギ.")), "礼", 0)
            await("礼 — bow; thanks")
            show(articleBullet("Strokes: 5 · Key (radical): 示 (as 礻, no. 113) · JLPT: N3 (community list)"), "component2-01")
            section("Meaning and origin")
            show(articleBullet("礼 belongs to the language of respect: a bow, good manners, or an expression of gratitude. 御礼 おれい means thanks; the same word can be written お礼. The polite wording does not make 礼 itself an honorific prefix."), "component2-03")
            show(articleBullet("Modern-shape mnemonic: beside 礻, imagine the bent stroke on the right as a person bending in a bow. This is only a memory picture for the modern form."), "component2-04")
            section("Readings")
            show(readingExample("礼 れい — bow; thanks; 御礼 おれい — thanks"), "component2-11")
            show(readingExample("失礼 しつれい — discourtesy; an \"excuse me\" expression"), "component2-14")
            show(articleBullet("The source also lists ライ; no kun reading is supplied."), "component2-15")
            section("Common words")
            show(articleBullet("御礼 おれい — thanks; gratitude"), "component2-17")
            show(articleBullet("礼 れい — bow; manners; thanks"), "component2-18")
            show(articleBullet("失礼 しつれい — discourtesy; excuse me"), "component2-19")
            show(articleBullet("礼儀 れいぎ — manners; etiquette"), "component2-20")
            section("Notes")
            show(articleBullet("礼をする (れいをする) means \"make a bow.\" 失礼します (しつれいします), \"excuse me,\" is a courtesy expression, not an announcement that one intends to be rude."), "component2-22")
            show(articleBullet("神, 祖, and 福 also begin with 礻. Identify 礼 by its much simpler right-hand stroke rather than treating the whole group as one meaning."), "component2-23")
            show(articleBullet("Word evidence: JMdict, entries 1270810, 1557450, 1320230."), "component2-24")
            section("Common words")
            inline(await(articleBullet("礼儀 れいぎ — manners; etiquette")), "礼儀", 0)
            await("礼儀 (れいぎ) - manners; etiquette")
            section("How the kanji combine")
            show(articleBullet("礼 contributes courtesy or respectful conduct, and 儀 contributes ceremony or form. Together they express the forms of considerate, socially appropriate behavior. The on readings are レイ + ギ."), "word2-legacy-backlink")
            back()
            await("Common words")
            capture("system-back-component2")
            back()
            await("How the kanji combine")
            capture("system-back-word2-component")
            back()
            await("Common words")
            capture("system-back-kanji-word2")
            section("Common words")
            inline(await(articleBullet("行儀 ぎょうぎ — manners; behavior")), "行儀", 0)
            await("行儀 (ぎょうぎ) - manners; behavior")
            section("Meaning")
            show(articleBullet("行儀 is a noun for manners or behavior, especially how someone conducts themselves around others. Learn it in 行儀がいい, \"well-mannered,\" and 行儀が悪い (ぎょうぎがわるい), \"badly behaved; ill-mannered.\""), "word3-02")
            show(articleBullet("子どもたちは行儀よく座っていました。 (こどもたちはぎょうぎよくすわっていました。) - The children were sitting nicely."), "word3-03")
            show(articleBullet("食事中に大声で騒ぐのは行儀が悪いです。 (しょくじちゅうにおおごえでさわぐのはぎょうぎがわるいです。) - Making a loud commotion during a meal is bad manners."), "word3-04")
            show(articleBullet("行儀よく modifies an action. Before a noun, 行儀のいい子 (ぎょうぎのいいこ) means \"a well-behaved child.\""), "word3-05")
            section("How the kanji combine")
            show(articleBullet("行 concerns conduct or actions here, rather than going to a destination. 儀 contributes forms or standards of behavior. Together they name the manner in which someone behaves. The readings are ギョウ + ギ."), "word3-07")
            section("Synonyms and antonyms")
            show(articleBullet("礼儀 (れいぎ) also concerns manners, with attention to courtesy and social etiquette. The words overlap, but 行儀 is useful for concrete conduct such as sitting or eating."), "word3-09")
            show(articleBullet("態度 (たいど) describes attitude or manner of dealing with someone more broadly."), "word3-10")
            section("Distinctive meaning")
            show(articleBullet("行儀 itself does not mean \"good manners\": the evaluation comes from いい or 悪い. Likewise, お行儀 (おぎょうぎ) adds the prefix お without changing the basic noun into an adjective. The contrasting evaluations, not two separate nouns, express good versus bad behavior."), "word3-12")
            show(articleBullet("Dictionary: JMdict, entry 1281890, sense 1."), "word3-13")
            section("How the kanji combine")
            inline(await(articleBullet("行 concerns conduct or actions here, rather than going to a destination. 儀 contributes forms or standards of behavior. Together they name the manner in which someone behaves. The readings are ギョウ + ギ.")), "儀", 72)
            await("Article contents")
            section("Readings")
            show(readingExample("儀式 ぎしき — ceremony; 礼儀 れいぎ — manners; etiquette"), "word3-new-kanji-backlink")
            back()
            section("How the kanji combine")
            inline(await(articleBullet("行 concerns conduct or actions here, rather than going to a destination. 儀 contributes forms or standards of behavior. Together they name the manner in which someone behaves. The readings are ギョウ + ギ.")), "行", 0)
            await("行 — go")
            show(articleBullet("Strokes: 6 · Key (radical): 行 (no. 144) · JLPT: N5 (community list)"), "component3-01")
            section("Meaning and origin")
            show(articleBullet("行 is commonly explained as a pictograph of a crossroads: the oldest forms show two roads crossing. The left and right halves later became independent components, 彳 (a step, as in 待 and 径) and 亍. From \"road\" the meanings extend to \"go\", \"travel\" and \"carry out\" (おこなう), and then to \"a line or row\" (as in a line of text, 一行 いちぎょう) and \"a business\" (as in 銀行, bank). Because 行 is its own radical, it is both a key and a character."), "component3-03")
            section("Readings")
            show(readingExample("旅行 りょこう, 銀行 ぎんこう, 運行 うんこう, 急行 きゅうこう"), "component3-10")
            show(readingExample("行事 ぎょうじ, 行間 ぎょうかん, 一行 いちぎょう (one line)"), "component3-13")
            show(readingExample("行脚 あんぎゃ, 行灯 あんどん (rare, from older Chinese readings)"), "component3-16")
            show(readingExample("行く いく, 行き先 いきさき, 行き方 いきかた"), "component3-19")
            show(readingExample("行く ゆく (literary or set phrases: 行く年 ゆくとし, 行方 ゆくえ)"), "component3-22")
            show(readingExample("行う おこなう (to carry out, hold an event)"), "component3-25")
            section("Common words")
            show(articleBullet("行く いく — to go"), "component3-27")
            show(articleBullet("旅行 りょこう — trip, travel"), "component3-28")
            show(articleBullet("銀行 ぎんこう — bank"), "component3-29")
            show(articleBullet("行儀 ぎょうぎ — manners; behavior"), "component3-30")
            section("Notes")
            show(articleBullet("The kun reading is い.く in everyday speech; ゆく is literary or fixed (行方 ゆくえ, 行く末 ゆくすえ). 行 plus 〜き gives 行き (bound for): 東京行き とうきょうゆき／とうきょういき."), "component3-32")
            show(articleBullet("行く is irregular in the て／た form: 行って, 行った (not 行いて)."), "component3-33")
            show(articleBullet("Special on readings: コウ is the usual one in compounds (旅行, 銀行), ギョウ is for \"line/event\" (行事), アン for a few Buddhist or old words."), "component3-34")
            show(articleBullet("Related: 来 (come, the opposite direction of travel in deixis) and 出 (go out)."), "component3-35")
            section("Common words")
            inline(await(articleBullet("行儀 ぎょうぎ — manners; behavior")), "行儀", 0)
            await("行儀 (ぎょうぎ) - manners; behavior")
            section("How the kanji combine")
            show(articleBullet("行 concerns conduct or actions here, rather than going to a destination. 儀 contributes forms or standards of behavior. Together they name the manner in which someone behaves. The readings are ギョウ + ギ."), "word3-legacy-backlink")
            back()
            await("Common words")
            capture("system-back-component3")
            back()
            await("How the kanji combine")
            capture("system-back-word3-component")
            back()
            await("Common words")
            capture("system-back-kanji-word3")
            section("Common words")
            inline(await(articleBullet("お辞儀 おじぎ — bow; bowing")), "お辞儀", 0)
            await("お辞儀 (おじぎ) - bow; bowing")
            section("Meaning")
            show(articleBullet("お辞儀 is a bow or bowing. Use お辞儀をする or お辞儀する for the action. The person bowed to can take に."), "word4-02")
            show(articleBullet("先生にお辞儀をしました。 (せんせいにおじぎをしました。) - I bowed to the teacher."), "word4-03")
            show(articleBullet("彼は深くお辞儀をして、部屋を出ました。 (かれはふかくおじぎをして、へやをでました。) - He bowed deeply and left the room."), "word4-04")
            show(articleBullet("The expression describes the bodily gesture; its purpose can be a greeting, thanks, respect, or an apology."), "word4-05")
            section("How the kanji combine")
            show(articleBullet("The spelling 御辞儀 also represents おじぎ: 御 writes the prefix お. In お辞儀, that prefix is written in kana. The base 辞儀 has the on-readings ジ + ギ; 辞 has speech-related associations and 儀 concerns formal conduct. Learn the established bowing meaning rather than a literal translation such as \"refusal ceremony.\""), "word4-07")
            show(articleBullet("The kango grouping describes the base 辞儀, not the origin of the Japanese prefix."), "word4-08")
            section("Synonyms and antonyms")
            show(articleBullet("礼 (れい) also names a bow, as in 礼をする (れいをする). 礼儀 (れいぎ) concerns manners or etiquette more generally, not one particular bow."), "word4-10")
            section("Distinctive meaning")
            show(articleBullet("Do not assume that every お辞儀 expresses gratitude: the gesture's social meaning depends on the situation. Nor does the polite prefix prescribe one correct angle or duration for every occasion. This article teaches the word and its basic construction, not a complete etiquette system."), "word4-12")
            show(articleBullet("Dictionary: JMdict, entry 1002030, sense 1; compare 1733730 and 1557450, sense 3."), "word4-13")
            section("How the kanji combine")
            inline(await(articleBullet("The spelling 御辞儀 also represents おじぎ: 御 writes the prefix お. In お辞儀, that prefix is written in kana. The base 辞儀 has the on-readings ジ + ギ; 辞 has speech-related associations and 儀 concerns formal conduct. Learn the established bowing meaning rather than a literal translation such as \"refusal ceremony.\"")), "儀", 178)
            await("Article contents")
            section("Readings")
            show(readingExample("儀式 ぎしき — ceremony; 礼儀 れいぎ — manners; etiquette"), "word4-new-kanji-backlink")
            back()
            section("How the kanji combine")
            inline(await(articleBullet("The spelling 御辞儀 also represents おじぎ: 御 writes the prefix お. In お辞儀, that prefix is written in kana. The base 辞儀 has the on-readings ジ + ギ; 辞 has speech-related associations and 儀 concerns formal conduct. Learn the established bowing meaning rather than a literal translation such as \"refusal ceremony.\"")), "辞", 140)
            await("辞 — words; resign")
            show(articleBullet("Strokes: 13 · Key (radical): 辛 (no. 160) · JLPT: N3 (community list)"), "component4-01")
            section("Meaning and origin")
            show(articleBullet("辞 has a word-related branch, seen in 辞書 じしょ, \"dictionary,\" and a leaving-a-position branch, seen in 辞める やめる, \"resign.\" Keep both meanings available instead of trying to translate every compound with one English gloss."), "component4-03")
            show(articleBullet("Modern-shape mnemonic: imagine the left 舌-shaped part delivering words beside the tall 辛 on the right. This labels visible shapes for memory only; it does not establish their historical roles."), "component4-04")
            section("Readings")
            show(readingExample("辞書 じしょ — dictionary; 辞任 じにん — resignation"), "component4-11")
            show(readingExample("辞める やめる — resign; quit a job"), "component4-14")
            section("Common words")
            show(articleBullet("辞書 じしょ — dictionary"), "component4-16")
            show(articleBullet("辞める やめる — resign; leave a job"), "component4-17")
            show(articleBullet("辞任 じにん — resignation from a position"), "component4-18")
            show(articleBullet("お辞儀 おじぎ — bow; bowing"), "component4-19")
            section("Notes")
            show(articleBullet("辞める concerns giving up a position, not every action translated \"stop.\" The left 舌 begins with strokes resembling 千; the right 辛 includes a 立-like upper shape. 新 has a partially similar upright arrangement but a different right side."), "component4-21")
            show(articleBullet("Dictionary: JMdict, entries 1318970, 1318950, 1319000."), "component4-22")
            section("Common words")
            inline(await(articleBullet("お辞儀 おじぎ — bow; bowing")), "お辞儀", 0)
            await("お辞儀 (おじぎ) - bow; bowing")
            section("How the kanji combine")
            show(articleBullet("The spelling 御辞儀 also represents おじぎ: 御 writes the prefix お. In お辞儀, that prefix is written in kana. The base 辞儀 has the on-readings ジ + ギ; 辞 has speech-related associations and 儀 concerns formal conduct. Learn the established bowing meaning rather than a literal translation such as \"refusal ceremony.\""), "word4-legacy-backlink")
            back()
            await("Common words")
            capture("system-back-component4")
            back()
            await("How the kanji combine")
            capture("system-back-word4-component")
            back()
            await("Common words")
            capture("system-back-kanji-word4")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            assertEquals("儀", (quiz.ui as QuizUi.Question).card.kanji)
            capture("meaning-question")
            click("ceremony; formal conduct")
            await("Correct!")
            assertEquals("儀", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKinds = mutableSetOf<ReadingKind>()
            repeat(1) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("儀", question.card.kanji)
                assertTrue("Duplicate target reading kind", answeredKinds.add(question.question.kind))
                assertEquals(ReadingKind.On, question.question.kind)
                val key = "ぎ"
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "儀" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf(ReadingKind.On), answeredKinds)
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "儀" && it.mode == ReadingKind.Kun.mode.name }
            })
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("ceremony; formal conduct").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "儀") })
            assertEquals(listOf("ギ"), card.onyomi.splitSep())
            assertEquals(emptyList<String>(), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("ギ"), card.quizOnyomi?.splitSep())
            assertEquals(emptyList<String>(), card.quizKunyomi?.splitSep())
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
                    it.kanji == "儀" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "儀" && it.mode == StudyMode.Draw.name && it.grade == 1 }
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
            File(app.getExternalFilesDir(null), "n1-068-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-068-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-068-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
