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

private fun disposable085() {
    assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
    assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
}

class N1Batch085GlyphTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Test fun concentrationLookalikesAndRadicalFallbacksAcrossFourProductionFamilies() {
        disposable085()
        val context = InstrumentationRegistry.getInstrumentation().targetContext
        val fonts = listOf(KanjiFont.Gothic, KanjiFont.Mincho, KanjiFont.Textbook, KanjiFont.Brush)
        val pages = listOf("中 付 冗 冫 冷 准 凍 凝 凹 力 努 固 堅 夢 夫 工 度 心 息 意 懲 気 注 液", "濃 点 焦 熱 疑 的 目 硬 肩 血 衣 装 見 隹 集", "凝 疑 准 冗 凹 冫 隹 凍 固 硬 凝固 凝る 凝らす")
        val page = mutableStateOf(0)
        rule.setContent {
            MaterialTheme {
                Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Batch 085: concentration / look-alikes / radical fallback")
                    Text("Panel ${page.value + 1} / ${pages.size}")
                    fonts.forEach { font ->
                        Text(font.name)
                        Text(pages[page.value], fontFamily = font.family(), fontSize = 18.sp, lineHeight = 26.sp)
                    }
                    Text("Inspect all 39 scoped Han; focused 凝/疑/准/冗/凹, 冫/隹. Fallback families may coincide.", fontSize = 16.sp)
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
            for (char in listOf("中", "付", "冗", "冫", "冷", "准", "凍", "凝", "凹", "力", "努", "固", "堅", "夢", "夫", "工", "度", "心", "息", "意", "懲", "気", "注", "液", "濃", "点", "焦", "熱", "疑", "的", "目", "硬", "肩", "血", "衣", "装", "見", "隹", "集")) {
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
            for (word in listOf("凝固", "凝る", "凝らす")) {
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
        assertEquals(168, rows.length())
        for (index in pages.indices) {
            rule.runOnIdle { page.value = index }
            rule.waitForIdle()
            rule.onAllNodesWithText(pages[index]).assertCountEquals(4)
            for (fontIndex in fonts.indices) rule.onAllNodesWithText(pages[index])[fontIndex].assertIsDisplayed()
            File(context.getExternalFilesDir(null), "n1-085-font-panel-${index + 1}.png").outputStream().use {
                assertTrue(rule.onRoot().captureToImage().asAndroidBitmap().compress(Bitmap.CompressFormat.PNG, 100, it))
            }
        }
        File(context.getExternalFilesDir(null), "n1-085-font-raster.json").writeText(JSONObject()
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fontScale", context.resources.configuration.fontScale).put("rows", rows)
            .put("individualGlyphProbes", 156).put("wholeWordRasterProbes", 12).put("panels", 3)
            .put("limits", "39 actual scoped Han including exact 冫/隹 fallback inspection, four production families, three bounded Compose panels and twelve whole-word rasters. Hashes are not readability or fallback-face evidence. Actual PNG inspection required; emulator not phone.")
            .toString(2))
    }
}

class N1Batch085ArticleTest {
    @get:Rule val rule = createEmptyComposeRule()
    private lateinit var app: KanjiApp
    private lateinit var scenario: ActivityScenario<MainActivity>

    @Test fun fullSingleImportOfflineConcentrationFourReciprocalPairsCuratedOnAndKunDrawingAndSystemBack() {
        disposable085()
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-085-${UUID.randomUUID()}", "main")
        val head = "1d2e329035789b160e495a7518d64183f799233e"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-085-1d2e3290-envelope.zip")
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
        assertEquals(1108, updated.kanji)
        assertEquals(5063, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("0c514711ae8d3212", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(117, n1.size)
        val concentration = n1.single { it.kanji == "凝" }
        assertEquals(listOf("准", "冗", "凹"), concentration.distractors.splitSep())
        assertEquals(listOf("ギョウ"), concentration.onyomi.splitSep())
        assertEquals(listOf("こ.る", "こ.らす", "こご.らす", "こご.らせる", "こご.る"), concentration.kunyomi.splitSep())
        assertNotNull(concentration.quizOnyomi)
        assertNotNull(concentration.quizKunyomi)
        assertEquals(listOf("ギョウ"), concentration.quizOnyomi?.splitSep())
        assertEquals(listOf("こ.る", "こ.らす"), concentration.quizKunyomi?.splitSep())
        assertEquals(listOf("ぎょう"), concentration.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(listOf("こる"), concentration.toReadingCard().quizKeys(ReadingKind.Kun))
        val expectedMeanings = mapOf(
            "凝" to "congeal; become absorbed", "准" to "quasi-; associate rank",
            "冗" to "superfluous; redundant", "凹" to "concave; sunken",
        )
        val all = runBlocking { app.db.content().kanjiLite(source.id) }
        val checkedPools = JSONObject()
        for ((poolName, pool) in listOf("N1" to n1, "All" to all)) {
            val cards = pool.map { QuizCard(it.kanji, it.title, it.tags.splitSep(), it.distractors.splitSep()) }
            val target = cards.single { it.kanji == "凝" }
            assertEquals(listOf("准", "冗", "凹"), target.distractors)
            assertEquals(expectedMeanings, cards.filter { it.kanji in expectedMeanings }.associate { it.kanji to it.title })
            val options = QuizBuilder.options(target, cards, kotlin.random.Random(595))
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
                        if (card.kanji == "凝") now - 60_000 else now + 30L * 86_400_000,
                        now - 2L * 86_400_000, 3, 0,
                    ))
                    for (kind in ReadingKind.entries) for (key in card.toReadingCard().quizKeys(kind)) {
                        app.db.reviews().putState(ReviewStateEntity(
                            source.id, "jlpt-n1", card.kanji, kind.mode.name, "Review", 30.0, 5.0,
                            if (card.kanji == "凝" && key == (if (kind == ReadingKind.On) "ぎょう" else "こる")) now - 60_000
                            else now + 30L * 86_400_000,
                            now - 2L * 86_400_000, 3, 0, reading = key,
                        ))
                    }
                }
                for (days in 1..2) app.db.reviews().putLog(ReviewLogEntity(
                    0, source.id, "jlpt-n1", "凝", StudyMode.Quiz.name, 3, now - days * 86_400_000L,
                ))
            }
        }
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable emulator Wi-Fi/data before offline acceptance", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(concentration.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(concentration.kunyomi.splitSep()))
            .put("quizOnKeys", JSONArray(concentration.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(concentration.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(concentration.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(concentration.quizKunyomi).splitSep()))
            .put("productionBuilderN1AndAllExactChoices", checkedPools)
            .put("transport", "Exact full git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("fixture", "Other N1 meanings/readings postponed; 凝 meaning and curated onぎょう/kunこる due. Selectedこ.らす shares normalizedこる, not independent queued mastery. Two historical good 凝 meaning logs unlock drawing. No drawing state seeded. Unique disposable source; not owner progress.")
            .put("phoneEvidence", false).put("passed", false)
        scenario = ActivityScenario.launch(MainActivity::class.java)
        try {
            click("Kanji")
            click("N1")
            rule.waitUntil(30_000) { app.settings.stack.value == "jlpt-n1" }
            await("N1 · 117 cards").performScrollTo().assertIsDisplayed()
            capture("selection")
            click("Browse all kanji")
            rule.onNode(hasSetTextAction()).performTextReplacement("凝")
            click("congeal; become absorbed")
            await("凝 — congeal; become absorbed")
            show(articleBullet("Strokes: 16 · Key (radical): 冫 (the two-stroke ice radical at left, no. 15) · JLPT: N1 (community list)"), "kanji-01")
            section("Meaning and origin")
            show(articleBullet("凝 connects congealing or stiffness with concentrated attention. 凝固 ぎょうこ names coagulation or solidification; 凝る こる can describe stiff muscles or becoming absorbed in a hobby. The word and construction determine which meaning applies."), "kanji-03")
            show(articleBullet("Modern-shape mnemonic, not etymology: imagine the two marks of 冫 beside 疑 as someone pausing so intently that they seem frozen in place. This is an invented memory scene, not a historical or phonetic explanation."), "kanji-04")
            section("Readings")
            show(readingExample("ギョウ"), "kanji-09")
            show(readingExample("凝固 ぎょうこ — coagulation; solidification"), "kanji-11")
            show(readingExample("こ.る"), "kanji-12")
            show(readingExample("凝る こる — become stiff; get absorbed in; be elaborate"), "kanji-14")
            show(readingExample("こ.らす"), "kanji-15")
            show(readingExample("凝らす こらす — concentrate; apply effort"), "kanji-17")
            show(readingExample("こご.らす"), "kanji-18")
            show(readingExample("凝らす こごらす — cause to congeal; freeze; a separately recorded reading, not the linked article's primary こらす"), "kanji-20")
            show(readingExample("こご.らせる"), "kanji-21")
            show(readingExample("凝らせる こごらせる — cause to congeal; freeze; written ending らせる"), "kanji-23")
            show(readingExample("こご.る"), "kanji-24")
            show(readingExample("凝る こごる — congeal; jell; usually written in kana as こごる"), "kanji-26")
            show(articleBullet("The three こご readings are dictionary-verified recognition material, not additional readings of every example above. In particular, shoulder stiffness and enthusiasm in the linked 凝る article use こる, not こごる. The written ending of 凝らす is らす in both こらす and こごらす."), "kanji-27")
            section("Common words")
            show(articleBullet("凝固 ぎょうこ — coagulation; solidification"), "kanji-29")
            show(articleBullet("凝る こる — become stiff; get absorbed in"), "kanji-30")
            show(articleBullet("凝らす こらす — concentrate; apply effort"), "kanji-31")
            show(articleBullet("肩が凝る（かたがこる）— have stiff shoulders"), "kanji-32")
            show(articleBullet("工夫を凝らす（くふうをこらす）— exercise one's ingenuity"), "kanji-33")
            section("Notes")
            show(articleBullet("Contrast activity + に凝る with 工夫 + を凝らす. The first describes becoming absorbed; the second describes applying ingenuity. They are not interchangeable verb endings."), "kanji-35")
            show(articleBullet("凝った（こった）, as in 凝った衣装（こったいしょう）, \"an elaborate outfit,\" is an inflected form of こる, not a new character reading."), "kanji-36")
            show(articleBullet("凍 concerns freezing, 固 firmness or hardening, and 硬 hardness or stiffness. These meanings overlap with parts of 凝's range; do not treat them as unrelated simply because the shapes differ."), "kanji-37")
            show(articleBullet("For shape comparison, 准 has 隹 beside 冫; 凝 has the more complex 疑-shaped right side. 冗 has a cover-like top, and 凹 has an inward dip. None means congealing or absorption."), "kanji-38")
            show(articleBullet("Metadata: KANJIDIC2, database 2026-306, 2026-11-02 (EDRDG; CC BY-SA 4.0). Words: JMdict, entries 1238990, 1239000, 1239010, 1239020, 1239060, 1239070, 1239120, 1309500 and 1636550. Usage: Digital Daijisen: 凝る, 凝らす and 凝固."), "kanji-39")
            section("Common words")
            show(articleBullet("凝固 ぎょうこ — coagulation; solidification"), "solidify-forward")
            inline(await(articleBullet("凝固 ぎょうこ — coagulation; solidification")), "凝固", 0)
            await("Article contents")
            await("凝固 (ぎょうこ) — coagulation; solidification")
            section("Meaning")
            show(articleBullet("凝固 names coagulation or solidification. With する, it describes a material congealing or becoming solid; the material takes が."), "solidify-02")
            show(articleBullet("血液が凝固する。（けつえきがぎょうこする。）— Blood coagulates."), "solidify-03")
            show(articleBullet("It also names a change to the solid state, including water becoming ice. The English translation depends on the material: blood coagulates; a liquid can solidify. Not every 凝固 is water freezing."), "solidify-04")
            section("How the kanji combine")
            show(articleBullet("凝 contributes congealing and 固 firmness or hardening. Their related meanings reinforce the solidifying idea. Read ギョウ + コ; learn the established scientific uses as whole-word meanings."), "solidify-06")
            section("Synonyms and antonyms")
            show(articleBullet("固まる（かたまる）, \"harden; solidify,\" overlaps in a material becoming firm. 凍る（こおる）, \"freeze,\" is useful for water or a surface freezing over. 冷凍（れいとう）concerns freezing or frozen storage, rather than every kind of coagulation."), "solidify-08")
            section("Distinctive meaning")
            show(articleBullet("凝固 is useful in descriptions of materials and blood. It is not the term for mental concentration: compare 集中（しゅうちゅう）. The physical process is not necessarily a change to ice, and this vocabulary explanation does not provide medical advice."), "solidify-10")
            show(articleBullet("Dictionary: JMdict, entry 1239120. Usage and the blood example: Digital Daijisen: 凝固."), "solidify-11")
            section("How the kanji combine")
            show(articleBullet("凝 contributes congealing and 固 firmness or hardening. Their related meanings reinforce the solidifying idea. Read ギョウ + コ; learn the established scientific uses as whole-word meanings."), "solid-kanji")
            inline(await(articleBullet("凝 contributes congealing and 固 firmness or hardening. Their related meanings reinforce the solidifying idea. Read ギョウ + コ; learn the established scientific uses as whole-word meanings.")), "固", 29)
            await("Article contents")
            await("固 — firm; harden")
            section("Common words")
            show(articleBullet("凝固 ぎょうこ — coagulation; solidification"), "solid-changed-bullet")
            inline(await(articleBullet("凝固 ぎょうこ — coagulation; solidification")), "凝固", 0)
            await("Article contents")
            await("凝固 (ぎょうこ) — coagulation; solidification")
            back()
            await(articleBullet("凝固 ぎょうこ — coagulation; solidification")).assertIsDisplayed()
            section("Common words")
            capture("solid-back-to-reused-kanji")
            back()
            await(articleBullet("凝 contributes congealing and 固 firmness or hardening. Their related meanings reinforce the solidifying idea. Read ギョウ + コ; learn the established scientific uses as whole-word meanings.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("solid-back-to-word")
            section("How the kanji combine")
            show(articleBullet("凝 contributes congealing and 固 firmness or hardening. Their related meanings reinforce the solidifying idea. Read ギョウ + コ; learn the established scientific uses as whole-word meanings."), "solidify-reverse")
            inline(await(articleBullet("凝 contributes congealing and 固 firmness or hardening. Their related meanings reinforce the solidifying idea. Read ギョウ + コ; learn the established scientific uses as whole-word meanings.")), "凝", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("ギョウ"), "solidify-kanji-backlink")
            back()
            await(articleBullet("凝 contributes congealing and 固 firmness or hardening. Their related meanings reinforce the solidifying idea. Read ギョウ + コ; learn the established scientific uses as whole-word meanings.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("solidify-system-back-to-word")
            back()
            await(articleBullet("凝固 ぎょうこ — coagulation; solidification")).assertIsDisplayed()
            section("Common words")
            capture("solidify-system-back-to-kanji")
            section("Common words")
            show(articleBullet("凝る こる — become stiff; get absorbed in"), "absorbed-forward")
            inline(await(articleBullet("凝る こる — become stiff; get absorbed in")), "凝る", 0)
            await("Article contents")
            await("凝る (こる) — become stiff; get absorbed")
            section("Meaning")
            show(articleBullet("凝る has three useful branches: muscles becoming stiff, becoming absorbed in an activity, and putting elaborate care into details."), "absorbed-02")
            show(articleBullet("肩が凝る。（かたがこる。）— My shoulders get stiff."), "absorbed-03")
            show(articleBullet("ゴルフに凝っています。（ゴルフにこっています。）— I'm really into golf."), "absorbed-04")
            show(articleBullet("凝った衣装（こったいしょう）— an elaborate outfit"), "absorbed-05")
            show(articleBullet("In the first pattern, the stiff body part takes が. In the hobby pattern, the activity takes に. This is an intransitive godan verb despite ending in る: 凝ります（こります）, 凝って（こって）, 凝らない（こらない）. 凝った is its た-form; before a noun it can mean \"elaborate.\" Do not add な as if 凝った were a na-adjective."), "absorbed-06")
            section("How the kanji combine")
            show(articleBullet("凝 writes こ in this native verb; る is the written ending. Its stiffness and absorption associations help connect the uses, but one English gloss does not predict every construction."), "absorbed-08")
            section("Synonyms and antonyms")
            show(articleBullet("熱中（ねっちゅう）and 夢中（むちゅう）overlap in absorption. 集中（しゅうちゅう）focuses on concentration and need not imply enthusiasm for a hobby."), "absorbed-10")
            show(articleBullet("凝らす（こらす）is transitive in expressions such as 工夫を凝らす（くふうをこらす）, \"exercise one's ingenuity.\" Do not simply replace the に in ゴルフに凝る with を."), "absorbed-11")
            section("Distinctive meaning")
            show(articleBullet("凝る is not the general adjective \"hard\": 硬い（かたい）describes hardness or stiffness. Nor must getting absorbed in a hobby be a problem. The elaborate-detail use can praise care and craftsmanship."), "absorbed-13")
            show(articleBullet("This article's primary reading is こる. Dictionaries separately record 凝る こごる, \"congeal; jell,\" usually written in kana, and しこる, \"stiffen; harden.\" Do not read the shoulder and golf examples as こごる or しこる. Daijisen also records gathering or cold-induced solidification under こる; the three practical branches above are not an exhaustive definition."), "absorbed-14")
            show(articleBullet("Dictionary: JMdict, entries 1239070, 1238990, 1239060, 1594250 and 1636550. Usage and example constructions: Digital Daijisen: 凝る."), "absorbed-15")
            section("How the kanji combine")
            show(articleBullet("凝 writes こ in this native verb; る is the written ending. Its stiffness and absorption associations help connect the uses, but one English gloss does not predict every construction."), "absorbed-reverse")
            inline(await(articleBullet("凝 writes こ in this native verb; る is the written ending. Its stiffness and absorption associations help connect the uses, but one English gloss does not predict every construction.")), "凝", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("ギョウ"), "absorbed-kanji-backlink")
            back()
            await(articleBullet("凝 writes こ in this native verb; る is the written ending. Its stiffness and absorption associations help connect the uses, but one English gloss does not predict every construction.")).assertIsDisplayed()
            section("How the kanji combine")
            capture("absorbed-system-back-to-word")
            back()
            await(articleBullet("凝る こる — become stiff; get absorbed in")).assertIsDisplayed()
            section("Common words")
            capture("absorbed-system-back-to-kanji")
            section("Common words")
            show(articleBullet("凝らす こらす — concentrate; apply effort"), "effort-forward")
            inline(await(articleBullet("凝らす こらす — concentrate; apply effort")), "凝らす", 0)
            await("Article contents")
            await("凝らす (こらす) — concentrate; apply effort")
            section("Meaning")
            show(articleBullet("凝らす directs concentrated attention or effort. Learn it with established objects marked by を, rather than using it for every English \"focus.\""), "effort-02")
            show(articleBullet("目を凝らして見ました。（めをこらしてみました。）— I looked closely, straining my eyes."), "effort-03")
            show(articleBullet("工夫を凝らしました。（くふうをこらしました。）— I exercised my ingenuity."), "effort-04")
            show(articleBullet("目を凝らす（めをこらす）concerns looking intently. 工夫を凝らす （くふうをこらす）concerns inventive effort, not staring at an idea. The verb is transitive and godan: 凝らします（こらします）, 凝らして（こらして）, 凝らさない（こらさない）."), "effort-05")
            section("How the kanji combine")
            show(articleBullet("凝 writes こ here, with らす as the written ending. This is one native verb, not a compound of separate words for \"concentration\" and \"doing.\""), "effort-07")
            section("Synonyms and antonyms")
            show(articleBullet("集中（しゅうちゅう）overlaps in focusing attention. 注ぐ（そそぐ）can describe devoting energy or attention. Their objects and particles must still fit the particular expression."), "effort-09")
            show(articleBullet("凝る（こる）instead describes stiffness, absorption, or elaborate care: compare ゴルフに凝る, \"be really into golf,\" with 工夫を凝らす, \"exercise one's ingenuity.\" The latter takes 工夫 as its object."), "effort-10")
            section("Distinctive meaning")
            show(articleBullet("The object affects the translation. 息を凝らす（いきをこらす）means \"hold one's breath,\" not \"stare at one's breath.\""), "effort-12")
            show(articleBullet("The same spelling has a separately recorded reading こごらす, including \"cause to congeal; freeze.\" This article teaches こらす. 凝らせる can be the potential form こらせる of this godan verb; the dictionary verb 凝らせる こごらせる, \"cause to congeal,\" is a different reading. The homophone 懲らす（こらす）means \"punish; chastise,\" not concentrate."), "effort-13")
            show(articleBullet("Dictionary: JMdict, entries 1239010, 1239000, 1239020, 1309500, 2572530, 2835904 and 1428180. Usage: Digital Daijisen: 凝らす."), "effort-14")
            section("How the kanji combine")
            show(articleBullet("凝 writes こ here, with らす as the written ending. This is one native verb, not a compound of separate words for \"concentration\" and \"doing.\""), "effort-reverse")
            inline(await(articleBullet("凝 writes こ here, with らす as the written ending. This is one native verb, not a compound of separate words for \"concentration\" and \"doing.\"")), "凝", 0)
            await("Article contents")
            section("Readings")
            show(readingExample("ギョウ"), "effort-kanji-backlink")
            back()
            await(articleBullet("凝 writes こ here, with らす as the written ending. This is one native verb, not a compound of separate words for \"concentration\" and \"doing.\"")).assertIsDisplayed()
            section("How the kanji combine")
            capture("effort-system-back-to-word")
            back()
            await(articleBullet("凝らす こらす — concentrate; apply effort")).assertIsDisplayed()
            section("Common words")
            capture("effort-system-back-to-kanji")
            back()
            await("Search kanji, meaning or reading")
            back()
            await("Meaning quiz")
            evidence.put("reciprocalLinkAndSystemBack", true)
                .put("mappedReciprocalPairs", 4).put("directedLinkTransitions", 8)
                .put("completeArticleProjections", 4).put("changedReusedBullets", 1)
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Meaning quiz"))))
            rule.waitUntil(30_000) { (model("quiz:") as? QuizViewModel)?.ui is QuizUi.Question }
            val quiz = model("quiz:") as QuizViewModel
            val meaning = quiz.ui as QuizUi.Question
            assertEquals("凝", meaning.card.kanji)
            val expectedMeanings = mapOf(
                "凝" to "congeal; become absorbed",
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
            click("congeal; become absorbed")
            await("Correct!")
            assertEquals("凝", (quiz.ui as QuizUi.Answer).card.kanji)
            capture("meaning-feedback")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Readings (on'yomi and kun'yomi)"))))
            val answeredKinds = mutableSetOf<ReadingKind>()
            repeat(2) {
                rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Question }
                val reading = model("kreading:") as KanjiReadingViewModel
                val question = reading.ui as ReadingUi.Question
                assertEquals("凝", question.card.kanji)
                assertTrue("Duplicate target reading kind", answeredKinds.add(question.question.kind))
                val key = if (question.question.kind == ReadingKind.On) "ぎょう" else "こる"
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
                    app.db.reviews().allLog().any { log -> log.sourceId == source.id && log.kanji == "凝" &&
                        log.mode == question.question.kind.mode.name && log.reading == key && log.grade == 3 }
                } }
            }
            assertEquals(setOf(ReadingKind.On, ReadingKind.Kun), answeredKinds)
            rule.waitUntil(30_000) { (model("kreading:") as? KanjiReadingViewModel)?.ui is ReadingUi.Done }
            val done = (model("kreading:") as KanjiReadingViewModel).ui as ReadingUi.Done
            assertEquals(2, done.answered)
            assertEquals(2, done.correct)
            val readingLogs = runBlocking {
                app.db.reviews().allLog().filter { it.sourceId == source.id && it.kanji == "凝" &&
                    it.mode in setOf(ReadingKind.On.mode.name, ReadingKind.Kun.mode.name) }
            }
            assertEquals(2, readingLogs.size)
            assertEquals(setOf("ぎょう", "こる"), readingLogs.map { it.reading }.toSet())
            capture("curated-on-kun-done")
            back()
            await("Meaning quiz")
            click(rule.onNode(hasText("Start") and hasAnyAncestor(hasText("Drawing"))))
            await("Trace the kanji for")
            await("congeal; become absorbed").assertIsDisplayed()
            val card = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "凝") })
            assertEquals(listOf("准", "冗", "凹"), card.distractors.splitSep())
            assertEquals(listOf("ギョウ"), card.onyomi.splitSep())
            assertEquals(listOf("こ.る", "こ.らす", "こご.らす", "こご.らせる", "こご.る"), card.kunyomi.splitSep())
            assertNotNull(card.quizOnyomi)
            assertNotNull(card.quizKunyomi)
            assertEquals(listOf("ギョウ"), card.quizOnyomi?.splitSep())
            assertEquals(listOf("こ.る", "こ.らす"), card.quizKunyomi?.splitSep())
            evidence.put("fullProjectionOnyomi", JSONArray(card.onyomi.splitSep()))
                .put("fullProjectionKunyomi", JSONArray(card.kunyomi.splitSep()))
                .put("fullProjectionQuizOnyomi", JSONArray(requireNotNull(card.quizOnyomi).splitSep()))
                .put("fullProjectionQuizKunyomi", JSONArray(requireNotNull(card.quizKunyomi).splitSep()))
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
                    it.kanji == "凝" && it.mode == StudyMode.Draw.name }
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
                app.db.reviews().allLog().any { it.sourceId == source.id && it.kanji == "凝" && it.mode == StudyMode.Draw.name && it.grade == 1 }
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
            File(app.getExternalFilesDir(null), "n1-085-article-route.json").writeText(evidence.toString(2))
            File(app.getExternalFilesDir(null), "n1-085-article-tree.txt").writeText(rule.onRoot().printToString())
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
        File(app.getExternalFilesDir(null), "n1-085-$step.png").outputStream().use {
            assertTrue(bitmap.compress(Bitmap.CompressFormat.PNG, 100, it))
        }
        bitmap.recycle()
    }
}
