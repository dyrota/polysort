import time
from polysort.interfaces import SortProblem


def shell_sort(problem: SortProblem, statistics=False, on_step=None):
    """
    Shell Sort — a generalization of insertion sort that allows the exchange of
    elements that are far apart. Uses Knuth's gap sequence (3^k - 1) / 2.

    Type: Comparison
    Stable: No
    Time complexity: O(n log^2 n) average (gap-dependent), O(n^2) worst
    Space complexity: O(1)

    :param on_step: Optional callback invoked with a dict for each compare/write/mark event,
                    for live tracing or visualization. Default is none (no-op).
    """
    data = problem.data().copy()
    comparisons = 0
    swaps = 0
    start_time = time.time()

    n = len(data)
    gap = 1
    while gap < n // 3:
        gap = gap * 3 + 1

    while gap >= 1:
        if on_step:
            on_step({'type': 'mark', 'kind': 'gap-change', 'gap': gap})
        for i in range(gap, n):
            key = data[i]
            j = i
            while j >= gap:
                comparisons += 1
                if on_step:
                    on_step({'type': 'compare', 'a': {'buffer': 'main', 'index': j - gap, 'value': data[j - gap]}, 'b': {'buffer': 'key', 'index': i, 'value': key}, 'comparisons': comparisons, 'swaps': swaps})
                if problem.comparator(data[j - gap], key) > 0:
                    data[j] = data[j - gap]
                    swaps += 1
                    if on_step:
                        on_step({'type': 'write', 'target': {'buffer': 'main', 'index': j}, 'value': data[j - gap], 'source': {'buffer': 'main', 'index': j - gap}, 'comparisons': comparisons, 'swaps': swaps})
                    j -= gap
                else:
                    break
            data[j] = key
            if on_step:
                on_step({'type': 'write', 'target': {'buffer': 'main', 'index': j}, 'value': key, 'source': None, 'comparisons': comparisons, 'swaps': swaps})
        gap //= 3

    elapsed = time.time() - start_time
    if statistics:
        return data, {"comparisons": comparisons, "swaps": swaps, "time": elapsed}
    return data
