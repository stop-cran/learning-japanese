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

private fun disposable079() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch079GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun crownLookalikesAndCoverRoofFallbacksAcrossFourProductionFamilies() {
        disposable079()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("一 世 住 元 冖 冗 冠 前 名 国 土 城 外 子 宀 守 完 寸 工 帽 技 最 栓 様", "流 玉 王 瓶 生 界 蓋 術 金 題 高", "冠 冗 完 守 冖 宀 元 寸 王 王冠 冠たる 世界 帽子 蓋 栓")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 079: crown / look-alikes / cover and roof fallback")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 35 scoped Han; focused 冠/冗/完/守/元/寸, 冖 and 宀. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("一", "世", "住", "元", "冖", "冗", "冠", "前", "名", "国", "土", "城", "外", "子", "宀", "守", "完", "寸", "工", "帽", "技", "最", "栓", "様", "流", "玉", "王", "瓶", "生", "界", "蓋", "術", "金", "題", "高")) {
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
            for (word in listOf("冠", "王冠")) {
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
        assertEquals(148, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-079-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-079-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 140).put("wholeWordRasterProbes", 8).put("panels", 3)
            .put("limits", "35 actual scoped Han including exact 冖/宀 fallback inspection, four production families, three bounded Compose panels and eight whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch079ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineCrownThreeReciprocalPairsBothReadingsDrawingAndSystemBack() {
        disposable079()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-079-${UUID.randomUUID()}", "main")
        val head = "3fdc0bf952e299060b5a07ac372bb6d926595a4c"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-079-3fdc0bf9-envelope.zip")
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
        assertEquals(1091, updated.kanji)
        assertEquals(5047, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("a01eb85b17601ac0", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(111, n1.size)
        val crown = n1.single { it.kanji == "冠" }
        assertEquals(listOf("カン"), crown.onyomi.splitSep())
        assertEquals(listOf("かんむり"), crown.kunyomi.splitSep())
        assertNotNull(crown.quizOnyomi)
        assertNotNull(crown.quizKunyomi)
        assertEquals(listOf("カン"), crown.quizOnyomi?.splitSep())
        assertEquals(listOf("かんむり"), crown.quizKunyomi?.splitSep())
        assertEquals(listOf("かん"), crown.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(listOf("かんむり"), crown.toReadingCard().quizKeys(ReadingKind.Kun))
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
                        if (card.kanji == "冠") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "冠" && ((kind == ReadingKind.On && key == "かん") || (kind == ReadingKind.Kun && key == "かんむり"))) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "冠", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(crown.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(crown.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(crown.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(crown.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(crown.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(crown.quizKunyomi).splitSep()))
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 冠 meaning and both complete curated keys かん/かんむり due. Two historical good 冠 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 111 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("冠")
            click("crown; peerless")
            await("冠 — crown; peerless")
            show(articleBullet("Strokes: 9 · Key (radical): 冖 (the cover-like upper part, no. 14) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("冠 means a crown or ceremonial head covering, and can also express being foremost or peerless. 冠 (かんむり) names the headgear; 王冠 (おうかん) is a royal crown and also a crown-type bottle cap. Learn each complete word rather than translating every 冠 compound as a physical crown."), "kanji-03")
            show(articleBullet("Modern-shape mnemonic: imagine the cover-like 冖 as a crown over 元, with 寸 at the lower right to hold it in place. This is an invented memory aid, not a historical explanation or a verified phonetic analysis."), "kanji-04")
            section("Readings")
            show(articleBullet("Both complete source readings are selected for practice. The native noun かんむり and the compound reading カン have separate examples."), "kanji-06")
            show(readingExample("カン"), "kanji-10")
            show(readingExample("王冠 おうかん — royal crown; crown-type bottle cap"), "kanji-12")
            show(readingExample("かんむり"), "kanji-13")
            show(readingExample("冠 かんむり — crown; ceremonial cap"), "kanji-15")
            section("Common words")
            show(articleBullet("冠 かんむり — crown; ceremonial cap; also a top component of a kanji"), "kanji-17")
            show(articleBullet("王冠 おうかん — royal crown; crown-type bottle cap"), "kanji-18")
            section("Notes")
            show(articleBullet("The \"peerless\" meaning belongs to the reading かん, not the native noun かんむり. Recognize the formal expression 世界に冠たる (せかいにかんたる), \"foremost in the world,\" used before a noun."), "kanji-20")
            show(articleBullet("In kanji terminology, かんむり names a top component: 宀 is called うかんむり. 冠 itself has 冖, without the upper dot of 宀 in 完 and 守. 冗 shares the cover-like top but has a much simpler lower part; 完 contains 元 below its roof, while 守 contains 寸. These are shape comparisons, not claims of a shared origin."), "kanji-21")
            show(articleBullet("Metadata: KANJIDIC2. Dictionary: JMdict, entries 1577620 and 1181450. Reading and meaning branches: Digital Daijisen: 冠."), "kanji-22")
            section("Common words")
            show(articleBullet("冠 かんむり — crown; ceremonial cap; also a top component of a kanji"), "冠-forward-13")
            inline(await(articleBullet("冠 かんむり — crown; ceremonial cap; also a top component of a kanji")), "冠", 0)
            await("Article contents")
            await("冠 (かんむり) - crown; ceremonial cap")
            section("Meaning")
            show(articleBullet("冠, read かんむり here, names a crown or diadem, and also traditional ceremonial headgear worn by courtiers or Shinto clergy. It does not mean every everyday hat."), "冠-02")
            show(articleBullet("王様は金の冠をかぶっていました。 (おうさまはきんのかんむりをかぶっていました。) - The king was wearing a gold crown."), "冠-03")
            show(articleBullet("In kanji terminology, かんむり is a component at the top of a character. For example, 宀 is called うかんむり; this use is not a physical item of clothing."), "冠-04")
            section("How the kanji combine")
            show(articleBullet("This is one kanji with the native reading かんむり. Learn the whole pronunciation rather than dividing it into separate sound values. The same written character also has other readings with different uses."), "冠-06")
            section("Synonyms and antonyms")
            show(articleBullet("帽子 (ぼうし) is the broader everyday hat or cap word. 冠 can also refer to a name or title attached to a program or event, including named sponsorship; 名前 (なまえ) is not restricted to that use."), "冠-08")
            section("Distinctive meaning")
            show(articleBullet("The source list's English \"first; best\" belongs to the separate reading かん, not かんむり. Recognize 冠たる (かんたる), \"foremost; peerless,\" as in 世界に冠たる技術 (せかいにかんたるぎじゅつ), \"world-leading technology.\" This is supplementary reading-specific teaching, not a new meaning pronounced かんむり."), "冠-10")
            show(articleBullet("Dictionary: JMdict, entry 1577620, senses 1-3 and 6; supplementary sense 5 is restricted to かん. Usage: Digital Daijisen, 冠, separate かん and かんむり entries."), "冠-11")
            section("How the kanji combine")
            show(articleBullet("This is one kanji with the native reading かんむり. Learn the whole pronunciation rather than dividing it into separate sound values. The same written character also has other readings with different uses."), "冠-reverse-21")
            inline(await(articleBullet("This is one kanji with the native reading かんむり. Learn the whole pronunciation rather than dividing it into separate sound values. The same written character also has other readings with different uses.")), "kanji", 12)
            await("Article contents")
            section("Readings")
            show(readingExample("かんむり"), "冠-kanji-backlink")
            back()
            await(articleBullet("This is one kanji with the native reading かんむり. Learn the whole pronunciation rather than dividing it into separate sound values. The same written character also has other readings with different uses.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("冠-system-back-to-word")
            back()
            await(articleBullet("冠 かんむり — crown; ceremonial cap; also a top component of a kanji")).assertIsDisplayed()
            section("Common words")
            capture("冠-system-back-to-kanji")
            section("Common words")
            show(articleBullet("王冠 おうかん — royal crown; crown-type bottle cap"), "王冠-forward-22")
            inline(await(articleBullet("王冠 おうかん — royal crown; crown-type bottle cap")), "王冠", 0)
            await("Article contents")
            await("王冠 (おうかん) — royal crown; bottle cap")
            section("Meaning")
            show(articleBullet("王冠 is a royal crown, worn as a sign of royal status. It can also name a crown awarded as an honor. A separate everyday-object sense is a crown-shaped metal bottle cap, such as the closure on a beer bottle."), "王冠-02")
            show(articleBullet("王は王冠をかぶっています。 (おうはおうかんをかぶっています。) — The king is wearing a crown."), "王冠-03")
            show(articleBullet("瓶の王冠を外しました。 (びんのおうかんをはずしました。) — I removed the bottle's crown cap."), "王冠-04")
            show(articleBullet("The second sentence concerns a bottle closure, not royal headgear. Use the context to choose the English meaning."), "王冠-05")
            section("How the kanji combine")
            show(articleBullet("王 means \"king; ruler,\" and 冠 means \"crown.\" This is a modifier + head compound: a ruler's crown. The on readings are オウ + カン. The bottle-cap sense extends the name to an object shaped like a crown; it is not a miniature item of royal clothing."), "王冠-07")
            section("Synonyms and antonyms")
            show(articleBullet("冠 (かんむり) is the broader crown or ceremonial-headgear word. 帽子 (ぼうし) means a hat or cap, not specifically a royal crown. For containers, 蓋 (ふた) is a broader lid or cap word, while 栓 (せん) can mean a stopper or plug. These words overlap for some closures, but are not interchangeable for every object. There is no useful single opposite noun."), "王冠-09")
            section("Distinctive meaning")
            show(articleBullet("王冠 does not name every lid or screw cap: the bottle sense concerns the crown-type metal closure. For the royal object, use かぶる for putting it on and かぶっている for wearing it. Do not transfer the separate 冠たる (かんたる), \"peerless,\" use of 冠 to 王冠."), "王冠-11")
            show(articleBullet("Dictionary: JMdict, entry 1181450, senses 1-2. Usage and bottle-cap sense: Digital Daijisen: 王冠, おうかん general-word entry."), "王冠-12")
            section("How the kanji combine")
            show(articleBullet("王 means \"king; ruler,\" and 冠 means \"crown.\" This is a modifier + head compound: a ruler's crown. The on readings are オウ + カン. The bottle-cap sense extends the name to an object shaped like a crown; it is not a miniature item of royal clothing."), "王冠-reverse-31")
            inline(await(articleBullet("王 means \"king; ruler,\" and 冠 means \"crown.\" This is a modifier + head compound: a ruler's crown. The on readings are オウ + カン. The bottle-cap sense extends the name to an object shaped like a crown; it is not a miniature item of royal clothing.")), "冠", 27)
            await("Article contents")
            section("Readings")
            show(readingExample("カン"), "王冠-kanji-backlink")
            back()
            await(articleBullet("王 means \"king; ruler,\" and 冠 means \"crown.\" This is a modifier + head compound: a ruler's crown. The on readings are オウ + カン. The bottle-cap sense extends the name to an object shaped like a crown; it is not a miniature item of royal clothing.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("王冠-system-back-to-word")
            section("How the kanji combine")
            show(articleBullet("王 means \"king; ruler,\" and 冠 means \"crown.\" This is a modifier + head compound: a ruler's crown. The on readings are オウ + カン. The bottle-cap sense extends the name to an object shaped like a crown; it is not a miniature item of royal clothing."), "王冠-王-32")
            inline(await(articleBullet("王 means \"king; ruler,\" and 冠 means \"crown.\" This is a modifier + head compound: a ruler's crown. The on readings are オウ + カン. The bottle-cap sense extends the name to an object shaped like a crown; it is not a miniature item of royal clothing.")), "王", 0)
            await("Article contents")
            await("王 — king")
            section("Common words")
            show(articleBullet("王冠 おうかん — royal crown; also a crown-type bottle cap"), "王-counterpart-33")
            inline(await(articleBullet("王冠 おうかん — royal crown; also a crown-type bottle cap")), "王冠", 0)
            await("Article contents")
            section("How the kanji combine")
            show(articleBullet("王 means \"king; ruler,\" and 冠 means \"crown.\" This is a modifier + head compound: a ruler's crown. The on readings are オウ + カン. The bottle-cap sense extends the name to an object shaped like a crown; it is not a miniature item of royal clothing."), "王冠-王-component-backlink")
            back()
            await(articleBullet("王冠 おうかん — royal crown; also a crown-type bottle cap")).assertIsDisplayed()
            section("Common words")
            capture("王冠-王-system-back-to-component")
            back()
            await(articleBullet("王 means \"king; ruler,\" and 冠 means \"crown.\" This is a modifier + head compound: a ruler's crown. The on readings are オウ + カン. The bottle-cap sense extends the name to an object shaped like a crown; it is not a miniature item of royal clothing.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("王冠-王-system-back-from-component")
            back()
            await(articleBullet("王冠 おうかん — royal crown; crown-type bottle cap")).assertIsDisplayed()
            section("Common words")
            capture("王冠-system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 3).put("directedLinkTransitions", 6)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            assertEquals("冠", (quiz.ui as QuizUi.Question).card.kanji)
            capture("meaning-question")
            click("crown; peerless")
            await("Correct!")
            assertEquals("冠", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKinds = mutableSetOf<ReadingKind>()
            repeat(2) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("冠", question.card.kanji)
                assertTrue("Duplicate target reading kind", answeredKinds.add(question.question.kind))
                val key = if (question.question.kind == ReadingKind.On) "かん" else "かんむり"
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "冠" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(2, done.answered)
            assertEquals(2, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "冠" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(2, readingLogs.size)
            assertEquals(setOf("かん", "かんむり"), readingLogs.map { it.reading }.toSet())
            capture("curated-both-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("crown; peerless").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "冠") })
            assertEquals(listOf("カン"), card.onyomi.splitSep())
            assertEquals(listOf("かんむり"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("カン"), card.quizOnyomi?.splitSep())
            assertEquals(listOf("かんむり"), card.quizKunyomi?.splitSep())
            evidence.put("fullProjectionOnyomi", JSONArray(card.onyomi.splitSep()))
                .put("fullProjectionKunyomi", JSONArray(card.kunyomi.splitSep()))
                .put("fullProjectionQuizOnyomi", JSONArray(requireNotNull(card.quizOnyomi).splitSep()))
                .put("fullProjectionQuizKunyomi", JSONArray(requireNotNull(card.quizKunyomi).splitSep()))
            val strokes = JSONObject(requireNotNull(card.strokesJson)).getJSONArray("strokes")
            assertEquals(9, strokes.length())
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
            rule.onNode(hasContentDescription("9 strokes drawn", substring = true)).assertExists()
            click("Check")
            await("Practice only: this attempt is not graded.")
            assertFalse(runBlocking {
                app.db.reviews().allLog().any { it.sourceId == source.id &&
                    it.kanji == "冠" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "冠" && it.mode == StudyMode.Draw.name && it.grade == 1 }
            } }
            back()
            await("Meaning quiz")
            assertEquals("jlpt-n1", app.settings.stack.value)
            assertNull(connectivity.activeNetwork)
            assertEquals(1, archiveRequests)
            evidence.put("meaningQuestionAndFeedback", true)
                .put("bothCuratedKindsPersistedGoodAndDone", true)
                .put("touchInjectedReferenceStrokes", strokes.length())
                .put("drawingTraceThenRecall", true).put("drawingGradeRecordedOnNext", true)
                .put("offline", true).put("passed", true)
        } finally {
            File(app.getExternalFilesDir(null), "n1-079-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-079-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-079-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
