# Polysort

A collection of sorting algorithms with a consistent `SortProblem` interface. Sibling library to [polysearch](https://github.com/dyrota/polysearch).

## Installation

```
pip install polysort
```

Install the latest version directly from GitHub:

```
pip install git+https://github.com/dyrota/polysort@main
```

## Quick Usage

```python
from polysort.algorithms import merge_sort
from polysort.datasets import RandomIntegers

problem = RandomIntegers(size=100, seed=42)

# Sort and get statistics
sorted_list, stats = merge_sort(problem, statistics=True)
print(sorted_list)
print(stats)  # {'comparisons': 536, 'swaps': 175, 'time': 0.00012}

# Sort without statistics
sorted_list = merge_sort(problem)
```

## Algorithms

| Algorithm       | Type            | Stable | Avg Complexity  |
|-----------------|-----------------|--------|-----------------|
| bubble_sort     | Comparison      | Yes    | O(n²)           |
| selection_sort  | Comparison      | No     | O(n²)           |
| insertion_sort  | Comparison      | Yes    | O(n²)           |
| merge_sort      | Comparison      | Yes    | O(n log n)      |
| quick_sort      | Comparison      | No     | O(n log n)      |
| heap_sort       | Comparison      | No     | O(n log n)      |
| counting_sort   | Non-comparison* | Yes    | O(n + k)        |
| radix_sort      | Non-comparison* | Yes    | O(n · d)        |
| shell_sort      | Comparison      | No     | O(n log² n)     |
| tim_sort        | Comparison      | Yes    | O(n log n)      |

\* Integer data only. `counting_sort` and `radix_sort` raise `TypeError` for non-integer inputs.

## Datasets

Four built-in datasets implement `SortProblem` for quick benchmarking:

| Class            | Description                                   |
|------------------|-----------------------------------------------|
| `RandomIntegers` | Random integers (`size`, `seed`)              |
| `NearlySorted`   | Sorted with a few random swaps (`size`, `swaps`, `seed`) |
| `ReverseSorted`  | Descending order (`size`)                     |
| `ManyDuplicates` | Few unique values repeated many times (`size`, `distinct`, `seed`) |

## Implementing Your Own SortProblem

Subclass `SortProblem` and implement two methods:

```python
from polysort.interfaces import SortProblem

class MyProblem(SortProblem):
    def data(self) -> list:
        return ["banana", "apple", "cherry"]

    def comparator(self, a, b) -> int:
        if a < b:
            return -1
        if a > b:
            return 1
        return 0

from polysort.algorithms import merge_sort

problem = MyProblem()
result = merge_sort(problem)
print(result)  # ['apple', 'banana', 'cherry']
```

- `data()` — returns the list to be sorted (algorithms copy this; originals are never mutated)
- `comparator(a, b)` — returns `-1`, `0`, or `1`; all comparison-based algorithms use this exclusively

## Running the Demo

```
python testing.py
```

Prints a table of all 10 algorithms × 4 datasets with comparison counts, swap counts, and elapsed time.

## Structure

```
polysort/
├── polysort/
│   ├── interfaces/       # SortProblem ABC
│   ├── algorithms/       # 10 sorting algorithm implementations
│   ├── datasets/         # 4 built-in SortProblem implementations
│   └── data_structures/  # supporting data structures
├── tests/
│   └── test_algorithms.py
├── testing.py
└── setup.py
```
