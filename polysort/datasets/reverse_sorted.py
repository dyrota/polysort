from polysort.interfaces import SortProblem


class ReverseSorted(SortProblem):
    """A dataset in descending (reverse) order."""

    def __init__(self, size=100):
        self._data = list(range(size - 1, -1, -1))

    def data(self) -> list:
        return self._data

    def comparator(self, a, b) -> int:
        if a < b:
            return -1
        if a > b:
            return 1
        return 0
