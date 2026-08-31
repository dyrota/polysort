import time
from polysort.interfaces import SortProblem


def merge_sort(problem: SortProblem, statistics=False, on_step=None):
    """
    Merge Sort — a divide-and-conquer algorithm that splits the list in half,
    recursively sorts each half, then merges the two sorted halves.

    Type: Comparison
    Stable: Yes
    Time complexity: O(n log n) all cases
    Space complexity: O(n)

    :param on_step: Optional callback invoked with a dict for each compare/write/mark event,
                    for live tracing or visualization. Default is none (no-op). compare/write
                    events carry literal values and a 'left'/'right' buffer tag rather than just
                    indices, since left_part/right_part are ephemeral local sub-lists, not
                    positions in the main array.
    """
    data = problem.data().copy()
    comparisons = 0
    swaps = 0
    start_time = time.time()

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

    def merge_sort_recursive(arr, left, right):
        if left < right:
            mid = (left + right) // 2
            merge_sort_recursive(arr, left, mid)
            merge_sort_recursive(arr, mid + 1, right)
            merge(arr, left, mid, right)

    if data:
        merge_sort_recursive(data, 0, len(data) - 1)

    elapsed = time.time() - start_time
    if statistics:
        return data, {"comparisons": comparisons, "swaps": swaps, "time": elapsed}
    return data
