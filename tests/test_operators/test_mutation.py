import pytest

from qgene.individual import Individual
from qgene.operators.mutation import TestMutation


@pytest.fixture
def parent():
    return Individual((1, 2, 3, 4))


def test_mutation(parent):
    child = TestMutation()(parent)
    assert child.genome == (4, 3, 2, 1)
