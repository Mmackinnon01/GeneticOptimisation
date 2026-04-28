import pytest

from qgene.individual import Individual
from qgene.score.base import TestScore


def test_score():
    indiv = Individual((1, -2, 3))
    TestScore()([indiv])
    assert indiv.score == -6
