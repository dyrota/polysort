import random
from polysort.interfaces import SortProblem


class RandomIntegers(SortProblem):
    """A dataset of random integers."""

    def __init__(self, size=100, seed=None):
        rng = random.Random(seed)
        self._data = [rng.randint(0, size * 10) for _ in range(size)]

    def data(self) -> list:
        return self._data

    def comparator(self, a, b) -> int:
        if a < b:
            return -1
        if a > b:
            return 1
        return 0
