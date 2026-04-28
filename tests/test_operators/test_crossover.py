import pytest

from qgene.individual import Individual
from qgene.operators.crossover import TestCrossover


@pytest.fixture
def parentA():
    return Individual((1, 2, 3, 4))


@pytest.fixture
def parentB():
    return Individual((0, 0, 0, 0))


def test_crossover_compatible_parents(parentA, parentB):
    child = TestCrossover()(parents=[parentA, parentB])
    assert child.genome == (1, 0, 3, 0)
