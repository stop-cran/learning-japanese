package io.github.stopcran.kanji.data

import android.app.Application
import androidx.room.Room
import io.github.stopcran.kanji.core.content.ContentParser
import io.github.stopcran.kanji.core.content.GrammarSet
import io.github.stopcran.kanji.core.content.RepoSource
import io.github.stopcran.kanji.core.content.SafeZip
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.json.Json
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode
import org.robolectric.annotation.SQLiteMode
import java.io.ByteArrayInputStream
import java.io.File
import java.io.InputStream
import java.security.MessageDigest

/** Real ContentSync and Room with a pinned local HTTP response, not a device or public-network test. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [28], manifest = Config.NONE, application = Application::class)
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@SQLiteMode(SQLiteMode.Mode.NATIVE)
class N3ArchiveSyncAcceptanceTest {
    @Test
    fun fullArchiveSurvivesOrdinarySyncDatabaseReopenAndForcedRefresh() = runBlocking {
        val archive = File(requireNotNull(System.getenv("N3_ACCEPTANCE_ARCHIVE")) {
            "N3_ACCEPTANCE_ARCHIVE must name the complete archive; this test must not skip"
        }).readBytes()
        assertEquals(
            "912a9dfc4e19653bc5eedbbd4aaae55fab5ee6a63060b3293ea71362f5c37e6a",
            MessageDigest.getInstance("SHA-256").digest(archive).joinToString("") { "%02x".format(it) },
        )
        val expected = ContentParser.parse(SafeZip.read(ByteArrayInputStream(archive)), SceneImages::problem)
        assertTrue(expected.problems.toString(), expected.problems.isEmpty())
        assertEquals(108, expected.grammar.size)
        assertEquals(3336, expected.grammar.sumOf { it.exercises.size })
        assertEquals(1139, expected.grammar.sumOf { set -> set.exercises.count { it.jlpt == 3 } })

        val source = RepoSource("n3-acceptance", "local-candidate", "pinned")
        val revision = "303667c9d4c5b96904fd1718b140fd3b7417def9"
        var downloads = 0
        val http = ContentHttp { url, _, _, _ ->
            val bytes = when (url) {
                "https://api.github.com/repos/${source.owner}/${source.repo}/commits/${source.branch}" ->
                    revision.toByteArray()
                source.commitZipUrl(revision) -> {
                    downloads++
                    archive
                }
                else -> error("Unexpected request: $url")
            }
            object : ContentResponse {
                override val code = 200
                override val body: InputStream = ByteArrayInputStream(bytes)
                override fun header(name: String): String? = null
                override fun close() { body.close() }
            }
        }
        val context = RuntimeEnvironment.getApplication()
        context.getSharedPreferences("settings", 0).edit().clear().commit()
        val settings = Settings(context)
        val databaseName = "n3-archive-acceptance.db"
        fun openDatabase() = Room.databaseBuilder(context, AppDatabase::class.java, databaseName)
            .allowMainThreadQueries().build()
        var db = openDatabase()
        try {
            val first = ContentSync(db, settings.sync, http).sync(source)
            assertTrue(first.toString(), first is SyncResult.Updated)
            first as SyncResult.Updated
            assertTrue(first.problems.toString(), first.problems.isEmpty())
            assertEquals(3336, first.grammar)
            assertEquals(108, db.content().grammar(source.id).size)
            assertEquals(1, downloads)

            val rows = db.content().grammar(source.id)
            assertEquals(expected.grammar, rows.map { Json.decodeFromString(GrammarSet.serializer(), it.json) })
            val meta = requireNotNull(db.content().meta(source.id))
            assertEquals("9320b98945604bbd", meta.contentVersion)
            assertEquals(0, meta.problems)
            assertNull(meta.grammarProblem)
            assertNull(meta.grammarCurriculumProblem)
            assertNotNull(meta.grammarCurriculumJson)
            assertEquals(revision, db.listeningTasks().sync(source.id)?.acceptedRevision)

            db.close()
            db = openDatabase()
            assertEquals(rows, db.content().grammar(source.id))
            assertEquals(meta, db.content().meta(source.id))
            val reopenedSync = ContentSync(db, Settings(context).sync, http)
            assertEquals(SyncResult.UpToDate, reopenedSync.sync(source))
            assertEquals(1, downloads)
            val refreshed = reopenedSync.sync(source, force = true)
            assertTrue(refreshed.toString(), refreshed is SyncResult.Updated)
            assertTrue((refreshed as SyncResult.Updated).problems.isEmpty())
            assertEquals(2, downloads)
            assertEquals(rows, db.content().grammar(source.id))
        } finally {
            db.close()
            context.deleteDatabase(databaseName)
        }
    }
}
