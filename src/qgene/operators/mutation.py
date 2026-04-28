from typing import Protocol

from qgene.individual import Individual


class MutationProtocol(Protocol):
    def __call__(self, target: Individual) -> Individual: ...


class TestMutation(MutationProtocol):
    def __call__(self, target: Individual) -> Individual:
        return Individual((4, 3, 2, 1))
