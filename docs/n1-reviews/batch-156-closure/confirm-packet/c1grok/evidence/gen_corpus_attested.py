# -*- coding: utf-8 -*-
"""Corpus-wide list of reachable ATTESTED options in the word reading quiz.

usage: python gen_corpus_attested.py REPO_ROOT LABEL
Reuses word_quiz_audit.py (loader, reading(), attested(), has_reading()) unchanged by executing its source up to the
report header. For every word with a reading quiz, lists the generated look-alikes and the corpus readings of the
reachable closeness tier that are also JMdict readings of the word's written form.
"""
import sys
from pathlib import Path

AUDIT = Path(__file__).resolve().parent.parent / "wordquiz" / "word_quiz_audit.py"
SRC = AUDIT.read_text(encoding="utf-8")
SRC = SRC[: SRC.index('print("# Word-quiz option audit")')]
root, label = sys.argv[1], sys.argv[2]
sys.argv = ["word_quiz_audit.py", root]
g = {"__name__": "corpus_attested"}
exec(compile(SRC, str(AUDIT), "exec"), g)
W, reading, attested, has_reading = g["W"], g["reading"], g["attested"], g["has_reading"]
rows, n_quiz, n_gen_only, n_corpus = [], 0, 0, 0
for t in W.values():
    if not has_reading(t):
        continue
    n_quiz += 1
    att = attested(t["word"])
    gen, n_gen, rneed, rthr, rc = reading(t)
    gflags = [x for x in gen if x in att]
    tier = [c for s, c in rc if s >= rthr] if rneed > 0 and rthr is not None else []
    hits = [c for c in tier if c["reading"] in att]
    if gflags or hits:
        if hits:
            n_corpus += 1
        else:
            n_gen_only += 1
        rows.append("%s\t%s\t%s\t%s\t%d" % (t["word"], t["reading"], ",".join(gflags),
                                            "; ".join("%s %s" % (c["word"], c["reading"]) for c in hits), len(tier)))
print("# Corpus-wide reachable ATTESTED options in the word reading quiz (%s, All word stack)" % label)
print("# columns: word, reading, attested generated look-alikes, attested corpus readings in the reachable tier, tier size")
print("# words with a reading quiz: %d; with reachable ATTESTED options: %d (generated only: %d; with corpus hits: %d)"
      % (n_quiz, len(rows), n_gen_only, n_corpus))
print("\n".join(rows))
