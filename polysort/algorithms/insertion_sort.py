import time
from polysort.interfaces import SortProblem


def insertion_sort(problem: SortProblem, statistics=False, on_step=None):
    """
    Insertion Sort — builds a sorted list one element at a time by inserting each
    new element into its correct position relative to those already sorted.

    Type: Comparison
    Stable: Yes
    Time complexity: O(n^2) average/worst, O(n) best
    Space complexity: O(1)

    :param on_step: Optional callback invoked with a dict for each compare/write event, for
                    live tracing or visualization. Default is none (no-op). Uses 'write' rather
                    than 'swap' since this shifts elements one direction, not a symmetric trade.
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
            if on_step:
                on_step({'type': 'compare', 'a': {'buffer': 'main', 'index': j, 'value': data[j]}, 'b': {'buffer': 'key', 'index': i, 'value': key}, 'comparisons': comparisons, 'swaps': swaps})
            if problem.comparator(data[j], key) > 0:
                data[j + 1] = data[j]
                swaps += 1
                if on_step:
                    on_step({'type': 'write', 'target': {'buffer': 'main', 'index': j + 1}, 'value': data[j], 'source': {'buffer': 'main', 'index': j}, 'comparisons': comparisons, 'swaps': swaps})
                j -= 1
            else:
                break
        data[j + 1] = key
        if on_step:
            on_step({'type': 'write', 'target': {'buffer': 'main', 'index': j + 1}, 'value': key, 'source': None, 'comparisons': comparisons, 'swaps': swaps})

    elapsed = time.time() - start_time
    if statistics:
        return data, {"comparisons": comparisons, "swaps": swaps, "time": elapsed}
    return data
