"""ELECTRE II algorithm."""

from __future__ import annotations

import numpy as np

from matrix_electre.concordance import Concordance
from matrix_electre.credibility import Credibility
from matrix_electre.discordance import Discordance
from matrix_electre.electre_i import ELECTRE_I
from matrix_electre.matrix_operations import MatrixOperations
from my_cycles.johnson_algorithm_io_int import JohnsonAlgorithm_io_int
from my_cycles.johnson_algorithm_io_str import JohnsonAlgorithm_io_str


class ELECTRE_II:
    @staticmethod
    def e_II_Algorithm(array: np.ndarray) -> np.ndarray:
        array_p1 = np.array(array, dtype=np.float64, copy=True)
        array_p2 = MatrixOperations.getColumnSum(array_p1)
        array_p3 = np.zeros(array_p2.shape, dtype=np.float64)
        for i in range(array_p2.shape[0]):
            if array_p2[i] == 0:
                array_p3[i] = i + 1
        for i in range(array_p3.shape[0]):
            if array_p3[i] == 0:
                for j in range(array_p1.shape[1]):
                    array_p1[i, j] = 0.0
        array_p2 = MatrixOperations.getColumnSum(array_p1)
        for i in range(array_p2.shape[0]):
            if array_p2[i] == 0:
                array_p3[i] = i + 1
        return array_p3

    @staticmethod
    def rankDescending(
        array: np.ndarray,
        weights: np.ndarray,
        eii_cp: float,
        eii_c: float,
        eii_cm: float,
        eii_d1: float,
        eii_d2: float,
        maximum_cycles: int = 15,
    ) -> np.ndarray:
        k = 0
        array_s = Credibility.getCredibilityMatrixEII(
            array, weights, eii_cp, eii_c, eii_cm, eii_d1, eii_d2
        )
        array_cr1 = JohnsonAlgorithm_io_int.cyclesElimination(array_s, 2, maximum_cycles)
        array_cr2 = JohnsonAlgorithm_io_int.cyclesElimination(array_cr1, 1, maximum_cycles)
        array_r = np.array(array_cr2, dtype=np.float64, copy=True)
        array_descending = np.zeros(array_r.shape, dtype=np.float64)
        while MatrixOperations.get2DMatrixTotalSum(array_descending) < array_r.shape[0]:
            array0 = MatrixOperations.getColumnSum(array_r)
            if MatrixOperations.getElementCountZero(array0) == 0:
                min_val = MatrixOperations.getMinValueInRowNonSorting(array0)
                r_sum = MatrixOperations.getRowSum(array_r)
                r_temp = np.zeros(array0.shape, dtype=np.float64)
                k_tie = 0
                for j in range(array0.shape[0]):
                    if array0[j] == min_val:
                        r_temp[j] = 1.0
                for j in range(r_temp.shape[0]):
                    r_temp[j] = r_temp[j] * r_sum[j]
                max_val = MatrixOperations.getMaxValueInRowNonSorting(r_temp)
                for j in range(r_temp.shape[0]):
                    if r_temp[j] >= max_val:
                        k_tie = j
                for i in range(array0.shape[0]):
                    array_r[i, k_tie] = 0.0
            array0 = MatrixOperations.getColumnSum(array_r)
            for i in range(array0.shape[0]):
                if array0[i] == 0:
                    for j in range(array0.shape[0]):
                        array_r[i, j] = 0.0
                    for j in range(array0.shape[0]):
                        if i == j:
                            array_r[i, j] = 0.0
                        else:
                            array_r[j, i] = 1.0
            for j in range(array0.shape[0]):
                if array0[j] == 0:
                    array_descending[k, j] = 1.0
            if MatrixOperations.getElementCountZero(array0) == 0:
                k += 0
            else:
                k += 1
        for i in range(array_descending.shape[0]):
            for j in range(array_descending.shape[1]):
                array_descending[i, j] = array_descending[i, j] * (i + 1)
        return array_descending

    @staticmethod
    def rankAscending(
        array: np.ndarray,
        weights: np.ndarray,
        eii_cp: float,
        eii_c: float,
        eii_cm: float,
        eii_d1: float,
        eii_d2: float,
        maximum_cycles: int = 15,
    ) -> np.ndarray:
        p = 0
        k = 0
        array_s = MatrixOperations.getTransposed2DMatrix(
            Credibility.getCredibilityMatrixEII(
                array, weights, eii_cp, eii_c, eii_cm, eii_d1, eii_d2
            )
        )
        array_cr1 = JohnsonAlgorithm_io_int.cyclesElimination(array_s, 2, maximum_cycles)
        array_cr2 = JohnsonAlgorithm_io_int.cyclesElimination(array_cr1, 1, maximum_cycles)
        array_r = np.array(array_cr2, dtype=np.float64, copy=True)
        array_ascending = np.zeros(array_r.shape, dtype=np.float64)
        array_invert = np.zeros(array_r.shape, dtype=np.float64)
        while MatrixOperations.get2DMatrixTotalSum(array_ascending) < array_r.shape[0]:
            array0 = MatrixOperations.getColumnSum(array_r)
            if MatrixOperations.getElementCountZero(array0) == 0:
                min_val = MatrixOperations.getMinValueInRowNonSorting(array0)
                r_sum = MatrixOperations.getRowSum(array_r)
                r_temp = np.zeros(array0.shape, dtype=np.float64)
                k_tie = 0
                for j in range(array0.shape[0]):
                    if array0[j] == min_val:
                        r_temp[j] = 1.0
                for j in range(r_temp.shape[0]):
                    r_temp[j] = r_temp[j] * r_sum[j]
                max_val = MatrixOperations.getMaxValueInRowNonSorting(r_temp)
                for j in range(r_temp.shape[0]):
                    if r_temp[j] >= max_val:
                        k_tie = j
                for i in range(array0.shape[0]):
                    array_r[i, k_tie] = 0.0
            array0 = MatrixOperations.getColumnSum(array_r)
            for i in range(array0.shape[0]):
                if array0[i] == 0:
                    for j in range(array0.shape[0]):
                        array_r[i, j] = 0.0
                    for j in range(array0.shape[0]):
                        if i == j:
                            array_r[i, j] = 0.0
                        else:
                            array_r[j, i] = 1.0
            for j in range(array0.shape[0]):
                if array0[j] == 0:
                    array_ascending[k, j] = 1.0
            if MatrixOperations.getElementCountZero(array0) == 0:
                k += 0
            else:
                k += 1
        p = MatrixOperations.getElementCountZero(MatrixOperations.getRowSum(array_ascending))
        for i in range(array_invert.shape[0] - p):
            for j in range(array_invert.shape[1]):
                array_invert[array_invert.shape[0] - 1 - p - i, j] = array_ascending[i, j]
        array_ascending = array_invert
        for i in range(array_ascending.shape[0]):
            for j in range(array_ascending.shape[1]):
                array_ascending[i, j] = array_ascending[i, j] * (i + 1)
        return array_ascending

    @staticmethod
    def rankFinal(
        array: np.ndarray,
        weights: np.ndarray,
        eii_cp: float,
        eii_c: float,
        eii_cm: float,
        eii_d1: float,
        eii_d2: float,
        maximum_cycles: int = 15,
    ) -> np.ndarray:
        array_ascending = ELECTRE_II.rankAscending(
            array, weights, eii_cp, eii_c, eii_cm, eii_d1, eii_d2, maximum_cycles
        )
        array_descending = ELECTRE_II.rankDescending(
            array, weights, eii_cp, eii_c, eii_cm, eii_d1, eii_d2, maximum_cycles
        )
        rd = MatrixOperations.getColumnSum(array_descending)
        ra = MatrixOperations.getColumnSum(array_ascending)
        rm = (ra + rd) / 2.0
        n = array.shape[0]

        array_output1 = ELECTRE_I._build_matrix_block(
            "Concordance Matrix:", Concordance.getConcordanceMatrixEII(array, weights), n
        )
        array_output2 = ELECTRE_I._build_matrix_block(
            "Discordance Matrix:", Discordance.getDiscordanceMatrixEII(array), n
        )
        cred = Credibility.getCredibilityMatrixEII(
            array, weights, eii_cp, eii_c, eii_cm, eii_d1, eii_d2
        )
        array_output3 = ELECTRE_I._build_matrix_block("Credibility Matrix:", cred, n)
        array_output3[0, 0] = "Credibility Matrix:"
        for i in range(array_output3.shape[0]):
            for j in range(array_output3.shape[1]):
                if array_output3[i, j] == "2.0":
                    array_output3[i, j] = "Ss"
                if array_output3[i, j] == "1.0":
                    array_output3[i, j] = "Ws"

        array_temp_s = JohnsonAlgorithm_io_str.cyclesElimination(cred, 2, maximum_cycles)
        array_output4 = np.full((array_temp_s.shape[0] + 1, array_temp_s.shape[1] + 1), "", dtype=object)
        array_output4[0, 0] = "Cycles Ss:"
        for i in range(array_temp_s.shape[0]):
            for j in range(array_temp_s.shape[1]):
                array_output4[i, j + 1] = array_temp_s[i, j]

        array_temp_s = JohnsonAlgorithm_io_str.cyclesElimination(cred, 1, maximum_cycles)
        array_output5 = np.full((array_temp_s.shape[0] + 1, array_temp_s.shape[1] + 1), "", dtype=object)
        array_output5[0, 0] = "Cycles Ws:"
        for i in range(array_temp_s.shape[0]):
            for j in range(array_temp_s.shape[1]):
                array_output5[i, j + 1] = array_temp_s[i, j]

        rows = max(rd.shape[0], ra.shape[0], rm.shape[0])
        array_output7 = np.full((rows + 2, 7), "", dtype=object)
        array_output7[0, 0] = "Ranking:"
        array_output7[0, 2] = "Ascend."
        array_output7[0, 3] = "Descend."
        array_output7[0, 4] = "Average"
        for i in range(ra.shape[0]):
            array_output7[i + 1, 1] = f"a{i + 1}"
            array_output7[i + 1, 2] = str(round(float(ra[i]) * 10000) / 10000)
            array_output7[i + 1, 3] = str(round(float(rd[i]) * 10000) / 10000)
            array_output7[i + 1, 4] = str(round(float(rm[i]) * 10000) / 10000)

        rf = np.full((array_ascending.shape[0], array_ascending.shape[1]), None, dtype=object)
        rg = np.full((array_ascending.shape[0], array_ascending.shape[1]), None, dtype=object)
        for i in range(array_ascending.shape[0]):
            for j in range(array_ascending.shape[1]):
                if rd[i] == rd[j] and ra[i] == ra[j]:
                    rf[i, j] = "I"
                    rg[i, j] = "I"
                elif (
                    (rd[i] < rd[j] and ra[i] < ra[j])
                    or (rd[i] == rd[j] and ra[i] < ra[j])
                    or (rd[i] < rd[j] and ra[i] == ra[j])
                ):
                    rf[i, j] = "P+"
                    rf[j, i] = "P-"
                    rg[i, j] = "P+"
                    rg[j, i] = "P-"
                else:
                    if rf[i, j] is None:
                        rf[i, j] = "R"
                        rg[i, j] = "R"
                if i == j:
                    rf[i, j] = "0"
                    rg[i, j] = "0"

        array_output8 = np.full((rg.shape[0] + 2, rg.shape[1] + 2), "", dtype=object)
        array_output8[0, 0] = "Dominance Matrix:"
        for i in range(rg.shape[0]):
            for j in range(rg.shape[1]):
                array_output8[0, j + 2] = f"a{j + 1}"
                array_output8[i + 1, 1] = f"a{i + 1}"
                array_output8[i + 1, j + 2] = rg[i, j]
        for i in range(array_output8.shape[0]):
            for j in range(array_output8.shape[1]):
                if array_output8[i, j] is None:
                    array_output8[i, j] = ""
                if i + 3 == j + 2 and j >= 2:
                    array_output8[i, j] = "-"

        blocks = [
            array_output1,
            array_output2,
            array_output3,
            array_output4,
            array_output5,
            array_output7,
            array_output8,
        ]
        cols = max(block.shape[1] for block in blocks)
        array_final = np.full((sum(b.shape[0] for b in blocks), cols), " ", dtype=object)
        offset = 0
        for block in blocks:
            ELECTRE_I._copy_block(array_final, block, offset)
            offset += block.shape[0]
        return array_final
