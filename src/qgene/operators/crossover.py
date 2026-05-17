import random
from typing import Protocol

from qgene.individual import Individual


class CrossoverProtocol(Protocol):
    def __call__(self, parents: list[Individual]) -> Individual: ...


class TestCrossover(CrossoverProtocol):
    def __call__(self, parents: list[Individual]) -> Individual:
        new_genes = []
        n_parents = len(parents)
        for i in range(parents[0].n_genes):
            new_genes.append(parents[i % n_parents].genome[i])

        return Individual(tuple(new_genes))


class UniformCrossover(CrossoverProtocol):
    def __call__(self, parents: list[Individual]) -> Individual:
        return Individual(tuple(random.choice(parents).genome[i] for i in range(parents[0].n_genes)))
