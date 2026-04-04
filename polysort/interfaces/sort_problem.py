from abc import ABC, abstractmethod


class SortProblem(ABC):
    @abstractmethod
    def data(self) -> list:
        """Return the list to be sorted."""
        pass

    @abstractmethod
    def comparator(self, a, b) -> int:
        """Compare two elements. Return -1, 0, or 1."""
        pass
