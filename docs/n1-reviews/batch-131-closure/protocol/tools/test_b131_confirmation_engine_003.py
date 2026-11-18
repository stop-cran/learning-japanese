import ast
import unittest

from common import frozen
from prepare_b131_confirmation_engine_001 import SOURCE, SOURCE_SHA
from prepare_b131_confirmation_engine_003 import final_text


class B131AuditorRouteTests(unittest.TestCase):
    def test_exact_digest_import_repair_preserves_auditor_functions(self):
        source = frozen(SOURCE, SOURCE_SHA).decode("utf-8")
        text = final_text(source)
        compile(text, "confirm_b131_003.py", "exec")
        self.assertEqual(2, text.count(' / "confirm-003"'))
        self.assertNotIn(' / "confirm-002"', text)
        self.assertIn("digest import: shared preparation-003 chain", text)
        old = 'sys.path.insert(0, str(HERE.parent))'
        new = "sys.path.insert(0, str(HERE.parent / 'preparation-003'))"
        from pathlib import Path
        from common import WS
        path = WS / "scratch-116" / "confirm" / "audit-confirm.py"
        original = frozen(path, "c6ec99949ef19057f432c052df3293184c3866e65ba7387e148a39505a3b2c9e").decode()
        revised = original.replace(old, new)
        functions = lambda value: [ast.dump(node) for node in ast.parse(value).body
                                   if isinstance(node, (ast.FunctionDef, ast.ClassDef))]
        self.assertEqual(functions(original), functions(revised))
        self.assertEqual(original, revised.replace(new, old))


if __name__ == "__main__":
    unittest.main()
