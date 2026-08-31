import time
from polysort.interfaces import SortProblem

MIN_RUN = 32


def tim_sort(problem: SortProblem, statistics=False, on_step=None):
    """
    Tim Sort — a hybrid sorting algorithm derived from merge sort and insertion
    sort. It divides the array into small "runs", sorts them with insertion sort,
    then merges them using merge sort logic.

    Type: Comparison
    Stable: Yes
    Time complexity: O(n log n) average/worst, O(n) best
    Space complexity: O(n)

    :param on_step: Optional callback invoked with a dict for each compare/write/mark event,
                    for live tracing or visualization. Default is none (no-op). Uses the same
                    event vocabulary as insertion_sort (for the run phase) and merge_sort (for
                    the merge phase), plus a 'merge-pass' mark for the doubling merge width,
                    which is tim_sort's defining visual beyond plain merge_sort.
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
                if on_step:
                    on_step({'type': 'compare', 'a': {'buffer': 'main', 'index': j, 'value': arr[j]}, 'b': {'buffer': 'key', 'index': i, 'value': key}, 'comparisons': comparisons, 'swaps': swaps})
                if problem.comparator(arr[j], key) > 0:
                    arr[j + 1] = arr[j]
                    swaps += 1
                    if on_step:
                        on_step({'type': 'write', 'target': {'buffer': 'main', 'index': j + 1}, 'value': arr[j], 'source': {'buffer': 'main', 'index': j}, 'comparisons': comparisons, 'swaps': swaps})
                    j -= 1
                else:
                    break
            arr[j + 1] = key
            if on_step:
                on_step({'type': 'write', 'target': {'buffer': 'main', 'index': j + 1}, 'value': key, 'source': None, 'comparisons': comparisons, 'swaps': swaps})

    def merge(arr, left, mid, right):
        nonlocal comparisons, swaps
        left_part = arr[left:mid + 1]
        right_part = arr[mid + 1:right + 1]
        if on_step:
            on_step({'type': 'mark', 'kind': 'merge-range', 'left': left, 'mid': mid, 'right': right})
        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            comparisons += 1
            if on_step:
                on_step({'type': 'compare', 'a': {'buffer': 'left', 'index': i, 'value': left_part[i]}, 'b': {'buffer': 'right', 'index': j, 'value': right_part[j]}, 'comparisons': comparisons, 'swaps': swaps})
            if problem.comparator(left_part[i], right_part[j]) <= 0:
                arr[k] = left_part[i]
                if on_step:
                    on_step({'type': 'write', 'target': {'buffer': 'main', 'index': k}, 'value': left_part[i], 'source': {'buffer': 'left', 'index': i}, 'comparisons': comparisons, 'swaps': swaps})
                i += 1
            else:
                arr[k] = right_part[j]
                swaps += 1
                if on_step:
                    on_step({'type': 'write', 'target': {'buffer': 'main', 'index': k}, 'value': right_part[j], 'source': {'buffer': 'right', 'index': j}, 'comparisons': comparisons, 'swaps': swaps})
                j += 1
            k += 1
        while i < len(left_part):
            arr[k] = left_part[i]
            if on_step:
                on_step({'type': 'write', 'target': {'buffer': 'main', 'index': k}, 'value': left_part[i], 'source': {'buffer': 'left', 'index': i}, 'comparisons': comparisons, 'swaps': swaps})
            i += 1
            k += 1
        while j < len(right_part):
            arr[k] = right_part[j]
            if on_step:
                on_step({'type': 'write', 'target': {'buffer': 'main', 'index': k}, 'value': right_part[j], 'source': {'buffer': 'right', 'index': j}, 'comparisons': comparisons, 'swaps': swaps})
            j += 1
            k += 1

    n = len(data)
    for i in range(0, n, MIN_RUN):
        run_left, run_right = i, min(i + MIN_RUN - 1, n - 1)
        if on_step:
            on_step({'type': 'mark', 'kind': 'run-boundary', 'left': run_left, 'right': run_right})
        insertion_sort_run(data, run_left, run_right)

    size = MIN_RUN
    while size < n:
        if on_step:
            on_step({'type': 'mark', 'kind': 'merge-pass', 'size': size})
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
