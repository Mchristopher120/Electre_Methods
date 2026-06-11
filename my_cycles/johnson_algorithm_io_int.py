"""Johnson cycle elimination returning numeric matrix."""

from __future__ import annotations

import numpy as np

from my_cycles.johnson_algorithm_elementary_cycles_search import JohnsonAlgorithm_ElementaryCyclesSearch


class JohnsonAlgorithm_io_int:
    @staticmethod
    def cyclesElimination(
        array: np.ndarray,
        p: int,
        maximum_cycles: int = 15,
    ) -> np.ndarray:
        k = 0
        result = np.array(array, dtype=np.float64, copy=True)
        array_boolean: list[list[bool]] = [
            [result[i, j] == p for j in range(result.shape[1])]
            for i in range(result.shape[0])
        ]

        nodes = [f"a{i + 1}" for i in range(result.shape[1])]
        ecs = JohnsonAlgorithm_ElementaryCyclesSearch(array_boolean, nodes, maximum_cycles)
        cycles = ecs.getElementaryCycles()

        if len(cycles) != 0:
            cycle_pairs: list[list[str]] = [
                [""] * (result.shape[1] + 1) for _ in range(len(cycles))
            ]

            for i, cycle in enumerate(cycles):
                for j, node in enumerate(cycle):
                    i_node = cycle[0]
                    cycle_pairs[i][j] = str(node)
                    if j == len(cycle) - 1:
                        cycle_pairs[i][j + 1] = str(i_node)

            for i in range(len(cycle_pairs)):
                for j in range(len(cycle_pairs[0])):
                    if cycle_pairs[i][j] is None:
                        cycle_pairs[i][j] = ""
                    cycle_pairs[i][j] = cycle_pairs[i][j].replace("a", "")

            cycle_pairs_value = np.zeros((len(cycle_pairs), len(cycle_pairs[0])), dtype=np.float64)
            for i in range(len(cycle_pairs)):
                for j in range(len(cycle_pairs[0])):
                    try:
                        float(cycle_pairs[i][j])
                    except ValueError:
                        cycle_pairs[i][j] = "0.5"
                    cycle_pairs_value[i, j] = float(cycle_pairs[i][j])

            element_count = int(np.sum(cycle_pairs_value == 0.5))
            totalpairs = (
                cycle_pairs_value.shape[0] * cycle_pairs_value.shape[1]
                - cycle_pairs_value.shape[0]
                - element_count
            )

            counter = np.zeros(cycle_pairs_value.shape[0], dtype=np.float64)
            for i in range(cycle_pairs_value.shape[0]):
                for j in range(cycle_pairs_value.shape[1]):
                    if cycle_pairs_value[i, j] != 0.5:
                        counter[i] = 1 + counter[i]

            pairs = np.zeros((int(totalpairs), 2), dtype=np.float64)
            for i in range(cycle_pairs_value.shape[0]):
                for j in range(int(counter[i]) - 1):
                    if cycle_pairs_value[i, j] != 0.5:
                        pairs[k, 0] = cycle_pairs_value[i, j]
                        pairs[k, 1] = cycle_pairs_value[i, j + 1]
                        k += 1

            for i in range(pairs.shape[0]):
                for m in range(result.shape[0]):
                    for n in range(result.shape[1]):
                        if m == int(pairs[i, 0]) - 1 and n == int(pairs[i, 1]) - 1:
                            result[m, n] = 0.0
        return result
