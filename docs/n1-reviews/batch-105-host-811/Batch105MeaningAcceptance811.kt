package io.github.stopcran.kanji.core

import io.github.stopcran.kanji.core.content.ContentParser
import io.github.stopcran.kanji.core.quiz.QuizBuilder
import io.github.stopcran.kanji.core.quiz.QuizCard
import io.github.stopcran.kanji.core.quiz.QuizOption
import io.github.stopcran.kanji.core.reading.KanjiReadingQuiz
import io.github.stopcran.kanji.core.reading.ReadingCard
import io.github.stopcran.kanji.core.reading.ReadingKind
import io.github.stopcran.kanji.core.words.WordCard
import io.github.stopcran.kanji.core.words.WordDirection
import io.github.stopcran.kanji.core.words.WordQuizBuilder
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.put
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File
import kotlin.random.Random

class Batch105MeaningAcceptance811 {
    @Test
    fun actualContentMeaningGuardsReadingAndHypothesisPairs() {
        val root = File("../../learning-japanese").canonicalFile
        assertEquals(File("C:\\Users\\stop-\\n1-kanji-workspace\\learning-japanese").canonicalFile, root)
        val parsed = ContentParser.parse(PublishableContentFixture.load(root))
        assertTrue(parsed.problems.toString(), parsed.problems.isEmpty())
        assertEquals("5572c6c467e6b73b", parsed.manifest.contentVersion)
        assertEquals(1128, parsed.kanji.size)
        assertEquals(5079, parsed.words.size)
        val all = parsed.kanji.map { QuizCard(it.kanji, it.title, it.tags, it.distractors, it.quizExclusions) }
        val byId = all.associateBy { it.kanji }
        val n1Ids = parsed.kanji.filter { it.jlpt == 1 }.map { it.kanji }.toSet()
        assertEquals(137, n1Ids.size)
        val n1 = all.filter { it.kanji in n1Ids }
        val target = byId.getValue("勁")
        val guards = listOf("強", "剛", "力", "勢")
        val curated = listOf("功", "劾", "剖")
        assertEquals(guards, target.quizExclusions)
        assertEquals(curated, target.distractors)
        assertEquals(setOf("劾", "剖"), curated.filter { it in n1Ids }.toSet())
        fun assertPairwiseSafe(options: List<QuizOption>) {
            val cards = options.map { byId.getValue(it.kanji) }
            for (left in cards) for (right in cards.filter { it.kanji != left.kanji }) {
                assertFalse("${left.kanji}/${right.kanji} guarded pair leaked",
                    right.kanji in left.quizExclusions || left.kanji in right.quizExclusions)
            }
        }
        fun optionsJson(options: List<QuizOption>) = JsonArray(options.map { buildJsonObject {
            put("kanji", it.kanji)
            put("title", it.title)
        } })
        val pools = linkedMapOf(
            "N1" to n1, "All" to all,
            "boundedCustom" to all.filter { it.kanji in curated + target.kanji },
            "randomN1Subset811" to listOf(target) + n1.filter { it.kanji != target.kanji }
                .shuffled(Random(811)).take(15),
        )
        val choices = mutableListOf<JsonObject>()
        for ((poolName, pool) in pools) repeat(16) { seed ->
            val options = QuizBuilder.options(target, pool, Random(seed))
            assertEquals(4, options.size)
            assertEquals(4, options.map { it.title }.toSet().size)
            assertEquals(1, options.count { it.kanji == target.kanji })
            assertTrue(options.none { it.kanji in guards })
            assertTrue(options.all { o -> pool.any { it.kanji == o.kanji && it.title == o.title } })
            assertPairwiseSafe(options)
            if (poolName == "All" || poolName == "boundedCustom") {
                assertEquals((curated + target.kanji).toSet(), options.map { it.kanji }.toSet())
            }
            choices += buildJsonObject {
                put("pool", poolName); put("seed", seed); put("options", optionsJson(options))
            }
        }
        val direct = mutableListOf<JsonObject>()
        for (excludedId in guards) {
            val pair = all.filter { it.kanji in setOf(target.kanji, excludedId) }
            assertEquals(2, pair.size)
            for (quizTarget in pair) repeat(16) { seed ->
                val excluded = pair.single { it.kanji != quizTarget.kanji }
                val sampled = pair + all.filter { it.kanji !in pair.map { p -> p.kanji } }
                    .shuffled(Random(811 + seed)).take(seed)
                val checkedPools = pools + linkedMapOf(
                    "sampledFiltered" to sampled, "pairOnly" to pair,
                    "targetOutsidePool" to sampled.filter { it.kanji != quizTarget.kanji })
                for ((poolName, pool) in checkedPools) {
                    val options = QuizBuilder.options(quizTarget, pool, Random(seed))
                    assertEquals(1, options.count { it.kanji == quizTarget.kanji })
                    assertFalse(options.any { it.kanji == excluded.kanji })
                    assertTrue(options.size in 1..4)
                    assertEquals(options.size, options.map { it.title }.toSet().size)
                    assertTrue(options.all { it.kanji == quizTarget.kanji || pool.any { p -> p.kanji == it.kanji } })
                    assertPairwiseSafe(options)
                    if (poolName == "pairOnly") assertEquals(1, options.size)
                    direct += buildJsonObject {
                        put("target", quizTarget.kanji); put("excluded", excluded.kanji)
                        put("pool", poolName); put("seed", seed)
                        put("poolMembershipInOrder", JsonArray(pool.map { JsonPrimitive(it.kanji) }))
                        put("options", optionsJson(options))
                    }
                }
            }
        }
        val nontransitive = mutableListOf<JsonObject>()
        val preexistingDirect = mutableSetOf<String>()
        for (left in guards) for (right in guards.filter { it != left }) {
            val pair = all.filter { it.kanji in setOf(left, right) }
            val a = byId.getValue(left)
            val b = byId.getValue(right)
            if (right in a.quizExclusions || left in b.quizExclusions) {
                preexistingDirect += "$left/$right"
                continue
            }
            repeat(16) { seed ->
                val options = QuizBuilder.options(a, pair, Random(seed))
                assertEquals(setOf(left, right), options.map { it.kanji }.toSet())
                nontransitive += buildJsonObject {
                    put("target", left); put("neighbor", right); put("seed", seed)
                    put("options", optionsJson(options))
                }
            }
        }
        val readings = parsed.kanji.map {
            ReadingCard(it.kanji, it.onyomi, it.kunyomi,
                it.quizOnyomi ?: it.onyomi, it.quizKunyomi ?: it.kunyomi, it.distractors)
        }
        val reading = readings.single { it.kanji == "勁" }
        assertEquals(listOf("ケイ"), reading.on)
        assertEquals(listOf("つよ.い"), reading.kun)
        assertEquals(reading.on, reading.askOn)
        assertTrue(reading.askKun.isEmpty())
        assertEquals(listOf("けい"), reading.quizKeys(ReadingKind.On))
        assertTrue(reading.quizKeys(ReadingKind.Kun).isEmpty())
        assertNull(KanjiReadingQuiz.question(reading, ReadingKind.Kun, readings, Random(0)))
        val readingRows = mutableListOf<JsonObject>()
        repeat(16) { seed ->
            val question = KanjiReadingQuiz.question(reading, ReadingKind.On, readings, Random(seed), reading = "けい")
            assertNotNull(question)
            question!!
            assertEquals("けい", question.correctKey)
            assertEquals(1, question.options.count { it.key == "けい" })
            assertEquals("ケイ", question.options.single { it.key == "けい" }.label)
            assertTrue(question.options.filter { it.key != "けい" }
                .none { it.key in KanjiReadingQuiz.excludedKeys(reading) })
            readingRows += buildJsonObject {
                put("kind", "On"); put("key", "けい"); put("seed", seed)
                put("options", JsonArray(question.options.map { buildJsonObject {
                    put("key", it.key); put("label", it.label)
                } }))
            }
        }
        val words = parsed.words.map {
            WordCard(it.word, it.reading, it.title, it.type, it.kanji, it.tags, it.jlpt,
                it.quizExclusions, it.quizDistractors)
        }.associateBy { it.word }
        val wordTarget = words.getValue("雄勁")
        val wordGuards = listOf("強い", "強力", "力強い", "剛健", "力", "勢い")
        assertEquals(wordGuards, wordTarget.quizExclusions)
        assertNull(wordTarget.jlpt)
        assertFalse(byId.containsKey("雄"))
        assertEquals("ゆうけい", wordTarget.reading)
        val wordDirect = mutableListOf<JsonObject>()
        for (excluded in wordGuards) {
            val pair = listOf(wordTarget, words.getValue(excluded))
            for (quizTarget in pair) for (direction in listOf(WordDirection.JpToEn, WordDirection.EnToJp)) {
                repeat(16) { seed ->
                    val options = WordQuizBuilder.options(quizTarget, pair, direction, Random(seed))
                    assertEquals(listOf(quizTarget.word), options.map { it.word })
                    wordDirect += buildJsonObject {
                        put("excluded", excluded); put("target", quizTarget.word)
                        put("direction", direction.name); put("seed", seed)
                        put("label", options.single().label)
                    }
                }
            }
        }
        val wordPools = linkedMapOf(
            "All" to words.values.toList(),
            "boundedCustom" to listOf(wordTarget) + listOf("不正", "叱る", "弾").map { words.getValue(it) },
        )
        val wordChoices = mutableListOf<JsonObject>()
        for ((poolName, pool) in wordPools) for (direction in listOf(WordDirection.JpToEn, WordDirection.EnToJp)) {
            repeat(16) { seed ->
                val options = WordQuizBuilder.options(wordTarget, pool, direction, Random(seed))
                assertEquals(4, options.size)
                assertEquals(1, options.count { it.word == wordTarget.word })
                val cards = options.map { words.getValue(it.word) }
                for (a in cards) for (b in cards.filter { it.word != a.word }) {
                    assertFalse(b.word in a.quizExclusions || a.word in b.quizExclusions)
                }
                wordChoices += buildJsonObject {
                    put("pool", poolName); put("direction", direction.name); put("seed", seed)
                    put("options", JsonArray(options.map { buildJsonObject {
                        put("word", it.word); put("label", it.label)
                    } }))
                }
            }
        }
        val hypothesis = mutableListOf<JsonObject>()
        for (hypothesisId in listOf("活気", "もりもり")) {
            val wordPair = listOf(wordTarget, words.getValue(hypothesisId))
            for (quizTarget in wordPair) for (direction in listOf(WordDirection.JpToEn, WordDirection.EnToJp)) {
                repeat(16) { seed ->
                    val options = WordQuizBuilder.options(quizTarget, wordPair, direction, Random(seed))
                    assertEquals(setOf("雄勁", hypothesisId), options.map { it.word }.toSet())
                    hypothesis += buildJsonObject {
                        put("type", "word"); put("target", quizTarget.word); put("neighbor", hypothesisId)
                        put("direction", direction.name); put("seed", seed)
                        put("options", JsonArray(options.map { buildJsonObject {
                            put("word", it.word); put("label", it.label)
                        } }))
                    }
                }
            }
        }
        assertEquals(64, choices.size)
        assertEquals(896, direct.size)
        assertEquals((12 - preexistingDirect.size) * 16, nontransitive.size)
        assertTrue(nontransitive.isNotEmpty())
        assertEquals(16, readingRows.size)
        assertEquals(384, wordDirect.size)
        assertEquals(64, wordChoices.size)
        assertEquals(128, hypothesis.size)
        val destination = File("C:\\Users\\stop-\\n1-kanji-workspace\\control\\logs\\ece8be08-73ca-41e8-90d7-0696f855889b")
        for ((name, value) in linkedMapOf(
            "pools" to buildJsonObject { pools.forEach { (name, pool) ->
                put(name, JsonArray(pool.map { JsonPrimitive(it.kanji) }))
            } },
            "word-pools" to buildJsonObject { wordPools.forEach { (name, pool) ->
                put(name, JsonArray(pool.map { JsonPrimitive(it.word) }))
            } },
            "choices" to JsonArray(choices), "direct-guards" to JsonArray(direct),
            "nontransitive" to JsonArray(nontransitive),
            "preexisting-neighbor-edges" to JsonArray(preexistingDirect.sorted().map { JsonPrimitive(it) }),
            "readings" to JsonArray(readingRows), "word-guards" to JsonArray(wordDirect),
            "word-choices" to JsonArray(wordChoices), "hypothesis-pairs" to JsonArray(hypothesis))) {
            val file = File(destination, "meaning-811-$name.json")
            check(!file.exists()) { "Do not overwrite acceptance evidence: $file" }
            file.writeText(value.toString() + "\n")
        }
    }
}
