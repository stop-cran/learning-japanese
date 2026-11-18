"""Write the frozen B134 Claude-001 coordinator adjudication (B134-specific content)."""
import hashlib
import json
import os
import stat
from pathlib import Path

H = Path(r"C:\Users\stop-\n1-kanji-workspace\scratch-134\review\neutral-preparation-001\projected-successor-001")
D = Path(__file__).resolve().parent
OUT = H / "N1-B134-CLAUDE-001-coordinator-adjudication.json"
CANDIDATE = "ba80afffc20a72d31be68b355b6f90aab36a5726"
FINAL = H / "N1-B134-CLAUDE-001-final.json"
REPORT = H / "reports-001" / "review-claude-001" / "initial-claude-001.md"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


final_sha = sha(FINAL)
final = json.loads(FINAL.read_text(encoding="utf-8"))
report_sha = sha(REPORT)
assert final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
assert final["report"]["sha256"] == report_sha
assert final["structure"]["overall"] == "UNVERIFIED"
assert final_sha == "65d9c8584b0fbdadc227a7c7c087ef2ebe6c0f7cb3b0fbfb9ed2bb3f99ae79c8"
assert report_sha == "2b8df7a7eaf9269cde98e27025d4b5d7175b80d3ed6f4b21f5053e9aeafc481e"
kot = D / "evidence" / "kotobank-kon.html"
web = D / "evidence" / "weblio-kon.html"
assert sha(kot) == "034cfdcee9becc92daa72857d15577059d8380016f4d0324b8d8f4c76f07b134"
assert sha(web) == "44342f184df45e4729777748885df2df131e25f2487819e89506ad9097f594bd"

AUD = "audit e7ea65f6b5dce77e470f72b7cb8d5306fcef0dc862730e69b1d04ae2f3556ed0"
KON = ("Coordinator capture 2026-11-17T05:10:39Z: Kotobank 紺 (sha 034cfdce...) 精選版日本国語大辞典 'こん【紺】 青黒く紫を含んだ色。濃い藍。'; "
       "普及版字通 訓義 '深青に赤を含んだいろ' (形声, 声符甘); Weblio デジタル大辞泉 (sha 44342f18...) '紫色を帯びた深い青色' and '紫色を帯びた濃い青色。濃い藍色。'")

checks = []


def add(claim, evidence, disposition):
    checks.append({"claim": claim, "evidence": evidence, "disposition": disposition})


add("Execution identity, complete ordered reads, single write/readback and report binding.",
    f"Final {final_sha}; {AUD}: actualResponseModels=[claude-opus-5-5], assistantModels=[claude-opus-5.5], bootstrapVerified, reviewerIdle, 49/49 core and 7/7 extension segments, writes=1, readbacks=1 verified, fetches=0, unexpectedUserMessages=0, breaches=0, 645 events extending the phase-1 snapshot; capacity PASS, zero compactions, peak/last input 449974 of observed 952000. Report 14332 bytes ReadOnly; note 'equals its single write after CRLF normalization'.",
    "Execution accepted. L1 (reviewer cannot self-verify identity) is preserved; coordinator telemetry establishes the observed Claude family. CRLF-normalized equality is disclosed, not raw-byte identity of the write payload.")
add("Report read-coverage statement: all core/extension segments, full title index and both complete extracts read through the chain.",
    "Audit counts 49/49 core and 7/7 extension; the title index (1262 lines) and two extracts are inside those chains; baseline is represented by the candidate index plus the exact one-line deletion delta.",
    "Accepted as reads of required in-chain sources only; O:none means no optional full KD records or derived indices were read (L5). No whole-corpus or full-source linguistic approval inferred.")
add("Overall verdict UNVERIFIED; facets Correctness CLEAN, Scoped coverage CLEAN, Consistency/quiz safety UNVERIFIED, Comprehensibility CLEAN; zero findings, three optional points, seven limits, 26 D/E rows.",
    "Final structure contract report-structure-v1 PASS with exactly these counts and facets.",
    "Verdict UNVERIFIED recorded unchanged. Its sole driver is the 紫/紺 evidence gap (O1/L2), which coordinator evidence now settles as C1; the report is not rewritten and its label does not become teaching approval or rejection.")
add("Correctness CLEAN: purple/violet, purple gromwell with white flowers and dye root, soy sauce, Nikkoku secondary senses, 字通 11-stroke label and ツツム gloss, name readings さい/ゆかり, 紫陽花 jukujikun, シ/むらさき, 12 strokes, 糸 no.120, grade 8.",
    "Coordinator-opened JMdict 1311640/1311680/1311700/1311730, full KD 紫 (12 strokes, rad 120, grade 8, シ/むらさき, nanori さい/ゆかり), 01-extract:10 (白い小花), :32 (paper/cloth), :34 (女), :35 (醤油), :36 (検校), :37 (江戸), :60 (名義抄 ムラサキ・ツツム); 02-extract:208 (ムラサキの花は白色); source/payload/gate proofs PASS for KanjiVG 12 strokes.",
    "Agreed. Card claims checked are source-supported with the card's own qualifications (unresolved ツツム scope, name-only readings, whole-word 紫陽花, 11 vs 12 strokes retained).")
add("Scoped coverage CLEAN; omission of the sourced 形声 analysis is optional (O2).",
    "Card body teaches color, plant, condiment, both readings with dispositions, words and qualified historical senses; mnemonic labelled non-etymological as docs/content-format.md permits.",
    "Agreed; see O2 disposition.")
add("Comprehensibility CLEAN with unexplained groupings noted as optional (O3).",
    "snapshot/kanji/紫.md Notes list precautions by broad label in plain English.",
    "Agreed with C2 caveat: the 久 grouping is not merely unexplained but has no displayed-label basis; see O3/C2.")
add("D1 紺: possible hue overlap; pair undeclared on both endpoints; Daijisen 紺 purplish cast unverified (O1/L2).",
    f"repo/kanji/紺.md:14 quiz_exclusions [青, 濃, 暗]; :24 'Daijisen describes a purplish cast'; 紫.md exclusions omit 紺; JMdict 1311690 紫紺 'dark purple; bluish purple' (jmdict-families.xml:88). {KON}. Author pair-dispositions.json has no 紫/紺 comparison. 紺 shares all three tags (jlpt-n1, grade-8, structure-unclassified) with 紫, so it is a preferred tag fallback choice.",
    "Evidence gap resolved by coordinator sources: the 紺 card's purplish-cast claim is accurate. 紺's ordinary dictionary meaning is a deep blue containing purple, bridged by 紫紺; the direct pair was never compared. Displayed English labels still name different base hues, so this is a precautionary consistency issue, not a proven wrong-key defect. Carried as coordinator claim C1 for reconciliation.")
add("D2 紅: harmless; English purple can include crimson; 紅紫 lists two colors.",
    "02-extract:214 ('purple'は紫と紅の両義を含める場合がある); JMdict 2831537 紅紫 'crimson and purple; red-purple; magenta' (line 354); repo/kanji/紅.md title 'crimson; deep red'.",
    "Agreed harmless: no ordinary 紫 sense is crimson and 'crimson; deep red' does not defensibly answer 紫; English 'purple' breadth does not make 紫 crimson.")
add("D3 青: harmless; 青紫 is a compound shade.",
    "JMdict 2614890 青紫 'bluish purple' (line 321); 02-extract:198 (青と赤の間色), :216 (violet as shortest-wavelength rainbow color); title 'blue, green'.",
    "Agreed harmless.")
add("D4 根: harmless; 紫根 is the dye root.",
    "JMdict 紫根 'gromwell root' is at jmdict-families.xml:281 (report cites :280, which is 紫貽貝); 紫 names plant/color (1311640); 根 title 'root; foundation'.",
    "Agreed harmless; citation off by one line, substance verified.")
add("D5 花: harmless; gromwell flowers are white and a specific plant name is not 'flower'.",
    "01-extract:10 '白い小花をつける'; 02-extract:208 'ムラサキの花は白色'; 花 title 'flower'; no 菫/'violet' card exists in the title index.",
    "Agreed harmless; coordinator title-index search found no other card titled violet/purple.")
add("D6 絹: harmless; silk link is an etymological theory; cloth sense is purple-colored cloth.",
    "01-extract:32 'その色の紙や布'; 01-extract:54 字通 quotes 説文 帛…赤色 (theory/description); 絹 title 'silk'.",
    "Agreed harmless.")
add("D7 層: harmless; specific historical rank title versus layers/class strata.",
    "01-extract:36 検校 rank via 紫衣; KD projection 層 (line 38) meanings stratum/social class; 層 title 'layer; stratum'.",
    "Agreed harmless; 紫 already guards rank-titled cards (丙 位 准 格 級 極).")
add("D8 列: harmless; 列 rank is a line/row, not a status title.",
    "JMdict 1558330 列 glosses 'row; line; …; rank; …(taxonomic rank)' (line 181); title 'row; queue'.",
    "Agreed harmless.")
add("D9 稲: harmless; different specific plants.",
    "JMdict 1167820 稲 いね (line 10); 1311640 gromwell sense; title 'rice plant'.",
    "Agreed harmless.")
add("D10 殿: harmless; palace meaning belongs to compounds such as 紫宸殿/紫闥.",
    "JMdict 2179880 紫闥 (line 268); 1442490 殿 との 'feudal lord; mansion; palace' archaic honorific (line 137); 01-extract:54 字通 紫宸・紫禁 as palace words; title 'palace; lord'.",
    "Agreed harmless: no source gives 紫 alone a palace or lord sense.")
add("D11 書: harmless; Genji/poetry titles are specific works, not write/book meanings.",
    "01-extract Nikkoku abbreviation senses for 源氏物語/紫式部; JMdict 書 ふみ literary book sense exists but displayed title is 'write'.",
    "Agreed harmless; 紫 already guards book/writing labels (冊 本 巻 編 文 著 話 記 筆).")
add("D12 妻: harmless; woman is not wife.",
    "01-extract:34 '女をいう。〔日葡辞書〕'; JMdict 2742880 妻 め has an archaic woman sense but displayed title is 'wife'; 婦 'woman; wife' and 女 'woman, female' are already excluded.",
    "Agreed harmless; the woman-labelled cards carry the guard.")
add("D13 町: harmless; Edo abbreviation is one city, not 'town'.",
    "01-extract:37 江戸紫→江戸; title 'town, neighborhood'; 市 京 都 already guarded.",
    "Agreed harmless.")
add("D14 油: harmless; soy sauce is not oil.",
    "01-extract:35 醤油 sense; title 'oil; grease'; no soy-sauce-titled card in the index.",
    "Agreed harmless.")
add("D15 被: harmless; ツツム is an unresolved 名義抄 gloss.",
    "名義抄 '紫 ムラサキ・ツツム' is at 01-extract:60 (report cites :59, the section header); 被 title 'cover; incur'.",
    "Agreed harmless; citation off by one, substance verified.")
add("D16 系: harmless; ゆかり is a name reading and literary association.",
    "01-extract:44 '紫のゆかり' from 古今集 poetry; KD nanori ゆかり; title 'lineage; system'.",
    "Agreed harmless; 紫 already guards relationship labels 仲 係 関 統 as precautions.")
add("D17 濃: harmless for modern display; Heian 濃 = deep purple is historical.",
    "01-extract:77 and :101 ('濃(こき)といえば濃紫…'; report cites :76/:100); title 'concentrated; dark'.",
    "Agreed harmless; 'dark' is not a defensible meaning of 紫, and the historical convention concerns 濃 alone, not 紫.")
add("D18 薄: harmless; Heian 薄色 = light purple is historical.",
    "01-extract:101 '薄色といえば薄紫をさした' (report cites :100); title 'thin; dilute'.",
    "Agreed harmless; citation off by one, substance verified.")
add("E1 久: declared; weak precautionary basis (久しい 'old (story)'), see O3.",
    "repo/kanji/久.md:29 '久しい - long (time that has passed); old (story)'; title 'a long time'; author pair-disposition basis: KD 'old story' versus the Genji abbreviation.",
    "Agreed the declaration exists; the basis does not concern 久's displayed label or any ordinary 紫 meaning. Carried as coordinator claim C2.")
add("E2 色: declared; color category versus specific color.",
    "02-extract:208 (Heian context) and author disposition 'particular color vs color generally'; title 'color'.",
    "Agreed justified precaution.")
add("E3 包: declared; latent つつむ reading collision only in smaller hypothetical pools.",
    "checks/reading-exposure.log:19-20: つつむ offered by 包 cannot be drawn in N1/All/Starter pools; risk class [紫 包] for hypothetical smaller pools; 紫 quizKunyomi is only むらさき.",
    "Agreed; latent collision disclosed, not production-drawable; no custom/multi-borrow acceptance inferred (L6).")
add("E4 統: declared; precautionary relationship label.",
    "KD projection 統 (line 84) includes relationship/lineage glosses; title 'unify; lineage'.",
    "Agreed precautionary.")
add("E5 館: declared; archaic noblewoman basis.",
    "JMdict 1216210 館/屋形 やかた archaic honorific noble sense (line 34); title 'hall; large building'.",
    "Agreed the declaration exists; basis is a non-displayed archaic sense versus a non-ordinary 紫 'woman' use. Included in C2 for explanation or removal.")
add("E6 札: declared; purple paper/cloth basis.",
    "01-extract:32 その色の紙や布; title 'tag; banknote'.",
    "Agreed precautionary.")
add("E7 植: declared; generic plant label.",
    "JMdict 1311640 plant sense; 植 title 'plant; put in the ground' (verbal); 草 苗 also guarded.",
    "Agreed precautionary and consistent with D5/D9.")
add("E8 極: declared; highest-rank gloss versus 検校 rank use.",
    "KD projection 極 (line 62) rank glosses; 01-extract:36 検校; title 'extreme; pole'.",
    "Agreed precautionary.")
add("Findings: none.",
    "Report Findings section 'None.'; structure findings=0.",
    "Accepted: no reviewer finding. Coordinator claims C1/C2 are coordinator-originated and must not be attributed to the reviewer.")
add("O1: decide and record the direct 紫/紺 pair; verify Daijisen 紺.",
    KON + " 紺.md:24 claim is accurate.",
    "Accepted as justified. Reconciliation requirement C1: the author either adds 紺 to 紫 quiz_exclusions with a brief qualified note (deep blue that dictionaries describe as purple-tinged; navy blue and purple remain different labels), or records an explicit source-backed distinguishing rationale in batch evidence. Original Claude reviewer confirmation required.")
add("O2: optionally mention 字通 形声 with phonetic 此.",
    "01-extract:54 '[字形] 形声 声符は此'; shape-evidence.json KanjiVG kvg:phon='此'; repository precedent: 0 of 271 delivered N1 cards carry phonetic-compound, and 紺 (字通 形声, 声符甘) is structure-unclassified.",
    "Optional, not required. Retaining structure-unclassified with the labelled mnemonic matches N1 precedent; a qualified 字通 line would be acceptable but must not change tags or add a phonetic field without the repository's structural-classification evidence standard.")
add("O3: explain or trim the weakest precaution groupings (久 under book/writing, 館 under woman).",
    "紫.md:65-69; 久.md:29; JMdict 1216210; author dispositions for 紫/久 (KD 'old story' versus Genji abbreviation) and 紫/館 (noblewoman); docs/content-format.md: 'Author a pair only from evidence about the actual displayed labels and ordinary meanings'.",
    "Accepted as justified. Reconciliation requirement C2: drop 久 from exclusions and notes unless the author records a displayed-label basis; for 館, either add a brief learner-facing reason (archaic やかた noble sense) or drop it. Exclusions are quiz-safe either way; the issue is basis and comprehensibility.")
add("L1: model identity not self-verifiable.", f"{AUD} model records claude-opus-5.5/claude-opus-5-5.", "Preserved; coordinator telemetry supplies identity.")
add("L2: Daijisen 紺 not in opened evidence.", KON, "Resolved for coordinator adjudication by the dated capture; the reviewer's own pass remains limited as stated.")
add("L3: identified but unread candidates 赤 典 紀 史 括 囲 菜 鮎 鯉 鯛 神.",
    "Title index: 赤 'red'; 典 'reference texts; rules; ceremony'; 紀 'chronicle'; 史 'history; chronicle'; 括 'tie together; enclose'; 囲 'surround; enclose'; 菜 'vegetables; greens'; 鮎 'sweetfish; ayu'; 鯉 'carp'; 鯛 'sea bream'; 神 'deity'. Full-index search for violet/purple/sardine/soy/sauce/indigo/lavender/magenta/navy returned only 紫 and 紺 color titles.",
    "Coordinator title check finds no defensible ordinary overlap: specific other fish, red, chronicles and enclose labels are not 紫 meanings, and exclusions are not transitive by design. Not adjudicated as full-card reads.")
add("L4: raw baseline index not read; historical glyph images unavailable.", "Packet design and disclosure.", "Preserved.")
add("L5: no optional KD records/derived indices requested.", "Phase-1 O:none.", "Preserved; KD facts rest on the documented projection.")
add("L6: gates are structural evidence only; bounded pools; no Kotlin/device/rendering/APK acceptance.", "Gate logs and reading-exposure scope.", "Preserved; no such acceptance inferred.")
add("L7: JLPT N1 label rests on source-row metadata and policy.", "Source row 831 and docs/jlpt-levels.md policy.", "Preserved.")

record = {
    "candidate": CANDIDATE,
    "run": "N1-B134-CLAUDE-001",
    "finalSha256": final_sha,
    "reportSha256": report_sha,
    "claimsAdjudicated": True,
    "verdict": "UNVERIFIED",
    "coordinatorAssessment": ("Original UNVERIFIED review accepted as evidence with zero findings. Its single unverified point (紫/紺) is settled by dated coordinator sources "
                              "as a justified precautionary consistency correction (C1); the weak 久/館 precaution bases are carried as C2. Report preserved unchanged; this is review acceptance, not teaching closure."),
    "acceptedFindings": [],
    "openClaimIds": ["O1", "O2", "O3"],
    "coordinatorClaimIds": ["C1", "C2"],
    "reconciliationRequirements": {
        "C1": "紫/紺: add 紺 to 紫 quiz_exclusions with a qualified note, or record a source-backed distinguishing rationale; cite the dated Kotobank/Weblio 紺 capture.",
        "C2": "久/館 groupings: drop 久 unless a displayed-label basis is recorded; explain or drop 館.",
        "O2": "Optional; record the decision. Default: keep structure-unclassified per N1 precedent.",
        "timing": "Only after the blind GPT initial review is accepted. No Claude report, finding or coordinator adjudication is sent to GPT.",
        "closure": "Signed author revision with source-backed dispositions, re-verified sources/payload/gates, and bounded original-reviewer confirmation. No forced reviewer agreement.",
    },
    "coordinatorEvidence": {
        "directory": str(D / "evidence"),
        "files": {"kotobank-kon.html": sha(kot), "weblio-kon.html": sha(web), "retrieval.txt": sha(D / "evidence" / "retrieval.txt")},
        "scope": "Coordinator adjudication evidence only; not part of the frozen reviewer packet.",
    },
    "citationNotes": "Reviewer line references off by one at jmdict-families.xml:280 (紫根 at 281), 01-extract:59 (ツツム at 60), 01-extract:76/100 (濃/薄色 at 77/101); substance verified.",
    "limits": "Review acceptance only. No teaching edit, publication, delivery credit, whole-set, native/device or rendering acceptance.",
    "claimChecks": checks,
}
assert all(all(isinstance(c[k], str) and c[k].strip() for k in ("claim", "evidence", "disposition")) for c in checks)
with OUT.open("x", encoding="utf-8", newline="\n") as stream:
    stream.write(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
os.chmod(OUT, stat.S_IREAD)
print(json.dumps({"path": str(OUT), "sha256": sha(OUT), "claimChecks": len(checks)}, ensure_ascii=False))
