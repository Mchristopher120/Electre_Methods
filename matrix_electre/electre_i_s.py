"""ELECTRE I_s algorithm."""

from __future__ import annotations

import numpy as np

from matrix_electre.concordance import Concordance
from matrix_electre.credibility import Credibility
from matrix_electre.discordance import Discordance
from matrix_electre.electre_i import ELECTRE_I
from matrix_electre.matrix_operations import MatrixOperations
from my_cycles.johnson_algorithm_io_int import JohnsonAlgorithm_io_int
from my_cycles.johnson_algorithm_io_str import JohnsonAlgorithm_io_str


class ELECTRE_I_s:
    @staticmethod
    def e_I_s_Algorithm(
        array: np.ndarray,
        weights: np.ndarray,
        p: np.ndarray,
        q: np.ndarray,
        v: np.ndarray,
        ei_s_lambda: float,
        maximum_cycles: int = 15,
    ) -> np.ndarray:
        cred = Credibility.getCredibilityMatrixEI_s(array, weights, p, q, v, ei_s_lambda)
        array_p1 = JohnsonAlgorithm_io_int.cyclesElimination(cred, 1, maximum_cycles)
        array_p2 = MatrixOperations.getColumnSum(array_p1)
        array_p3 = np.zeros(array_p2.shape, dtype=np.float64)
        array_solution = np.full((3, array.shape[0] + 1), " ", dtype=object)
        array_output = np.full((3, array.shape[0] + 1), " ", dtype=object)
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
                    k += 1
        if MatrixOperations.getElementCountZero(array_p3) == 0 and set_kd == 0:
            for i in range(array_p3.shape[0]):
                if array_p3[i] > 0:
                    d_set += 1
            for i in range(array_p3.shape[0]):
                if array_p3[i] > 0:
                    array_solution[1, i + 1] = f"a{round((i + 1) * 1) // 1}"
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
                    k += 1
                else:
                    array_solution[1, i + 1] = f"a{round((i + 1) * 1) // 1}"
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
            "Concordance Matrix:", Concordance.getConcordanceMatrixEI_s(array, weights, p, q), n
        )

        n = array.shape[0]
        array_temp_d = np.zeros((n, n), dtype=np.float64)
        c = ei_s_lambda
        for k_idx in range(array.shape[1]):
            array_dmj = Discordance.getDiscordanceMatrixEI_s(
                c, array, weights, p, q, v, k_idx, ei_s_lambda
            )
            array_temp_d = MatrixOperations.get2DMatrixSum(array_temp_d, array_dmj)
        for j in range(array.shape[0]):
            for i in range(array.shape[0]):
                if i == j:
                    array_temp_d[i, j] = 0.0
        for j in range(array.shape[0]):
            for i in range(array.shape[0]):
                array_temp_d[i, j] = 1.0 if array_temp_d[i, j] > 0 else 0.0
        array_output2 = ELECTRE_I._build_matrix_block("Discordance Matrix:", array_temp_d, n)
        array_output2[0, 0] = "Discordance Matrix:"

        array_output3 = ELECTRE_I._build_matrix_block("Credibility Matrix:", cred, n)
        array_output3[0, 0] = "Credibility Matrix:"

        array_temp_s = JohnsonAlgorithm_io_str.cyclesElimination(cred, 1, maximum_cycles)
        array_output4 = np.full((array_temp_s.shape[0] + 1, array_temp_s.shape[1] + 1), "", dtype=object)
        array_output4[0, 0] = "Cycles:"
        for i in range(array_temp_s.shape[0]):
            for j in range(array_temp_s.shape[1]):
                array_output4[i, j + 1] = array_temp_s[i, j]
        for i in range(array_output4.shape[0]):
            for j in range(array_output4.shape[1]):
                if array_output4[i, j] is None:
                    array_output4[i, j] = ""

        cols = max(
            array_output1.shape[1],
            array_output2.shape[1],
            array_output3.shape[1],
            array_output4.shape[1],
        )
        array_final = np.full(
            (
                array_output1.shape[0]
                + array_output2.shape[0]
                + array_output3.shape[0]
                + array_output4.shape[0]
                + array_output.shape[0],
                cols + 2,
            ),
            " ",
            dtype=object,
        )
        offsets = [
            0,
            array_output1.shape[0],
            array_output1.shape[0] + array_output2.shape[0],
            array_output1.shape[0] + array_output2.shape[0] + array_output3.shape[0],
            array_output1.shape[0]
            + array_output2.shape[0]
            + array_output3.shape[0]
            + array_output4.shape[0],
        ]
        for block, offset in zip(
            [array_output1, array_output2, array_output3, array_output4, array_output],
            offsets,
        ):
            ELECTRE_I._copy_block(array_final, block, offset)
        return array_final
