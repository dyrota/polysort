import time
from polysort.interfaces import SortProblem


def bubble_sort(problem: SortProblem, statistics=False):
    """
    Bubble Sort — repeatedly steps through the list, compares adjacent elements,
    and swaps them if they are in the wrong order. The pass is repeated until
    no swaps are needed.

    Type: Comparison
    Stable: Yes
    Time complexity: O(n^2) average/worst, O(n) best
    Space complexity: O(1)
    """
    data = problem.data().copy()
    comparisons = 0
    swaps = 0
    start_time = time.time()

    n = len(data)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if problem.comparator(data[j], data[j + 1]) > 0:
                data[j], data[j + 1] = data[j + 1], data[j]
                swaps += 1
                swapped = True
        if not swapped:
            break

    elapsed = time.time() - start_time
    if statistics:
        return data, {"comparisons": comparisons, "swaps": swaps, "time": elapsed}
    return data
