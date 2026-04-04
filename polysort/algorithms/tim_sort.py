import time
from polysort.interfaces import SortProblem

MIN_RUN = 32


def tim_sort(problem: SortProblem, statistics=False):
    """
    Tim Sort — a hybrid sorting algorithm derived from merge sort and insertion
    sort. It divides the array into small "runs", sorts them with insertion sort,
    then merges them using merge sort logic.

    Type: Comparison
    Stable: Yes
    Time complexity: O(n log n) average/worst, O(n) best
    Space complexity: O(n)
    """
    data = problem.data().copy()
    comparisons = 0
    swaps = 0
    start_time = time.time()

    def insertion_sort_run(arr, left, right):
        nonlocal comparisons, swaps
        for i in range(left + 1, right + 1):
            key = arr[i]
            j = i - 1
            while j >= left:
                comparisons += 1
                if problem.comparator(arr[j], key) > 0:
                    arr[j + 1] = arr[j]
                    swaps += 1
                    j -= 1
                else:
                    break
            arr[j + 1] = key

    def merge(arr, left, mid, right):
        nonlocal comparisons, swaps
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]
        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            comparisons += 1
            if problem.comparator(left_part[i], right_part[j]) <= 0:
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                swaps += 1
                j += 1
            k += 1
        while i < len(left_part):
            arr[k] = left_part[i]
            i += 1
            k += 1
        while j < len(right_part):
            arr[k] = right_part[j]
            j += 1
            k += 1

    n = len(data)
    for i in range(0, n, MIN_RUN):
        insertion_sort_run(data, i, min(i + MIN_RUN - 1, n - 1))

    size = MIN_RUN
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(left + size - 1, n - 1)
            right = min(left + 2 * size - 1, n - 1)
            if mid < right:
                merge(data, left, mid, right)
        size *= 2

    elapsed = time.time() - start_time
    if statistics:
        return data, {"comparisons": comparisons, "swaps": swaps, "time": elapsed}
    return data
