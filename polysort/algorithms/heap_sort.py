import time
from polysort.interfaces import SortProblem


def heap_sort(problem: SortProblem, statistics=False, on_step=None):
    """
    Heap Sort — builds a max-heap from the list, then repeatedly extracts the
    maximum element to produce a sorted list.

    Type: Comparison
    Stable: No
    Time complexity: O(n log n) all cases
    Space complexity: O(1)

    :param on_step: Optional callback invoked with a dict for each compare/swap event,
                    for live tracing or visualization. Default is none (no-op). Since array
                    index i's children are always 2i+1/2i+2, the same events can drive either
                    a flat bar-array view or a binary-tree view.
    """
    data = problem.data().copy()
    comparisons = 0
    swaps = 0
    start_time = time.time()

    def heapify(arr, n, i):
        nonlocal comparisons, swaps
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n:
            comparisons += 1
            if on_step:
                on_step({'type': 'compare', 'a': {'buffer': 'main', 'index': left, 'value': arr[left]}, 'b': {'buffer': 'main', 'index': largest, 'value': arr[largest]}, 'comparisons': comparisons, 'swaps': swaps})
            if problem.comparator(arr[left], arr[largest]) > 0:
                largest = left

        if right < n:
            comparisons += 1
            if on_step:
                on_step({'type': 'compare', 'a': {'buffer': 'main', 'index': right, 'value': arr[right]}, 'b': {'buffer': 'main', 'index': largest, 'value': arr[largest]}, 'comparisons': comparisons, 'swaps': swaps})
            if problem.comparator(arr[right], arr[largest]) > 0:
                largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            swaps += 1
            if on_step:
                on_step({'type': 'swap', 'a': {'buffer': 'main', 'index': i}, 'b': {'buffer': 'main', 'index': largest}, 'comparisons': comparisons, 'swaps': swaps})
            heapify(arr, n, largest)

    n = len(data)
    for i in range(n // 2 - 1, -1, -1):
        heapify(data, n, i)

    for i in range(n - 1, 0, -1):
        data[0], data[i] = data[i], data[0]
        swaps += 1
        if on_step:
            on_step({'type': 'swap', 'a': {'buffer': 'main', 'index': 0}, 'b': {'buffer': 'main', 'index': i}, 'comparisons': comparisons, 'swaps': swaps})
        heapify(data, i, 0)

    elapsed = time.time() - start_time
    if statistics:
        return data, {"comparisons": comparisons, "swaps": swaps, "time": elapsed}
    return data
