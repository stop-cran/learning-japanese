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

private fun disposable074() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch074GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun exemptionLookalikesAndIsolatedRadicalAcrossFourProductionFamilies() {
        disposable074()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val text = "任 使 儿 元 兄 先 免 助 午 去 取 口 可 品 商 年 幸 店 持 救 方 書 格 無 物 税 舌 見 言 訪 許 証 話 課 責 買 資 転 辞 逃 運 避 金 免れる 免許 免税"
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 074: exemption / look-alikes / isolated radical")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(text, fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect 免/兄/元/先, isolated 儿 and 許/税; all authored Han, 免れる/免許/免税. Fallback families may coincide.", fontSize = 18.sp)
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
            for (char in listOf("任", "使", "儿", "元", "兄", "先", "免", "助", "午", "去", "取", "口", "可", "品", "商", "年", "幸", "店", "持", "救", "方", "書", "格", "無", "物", "税", "舌", "見", "言", "訪", "許", "証", "話", "課", "責", "買", "資", "転", "辞", "逃", "運", "避", "金")) {
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
            for (word in listOf("免れる", "免許", "免税")) {
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
        assertEquals(184, rows.length())
        rule.waitForIdle()
        rule.onAllNodesWithText(text).assertCountEquals(4)
        for (index in fonts.indices) rule.onAllNodesWithText(text)[index].assertIsDisplayed()
        File(context.getExternalFilesDir(null), "n1-074-font-pairs.png").outputStream().use {
            assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        File(context.getExternalFilesDir(null), "n1-074-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 172).put("wholeWordRasterProbes", 12)
            .put("limits", "Native Paint probes cover all43 actual authored Han including isolated 儿; twelve whole-word rasters and four production Compose rows. Actual readability requires visual inspection; emulator not phone; fallback face not identified.")
            .toString(2))
    }
}

class N1Batch074ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineExemptionFiveReciprocalPairsBothReadingsDrawingAndSystemBack() {
        disposable074()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-074-${UUID.randomUUID()}", "main")
        val head = "4078c7d42e6bc2173c555e73d0bd39fb5d69eb08"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-074-4078c7d4-envelope.zip")
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
        assertEquals(1086, updated.kanji)
        assertEquals(5043, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("c507eceeb764bc3f", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(106, n1.size)
        val exemption = n1.single { it.kanji == "免" }
        assertEquals(listOf("メン"), exemption.onyomi.splitSep())
        assertEquals(listOf("まぬか.れる", "まぬが.れる"), exemption.kunyomi.splitSep())
        assertNotNull(exemption.quizOnyomi)
        assertNotNull(exemption.quizKunyomi)
        assertEquals(listOf("メン"), exemption.quizOnyomi?.splitSep())
        assertEquals(listOf("まぬが.れる"), exemption.quizKunyomi?.splitSep())
        assertEquals(listOf("めん"), exemption.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(listOf("まぬがれる"), exemption.toReadingCard().quizKeys(ReadingKind.Kun))
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
                        if (card.kanji == "免") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "免" && ((kind == ReadingKind.On && key == "めん") || (kind == ReadingKind.Kun && key == "まぬがれる"))) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "免", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(exemption.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(exemption.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(exemption.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(exemption.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(exemption.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(exemption.quizKunyomi).splitSep()))
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 免 meaning and curated on and kun due; valid alternate まぬか.れる retained but not offered. Two historical good 免 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 106 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("免")
            click("exempt; be spared")
            await("免 — exempt; be spared")
            show(articleBullet("Strokes: 8 · Key (radical): 儿 (no. 10) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("免 concerns exemption, release from an obligation, or being spared something unwelcome. 免税 めんぜい is tax exemption; 免れる まぬがれる means escaping harm or avoiding an unwelcome outcome. In 免許 めんきょ, learn the whole word as a license or official permission. The character also has a dismissal-from-office sense; one English gloss does not fit every compound."), "kanji-03")
            show(articleBullet("The indexing radical 儿 appears in the two leg-like lower strokes. Modern-shape mnemonic: picture those legs stepping clear of an obligation under the hooked upper shape and box-like middle. This is an invented spelling aid, not a historical derivation or a phonetic analysis."), "kanji-04")
            section("Readings")
            show(readingExample("メン"), "kanji-09")
            show(readingExample("免許 めんきょ — license; 免税 めんぜい — tax exemption"), "kanji-11")
            show(readingExample("まぬか.れる"), "kanji-12")
            show(readingExample("source-only for this quiz: 免れる まぬかれる — escape harm; a valid alternate pronunciation of the verb below"), "kanji-14")
            show(readingExample("まぬが.れる"), "kanji-15")
            show(readingExample("免れる まぬがれる — escape harm; avoid an unwelcome outcome"), "kanji-17")
            show(articleBullet("Both まぬかれる and まぬがれる are valid. Practice selects まぬがれる to avoid two variant questions for the same written verb; this does not label まぬかれる rare or incorrect. All sourced readings remain in their original metadata order. The dot marks where the written ending れる begins."), "kanji-18")
            section("Common words")
            show(articleBullet("免許 めんきょ — license; official permission"), "kanji-20")
            show(articleBullet("免税 めんぜい — tax exemption; duty exemption"), "kanji-21")
            show(articleBullet("免れる まぬがれる, also まぬかれる — escape harm; avoid an unwelcome outcome"), "kanji-22")
            section("Notes")
            show(articleBullet("兄, \"older brother,\" has 口 above its legs; 元, \"origin, former,\" has two horizontal lines. 先, \"previous; ahead,\" has a different upper shape."), "kanji-24")
            show(articleBullet("許, \"permit; forgive,\" overlaps in permission-related meanings. It is not a freely interchangeable spelling of 免."), "kanji-25")
            show(articleBullet("逃, \"escape; flee,\" overlaps in escape contexts. 免れる does not require physical flight: 責任を免れる (せきにんをまぬがれる) means \"evade responsibility.\""), "kanji-26")
            show(articleBullet("Metadata: KANJIDIC2, 2026-11-02 snapshot. Words: JMdict, entries 1533130, 1533230 and 1584670. Meaning and pronunciation: Daijisen and Nikkoku, 免れる; Daijisen and Nikkoku, 免."), "kanji-27")
            section("Common words")
            inline(await(articleBullet("免れる まぬがれる, also まぬかれる — escape harm; avoid an unwelcome outcome")), "免れる", 0)
            await("Article contents")
            await("免れる (まぬがれる) — escape harm; avoid an unwelcome outcome")
            section("Meaning")
            show(articleBullet("免れる means escaping something unwelcome, such as injury or disaster, or avoiding a burden such as punishment or responsibility. The unwelcome event or responsibility takes を: けがを免れる, \"escape injury,\" and 責任を免れる (せきにんをまぬがれる), \"evade responsibility.\""), "免れる-02")
            show(articleBullet("幸い、けがを免れました。 (さいわい、けがをまぬがれました。) — Fortunately, I escaped injury."), "免れる-03")
            show(articleBullet("責任を免れることはできません。 (せきにんをまぬがれることはできません。) — You cannot evade responsibility."), "免れる-04")
            show(articleBullet("This is an ichidan verb: replace the final る to form 免れます (まぬがれます), 免れた (まぬがれた), and 免れない (まぬがれない). The alternative pronunciation まぬかれる is also valid, with forms such as まぬかれます and まぬかれた. It is not a different written word."), "免れる-05")
            section("How the kanji combine")
            show(articleBullet("免 writes まぬが here, followed by れる as okurigana; with the alternate pronunciation it writes まぬか. There is no second kanji to combine. The ending れる is part of this verb, not a passive conjugation added to a verb called まぬが."), "免れる-07")
            section("Synonyms and antonyms")
            show(articleBullet("逃げる (にげる) can describe fleeing and also evading responsibility. 免れる need not involve running or moving away. 避ける (さける) overlaps in avoiding an unwelcome situation; the words are not unrestricted substitutes in every sentence."), "免れる-09")
            show(articleBullet("助かる (たすかる) overlaps when someone survives or is spared harm, but it also describes receiving practical help. 救う (すくう) presents saving someone or something else; 免れる does not itself identify a rescuer. Suffering the harm is a contextual contrast, not a single fixed antonym for every use."), "免れる-10")
            section("Distinctive meaning")
            show(articleBullet("The injury example reports being spared harm; it does not say whether that happened through deliberate action, another person's help, or luck. Avoiding responsibility can instead be blameworthy. Do not infer either physical escape or approval from the verb alone."), "免れる-12")
            show(articleBullet("Dictionaries differ in classification: JMdict calls this verb transitive, while Nikkoku calls it intransitive. Learn the attested unwelcome event を免れる construction directly rather than changing を to match an English gloss or treating one classification as universal."), "免れる-13")
            show(articleBullet("Dictionary: JMdict, entry 1584670, senses 1-2. Pronunciation, construction and classification: Daijisen and Nikkoku, 免れる."), "免れる-14")
            section("How the kanji combine")
            inline(await(articleBullet("免 writes まぬが here, followed by れる as okurigana; with the alternate pronunciation it writes まぬか. There is no second kanji to combine. The ending れる is part of this verb, not a passive conjugation added to a verb called まぬが.")), "免", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("まぬが.れる"), "免れる-kanji-backlink")
            back()
            await(articleBullet("免 writes まぬが here, followed by れる as okurigana; with the alternate pronunciation it writes まぬか. There is no second kanji to combine. The ending れる is part of this verb, not a passive conjugation added to a verb called まぬが.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("免れる-system-back-to-word")
            back()
            await(articleBullet("免れる まぬがれる, also まぬかれる — escape harm; avoid an unwelcome outcome")).assertIsDisplayed()
            section("Common words")
            capture("免れる-system-back-to-kanji")
            section("Common words")
            inline(await(articleBullet("免許 めんきょ — license; official permission")), "免許", 0)
            await("Article contents")
            await("免許 (めんきょ) - license; official permission")
            section("How the kanji combine")
            show(articleBullet("免 contributes release or exemption, and 許 contributes permitting. Together they concern granting authorization. This is a guide to the characters' meanings, not a claim about a particular modern licensing law. The readings are メン + キョ."), "免許-07")
            section("How the kanji combine")
            inline(await(articleBullet("免 contributes release or exemption, and 許 contributes permitting. Together they concern granting authorization. This is a guide to the characters' meanings, not a claim about a particular modern licensing law. The readings are メン + キョ.")), "免", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("まぬが.れる"), "免許-kanji-backlink")
            back()
            await(articleBullet("免 contributes release or exemption, and 許 contributes permitting. Together they concern granting authorization. This is a guide to the characters' meanings, not a claim about a particular modern licensing law. The readings are メン + キョ.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("免許-system-back-to-word")
            section("How the kanji combine")
            inline(await(articleBullet("免 contributes release or exemption, and 許 contributes permitting. Together they concern granting authorization. This is a guide to the characters' meanings, not a claim about a particular modern licensing law. The readings are メン + キョ.")), "許", 40)
            await("Article contents")
            await("許 — permit; forgive")
            section("Common words")
            show(articleBullet("免許 めんきょ — license; official permission"), "permit-example-18")
            section("Common words")
            inline(await(articleBullet("免許 めんきょ — license; official permission")), "免許", 0)
            await("Article contents")
            section("How the kanji combine")
            show(articleBullet("免 contributes release or exemption, and 許 contributes permitting. Together they concern granting authorization. This is a guide to the characters' meanings, not a claim about a particular modern licensing law. The readings are メン + キョ."), "免許-component-backlink")
            back()
            await(articleBullet("免許 めんきょ — license; official permission")).assertIsDisplayed()
            section("Common words")
            capture("免許-system-back-to-component")
            back()
            await(articleBullet("免 contributes release or exemption, and 許 contributes permitting. Together they concern granting authorization. This is a guide to the characters' meanings, not a claim about a particular modern licensing law. The readings are メン + キョ.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("免許-system-back-from-component")
            back()
            await(articleBullet("免許 めんきょ — license; official permission")).assertIsDisplayed()
            section("Common words")
            capture("免許-system-back-to-kanji")
            section("Common words")
            inline(await(articleBullet("免税 めんぜい — tax exemption; duty exemption")), "免税", 0)
            await("Article contents")
            await("免税 (めんぜい) - tax exemption; duty exemption")
            section("How the kanji combine")
            show(articleBullet("免 contributes exemption or release; 税 names tax. The on readings メン + ゼイ form めんぜい. Here English \"duty\" means a tax, not a person's responsibility or assigned task."), "免税-07")
            section("How the kanji combine")
            inline(await(articleBullet("免 contributes exemption or release; 税 names tax. The on readings メン + ゼイ form めんぜい. Here English \"duty\" means a tax, not a person's responsibility or assigned task.")), "免", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("まぬが.れる"), "免税-kanji-backlink")
            back()
            await(articleBullet("免 contributes exemption or release; 税 names tax. The on readings メン + ゼイ form めんぜい. Here English \"duty\" means a tax, not a person's responsibility or assigned task.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("免税-system-back-to-word")
            section("How the kanji combine")
            inline(await(articleBullet("免 contributes exemption or release; 税 names tax. The on readings メン + ゼイ form めんぜい. Here English \"duty\" means a tax, not a person's responsibility or assigned task.")), "税", 36)
            await("Article contents")
            section("Common words")
            inline(await(articleBullet("免税 めんぜい - tax exemption; duty exemption")), "免税", 0)
            await("Article contents")
            section("How the kanji combine")
            show(articleBullet("免 contributes exemption or release; 税 names tax. The on readings メン + ゼイ form めんぜい. Here English \"duty\" means a tax, not a person's responsibility or assigned task."), "免税-component-backlink")
            back()
            await(articleBullet("免税 めんぜい - tax exemption; duty exemption")).assertIsDisplayed()
            section("Common words")
            capture("免税-system-back-to-component")
            back()
            await(articleBullet("免 contributes exemption or release; 税 names tax. The on readings メン + ゼイ form めんぜい. Here English \"duty\" means a tax, not a person's responsibility or assigned task.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("免税-system-back-from-component")
            back()
            await(articleBullet("免税 めんぜい — tax exemption; duty exemption")).assertIsDisplayed()
            section("Common words")
            capture("免税-system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 5).put("directedLinkTransitions", 10)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            assertEquals("免", (quiz.ui as QuizUi.Question).card.kanji)
            capture("meaning-question")
            click("exempt; be spared")
            await("Correct!")
            assertEquals("免", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKinds = mutableSetOf<ReadingKind>()
            repeat(2) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("免", question.card.kanji)
                assertTrue("Duplicate target reading kind", answeredKinds.add(question.question.kind))
                val key = if (question.question.kind == ReadingKind.On) "めん" else "まぬがれる"
                assertNotEquals("まぬかれる", question.question.correctKey)
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "免" &&
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
                    it.kanji == "免" && it.mode == ReadingKind.Kun.mode.name && it.reading == "まぬかれる" }
            })
            capture("curated-both-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("exempt; be spared").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "免") })
            assertEquals(listOf("メン"), card.onyomi.splitSep())
            assertEquals(listOf("まぬか.れる", "まぬが.れる"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("メン"), card.quizOnyomi?.splitSep())
            assertEquals(listOf("まぬが.れる"), card.quizKunyomi?.splitSep())
            evidence.put("fullProjectionOnyomi", JSONArray(card.onyomi.splitSep()))
                .put("fullProjectionKunyomi", JSONArray(card.kunyomi.splitSep()))
                .put("fullProjectionQuizOnyomi", JSONArray(requireNotNull(card.quizOnyomi).splitSep()))
                .put("fullProjectionQuizKunyomi", JSONArray(requireNotNull(card.quizKunyomi).splitSep()))
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(8, strokes.length())
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
            rule.onNode(hasContentDescription("8 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "免" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "免" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("bothCuratedKindsPersistedGoodNoAlternateAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-074-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-074-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-074-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
