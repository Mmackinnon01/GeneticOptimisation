from typing import Protocol

import numpy as np

from qgene.individual import Individual


class ScoreProtocol(Protocol):
    def __call__(self, indivs: list[Individual]) -> None: ...


class TestScore(ScoreProtocol):
    def __call__(self, indivs: list[Individual]) -> None:
        for i in indivs:
            i.score = -np.sum(np.abs(np.array(i.genome)))
