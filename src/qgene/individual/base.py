from dataclasses import dataclass


@dataclass
class Individual:
    genome: tuple
    score: float | None = None

    @property
    def n_genes(self) -> int:
        return len(self.genome)

    def __hash__(self):
        return hash(self.genome)

    def __eq__(self, value: object) -> bool:
        if value.genome == self.genome:
            return True
        return False
