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

    def __init__(self, sd: float, lower = None, upper = None):
        self.sd = sd

        if lower is None:
            lower = -10**10
        if upper is None:
            upper = 10**10

        self.lower = lower
        self.upper = upper

    def __call__(self, target: Individual) -> Individual:
            return Individual(tuple(self.mutate(gene) for i, gene in enumerate(target.genome)))

    def mutate(self, gene: Any):
        new_gene = gene + np.random.normal(0, self.sd)

        while new_gene < self.lower or new_gene > self.upper:
            if new_gene < self.lower:
                new_gene = self.lower + np.abs(self.lower - new_gene)
            elif new_gene > self.upper:
                new_gene = self.upper - np.abs(self.upper - new_gene)
        return new_gene