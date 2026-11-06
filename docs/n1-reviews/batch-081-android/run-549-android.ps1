$ErrorActionPreference = 'Stop'
$env:JAVA_HOME = 'C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot'
$env:ANDROID_HOME = 'C:\Users\stop-\AppData\Local\Android\Sdk'
$log = 'C:\Users\stop-\n1-kanji-workspace\control\logs\483d3eeb-91f9-428c-881e-418300821fd9'
Set-Location 'C:\Users\stop-\n1-kanji-workspace\kanji-cards-android'
$command = '.\gradlew.bat :core:test --tests io.github.stopcran.kanji.core.RealContentTest :app:testDebugUnitTest --tests io.github.stopcran.kanji.core.RareHanTest --no-daemon --no-parallel --max-workers=1 --rerun-tasks -Pkotlin.compiler.execution.strategy=in-process --init-script C:\Users\stop-\n1-kanji-workspace\control\batch-065-host-integration-heap.init.gradle'
$command | Set-Content "$log\android-command.txt" -Encoding utf8
[DateTimeOffset]::UtcNow.ToString('o') | Set-Content "$log\android-start.txt" -Encoding utf8
& .\gradlew.bat :core:test --tests io.github.stopcran.kanji.core.RealContentTest :app:testDebugUnitTest --tests io.github.stopcran.kanji.core.RareHanTest --no-daemon --no-parallel --max-workers=1 --rerun-tasks '-Pkotlin.compiler.execution.strategy=in-process' --init-script 'C:\Users\stop-\n1-kanji-workspace\control\batch-065-host-integration-heap.init.gradle' *> "$log\android.txt"
$result = $LASTEXITCODE
[DateTimeOffset]::UtcNow.ToString('o') | Set-Content "$log\android-end.txt" -Encoding utf8
$result | Set-Content "$log\android-exit.txt" -Encoding utf8
Get-Content "$log\android.txt" -Tail 12
exit $result
