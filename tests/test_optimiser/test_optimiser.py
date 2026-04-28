import pytest

from qgene.individual import Individual
from qgene.operators.crossover import TestCrossover
from qgene.operators.mutation import TestMutation
from qgene.optimisation import GeneticOptimiser
from qgene.score.base import TestScore
from qgene.selection.base import TestSelection


@pytest.fixture
def population():
    return [Individual((1, 1, 1, 1)) for i in range(3)]


@pytest.fixture
def optimiser(population):
    return GeneticOptimiser(
        p0=population,
        score_func=TestScore(),
        crossover_func=TestCrossover(),
        mutation_func=TestMutation(),
        selection_func=TestSelection(),
    )


def test_initialise_optimiser(optimiser):
    assert len(optimiser.pop) == 3
    assert optimiser.pop[0].score == -4


def test_iterate(optimiser):
    p0 = optimiser.pop
    optimiser.iterate()
    assert {id(x) for x in p0}.isdisjoint(id(y) for y in optimiser.pop)
    assert optimiser.pop[0].score is not None


def test_optimal_solution(optimiser):
    assert optimiser.optimal_individual == Individual((1, 1, 1, 1))


def test_retention(optimiser):
    optimiser.retention = 0.2
    p0 = optimiser.pop
    optimiser.iterate()
