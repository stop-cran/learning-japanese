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
import io.github.stopcran.kanji.core.words.WordDirection
import io.github.stopcran.kanji.core.words.WordQuizBuilder
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

class N1Batch095CombinedImport698Test {
    @Test fun exactCombinedArchiveSingleImportCurationGuardsAndLinks() {
        assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
        assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        val app = instrumentation.targetContext.applicationContext as KanjiApp
        val source = RepoSource("acceptance-fixture", "n1-095-combined-698-${UUID.randomUUID()}", "main")
        val head = "6a7514c1ce11c25d58d43a8195540937a13378be"
        assertTrue(app.settings.setSource("https://github.com/${source.id}", source.branch))
        var archiveRequests = 0
        val http = ContentHttp { url, _, _, _ ->
            val input = when (url) {
                "https://api.github.com/repos/${source.id}/commits/main" -> ByteArrayInputStream(head.toByteArray())
                source.commitZipUrl(head) -> {
                    archiveRequests++
                    instrumentation.context.assets.open("n1-batch-095-combined-6a7514c1-envelope.zip")
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
        assertEquals(1118, updated.kanji)
        assertEquals(5071, updated.words)
        assertTrue(updated.problems.toString(), updated.problems.isEmpty())
        val meta = requireNotNull(runBlocking { app.db.content().meta(source.id) })
        assertEquals("3eebfff0fdad5e28", meta.contentVersion)
        assertEquals(0, meta.problems)
        assertNull(meta.grammarProblem)
        assertNull(meta.listeningProblem)
        assertNull(meta.grammarCurriculumProblem)
        assertEquals(1, ContentParser.KANJI_READING_PARSER_EPOCH)
        assertEquals(ContentParser.KANJI_READING_PARSER_EPOCH, meta.kanjiReadingParserEpoch)
        val n1 = runBlocking { app.db.content().kanjiLite(source.id).filter { it.jlpt == 1 } }
        assertEquals(127, n1.size)
        val dissection = n1.single { it.kanji == "剖" }
        assertEquals(listOf("部", "倍", "副"), dissection.distractors.splitSep())
        assertEquals(listOf("ボウ"), dissection.onyomi.splitSep())
        assertEquals(emptyList<String>(), dissection.kunyomi.splitSep())
        assertNotNull(dissection.quizOnyomi)
        assertNotNull(dissection.quizKunyomi)
        assertEquals(listOf("ボウ"), dissection.quizOnyomi?.splitSep())
        assertEquals(emptyList<String>(), dissection.quizKunyomi?.splitSep())
        assertEquals(listOf("ぼう"), dissection.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(emptyList<String>(), dissection.toReadingCard().quizKeys(ReadingKind.Kun))
        val expectedMeanings = mapOf(
            "剖" to "dissect; split open", "副" to "vice-; secondary",
            "部" to "section; department", "倍" to "multiple; double",
        )
        val all = runBlocking { app.db.content().kanjiLite(source.id) }
        assertEquals(n1.map { it.kanji }.toSet(),
            all.filter { "jlpt-n1" in it.tags.splitSep() }.map { it.kanji }.toSet())
        val curatedIds = listOf("部", "倍", "副")
        assertEquals(emptyList<String>(), curatedIds.filter { id -> n1.any { it.kanji == id } })
        val boundedCustom = all.filter { it.kanji in expectedMeanings }
        val randomSubset = listOf(dissection) +
            n1.filter { it.kanji != "剖" }.shuffled(kotlin.random.Random(693)).take(15)
        val checkedPools = JSONArray()
        for ((poolName, pool) in listOf("N1" to n1, "All" to all,
            "boundedCustom" to boundedCustom, "randomN1Subset" to randomSubset)) {
            val cards = pool.map { QuizCard(it.kanji, it.title, it.tags.splitSep(), it.distractors.splitSep()) }
            val target = cards.single { it.kanji == "剖" }
            assertEquals(curatedIds, target.distractors)
            val available = curatedIds.filter { id -> cards.any { it.kanji == id } }
            val expectedAvailable = if (poolName == "N1" || poolName == "randomN1Subset") 0 else 3
            assertEquals(expectedAvailable, available.size)
            repeat(16) { seed ->
                val options = QuizBuilder.options(target, cards, kotlin.random.Random(seed))
                assertEquals(4, options.size)
                assertEquals(4, options.map { it.title }.toSet().size)
                assertEquals(1, options.count { it.kanji == target.kanji })
                assertTrue(options.all { option -> cards.any { it.kanji == option.kanji && it.title == option.title } })
                assertTrue(available.all { id -> options.any { it.kanji == id } })
                if (expectedAvailable == 3) assertEquals(expectedMeanings, options.associate { it.kanji to it.title })
                checkedPools.put(JSONObject().put("pool", poolName).put("poolSize", pool.size).put("seed", seed)
                    .put("options", JSONArray().also { rows ->
                        options.forEach { rows.put(JSONObject().put("kanji", it.kanji).put("title", it.title)) }
                    }).put("availableCuratedCount", available.size)
                    .put("fallbackOptions", options.count { it.kanji != target.kanji && it.kanji !in available }))
            }
        }
        assertEquals(64, checkedPools.length())
        val words = runBlocking { app.db.content().wordsLite(source.id) }.map { it.toCard() }
        val importedDissection = words.single { it.word == "解剖" }
        assertEquals(listOf("分析", "分解", "検査"), importedDissection.quizExclusions)
        assertEquals("かいぼう", importedDissection.reading)
        assertNull(importedDissection.jlpt)
        val directGuardChecks = JSONArray()
        val guardPairs = listOf("解剖" to "分析", "解剖" to "分解", "解剖" to "検査")
        for ((leftId, rightId) in guardPairs) {
            val left = words.single { it.word == leftId }
            val right = words.single { it.word == rightId }
            assertTrue(right.word in left.quizExclusions)
            for ((target, excluded) in listOf(left to right, right to left)) {
                val custom = listOf(target, excluded) + words.filter {
                    it.word !in setOf(target.word, excluded.word) && it.title !in setOf(target.title, excluded.title) &&
                        it.word !in target.quizExclusions && target.word !in it.quizExclusions
                }.take(12)
                for ((poolName, pool) in listOf("All" to words, "boundedCustom" to custom)) {
                    for (direction in listOf(WordDirection.JpToEn, WordDirection.EnToJp)) {
                        repeat(16) { seed ->
                            val options = WordQuizBuilder.options(target, pool, direction, kotlin.random.Random(seed))
                            assertEquals(4, options.size)
                            assertEquals(1, options.count { it.word == target.word })
                            assertFalse("Direct exclusion leaked", options.any { it.word == excluded.word })
                            directGuardChecks.put(JSONObject().put("target", target.word).put("excluded", excluded.word)
                                .put("pool", poolName).put("direction", direction.name).put("seed", seed)
                                .put("options", JSONArray().also { rows ->
                                    options.forEach { rows.put(JSONObject().put("word", it.word).put("label", it.label)) }
                                }))
                        }
                    }
                }
            }
        }
        assertEquals(384, directGuardChecks.length())

        val full = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "剖") })
        assertEquals(listOf("ボウ"), full.onyomi.splitSep())
        assertEquals(emptyList<String>(), full.kunyomi.splitSep())
        assertNotNull(full.quizOnyomi)
        assertNotNull(full.quizKunyomi)
        assertEquals(listOf("ボウ"), full.quizOnyomi?.splitSep())
        assertEquals(emptyList<String>(), full.quizKunyomi?.splitSep())
        assertEquals(listOf("ぼう"), full.toReadingCard().quizKeys(ReadingKind.On))
        assertEquals(emptyList<String>(), full.toReadingCard().quizKeys(ReadingKind.Kun))
        val word = requireNotNull(runBlocking { app.db.content().word(source.id, "解剖") })
        val kai = requireNotNull(runBlocking { app.db.content().kanjiCard(source.id, "解") })
        assertTrue(full.body.contains("[解剖](../words/解剖.md)"))
        assertTrue(word.body.contains("[剖](../kanji/剖.md)"))
        assertTrue(word.body.contains("[解](../kanji/解.md)"))
        assertTrue(kai.body.contains("[解剖](../words/解剖.md)"))
        val connectivity = app.getSystemService(ConnectivityManager::class.java)
        assertNull("Disable disposable Wi-Fi/data before import", connectivity.activeNetwork)
        val evidence = JSONObject().put("contentSnapshot", head).put("contentVersion", meta.contentVersion)
            .put("archiveRequests", archiveRequests).put("importedKanji", updated.kanji).put("importedWords", updated.words)
            .put("problems", updated.problems.size).put("n1Cards", n1.size)
            .put("acceptedReadingParserEpoch", meta.kanjiReadingParserEpoch)
            .put("fullOnyomi", JSONArray(full.onyomi.splitSep()))
            .put("fullKunyomi", JSONArray(full.kunyomi.splitSep()))
            .put("fullQuizOnyomi", JSONArray(requireNotNull(full.quizOnyomi).splitSep()))
            .put("fullQuizKunyomi", JSONArray(requireNotNull(full.quizKunyomi).splitSep()))
            .put("liteOnyomi", JSONArray(dissection.onyomi.splitSep()))
            .put("liteKunyomi", JSONArray(dissection.kunyomi.splitSep()))
            .put("liteQuizOnyomi", JSONArray(requireNotNull(dissection.quizOnyomi).splitSep()))
            .put("liteQuizKunyomi", JSONArray(requireNotNull(dissection.quizKunyomi).splitSep()))
            .put("quizOnKeys", JSONArray(full.toReadingCard().quizKeys(ReadingKind.On)))
            .put("quizKunKeys", JSONArray(full.toReadingCard().quizKeys(ReadingKind.Kun)))
            .put("directGuardBuilderChecks", directGuardChecks).put("productionBuilderChoices", checkedPools)
            .put("reciprocalPairs", 2).put("linkDirections", 4)
            .put("transport", "Exact full combined git envelope through production ContentSync ONCE; synthetic source/HEAD")
            .put("fingerprint", Build.FINGERPRINT).put("sdk", Build.VERSION.SDK_INT)
            .put("phoneEvidence", false).put("newVisualOrRouteAcceptance", false).put("passed", true)
        File(requireNotNull(app.getExternalFilesDir(null)), "n1-095-combined-import-698.json")
            .writeText(evidence.toString(2))
    }
}
