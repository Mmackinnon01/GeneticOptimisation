import copy
from typing import Callable

import numpy as np
from tqdm.auto import tqdm

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
            self.mutate(self.crossover(parents))
            for parents in self.selection(self.pop, len(self.pop) - len(new_pop))
        ]
        self.pop = new_pop
        self.score(self.pop)
        for callback in self.callbacks:
            callback(self.pop)

    def optimise(self, max_iter=100, early_stopping=False):
        optimal_score = self.optimal_individual.score
        early_stopping_counter = 0
        iters = range(max_iter)
        if self.verbose == 1:
            iters = tqdm(iters)
            self.annotatePBar(iters)
        for iteration in iters:
            self.iterate()
            if self.verbose == 1:
                self.annotatePBar(iters)
            if optimal_score >= self.optimal_individual.score:
                early_stopping_counter += 1
                if early_stopping and early_stopping_counter == 10:
                    if self.verbose == 1:
                        print("Early stopping")
                    break
            else:
                early_stopping_counter = 0
                optimal_score = self.optimal_individual.score

    def annotatePBar(self, pbar: tqdm) -> None:
        fitnesses = np.array([ind.score for ind in self.pop])
        best = self.optimal_individual.score
        mean = np.mean(fitnesses)

        genomes = np.array([ind.genome for ind in self.pop])
        diversity = np.mean(np.std(genomes, axis=0))
        pbar.set_description(
                f"Best: {best:.4f} | Mean: {mean:.4f} | Div: {diversity:.4f}"
            )