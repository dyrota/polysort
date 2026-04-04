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

algorithms = [
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

datasets = [
    ("random_integers", RandomIntegers(size=100, seed=0)),
    ("nearly_sorted", NearlySorted(size=100, swaps=5, seed=0)),
    ("reverse_sorted", ReverseSorted(size=100)),
    ("many_duplicates", ManyDuplicates(size=100, distinct=5, seed=0)),
]

header = f"{'Algorithm':<20} | {'Dataset':<20} | {'Comparisons':>11} | {'Swaps':>8} | {'Time (ms)':>10}"
separator = "-" * len(header)

print(header)
print(separator)

for algorithm in algorithms:
    for dataset_name, dataset in datasets:
        _, stats = algorithm(dataset, statistics=True)
        comparisons = stats["comparisons"]
        swaps = stats["swaps"]
        time_ms = stats["time"] * 1000
        print(
            f"{algorithm.__name__:<20} | {dataset_name:<20} | {comparisons:>11} | {swaps:>8} | {time_ms:>10.2f}"
        )
