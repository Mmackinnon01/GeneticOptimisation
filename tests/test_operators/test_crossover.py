import pytest

from qgene.individual import Individual
from qgene.operators.crossover import TestCrossover, UniformCrossover


@pytest.fixture
def parentA():
    return Individual((1, 2, 3, 4))


@pytest.fixture
def parentB():
    return Individual((0, 0, 0, 0))


def test_crossover_compatible_parents(parentA, parentB):
    child = TestCrossover()(parents=[parentA, parentB])
    assert child.genome == (1, 0, 3, 0)


def test_uniform_crossover(parentA, parentB):
    child = UniformCrossover()([parentA, parentB])
    assert child.n_genes == parentA.n_genes