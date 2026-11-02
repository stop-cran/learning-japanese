package io.github.stopcran.kanji.ui

import android.os.Build
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.*
import org.junit.Test
import java.io.File

class N1EvidenceExportTest {
    @Test fun exportBoundedPilotEvidence() {
        assertEquals("true", InstrumentationRegistry.getArguments().getString("n1Disposable"))
        assertTrue(Build.HARDWARE in setOf("ranchu", "goldfish"))
        val instrumentation = InstrumentationRegistry.getInstrumentation()
        val names = (1..7).map { "n1-font-page-$it.png" } + listOf(
            "n1-font-raster.json", "n1-native-route.json", "n1-native-route-tree.txt",
            "n1-selection.png", "n1-meaning-question.png", "n1-support-article.png",
            "n1-article-back.png", "n1-drawing-trace.png", "n1-drawing-feedback.png",
            "n1-drawing-recall-feedback.png",
        )
        for (name in names) {
            val file = File(instrumentation.targetContext.getExternalFilesDir(null), name)
            if (!file.isFile) continue
            val encoded = android.util.Base64.encodeToString(file.readBytes(), android.util.Base64.NO_WRAP)
            encoded.chunked(8000).forEachIndexed { index, chunk ->
                instrumentation.sendStatus(2, android.os.Bundle().also {
                    it.putString("n1File", name)
                    it.putInt("n1Part", index)
                    it.putString("n1Data", chunk)
                })
            }
        }
    }
}
