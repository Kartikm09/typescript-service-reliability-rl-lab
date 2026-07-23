from __future__ import annotations

from typing import Dict, Iterable

from .schemas import StageResult


def calculate_score(stages: Iterable[StageResult], weights: Dict[str, int]) -> Dict[str, object]:
    by_name = {stage.name: stage for stage in stages}
    awarded: Dict[str, int] = {}
    for name, weight in weights.items():
        awarded[name] = weight if by_name.get(name) and by_name[name].passed else 0
    return {
        "weights": dict(weights),
        "awarded": awarded,
        "score": sum(awarded.values()),
        "maximum": sum(weights.values()),
        "functional_weight": sum(
            weights.get(name, 0)
            for name in ("build", "public_tests", "held_out_tests", "regression_tests")
        ),
    }
