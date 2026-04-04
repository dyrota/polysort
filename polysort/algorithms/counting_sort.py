import time
from polysort.interfaces import SortProblem


def counting_sort(problem: SortProblem, statistics=False):
    """
    Counting Sort — a non-comparison integer sorting algorithm. Counts the
    occurrences of each value, then reconstructs the sorted list from those
    counts.

    Type: Non-comparison (integer only)
    Stable: Yes
    Time complexity: O(n + k) where k is the range of values
    Space complexity: O(k)

    Note: Only works with integer data. Raises TypeError for non-integer inputs.
    """
    data = problem.data().copy()
    comparisons = 0
    swaps = 0
    start_time = time.time()

    if data and not all(isinstance(x, int) for x in data):
        raise TypeError("counting_sort requires integer data.")

    if data:
        min_val = min(data)
        max_val = max(data)
        count_len = max_val - min_val + 1
        count = [0] * count_len

        for val in data:
            count[val - min_val] += 1

        idx = 0
        for i, c in enumerate(count):
            for _ in range(c):
                data[idx] = i + min_val
                idx += 1

    elapsed = time.time() - start_time
    if statistics:
        return data, {"comparisons": comparisons, "swaps": swaps, "time": elapsed}
    return data
