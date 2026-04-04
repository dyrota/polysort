import time
from polysort.interfaces import SortProblem


def quick_sort(problem: SortProblem, statistics=False):
    """
    Quick Sort — selects a pivot element and partitions the list into elements
    less than and greater than the pivot, then recursively sorts each partition.
    Uses the last element as the pivot.

    Type: Comparison
    Stable: No
    Time complexity: O(n log n) average, O(n^2) worst
    Space complexity: O(log n) average (stack)
    """
    data = problem.data().copy()
    comparisons = 0
    swaps = 0
    start_time = time.time()

    def partition(arr, low, high):
        nonlocal comparisons, swaps
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            comparisons += 1
            if problem.comparator(arr[j], pivot) <= 0:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                swaps += 1
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        swaps += 1
        return i + 1

    def quick_sort_recursive(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort_recursive(arr, low, pi - 1)
            quick_sort_recursive(arr, pi + 1, high)

    if data:
        quick_sort_recursive(data, 0, len(data) - 1)

    elapsed = time.time() - start_time
    if statistics:
        return data, {"comparisons": comparisons, "swaps": swaps, "time": elapsed}
    return data
