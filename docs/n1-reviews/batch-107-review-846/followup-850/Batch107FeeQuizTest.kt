package io.github.stopcran.kanji.core

import io.github.stopcran.kanji.core.content.ContentParser
import io.github.stopcran.kanji.core.words.WordCard
import io.github.stopcran.kanji.core.words.WordDirection
import io.github.stopcran.kanji.core.words.WordOption
import io.github.stopcran.kanji.core.words.WordQuizBuilder
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File
import kotlin.random.Random

class Batch107FeeQuizTest {
    private fun excluded(a: WordCard, b: WordCard) =
        b.word in a.quizExclusions || a.word in b.quizExclusions

    private fun checkOptions(
        options: List<WordOption>, target: WordCard, blocked: WordCard,
        cards: Map<String, WordCard>, expectedSize: Int,
    ) {
        assertEquals(expectedSize, options.size)
        assertEquals(1, options.count { it.word == target.word })
        assertFalse(options.any { it.word == blocked.word })
        assertEquals(options.size, options.map { it.word }.toSet().size)
        assertEquals(options.size, options.map { it.label }.toSet().size)
        options.map { cards.getValue(it.word) }.forEachIndexed { index, card ->
            options.take(index).forEach { assertFalse(excluded(card, cards.getValue(it.word))) }
        }
    }

    @Test
    fun feeSafeguardIsDirectSymmetricAndPreservesEarlierPairs() {
        val root = File("../../learning-japanese")
        assertTrue("The actual sibling content checkout is required", File(root, "manifest.json").isFile)
        val parsed = ContentParser.parse(PublishableContentFixture.load(root))
        assertEquals(emptyList<String>(), parsed.problems)
        val words = parsed.words.map {
            WordCard(it.word, it.reading, it.title, it.type, it.kanji, it.tags,
                it.jlpt, it.quizExclusions, it.quizDistractors, it.quizImage)
        }
        val cards = words.associateBy { it.word }
        assertEquals(words.size, cards.size)
        assertEquals(listOf("感覚"), cards.getValue("勘").quizExclusions)
        assertEquals(listOf("計算", "支払う", "給与", "払う", "代金", "料金"),
            cards.getValue("勘定").quizExclusions)
        val pairs = listOf(
            "勘" to "感覚", "勘定" to "計算", "勘定" to "支払う", "勘定" to "給与",
            "勘定" to "払う", "勘定" to "代金", "勘定" to "料金",
        )
        val directions = listOf(WordDirection.JpToEn, WordDirection.EnToJp)
        for ((first, second) in pairs) {
            val a = cards.getValue(first)
            val b = cards.getValue(second)
            assertTrue("$first / $second must be a direct pair", excluded(a, b))
            for (direction in directions) {
                for ((target, blocked) in listOf(a to b, b to a)) {
                    repeat(10) { seed ->
                        checkOptions(WordQuizBuilder.options(target, listOf(a, b), direction, Random(seed)),
                            target, blocked, cards, 1)
                    }
                }
            }
        }
        val bill = cards.getValue("勘定")
        val fee = cards.getValue("料金")
        assertEquals("reckoning; bill", bill.title)
        assertEquals("fee; charge; fare", fee.title)
        val fillers = mutableListOf<WordCard>()
        for (candidate in words.sortedBy { it.word }) {
            if (candidate.word in setOf(bill.word, fee.word) || candidate.title in setOf(bill.title, fee.title) ||
                excluded(candidate, bill) || excluded(candidate, fee) ||
                fillers.any { it.title == candidate.title || excluded(it, candidate) }) continue
            fillers += candidate
            if (fillers.size == 5) break
        }
        assertEquals(5, fillers.size)
        val custom = listOf(bill, fee) + fillers
        val oldBill = bill.copy(quizExclusions = bill.quizExclusions - fee.word)
        val oldFee = fee.copy(quizExclusions = fee.quizExclusions - bill.word)
        val oldPool = listOf(oldBill, oldFee)
        for (direction in directions) {
            for ((target, blocked) in listOf(bill to fee, fee to bill)) {
                for ((name, pool) in listOf("all" to words, "custom" to custom)) {
                    repeat(20) { seed ->
                        val options = WordQuizBuilder.options(target, pool, direction, Random(seed))
                        checkOptions(options, target, blocked, cards, 4)
                        if (seed == 0) println("FEE $name $direction ${target.word}: $options")
                    }
                }
            }
            for (target in oldPool) {
                val options = WordQuizBuilder.options(target, oldPool, direction, Random(0))
                assertEquals(setOf(bill.word, fee.word), options.map { it.word }.toSet())
                println("FEE unguarded $direction ${target.word}: $options")
            }
            val neutral = fillers.first()
            repeat(20) { seed ->
                val options = WordQuizBuilder.options(neutral, listOf(neutral, bill, fee), direction, Random(seed))
                assertEquals(2, options.size)
                assertEquals(1, options.count { it.word == bill.word || it.word == fee.word })
            }
        }
    }
}
