"""Johnson cycle elimination returning string matrix."""

from __future__ import annotations

import numpy as np

from my_cycles.johnson_algorithm_elementary_cycles_search import JohnsonAlgorithm_ElementaryCyclesSearch


def _get2d_remove_column_string(array1: list[list[str]], column: int) -> list[list[str]]:
    array_rd: list[list[str]] = [
        [""] * (len(array1[0]) - 1) for _ in range(len(array1))
    ]
    p = 0
    for i in range(len(array1)):
        q = 0
        for j in range(len(array1[0])):
            if j == column:
                continue
            array_rd[p][q] = array1[i][j]
            q += 1
        p += 1
    return array_rd


def _get2d_remove_row_string(array1: list[list[str]], row: int) -> list[list[str]]:
    array_rd: list[list[str]] = [
        [""] * len(array1[0]) for _ in range(len(array1) - 1)
    ]
    p = 0
    for i in range(len(array1)):
        if i == row:
            continue
        q = 0
        for j in range(len(array1[0])):
            array_rd[p][q] = array1[i][j]
            q += 1
        p += 1
    return array_rd


class JohnsonAlgorithm_io_str:
    @staticmethod
    def cyclesElimination(
        array: np.ndarray,
        p: int,
        maximum_cycles: int = 15,
    ) -> np.ndarray:
        result = np.array(array, dtype=np.float64, copy=True)
        array_boolean: list[list[bool]] = [
            [result[i, j] == p for j in range(result.shape[1])]
            for i in range(result.shape[0])
        ]

        nodes = [f"a{i + 1}" for i in range(result.shape[1])]
        ecs = JohnsonAlgorithm_ElementaryCyclesSearch(array_boolean, nodes, maximum_cycles)
        cycles = ecs.getElementaryCycles()

        array_cycle: list[list[str]] = [
            [""] * 1000 for _ in range(maximum_cycles + 1)
        ]
        array_solution: list[list[str]] = [
            [""] * 1000 for _ in range(maximum_cycles + 1)
        ]

        if len(cycles) != 0:
            for i, cycle in enumerate(cycles):
                for j, node in enumerate(cycle):
                    i_node = cycle[0]
                    node_str = str(node)
                    i_node_str = str(i_node)
                    if j < len(cycle) - 1:
                        array_cycle[i][j] = node_str
                    else:
                        array_cycle[i][j] = node_str
                        array_cycle[i][j + 1] = i_node_str

            for i in range(len(array_cycle) - 1, 0, -1):
                if array_cycle[i][0] is None or array_cycle[i][0] == "":
                    array_cycle = _get2d_remove_row_string(array_cycle, i)

            count = 0
            for j in range(len(array_cycle[0]) - 1, 0, -1):
                if array_cycle[0][j] is None:
                    for i in range(len(array_cycle)):
                        if array_cycle[i][j] is None:
                            count += 1
                        if count == len(array_cycle):
                            array_cycle = _get2d_remove_column_string(array_cycle, j)
                            count = 0

            for j in range(len(array_cycle[0]) - 1, 0, -1):
                if array_cycle[0][j] is None:
                    for i in range(len(array_cycle)):
                        if array_cycle[i][j] is None:
                            array_cycle[i][j] = ""

            for j in range(len(array_solution[0])):
                for i in range(len(array_solution)):
                    array_solution[i][j] = ""

            for i in range(len(array_cycle)):
                for j in range(len(array_cycle[0])):
                    if array_cycle[i][j] != "":
                        array_solution[i][j] = array_cycle[i][j]

        for i in range(len(array_solution) - 1, 0, -1):
            if array_solution[i][0] == "" or array_solution[0][0] is None:
                array_solution = _get2d_remove_row_string(array_solution, i)

        count = 0
        for j in range(len(array_solution[0]) - 1, 0, -1):
            if array_solution[0][j] is None:
                for i in range(len(array_solution)):
                    if array_solution[i][j] is None:
                        count += 1
                    if count == len(array_solution):
                        array_solution = _get2d_remove_column_string(array_solution, j)
                        count = 0

        if array_solution[0][0] == "" or array_solution[0][0] is None:
            for i in range(len(array_solution) - 1, 0, -1):
                array_solution = _get2d_remove_row_string(array_solution, i)
            for j in range(len(array_solution[0]) - 1, 0, -1):
                array_solution = _get2d_remove_column_string(array_solution, j)
            array_solution[0][0] = "None"

        return np.array(array_solution, dtype=object)
