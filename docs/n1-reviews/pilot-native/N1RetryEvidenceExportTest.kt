package io.github.stopcran.kanji.ui

import android.os.Build
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.*
import org.junit.Test
import java.io.File

class N1RetryEvidenceExportTest {
    @Test fun exportBoundedRetryEvidence() {
        assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
        assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        val names = listOf("native-route.json", "native-route-tree.txt") + listOf(
            "selection", "meaning-question", "support-article", "article-back", "curated-reading-question",
            "curated-reading-feedback", "drawing-trace", "drawing-feedback", "drawing-recall-feedback",
        ).map { "$it.png" }
        for (suffix in names) {
            val name = "n1-retry-$suffix"
            val file = File(instrumentation.targetContext.getExternalFilesDir(null), name)
            require(file.isFile) { "Missing required retry evidence: $name" }
            android.util.Base64.encodeToString(file.readBytes(), android.util.Base64.NO_WRAP)
                .chunked(8000).forEachIndexed { index, chunk ->
                    instrumentation.sendStatus(2, android.os.Bundle().also {
                        it.putString("n1File", name)
                        it.putInt("n1Part", index)
                        it.putString("n1Data", chunk)
                    })
                }
        }
    }
}
