import numpy as np
import pytest

from qgene.individual import Individual
from qgene.selection.base import TestSelection, UniformSelection


@pytest.fixture
def population():
    return [
        Individual((0, 0, 0, 0), score=1),
        Individual((0, 1, 0, 0), score=20),
        Individual((0, 10, 0, 0), score=11),
        Individual((0, 0, 5, 0), score=10),
    ]


def test_selection(population):
    selection = TestSelection()(population, 2)
    assert selection == [
        [Individual((0, 1, 0, 0)), Individual((0, 10, 0, 0))],
        [Individual((0, 1, 0, 0)), Individual((0, 10, 0, 0))],
    ]


def test_uniform_selection(population):
    selection = UniformSelection(0.5)(population, 50)
    assert set(np.array(selection).flatten()) == set([population[1], population[2]])