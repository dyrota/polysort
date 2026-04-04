import time
from polysort.interfaces import SortProblem


def heap_sort(problem: SortProblem, statistics=False):
    """
    Heap Sort — builds a max-heap from the list, then repeatedly extracts the
    maximum element to produce a sorted list.

    Type: Comparison
    Stable: No
    Time complexity: O(n log n) all cases
    Space complexity: O(1)
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
            if problem.comparator(arr[left], arr[largest]) > 0:
                largest = left

        if right < n:
            comparisons += 1
            if problem.comparator(arr[right], arr[largest]) > 0:
                largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            swaps += 1
            heapify(arr, n, largest)

    n = len(data)
    for i in range(n // 2 - 1, -1, -1):
        heapify(data, n, i)

    for i in range(n - 1, 0, -1):
        data[0], data[i] = data[i], data[0]
        swaps += 1
        heapify(data, i, 0)

    elapsed = time.time() - start_time
    if statistics:
        return data, {"comparisons": comparisons, "swaps": swaps, "time": elapsed}
    return data
