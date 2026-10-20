import pytest
import numpy as np

from qgene.individual import Individual
from qgene.operators.mutation import DiscreteMutation, TestMutation, ContinuousMutation


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
    child = DiscreteMutation(p=1, vals=[[0,1] for i in range(4)])(parent2)
    assert child.genome == (0,0,1,1)

def test_continuous_mutation(parent):
    child = ContinuousMutation(100, lower = 0, upper = 4)(parent)
    assert np.max(child.genome) <= 4 and np.min(child.genome) >= 0