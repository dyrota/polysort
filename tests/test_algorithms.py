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
