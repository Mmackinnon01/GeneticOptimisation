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

class ContinuousMutation(MutationProtocol):

    def __init__(self, sd: float, lowers = None, uppers = None):
        self.sd = sd

        if lowers is None:
            lowers = -10**10
        if uppers is None:
            uppers = 10**10

        self.lowers = lowers
        self.uppers = uppers

    def __call__(self, target: Individual) -> Individual:
            return Individual(tuple(self.mutate(gene, i) for i, gene in enumerate(target.genome)))

    def mutate(self, gene: Any, index: int):
        new_gene = gene + np.random.normal(0, self.sd)

        lower = self.lowers[index]
        upper = self.uppers[index]

        while new_gene < lower or new_gene > upper:
            if new_gene < lower:
                new_gene = lower + np.abs(lower - new_gene)
            elif new_gene > upper:
                new_gene = upper - np.abs(upper - new_gene)
        return new_gene