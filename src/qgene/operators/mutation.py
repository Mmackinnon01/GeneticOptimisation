import random
from typing import Any, Protocol

import numpy as np

from qgene.individual import Individual


class MutationProtocol(Protocol):
    def __call__(self, target: Individual) -> Individual: ...


class TestMutation(MutationProtocol):
    def __call__(self, target: Individual) -> Individual:
        return Individual((4, 3, 2, 1))

class DiscreteMutation(MutationProtocol):

    def __init__(self, p: float, vals: list[list]) -> None:
        self.p = p
        self.vals = vals

    def __call__(self, target: Individual) -> Individual:
        return Individual(tuple(self.mutate(gene, i) for i, gene in enumerate(target.genome)))

    def mutate(self, gene: Any, index: int) -> Any:
        if np.random.rand() < self.p:
            choices = [x for x in self.vals[index] if x != gene]
            gene = random.choice(choices)
        return gene