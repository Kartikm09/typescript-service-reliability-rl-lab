import tempfile
import unittest
from pathlib import Path

from rl_evaluator.workspace import WorkspaceSet


class WorkspaceTests(unittest.TestCase):
    def test_candidate_excludes_held_out_and_golden_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            baseline = root / "tasks/task-001/baseline/workspace"
            public = root / "tasks/task-001/public_tests/tests"
            held = root / "tasks/task-001/held_out_tests/tests"
            baseline.mkdir(parents=True)
            public.mkdir(parents=True)
            held.mkdir(parents=True)
            (baseline / "source.txt").write_text("source", encoding="utf-8")
            (public / "public.txt").write_text("public", encoding="utf-8")
            (held / "held.txt").write_text("held", encoding="utf-8")
            workspaces = WorkspaceSet(root, "task-001")
            try:
                workspaces.prepare_candidate()
                self.assertTrue((workspaces.candidate / "tests/public.txt").is_file())
                self.assertFalse((workspaces.candidate / "tests/held.txt").exists())
                workspaces.prepare_internal()
                self.assertTrue((workspaces.internal / "tests/held.txt").is_file())
            finally:
                workspaces.close()


if __name__ == "__main__":
    unittest.main()
