import pytest

from qgene.individual import Individual
from qgene.operators.mutation import DiscreteMutation, TestMutation


@pytest.fixture
def parent():
    return Individual((1, 2, 3, 4))

@pytest.fixture
def parent2():
    return Individual((1, 1, 0, 0))


def test_mutation(parent):
    child = TestMutation()(parent)
    assert child.genome == (4, 3, 2, 1)


def test_discrete_mutation(parent2):
    child = DiscreteMutation(p=1, vals=[0,1])(parent2)
    assert child.genome == (0,0,1,1)