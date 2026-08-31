import time
from polysort.interfaces import SortProblem


def radix_sort(problem: SortProblem, statistics=False, on_step=None):
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

    :param on_step: Optional callback invoked with a dict for each write/mark event, for live
                    tracing or visualization. Default is none (no-op). The negative-number
                    branch is instrumented the same generic way as the non-negative branch
                    (via the shared counting_sort_by_digit helper), but none of the four
                    built-in datasets ever produce negative values, so that branch is dead
                    code in practice - no special-cased instrumentation was built for it.
    """
    data = problem.data().copy()
    comparisons = 0
    swaps = 0
    start_time = time.time()

    if data and not all(isinstance(x, int) for x in data):
        raise TypeError("radix_sort requires integer data.")

    def counting_sort_by_digit(arr, exp, buffer_name):
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
            if on_step:
                on_step({'type': 'write', 'target': {'buffer': 'output', 'index': count[index] - 1}, 'value': arr[i], 'source': {'buffer': buffer_name, 'index': i}, 'comparisons': comparisons, 'swaps': swaps})
            count[index] -= 1

        for i in range(n):
            arr[i] = output[i]
            if on_step:
                on_step({'type': 'write', 'target': {'buffer': buffer_name, 'index': i}, 'value': output[i], 'source': {'buffer': 'output', 'index': i}, 'comparisons': comparisons, 'swaps': swaps})

    if data:
        # Handle negative numbers by splitting, sorting, and merging
        negatives = [-x for x in data if x < 0]
        non_negatives = [x for x in data if x >= 0]

        if negatives:
            max_neg = max(negatives)
            exp = 1
            while max_neg // exp > 0:
                if on_step:
                    on_step({'type': 'mark', 'kind': 'digit-pass', 'exp': exp, 'phase': 'negatives'})
                counting_sort_by_digit(negatives, exp, 'negatives')
                exp *= 10
            negatives = [-x for x in reversed(negatives)]

        if non_negatives:
            max_val = max(non_negatives)
            exp = 1
            while max_val // exp > 0:
                if on_step:
                    on_step({'type': 'mark', 'kind': 'digit-pass', 'exp': exp, 'phase': 'non_negatives'})
                counting_sort_by_digit(non_negatives, exp, 'non_negatives')
                exp *= 10

        data[:] = negatives + non_negatives

    elapsed = time.time() - start_time
    if statistics:
        return data, {"comparisons": comparisons, "swaps": swaps, "time": elapsed}
    return data
