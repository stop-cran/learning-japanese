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

private fun disposable070() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch070GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun recompenseLookalikesAndRadicalVariantsAcrossFourProductionFamilies() {
        disposable070()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val text = "償 賞 儀 僧 億 人 亻 補 衣 衤 礻 甫 捕 手 扌 初 複 保 証 埋 損 害 償う 補償 補う"
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 070: recompense / look-alikes / radical variants")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(text, fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect 償/賞 and 人/亻; 補 has 衣 as 衤, not 礻. Compare 捕/扌 and 初/複. Check all three words. Fallback families may coincide.", fontSize = 18.sp)
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
            for (char in listOf("償", "賞", "儀", "僧", "億", "人", "亻", "補", "衣", "衤", "礻", "甫", "捕", "手", "扌", "初", "複", "保", "証", "埋", "損", "害")) {
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
            for (word in listOf("償う", "補償", "補う")) {
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
        assertEquals(100, rows.length())
        rule.waitForIdle()
        rule.onAllNodesWithText(text).assertCountEquals(4)
        for (index in fonts.indices) rule.onAllNodesWithText(text)[index].assertIsDisplayed()
        File(context.getExternalFilesDir(null), "n1-070-font-pairs.png").outputStream().use {
            assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        File(context.getExternalFilesDir(null), "n1-070-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 88).put("wholeWordRasterProbes", 12)
            .put("limits", "Native single-character Paint probes including 人/亻 and 衣/衤/礻 plus twelve whole-word rasters and four production Compose rows. Actual readability requires visual inspection; emulator not phone; fallback face not identified.")
            .toString(2))
    }
}

class N1Batch070ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineRecompenseThreeReciprocalPairsBothReadingsDrawingAndSystemBack() {
        disposable070()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-070-${UUID.randomUUID()}", "main")
        val head = "fce81d63caba02c311d9d87ba955002ec79fc4c9"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-070-fce81d63-envelope.zip")
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
        assertEquals(1082, updated.kanji)
        assertEquals(5040, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("a9867cc4b455639a", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(102, n1.size)
        val recompense = n1.single { it.kanji == "償" }
        assertEquals(listOf("ショウ"), recompense.onyomi.splitSep())
        assertEquals(listOf("つぐな.う"), recompense.kunyomi.splitSep())
        assertNotNull(recompense.quizOnyomi)
        assertNotNull(recompense.quizKunyomi)
        assertEquals(listOf("ショウ"), recompense.quizOnyomi?.splitSep())
        assertEquals(listOf("つぐな.う"), recompense.quizKunyomi?.splitSep())
        assertEquals(listOf("しょう"), recompense.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(listOf("つぐなう"), recompense.toReadingCard().quizKeys(ReadingKind.Kun))
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
                        if (card.kanji == "償") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "償" && ((kind == ReadingKind.On && key == "しょう") || (kind == ReadingKind.Kun && key == "つぐなう"))) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "償", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(recompense.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(recompense.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(recompense.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(recompense.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 償 meaning and both curated on/kun keys due. Two historical good 償 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 102 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("償")
            click("recompense; make amends")
            await("償 — recompense; make amends")
            show(articleBullet("Strokes: 17 · Key (radical): 人 (as 亻, no. 9) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("償 concerns making up for a loss, recompensing someone or making amends. 補償 ほしょう is compensation for loss; 償う つぐなう can describe compensating for a loss or atoning for wrongdoing. Not every use implies that someone committed a crime."), "kanji-03")
            show(articleBullet("The visible parts are 亻, the side form of 人, and 賞 on the right. Modern-shape mnemonic: picture a person handing over something valuable to make good a loss. This is a visual memory aid, not a historical or phonetic explanation."), "kanji-04")
            section("Readings")
            show(readingExample("補償 ほしょう — compensation for loss"), "kanji-11")
            show(readingExample("償う つぐなう — make amends; compensate for loss"), "kanji-14")
            show(articleBullet("In 償う, the kanji represents つぐな and う is okurigana. Both sourced readings are retained and selected for reading questions."), "kanji-15")
            section("Common words")
            show(articleBullet("補償 ほしょう — compensation for loss"), "kanji-17")
            show(articleBullet("償う つぐなう — make amends; compensate for loss"), "kanji-18")
            section("Notes")
            show(articleBullet("賞 also has ショウ, but its prize or reward meaning does not make 賞 and 償 interchangeable. Notice the extra 亻 in 償."), "kanji-20")
            show(articleBullet("補, \"supplement; make good,\" overlaps in supplying what is missing. Learn the whole word rather than dividing compensation and supplementation into absolute categories."), "kanji-21")
            show(articleBullet("儀, \"ceremony; formal conduct,\" 僧, \"Buddhist monk; priest,\" and 億, \"hundred million,\" share 亻 but have different right-hand shapes."), "kanji-22")
            show(articleBullet("Metadata: KANJIDIC2, 2026-11-02 snapshot. Word pairs: JMdict, entries 1346020 and 1514650. Usage: Daijisen and Nikkoku, 償う; Nikkoku, 補償."), "kanji-23")
            section("Common words")
            inline(await(articleBullet("償う つぐなう — make amends; compensate for loss")), "償う", 0)
            await("償う (つぐなう) - make amends; compensate for loss")
            section("Meaning")
            show(articleBullet("償う is a transitive godan verb: make up for a loss or debt, or make amends for wrongdoing. The loss, debt or wrongdoing being made up for takes を. Compensation can involve money or goods; making amends can also involve actions."), "word1-02")
            show(articleBullet("彼は損害を償いました。 (かれはそんがいをつぐないました。) - He compensated for the damage."), "word1-03")
            show(articleBullet("彼は自分の過ちを償おうとしています。 (かれはじぶんのあやまちをつぐなおうとしています。) - He is trying to make amends for his mistake."), "word1-04")
            show(articleBullet("Forms include 償います (つぐないます), 償わない (つぐなわない), 償った (つぐなった), and 償って (つぐなって)."), "word1-05")
            section("How the kanji combine")
            show(articleBullet("償 contributes making good a loss or making amends. つぐな is represented by the kanji; う is okurigana. The compound reading ショウ does not replace つぐな in this verb."), "word1-07")
            section("Synonyms and antonyms")
            show(articleBullet("補償 (ほしょう), used with する, focuses on compensation for loss. 補う (おぎなう) is broader supplementation or making up for a shortage; the words can overlap in loss contexts. Apologizing is not necessarily the same as making amends, and there is no single opposite that reverses both the compensation and atonement senses."), "word1-09")
            section("Distinctive meaning")
            show(articleBullet("償う does not always imply moral guilt: 損害 (そんがい), damage or loss, can be its object. Conversely, making amends for a mistake need not mean simply paying money. Context determines what would count as making good the harm."), "word1-11")
            show(articleBullet("The dictionary also records 償う as つぐのう. Nikkoku identifies つぐなう as the form much used today; this article teaches つぐなう rather than treating every recorded pronunciation as the modern default."), "word1-12")
            show(articleBullet("Dictionary: JMdict, entry 1346020. Usage and alternate reading: Daijisen and Nikkoku, 償う."), "word1-13")
            section("How the kanji combine")
            inline(await(articleBullet("償 contributes making good a loss or making amends. つぐな is represented by the kanji; う is okurigana. The compound reading ショウ does not replace つぐな in this verb.")), "償", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("償う つぐなう — make amends; compensate for loss"), "word1-new-kanji-backlink")
            back()
            await(articleBullet("償 contributes making good a loss or making amends. つぐな is represented by the kanji; う is okurigana. The compound reading ショウ does not replace つぐな in this verb.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("system-back-word1-kanji")
            back()
            await(articleBullet("償う つぐなう — make amends; compensate for loss")).assertIsDisplayed()
            section("Common words")
            capture("system-back-kanji-word1")
            section("Common words")
            inline(await(articleBullet("補償 ほしょう — compensation for loss")), "補償", 0)
            await("補償 (ほしょう) - compensation for loss")
            section("Meaning")
            show(articleBullet("補償 is compensation that makes good a loss. It is a noun and forms a transitive verb with する. With 補償する, the loss being compensated for takes を."), "word2-02")
            show(articleBullet("会社は事故による損害を補償しました。 (かいしゃはじこによるそんがいをほしょうしました。) - The company compensated for the damage caused by the accident."), "word2-03")
            show(articleBullet("私たちは補償を求めています。 (わたしたちはほしょうをもとめています。) - We are seeking compensation."), "word2-04")
            show(articleBullet("In the second example, 補償 is the noun object of 求める (もとめる), \"seek.\" Seeking compensation does not mean that it has already been paid."), "word2-05")
            section("How the kanji combine")
            show(articleBullet("補 contributes supplying what is missing; 償 contributes recompense or making good a loss. The near-synonymous parts reinforce the idea of making up for a loss. 補 supplies ホ and 償 supplies ショウ in ほしょう."), "word2-07")
            section("Synonyms and antonyms")
            show(articleBullet("償う (つぐなう) can mean compensating for a loss or making amends. 補う (おぎなう) is broader: it can also mean supplementing an explanation. 保証 (ほしょう), \"guarantee; warranty,\" is a different word despite the shared pronunciation. A promise or warranty is not itself compensation paid for a loss. There is no single everyday antonym covering every compensation context."), "word2-09")
            section("Distinctive meaning")
            show(articleBullet("This article focuses on practical compensation for loss, not the separate psychological or technical uses. Legal sources can distinguish particular types of 補償 from damages, but ordinary use can be broader; do not infer that 補償 always excludes damages or automatically establishes someone's liability. Whether compensation is owed or paid depends on the actual circumstances and conditions."), "word2-11")
            show(articleBullet("Dictionary: JMdict, entry 1514650. Scope: Nikkoku and World Encyclopedia, 補償."), "word2-12")
            section("How the kanji combine")
            inline(await(articleBullet("補 contributes supplying what is missing; 償 contributes recompense or making good a loss. The near-synonymous parts reinforce the idea of making up for a loss. 補 supplies ホ and 償 supplies ショウ in ほしょう.")), "償", 41)
            await("Article contents")
            section("Readings")
            show(readingExample("補償 ほしょう — compensation for loss"), "word2-new-kanji-backlink")
            back()
            await(articleBullet("補 contributes supplying what is missing; 償 contributes recompense or making good a loss. The near-synonymous parts reinforce the idea of making up for a loss. 補 supplies ホ and 償 supplies ショウ in ほしょう.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("system-back-word2-kanji")
            section("How the kanji combine")
            inline(await(articleBullet("補 contributes supplying what is missing; 償 contributes recompense or making good a loss. The near-synonymous parts reinforce the idea of making up for a loss. 補 supplies ホ and 償 supplies ショウ in ほしょう.")), "補", 0)
            await("補 — supplement; make good")
            show(articleBullet("Strokes: 12 · Key (radical): 衣 (no. 145) · JLPT: N2 (community list)"), "component1-01")
            section("Meaning and origin")
            show(articleBullet("補 concerns supplying what is missing, supplementing or making good a shortage. 候補 こうほ names a candidate, while 補う おぎなう directly expresses supplementing or compensating."), "component1-03")
            show(articleBullet("Modern-shape mnemonic, not etymology: Imagine a new patch, the right-hand 甫-shaped block, supplying a missing part of a garment 衤. This is a mnemonic rather than a claim about the component's historical role."), "component1-04")
            show(articleBullet("The indexing radical 衣 appears as left-hand 衤, not the similar-looking 礻."), "component1-05")
            section("Readings")
            show(readingExample("候補 こうほ - candidate; possible choice"), "component1-12")
            show(readingExample("補う おぎなう - supplement; make up for"), "component1-15")
            section("Common words")
            show(articleBullet("候補 こうほ - candidate; possible choice"), "component1-17")
            show(articleBullet("補う おぎなう - supplement; make up for"), "component1-18")
            show(articleBullet("補償 ほしょう - compensation for loss"), "component1-19")
            show(articleBullet("補充 ほじゅう - replenishment; refilling"), "component1-20")
            section("Notes")
            show(articleBullet("Compare 捕, capture: its left-hand 扌 differs from the clothing form 衤 in 補."), "component1-22")
            show(articleBullet("補う is a transitive godan verb, not an adjective meaning enough. Learn 候補 as a whole word rather than expecting the two character glosses to reproduce every modern use."), "component1-23")
            show(articleBullet("Metadata: KANJIDIC2, 2026-10-21 snapshot. Word pairs: JMdict, entries 1272730, 1514460, 1514580."), "component1-24")
            section("Common words")
            inline(await(articleBullet("補償 ほしょう - compensation for loss")), "補償", 0)
            await("Article contents")
            section("How the kanji combine")
            capture("word2-legacy-backlink")
            back()
            await(articleBullet("補償 ほしょう - compensation for loss")).assertIsDisplayed()
            section("Common words")
            capture("system-back-component1-word2")
            section("Common words")
            inline(await(articleBullet("補う おぎなう - supplement; make up for")), "補う", 0)
            await("補う (おぎなう) - make up for; supplement")
            section("Meaning")
            show(articleBullet("補う means supplying something missing, making up a shortage or loss, or supplementing something insufficient. It is a transitive godan verb. The shortage, lack, or material being supplemented takes を."), "comparison-02")
            show(articleBullet("足りない生活費をアルバイトで補っています。 (たりないせいかつひをアルバイトでおぎなっています。) - I make up the shortfall in living expenses with a part-time job."), "comparison-03")
            show(articleBullet("図を使って説明を補いました。 (ずをつかってせつめいをおぎないました。) - I supplemented the explanation with a diagram."), "comparison-04")
            show(articleBullet("Forms include 補います (おぎないます), 補わない (おぎなわない), 補った (おぎなった), and 補って (おぎなって)."), "comparison-05")
            section("How the kanji combine")
            show(articleBullet("補 contributes supplying what is missing. おぎな is represented by the kanji and う is okurigana. The compound reading ホ does not replace おぎな in this verb."), "comparison-07")
            section("Synonyms and antonyms")
            show(articleBullet("埋める (うめる) also covers filling a gap or making up a loss. 足す (たす) and 加える (くわえる) describe adding; 補う makes the insufficiency or missing part important. 補充 (ほじゅう) is replenishment; 補足 (ほそく) is supplementation."), "comparison-09")
            section("Distinctive meaning")
            show(articleBullet("The supplement need not be money or a physical patch. The diagram example adds information that the explanation lacks. English \"compensate\" here does not automatically mean paying legal damages: 補償する (ほしょうする) is the relevant comparison for compensation or reparation."), "comparison-11")
            show(articleBullet("Dictionary: JMdict, entry 1514460, sense 1; compare 1524500 sense 4, 1514580, 1514700 and 1514650."), "comparison-12")
            section("How the kanji combine")
            inline(await(articleBullet("補 contributes supplying what is missing. おぎな is represented by the kanji and う is okurigana. The compound reading ホ does not replace おぎな in this verb.")), "補", 0)
            await("Article contents")
            section("Readings")
            capture("comparison-component-backlink")
            back()
            await(articleBullet("補 contributes supplying what is missing. おぎな is represented by the kanji and う is okurigana. The compound reading ホ does not replace おぎな in this verb.")).assertIsDisplayed()
            section("Distinctive meaning")
            capture("system-back-comparison-component")
            section("Distinctive meaning")
            inline(await(articleBullet("The supplement need not be money or a physical patch. The diagram example adds information that the explanation lacks. English \"compensate\" here does not automatically mean paying legal damages: 補償する (ほしょうする) is the relevant comparison for compensation or reparation.")), "補償", 195)
            await("Article contents")
            section("Distinctive meaning")
            capture("comparison-compensation-target")
            back()
            await(articleBullet("The supplement need not be money or a physical patch. The diagram example adds information that the explanation lacks. English \"compensate\" here does not automatically mean paying legal damages: 補償する (ほしょうする) is the relevant comparison for compensation or reparation.")).assertIsDisplayed()
            section("Distinctive meaning")
            capture("system-back-comparison-compensation")
            back()
            await(articleBullet("補う おぎなう - supplement; make up for")).assertIsDisplayed()
            section("Common words")
            capture("system-back-component1-comparison")
            back()
            await(articleBullet("補 contributes supplying what is missing; 償 contributes recompense or making good a loss. The near-synonymous parts reinforce the idea of making up for a loss. 補 supplies ホ and 償 supplies ショウ in ほしょう.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("system-back-word2-component1")
            back()
            await(articleBullet("補償 ほしょう — compensation for loss")).assertIsDisplayed()
            section("Common words")
            capture("system-back-kanji-word2")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            assertEquals("償", (quiz.ui as QuizUi.Question).card.kanji)
            capture("meaning-question")
            click("recompense; make amends")
            await("Correct!")
            assertEquals("償", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKinds = mutableSetOf<ReadingKind>()
            repeat(2) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("償", question.card.kanji)
                assertTrue("Duplicate target reading kind", answeredKinds.add(question.question.kind))
                val key = if (question.question.kind == ReadingKind.On) "しょう" else "つぐなう"
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "償" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("recompense; make amends").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "償") })
            assertEquals(listOf("ショウ"), card.onyomi.splitSep())
            assertEquals(listOf("つぐな.う"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("ショウ"), card.quizOnyomi?.splitSep())
            assertEquals(listOf("つぐな.う"), card.quizKunyomi?.splitSep())
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(17, strokes.length())
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
            rule.onNode(hasContentDescription("17 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "償" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "償" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("bothCuratedKindsAndPersistedGrades", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-070-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-070-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-070-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
