import random
from polysort.interfaces import SortProblem


class ManyDuplicates(SortProblem):
    """A dataset with few unique values and many repeated elements."""

    def __init__(self, size=100, distinct=5, seed=None):
        rng = random.Random(seed)
        pool = list(range(distinct))
        self._data = [rng.choice(pool) for _ in range(size)]

    def data(self) -> list:
        return self._data

    def comparator(self, a, b) -> int:
        if a < b:
            return -1
        if a > b:
            return 1
        return 0
