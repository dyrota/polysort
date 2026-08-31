import pytest
from polysort.algorithms import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    heap_sort,
    counting_sort,
    radix_sort,
    shell_sort,
    tim_sort,
)
from polysort.datasets import (
    RandomIntegers,
    NearlySorted,
    ReverseSorted,
    ManyDuplicates,
)

ALGORITHMS = [
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    heap_sort,
    counting_sort,
    radix_sort,
    shell_sort,
    tim_sort,
]

DATASETS = [
    RandomIntegers(size=50, seed=42),
    NearlySorted(size=50, swaps=5, seed=42),
    ReverseSorted(size=50),
    ManyDuplicates(size=50, distinct=5, seed=42),
]


@pytest.mark.parametrize("algorithm", ALGORITHMS, ids=lambda f: f.__name__)
@pytest.mark.parametrize("dataset", DATASETS, ids=lambda d: type(d).__name__)
def test_correctness(algorithm, dataset):
    result = algorithm(dataset)
    assert result == sorted(dataset.data())


@pytest.mark.parametrize("algorithm", ALGORITHMS, ids=lambda f: f.__name__)
@pytest.mark.parametrize("dataset", DATASETS, ids=lambda d: type(d).__name__)
def test_statistics_return_type(algorithm, dataset):
    result = algorithm(dataset, statistics=True)
    assert isinstance(result, tuple), "statistics=True must return a tuple"
    assert len(result) == 2
    sorted_list, stats = result
    assert isinstance(sorted_list, list)
    assert isinstance(stats, dict)
    assert "comparisons" in stats
    assert "swaps" in stats
    assert "time" in stats


@pytest.mark.parametrize("algorithm", ALGORITHMS, ids=lambda f: f.__name__)
@pytest.mark.parametrize("dataset", DATASETS, ids=lambda d: type(d).__name__)
def test_no_statistics_returns_list(algorithm, dataset):
    result = algorithm(dataset, statistics=False)
    assert isinstance(result, list)


@pytest.mark.parametrize("algorithm", ALGORITHMS, ids=lambda f: f.__name__)
@pytest.mark.parametrize("dataset", DATASETS, ids=lambda d: type(d).__name__)
def test_original_data_not_mutated(algorithm, dataset):
    original = dataset.data().copy()
    algorithm(dataset)
    assert dataset.data() == original


def test_counting_sort_raises_on_non_int():
    from polysort.interfaces import SortProblem

    class FloatProblem(SortProblem):
        def data(self):
            return [1.5, 2.3, 0.1]

        def comparator(self, a, b):
            return -1 if a < b else (1 if a > b else 0)

    with pytest.raises(TypeError):
        counting_sort(FloatProblem())


def test_radix_sort_raises_on_non_int():
    from polysort.interfaces import SortProblem

    class FloatProblem(SortProblem):
        def data(self):
            return [1.5, 2.3, 0.1]

        def comparator(self, a, b):
            return -1 if a < b else (1 if a > b else 0)

    with pytest.raises(TypeError):
        radix_sort(FloatProblem())


@pytest.mark.parametrize("algorithm", ALGORITHMS, ids=lambda f: f.__name__)
@pytest.mark.parametrize("dataset", DATASETS, ids=lambda d: type(d).__name__)
def test_on_step_is_noop_when_omitted(algorithm, dataset):
    # on_step defaults to None and must not change the sorted result or the
    # existing statistics=True counters, across every algorithm and dataset.
    # (Deliberately not comparing full stats dicts - 'time' is wall-clock and
    # will never match across two independent calls, on_step or not.)
    result_default = algorithm(dataset)
    result_explicit_none = algorithm(dataset, on_step=None)
    assert result_default == result_explicit_none == sorted(dataset.data())
    _, stats_a = algorithm(dataset, statistics=True)
    _, stats_b = algorithm(dataset, statistics=True, on_step=None)
    assert stats_a['comparisons'] == stats_b['comparisons']
    assert stats_a['swaps'] == stats_b['swaps']


def test_bubble_sort_on_step_counts_match_statistics():
    dataset = RandomIntegers(size=30, seed=7)
    events = []
    result, stats = bubble_sort(dataset, statistics=True, on_step=events.append)
    assert result == sorted(dataset.data())
    compare_events = [e for e in events if e['type'] == 'compare']
    swap_events = [e for e in events if e['type'] == 'swap']
    assert len(compare_events) == stats['comparisons']
    assert len(swap_events) == stats['swaps']
    # Running counts on the last event of each kind should match the final totals.
    assert compare_events[-1]['comparisons'] == stats['comparisons']
    assert swap_events[-1]['swaps'] == stats['swaps']


def test_insertion_sort_on_step_write_count_matches_statistics():
    # insertion_sort is a Bucket B (shift/write, not swap) algorithm - confirm the
    # 'write' vocabulary is used instead of 'swap', and that shift-writes are
    # exactly the reported swap count (the final placement write is one extra,
    # non-counted write per outer iteration).
    dataset = NearlySorted(size=30, swaps=8, seed=3)
    events = []
    result, stats = insertion_sort(dataset, statistics=True, on_step=events.append)
    assert result == sorted(dataset.data())
    assert all(e['type'] != 'swap' for e in events)
    shift_writes = [e for e in events if e['type'] == 'write' and e['source'] is not None]
    assert len(shift_writes) == stats['swaps']


def test_counting_sort_on_step_never_emits_compare():
    dataset = RandomIntegers(size=30, seed=11)
    events = []
    counting_sort(dataset, on_step=events.append)
    assert all(e['type'] != 'compare' for e in events)
    assert any(e['type'] == 'write' for e in events)


def test_radix_sort_on_step_emits_digit_pass_marks():
    dataset = RandomIntegers(size=30, seed=11)
    events = []
    radix_sort(dataset, on_step=events.append)
    digit_pass_marks = [e for e in events if e['type'] == 'mark' and e['kind'] == 'digit-pass']
    assert len(digit_pass_marks) > 0
    assert all(e['phase'] == 'non_negatives' for e in digit_pass_marks)  # no dataset produces negatives


# --- non-comparison sorts must not silently ignore the comparator -----------

from polysort.interfaces import SortProblem

NON_COMPARISON = [counting_sort, radix_sort]
COMPARISON = [bubble_sort, selection_sort, insertion_sort, merge_sort,
              quick_sort, heap_sort, shell_sort, tim_sort]


class _DescendingProblem(SortProblem):
    def __init__(self, values=(5, 3, 8, 1, 9, 2)):
        self._values = list(values)

    def data(self):
        return list(self._values)

    def comparator(self, a, b):
        return (a < b) - (a > b)


class _AscendingProblem(SortProblem):
    def __init__(self, values=(5, 3, 8, 1, 9, 2)):
        self._values = list(values)

    def data(self):
        return list(self._values)

    def comparator(self, a, b):
        return (a > b) - (a < b)


@pytest.mark.parametrize("algorithm", NON_COMPARISON)
def test_non_comparison_sort_refuses_a_comparator_it_cannot_honor(algorithm):
    # These order by value and never consult comparator(), so a descending
    # comparator previously produced a correctly-ASCENDING list -- the right
    # answer to a question nobody asked, with nothing to signal it.
    with pytest.raises(TypeError) as excinfo:
        algorithm(_DescendingProblem())
    assert "non-comparison" in str(excinfo.value)


@pytest.mark.parametrize("algorithm", NON_COMPARISON)
def test_non_comparison_sort_error_points_at_a_usable_alternative(algorithm):
    with pytest.raises(TypeError) as excinfo:
        algorithm(_DescendingProblem())
    assert "merge_sort" in str(excinfo.value)


@pytest.mark.parametrize("algorithm", NON_COMPARISON)
def test_non_comparison_sort_still_accepts_an_ascending_comparator(algorithm):
    assert algorithm(_AscendingProblem()) == [1, 2, 3, 5, 8, 9]


@pytest.mark.parametrize("algorithm", NON_COMPARISON)
def test_non_comparison_validation_does_not_inflate_comparisons(algorithm):
    # Counting sort performing zero comparisons WHILE SORTING is the point of
    # it; the guard checks the result afterwards and must not be counted.
    _, stats = algorithm(_AscendingProblem(), statistics=True)
    assert stats["comparisons"] == 0


@pytest.mark.parametrize("algorithm", COMPARISON)
def test_comparison_sorts_do_honor_a_descending_comparator(algorithm):
    # The other eight are comparison-based and must genuinely sort descending.
    assert algorithm(_DescendingProblem()) == [9, 8, 5, 3, 2, 1]


# --- documented stability must match actual behavior ------------------------

# Comparator inspects only the first element, so a stable sort has to preserve
# the original order of the tags among equal keys.
_STABILITY_PAIRS = [(3, "a"), (1, "b"), (3, "c"), (1, "d"), (2, "e"), (3, "f"), (1, "g"), (2, "h")]


class _PairProblem(SortProblem):
    def data(self):
        return list(_STABILITY_PAIRS)

    def comparator(self, a, b):
        return (a[0] > b[0]) - (a[0] < b[0])


@pytest.mark.parametrize("algorithm", COMPARISON)
def test_stability_matches_the_documented_claim(algorithm):
    claims_stable = "Stable: Yes" in (algorithm.__doc__ or "")
    result = algorithm(_PairProblem())
    # Python's own sort is stable, so this is the reference ordering.
    is_stable = result == sorted(_STABILITY_PAIRS, key=lambda pair: pair[0])
    assert is_stable == claims_stable, (
        f"{algorithm.__name__} documents 'Stable: {'Yes' if claims_stable else 'No'}' "
        f"but behaves {'stably' if is_stable else 'unstably'}"
    )
