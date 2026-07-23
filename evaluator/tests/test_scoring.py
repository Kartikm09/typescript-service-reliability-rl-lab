import unittest

from rl_evaluator.schemas import StageResult
from rl_evaluator.scoring import calculate_score


class ScoringTests(unittest.TestCase):
    def test_awards_only_passing_stage_weights(self) -> None:
        stages = [
            StageResult("build", ["build"], True, 0, 1),
            StageResult("public_tests", ["test"], False, 1, 1),
        ]
        result = calculate_score(stages, {"build": 20, "public_tests": 40})
        self.assertEqual(20, result["score"])
        self.assertEqual(60, result["functional_weight"])


if __name__ == "__main__":
    unittest.main()
