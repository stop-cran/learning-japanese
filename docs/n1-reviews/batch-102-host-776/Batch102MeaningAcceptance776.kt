package io.github.stopcran.kanji.core

import io.github.stopcran.kanji.core.content.ContentParser
import io.github.stopcran.kanji.core.quiz.QuizBuilder
import io.github.stopcran.kanji.core.quiz.QuizCard
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.put
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File
import kotlin.random.Random

class Batch102MeaningAcceptance776 {
    @Test
    fun actualPublishedFixtureChoicesDirectSymmetricAndNontransitiveGuards() {
        val root = File("../../learning-japanese").canonicalFile
        assertEquals(File("C:\\Users\\stop-\\n1-kanji-workspace\\learning-japanese").canonicalFile, root)
        val parsed = ContentParser.parse(PublishableContentFixture.load(root))
        assertTrue(parsed.problems.toString(), parsed.problems.isEmpty())
        assertEquals("f376333b242ebb23", parsed.manifest.contentVersion)
        assertEquals(1125, parsed.kanji.size)
        assertEquals(5074, parsed.words.size)
        val all = parsed.kanji.map { QuizCard(it.kanji, it.title, it.tags, it.distractors, it.quizExclusions) }
        val n1Ids = parsed.kanji.filter { it.jlpt == 1 }.map { it.kanji }.toSet()
        assertEquals(134, n1Ids.size)
        val n1 = all.filter { it.kanji in n1Ids }
        val target = all.single { it.kanji == "劣" }
        val guards = listOf("弱", "悪", "下", "低", "貧", "負", "少")
        val curated = listOf("努", "功", "省")
        assertEquals(guards, target.quizExclusions)
        assertEquals(curated, target.distractors)
        assertEquals(listOf("功"), curated.filter { it in n1Ids })
        fun assertPairwiseSafe(options: List<io.github.stopcran.kanji.core.quiz.QuizOption>) {
            val cards = options.map { option -> all.single { it.kanji == option.kanji } }
            for (left in cards) for (right in cards.filter { it.kanji != left.kanji }) {
                assertFalse("${left.kanji}/${right.kanji} guarded pair leaked",
                    right.kanji in left.quizExclusions || left.kanji in right.quizExclusions)
            }
        }
        val custom = all.filter { it.kanji in curated + target.kanji }
        val randomSubset = listOf(target) + n1.filter { it.kanji != target.kanji }
            .shuffled(Random(776)).take(15)
        val rows = mutableListOf<kotlinx.serialization.json.JsonObject>()
        val pools = linkedMapOf("N1" to n1, "All" to all, "boundedCustom" to custom,
            "randomN1Subset776" to randomSubset)
        for ((poolName, pool) in pools) repeat(16) { seed ->
            val options = QuizBuilder.options(target, pool, Random(seed))
            assertEquals(4, options.size)
            assertEquals(4, options.map { it.title }.toSet().size)
            assertEquals(1, options.count { it.kanji == target.kanji })
            assertTrue(options.none { it.kanji in guards })
            assertTrue(curated.filter { id -> pool.any { it.kanji == id } }
                .all { id -> options.any { it.kanji == id } })
            assertTrue(options.all { o -> pool.any { it.kanji == o.kanji && it.title == o.title } })
            assertPairwiseSafe(options)
            if (poolName == "All" || poolName == "boundedCustom") {
                assertEquals((curated + target.kanji).toSet(), options.map { it.kanji }.toSet())
            }
            rows += buildJsonObject {
                put("pool", poolName)
                put("seed", seed)
                put("poolMembershipInOrder", JsonArray(pool.map { JsonPrimitive(it.kanji) }))
                put("options", JsonArray(options.map { option -> buildJsonObject {
                    put("kanji", option.kanji)
                    put("title", option.title)
                } }))
            }
        }
        val guardRows = mutableListOf<kotlinx.serialization.json.JsonObject>()
        for (excludedId in guards) {
            val pair = all.filter { it.kanji in setOf(target.kanji, excludedId) }
            assertEquals(2, pair.size)
            for (quizTarget in pair) repeat(16) { seed ->
                val excluded = pair.single { it.kanji != quizTarget.kanji }
                val sampled = pair + all.filter { it.kanji !in pair.map { p -> p.kanji } }
                    .shuffled(Random(776 + seed)).take(seed)
                val checkedPools = pools + linkedMapOf(
                    "sampledFiltered" to sampled, "pairOnly" to pair,
                    "targetOutsidePool" to sampled.filter { it.kanji != quizTarget.kanji })
                for ((poolName, pool) in checkedPools) {
                    val options = QuizBuilder.options(quizTarget, pool, Random(seed))
                    assertEquals(1, options.count { it.kanji == quizTarget.kanji })
                    assertFalse("$excludedId leaked in $poolName", options.any { it.kanji == excluded.kanji })
                    assertTrue(options.size in 1..4)
                    assertEquals(options.size, options.map { it.title }.toSet().size)
                    assertTrue(options.all { it.kanji == quizTarget.kanji || pool.any { p -> p.kanji == it.kanji } })
                    assertPairwiseSafe(options)
                    if (poolName == "pairOnly") assertEquals(1, options.size)
                    guardRows += buildJsonObject {
                        put("target", quizTarget.kanji)
                        put("excluded", excluded.kanji)
                        put("pool", poolName)
                        put("seed", seed)
                        put("poolMembershipInOrder", JsonArray(pool.map { JsonPrimitive(it.kanji) }))
                        put("options", JsonArray(options.map { JsonPrimitive(it.kanji) }))
                    }
                }
            }
        }
        val nontransitiveRows = mutableListOf<kotlinx.serialization.json.JsonObject>()
        val preexistingDirect = mutableSetOf<String>()
        for (left in guards) for (right in guards.filter { it != left }) {
            val pair = all.filter { it.kanji in setOf(left, right) }
            val leftCard = pair.single { it.kanji == left }
            val rightCard = pair.single { it.kanji == right }
            if (right in leftCard.quizExclusions || left in rightCard.quizExclusions) {
                preexistingDirect += "$left/$right"
                continue
            }
            repeat(16) { seed ->
                val options = QuizBuilder.options(leftCard, pair, Random(seed))
                assertEquals(setOf(left, right), options.map { it.kanji }.toSet())
                nontransitiveRows += buildJsonObject {
                    put("target", left)
                    put("neighbor", right)
                    put("seed", seed)
                    put("options", JsonArray(options.map { JsonPrimitive(it.kanji) }))
                }
            }
        }
        assertEquals(64, rows.size)
        assertEquals(1568, guardRows.size)
        assertEquals((42 - preexistingDirect.size) * 16, nontransitiveRows.size)
        assertTrue(nontransitiveRows.isNotEmpty())
        val destination = File("C:\\Users\\stop-\\n1-kanji-workspace\\control\\logs\\64a0077c-7184-42a6-98c3-7adf3654d63e")
        for ((name, value) in linkedMapOf(
            "choices" to JsonArray(rows), "direct-guards" to JsonArray(guardRows),
            "nontransitive" to JsonArray(nontransitiveRows),
            "preexisting-neighbor-edges" to JsonArray(preexistingDirect.sorted().map { JsonPrimitive(it) }))) {
            val file = File(destination, "meaning-776-$name.json")
            check(!file.exists()) { "Do not overwrite acceptance evidence: $file" }
            file.writeText(value.toString() + "\n")
        }
    }
}
