"""ELECTRE I algorithm."""

from __future__ import annotations

import numpy as np

from matrix_electre.concordance import Concordance
from matrix_electre.credibility import Credibility
from matrix_electre.discordance import Discordance
from matrix_electre.matrix_operations import MatrixOperations


class ELECTRE_I:
    @staticmethod
    def e_I_Algorithm(
        array: np.ndarray,
        weights: np.ndarray,
        ei_p: float,
        ei_q: float,
    ) -> np.ndarray:
        array_p1 = Credibility.getCredibilityMatrixEI(array, weights, ei_p, ei_q)
        array_partition = np.zeros((2, array.shape[0]), dtype=np.float64)
        array_p2 = MatrixOperations.getColumnSum(array_p1)
        array_p3 = np.zeros(array_p2.shape, dtype=np.float64)
        array_solution = np.full((2, array.shape[0] + 1), " ", dtype=object)
        array_output = np.full((2, array.shape[0] + 1), " ", dtype=object)
        k_set = 0
        d_set = 0
        k = 0
        d = 0
        f = 0
        set_kd = 0

        array_solution[0, 0] = "Kernel: "
        array_solution[1, 0] = "Dominated: "
        for i in range(array_p2.shape[0]):
            if array_p2[i] == 0:
                array_p3[i] = i + 1
        if MatrixOperations.getElementCountZero(array_p2) != 0:
            set_kd = 1
        for i in range(array_p3.shape[0]):
            if array_p3[i] == 0:
                for j in range(array_p1.shape[1]):
                    array_p1[i, j] = 0.0
        array_p2 = MatrixOperations.getColumnSum(array_p1)
        for i in range(array_p2.shape[0]):
            if array_p2[i] == 0:
                array_p3[i] = i + 1

        if MatrixOperations.getElementCountZero(array_p3) == 0 and set_kd == 1:
            for i in range(array_p3.shape[0]):
                if array_p3[i] > 0:
                    k_set += 1
            for i in range(array_p3.shape[0]):
                if array_p3[i] > 0:
                    array_solution[0, i + 1] = f"a{round((i + 1) * 1) // 1}"
                    array_partition[0, i] = 1.0
                    k += 1
        if MatrixOperations.getElementCountZero(array_p3) == 0 and set_kd == 0:
            for i in range(array_p3.shape[0]):
                if array_p3[i] > 0:
                    d_set += 1
            for i in range(array_p3.shape[0]):
                if array_p3[i] > 0:
                    array_solution[1, i + 1] = f"a{round((i + 1) * 1) // 1}"
                    array_partition[1, i] = 1.0
                    d += 1
        if MatrixOperations.getElementCountZero(array_p3) != 0:
            for i in range(array_p3.shape[0]):
                if array_p3[i] > 0:
                    k_set += 1
                else:
                    d_set += 1
            for i in range(array_p3.shape[0]):
                if array_p3[i] > 0:
                    array_solution[0, i + 1] = f"a{round((i + 1) * 1) // 1}"
                    array_partition[0, i] = 1.0
                    k += 1
                else:
                    array_solution[1, i + 1] = f"a{round((i + 1) * 1) // 1}"
                    array_partition[1, i] = 1.0
                    d += 1

        for i in range(array_solution.shape[0]):
            f = 0
            for j in range(array_solution.shape[1]):
                if array_solution[i, j] != " ":
                    array_output[i, f] = array_solution[i, j]
                    if f + 1 < array_solution.shape[1]:
                        f += 1

        n = array.shape[0]
        array_output1 = ELECTRE_I._build_matrix_block(
            "Concordance Matrix:", Concordance.getConcordanceMatrixEI(array, weights), n
        )
        array_output2 = ELECTRE_I._build_matrix_block(
            "Discordance Matrix:", Discordance.getDiscordanceMatrixEI(array), n
        )
        array_output3 = ELECTRE_I._build_matrix_block(
            "Dominance Matrix:",
            Credibility.getCredibilityMatrixEI(array, weights, ei_p, ei_q),
            n,
        )
        cols = max(
            array_output1.shape[1],
            array_output2.shape[1],
            array_output3.shape[1],
            array_output.shape[1] + 2,
        )
        array_final = np.full(
            (
                array_output1.shape[0]
                + array_output2.shape[0]
                + array_output3.shape[0]
                + array_output.shape[0]
                + 1,
                cols,
            ),
            " ",
            dtype=object,
        )
        ELECTRE_I._copy_block(array_final, array_output1, 0)
        ELECTRE_I._copy_block(array_final, array_output2, array_output1.shape[0])
        ELECTRE_I._copy_block(
            array_final,
            array_output3,
            array_output1.shape[0] + array_output2.shape[0],
        )
        ELECTRE_I._copy_block(
            array_final,
            array_output,
            array_output1.shape[0] + array_output2.shape[0] + array_output3.shape[0],
        )
        return array_final

    @staticmethod
    def _build_matrix_block(title: str, array_temp: np.ndarray, n: int) -> np.ndarray:
        array_output = np.full((n + 2, n + 2), "", dtype=object)
        array_output[0, 0] = title
        for i in range(n):
            for j in range(n):
                array_output[0, j + 2] = f"a{j + 1}"
                array_output[i + 1, 1] = f"a{i + 1}"
        for i in range(n):
            for j in range(n):
                array_output[i + 1, j + 2] = str(round(float(array_temp[i, j]) * 10000) / 10000)
        for i in range(array_output.shape[0]):
            for j in range(array_output.shape[1]):
                if array_output[i, j] is None:
                    array_output[i, j] = ""
                if i + 3 == j + 2 and j >= 2:
                    array_output[i, j] = "-"
        return array_output

    @staticmethod
    def _copy_block(target: np.ndarray, source: np.ndarray, row_offset: int) -> None:
        for i in range(source.shape[0]):
            for j in range(source.shape[1]):
                target[row_offset + i, j] = source[i, j]
