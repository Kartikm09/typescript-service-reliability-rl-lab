import unittest

from rl_evaluator.patching import PatchError, parse_changed_paths, prohibited_paths


class PatchingTests(unittest.TestCase):
    def test_extracts_safe_changed_path(self) -> None:
        patch = "diff --git a/src/example.txt b/src/example.txt\n"
        self.assertEqual(["src/example.txt"], parse_changed_paths(patch))

    def test_rejects_traversal(self) -> None:
        with self.assertRaises(PatchError):
            parse_changed_paths("diff --git a/../secret b/../secret\n")

    def test_reports_prohibited_paths(self) -> None:
        self.assertEqual(["tests/owned.py"], prohibited_paths(["src/a.py", "tests/owned.py"], ["src/**"]))


if __name__ == "__main__":
    unittest.main()
