from pathlib import Path
import unittest

from rl_evaluator.limits import redact_paths


class PathRedactionTests(unittest.TestCase):
    def test_redacts_temporary_and_home_paths(self) -> None:
        text = (
            "/private/var/folders/aa/run/candidate/source.py:12\n"
            "/" + "Users/example/work/toolchain/testing.go:20"
        )
        redacted = redact_paths(text, Path("/var/folders/aa/run/candidate"))
        self.assertNotIn("/" + "Users/", redacted)
        self.assertNotIn("/private/var/", redacted)
        self.assertIn("<temporary-path>", redacted)
        self.assertIn("<local-path>", redacted)
