"""Shared guard for the two algorithms that are not comparison-based.

counting_sort and radix_sort accept a SortProblem but can only ever honor half
of its contract. They order elements by their VALUE -- by counting occurrences,
or by digit -- and never consult problem.comparator() at all, because there is
nothing in their design that could. That is a genuine property of
non-comparison sorting, not a gap in these implementations.

The failure mode is silence: hand either of them a descending comparator and it
returns a correctly ascending list, which is the wrong answer to the question
that was asked, with nothing to indicate anything went wrong. A caller that then
checks its own result -- `all(comparator(out[i], out[i+1]) <= 0)`, the obvious
way to verify a sort -- sees an unsorted list and blames the comparator.

So the result is checked against the comparator that was actually supplied, and
a mismatch raises. This is the same bargain the existing integer-only guard in
both files already strikes: refuse clearly rather than return something
plausible and wrong.
"""


def assert_comparator_is_ascending(problem, data, algorithm_name):
    """Raise if `data` (sorted ascending by value) contradicts the problem's comparator.

    The comparisons made here deliberately do not count toward the algorithm's
    reported `comparisons` statistic: this is validation of the result, not part
    of the sort, and counting sort performing zero comparisons while sorting is
    the whole point of it.
    """
    for i in range(len(data) - 1):
        if problem.comparator(data[i], data[i + 1]) > 0:
            raise TypeError(
                f"{algorithm_name} is a non-comparison sort: it orders elements by value and "
                f"cannot honor a custom comparator. The supplied comparator disagrees with the "
                f"ascending order it produces (at index {i}: {data[i]!r} before {data[i + 1]!r}). "
                f"Use a comparison-based algorithm such as merge_sort or quick_sort instead."
            )
