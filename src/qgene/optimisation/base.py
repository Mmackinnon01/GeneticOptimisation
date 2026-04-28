import copy
from typing import Callable

from qgene.individual.base import Individual
from qgene.operators.crossover import CrossoverProtocol
from qgene.operators.mutation import MutationProtocol
from qgene.score.base import ScoreProtocol
from qgene.selection.base import SelectionProtocol


class GeneticOptimiser:

    def __init__(
        self,
        p0: list[Individual],
        score_func: ScoreProtocol,
        selection_func: SelectionProtocol,
        crossover_func: CrossoverProtocol,
        mutation_func: MutationProtocol,
        callbacks: list[Callable] = [],
        verbose: int = 0,
        retention: float = 0,
    ):
        self.optimal_individual = None
        self.score = score_func
        self.pop = p0
        self.mutate = mutation_func
        self.crossover = crossover_func
        self.selection = selection_func
        self.callbacks = callbacks
        self.verbose = verbose
        self.retention = retention

    @property
    def pop(self) -> list[Individual]:
        return self._pop

    @pop.setter
    def pop(self, pop: list[Individual]) -> None:
        self.score(pop)
        self._pop = list(sorted(pop, key=lambda x: x.score, reverse=True))
        if not self.optimal_individual:
            self.optimal_individual = self.pop[0]
        else:
            if self.pop[0].score > self.optimal_individual.score:
                self.optimal_individual = self.pop[0]

    def iterate(self):
        new_pop = copy.deepcopy(self.pop[: int(len(self.pop) * self.retention)])
        new_pop += [
            self.crossover(parents)
            for parents in self.selection(self.pop, len(self.pop) - len(new_pop))
        ]
        self.pop = [self.mutate(i) for i in new_pop]
        self.score(self.pop)
        for callback in self.callbacks:
            callback(self.pop)

    def optimise(self, max_iter=100, early_stopping=False):
        iter = 1
        optimal_score = self.optimal_individual.score
        early_stopping_counter = 0
        while iter <= max_iter:
            self.iterate()
            if optimal_score <= self.optimal_individual.score:
                early_stopping_counter += 1
                if early_stopping and early_stopping_counter == 10:
                    if self.verbose == 1:
                        print("Early stopping")
                    break
            else:
                early_stopping_counter = 0
                optimal_score = self.optimal_individual.score
