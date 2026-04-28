import pytest

from qgene import Individual


def test_create_individual():
    indiv = Individual(genome=("a", "b", "c"))
    indiv.score = 10
    assert indiv.genome == ("a", "b", "c")
    assert indiv.score == 10


def test_genome_length():
    assert Individual(genome=(1, 2, 3)).n_genes == 3


def test_compare():
    assert Individual((1, 2, 3)) == Individual((1, 2, 3), score=1)
