import random
from polysort.interfaces import SortProblem


class NearlySorted(SortProblem):
    """A dataset that is sorted except for a few random swaps."""

    def __init__(self, size=100, swaps=5, seed=None):
        rng = random.Random(seed)
        self._data = list(range(size))
        for _ in range(swaps):
            i, j = rng.randrange(size), rng.randrange(size)
            self._data[i], self._data[j] = self._data[j], self._data[i]

    def data(self) -> list:
        return self._data

    def comparator(self, a, b) -> int:
        if a < b:
            return -1
        if a > b:
            return 1
        return 0
