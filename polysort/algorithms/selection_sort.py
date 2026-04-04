import time
from polysort.interfaces import SortProblem


def selection_sort(problem: SortProblem, statistics=False):
    """
    Selection Sort — divides the list into a sorted and unsorted region. On each
    pass it selects the minimum element from the unsorted region and moves it to
    the end of the sorted region.

    Type: Comparison
    Stable: No
    Time complexity: O(n^2) all cases
    Space complexity: O(1)
    """
    data = problem.data().copy()
    comparisons = 0
    swaps = 0
    start_time = time.time()

    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if problem.comparator(data[j], data[min_idx]) < 0:
                min_idx = j
        if min_idx != i:
            data[i], data[min_idx] = data[min_idx], data[i]
            swaps += 1

    elapsed = time.time() - start_time
    if statistics:
        return data, {"comparisons": comparisons, "swaps": swaps, "time": elapsed}
    return data
