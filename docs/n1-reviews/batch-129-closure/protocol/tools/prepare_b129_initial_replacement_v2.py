"""Handle source CRLF without altering the frozen first derivation or its failure."""
import ast
import json
from pathlib import Path

import prepare_b129_initial_replacement as prior
from common import TOOLS, freeze_json, frozen, require, review_dir, write_frozen
from prepare_b129_initial_replacement import binding, replacement_prompt


def verify_replacement(spec, config, initial, launch, records):
    return prior.verify_replacement(spec, config, initial, launch, records) + [binding(Path(__file__))]


def derive_text(text):
    result = prior.derive_text(text.replace("\r\n", "\n"))
    old = "from prepare_b129_initial_replacement import verify_replacement, replacement_prompt"
    require(result.count(old) == 1, "Unexpected helper import")
    return result.replace(old, "from prepare_b129_initial_replacement_v2 import "
                          "verify_replacement, replacement_prompt")


def main():
    source = TOOLS / "confirm_b127.py"
    original = frozen(source, prior.SOURCE_SHA).decode("utf-8")
    derived = derive_text(original)
    functions = lambda text: {node.name: ast.dump(node) for node in ast.parse(text).body
                              if isinstance(node, ast.FunctionDef) and node.name != "build"}
    require(functions(original) == functions(derived), "Non-builder mechanics changed")
    compile(derived, "confirm_b129_context_replacement.py", "exec")
    output = write_frozen(TOOLS / "confirm_b129_context_replacement.py", derived.encode("utf-8"))
    review = review_dir(129)
    print(json.dumps(freeze_json(review / "context-replacement-tooling-001.json", {
        "source": binding(source), "output": output, "producer": binding(Path(__file__)),
        "lineageHelper": binding(Path(prior.__file__)),
        "preservedFailedTests": binding(review / "initial-replacement-tooling-tests-001" / "receipt.json"),
        "unchangedFunctions": list(functions(original)),
        "failure": binding(review / "confirm" / f"{prior.FAILED_RUN}-superseded.json"),
        "scope": "Executed VOID first-confirmation replacement, not an accepted-confirmation follow-up. "
                 "Exact source selection and correction snapshot; explicit historical attribution. "
                 "CRLF normalized before exact code-anchor matching; all non-builder functions AST-identical. "
                 "Access/report/source/RAM/context/structure/final audit gates unchanged.",
        "reviewersLaunched": False,
    })))


if __name__ == "__main__":
    main()
