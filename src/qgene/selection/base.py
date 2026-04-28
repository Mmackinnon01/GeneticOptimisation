from typing import Protocol

from qgene.individual.base import Individual


class SelectionProtocol(Protocol):
    def __call__(
        self, population: list[Individual], n: int
    ) -> list[list[Individual]]: ...


class TestSelection(SelectionProtocol):

    def __call__(self, population: list[Individual], n: int) -> list[list[Individual]]:
        population = list(sorted(population, key=(lambda x: x.score), reverse=True))
        return [[population[0], population[1]] for i in range(n)]
