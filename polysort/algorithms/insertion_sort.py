import time
from polysort.interfaces import SortProblem


def insertion_sort(problem: SortProblem, statistics=False):
    """
    Insertion Sort — builds a sorted list one element at a time by inserting each
    new element into its correct position relative to those already sorted.

    Type: Comparison
    Stable: Yes
    Time complexity: O(n^2) average/worst, O(n) best
    Space complexity: O(1)
    """
    data = problem.data().copy()
    comparisons = 0
    swaps = 0
    start_time = time.time()

    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if problem.comparator(data[j], key) > 0:
                data[j + 1] = data[j]
                swaps += 1
                j -= 1
            else:
                break
        data[j + 1] = key

    elapsed = time.time() - start_time
    if statistics:
        return data, {"comparisons": comparisons, "swaps": swaps, "time": elapsed}
    return data
