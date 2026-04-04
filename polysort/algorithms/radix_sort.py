import time
from polysort.interfaces import SortProblem


def radix_sort(problem: SortProblem, statistics=False):
    """
    Radix Sort — a non-comparison integer sorting algorithm that sorts digit by
    digit from least significant to most significant using counting sort as a
    subroutine.

    Type: Non-comparison (integer only)
    Stable: Yes
    Time complexity: O(n * d) where d is the number of digits
    Space complexity: O(n + k)

    Note: Only works with non-negative integer data. Raises TypeError for
    non-integer inputs.
    """
    data = problem.data().copy()
    comparisons = 0
    swaps = 0
    start_time = time.time()

    if data and not all(isinstance(x, int) for x in data):
        raise TypeError("radix_sort requires integer data.")

    def counting_sort_by_digit(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for val in arr:
            index = (val // exp) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1

        for i in range(n):
            arr[i] = output[i]

    if data:
        # Handle negative numbers by splitting, sorting, and merging
        negatives = [-x for x in data if x < 0]
        non_negatives = [x for x in data if x >= 0]

        if negatives:
            max_neg = max(negatives)
            exp = 1
            while max_neg // exp > 0:
                counting_sort_by_digit(negatives, exp)
                exp *= 10
            negatives = [-x for x in reversed(negatives)]

        if non_negatives:
            max_val = max(non_negatives)
            exp = 1
            while max_val // exp > 0:
                counting_sort_by_digit(non_negatives, exp)
                exp *= 10

        data[:] = negatives + non_negatives

    elapsed = time.time() - start_time
    if statistics:
        return data, {"comparisons": comparisons, "swaps": swaps, "time": elapsed}
    return data
