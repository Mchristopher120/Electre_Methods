"""ELECTRE IV algorithm."""

from __future__ import annotations

import numpy as np

from matrix_electre.credibility import Credibility
from matrix_electre.electre_i import ELECTRE_I
from matrix_electre.matrix_operations import MatrixOperations


class ELECTRE_IV:
    @staticmethod
    def e_IV_Algorithm(
        array: np.ndarray,
        p: np.ndarray,
        q: np.ndarray,
        v: np.ndarray,
    ) -> np.ndarray:
        return Credibility.getCredibilityMatrixEIV(array, p, q, v)

    @staticmethod
    def rankDescending(
        array: np.ndarray,
        p: np.ndarray,
        q: np.ndarray,
        v: np.ndarray,
    ) -> np.ndarray:
        array_d = np.array(ELECTRE_IV.e_IV_Algorithm(array, p, q, v), dtype=np.float64, copy=True)
        array_dtie = np.zeros(array_d.shape, dtype=np.float64)
        array_l1 = np.zeros(array_d.shape, dtype=np.float64)
        array_l2 = np.zeros(array_d.shape, dtype=np.float64)
        array_q = np.zeros(array_d.shape, dtype=np.float64)
        array_qtie = np.zeros(array_d.shape, dtype=np.float64)
        array_total = np.zeros((array.shape[0], 3), dtype=np.float64)
        array_ttie = np.zeros((array.shape[0], 3), dtype=np.float64)
        array_rank_d = np.zeros((array.shape[0], array.shape[0]), dtype=np.float64)
        alternatives = np.zeros(array.shape[0], dtype=np.float64)
        alpha = 0.3
        beta = -0.15
        s_lambda_max = 0.1
        s_lambda1_max = 0.1
        k = 0
        count = 0
        while MatrixOperations.get2DMatrixTotalSum(array_rank_d) < array.shape[0]:
            lambda_max = MatrixOperations.getMaxValueInRowSorting(
                MatrixOperations.getMaxValueInColumn(array_d)
            )
            for j in range(array_d.shape[1]):
                for i in range(array_d.shape[0]):
                    if array_d[i, j] < lambda_max - s_lambda_max:
                        array_l1[i, j] = array_d[i, j]
                    else:
                        array_l1[i, j] = 0.0
                    if i == j:
                        array_l1[i, j] = 0.0
            lambda1_max = MatrixOperations.getMaxValueInRowSorting(
                MatrixOperations.getMaxValueInColumn(array_l1)
            )
            for j in range(array_d.shape[1]):
                for i in range(array_d.shape[0]):
                    if array_d[i, j] > lambda1_max and array_d[i, j] > (
                        array_d[j, i] + alpha + beta * array_d[i, j]
                    ):
                        array_q[i, j] = 1.0
                    else:
                        array_q[i, j] = 0.0
                    if i == j:
                        array_q[i, j] = 0.0
            for i in range(array.shape[0]):
                if array_total[i, 0] != -10001:
                    array_total[i, 0] = MatrixOperations.getWeightsSum(array_q[i])
                if array_total[i, 1] != -10001:
                    array_total[i, 1] = MatrixOperations.getCriterionSum(array_q, i)
                if array_total[i, 2] != -10001:
                    array_total[i, 2] = array_total[i, 0] - array_total[i, 1]
            max_total = MatrixOperations.getMaxValueInColumnJ(array_total, 2)
            count = 0
            for i1 in range(array.shape[0]):
                if array_total[i1, 2] == max_total:
                    count += 1
                    alternatives[i1] = 1.0
                else:
                    alternatives[i1] = 0.0
            if count == 1:
                for i1 in range(array.shape[0]):
                    if array_total[i1, 2] == max_total:
                        array_rank_d[k, i1] = 1.0
                        array_total[i1, 0] = -10001
                        array_total[i1, 1] = -10001
                        array_total[i1, 2] = -10001
                        for remove in range(array.shape[0]):
                            array_d[i1, remove] = 0.0
                            array_d[remove, i1] = 0.0
            if count > 1:
                array_dtie[:, :] = 0.0
                for j2 in range(alternatives.shape[0]):
                    if alternatives[j2] == 1.0:
                        for i2 in range(array_dtie.shape[0]):
                            if alternatives[i2] == 1.0:
                                array_dtie[i2, j2] = array_d[i2, j2]
                for j2 in range(array_dtie.shape[1]):
                    for i2 in range(array_dtie.shape[0]):
                        if array_dtie[i2, j2] < lambda1_max - s_lambda1_max:
                            array_l2[i2, j2] = array_dtie[i2, j2]
                        else:
                            array_l2[i2, j2] = 0.0
                        if i2 == j2:
                            array_l2[i2, j2] = 0.0
                lambda2_max = MatrixOperations.getMaxValueInRowSorting(
                    MatrixOperations.getMaxValueInColumn(array_l2)
                )
                for j2 in range(array_dtie.shape[1]):
                    for i2 in range(array_dtie.shape[0]):
                        if array_dtie[i2, j2] < lambda2_max - s_lambda1_max:
                            array_l2[i2, j2] = array_dtie[i2, j2]
                        else:
                            array_l2[i2, j2] = 0.0
                        if i2 == j2:
                            array_l2[i2, j2] = 0.0
                lambda2_max = MatrixOperations.getMaxValueInRowSorting(
                    MatrixOperations.getMaxValueInColumn(array_l2)
                )
                for j2 in range(array_dtie.shape[1]):
                    for i2 in range(array_dtie.shape[0]):
                        if array_dtie[i2, j2] > lambda2_max and array_dtie[i2, j2] > (
                            array_dtie[j2, i2] + alpha + beta * array_dtie[i2, j2]
                        ):
                            array_qtie[i2, j2] = 1.0
                        else:
                            array_qtie[i2, j2] = 0.0
                        if i2 == j2:
                            array_qtie[i2, j2] = 0.0
                for i2 in range(array.shape[0]):
                    if alternatives[i2] == 0.0:
                        array_ttie[i2, 0] = -10001
                        array_ttie[i2, 1] = -10001
                        array_ttie[i2, 2] = -10001
                    else:
                        array_ttie[i2, 0] = MatrixOperations.getWeightsSum(array_qtie[i2])
                        array_ttie[i2, 1] = MatrixOperations.getCriterionSum(array_qtie, i2)
                        array_ttie[i2, 2] = array_ttie[i2, 0] - array_ttie[i2, 1]
                max_ttie = MatrixOperations.getMaxValueInColumnJ(array_ttie, 2)
                for i2 in range(array.shape[0]):
                    if array_ttie[i2, 2] == max_ttie:
                        array_rank_d[k, i2] = 1.0
                        array_ttie[i2, 0] = -10001
                        array_ttie[i2, 1] = -10001
                        array_ttie[i2, 2] = -10001
                        array_total[i2, 0] = -10001
                        array_total[i2, 1] = -10001
                        array_total[i2, 2] = -10001
                        for remove in range(array.shape[0]):
                            array_d[i2, remove] = 0.0
                            array_d[remove, i2] = 0.0
            k += 1
            count = 0
        for i in range(array_rank_d.shape[0]):
            for j in range(array_rank_d.shape[1]):
                array_rank_d[i, j] = array_rank_d[i, j] * (i + 1)
        return array_rank_d

    @staticmethod
    def rankAscending(
        array: np.ndarray,
        p: np.ndarray,
        q: np.ndarray,
        v: np.ndarray,
    ) -> np.ndarray:
        array_a = np.array(ELECTRE_IV.e_IV_Algorithm(array, p, q, v), dtype=np.float64, copy=True)
        array_atie = np.zeros(array_a.shape, dtype=np.float64)
        array_l1 = np.zeros(array_a.shape, dtype=np.float64)
        array_l2 = np.zeros(array_a.shape, dtype=np.float64)
        array_q = np.zeros(array_a.shape, dtype=np.float64)
        array_qtie = np.zeros(array_a.shape, dtype=np.float64)
        array_total = np.zeros((array.shape[0], 3), dtype=np.float64)
        array_ttie = np.zeros((array.shape[0], 3), dtype=np.float64)
        array_rank_a = np.zeros((array.shape[0], array.shape[0]), dtype=np.float64)
        array_invert = np.zeros((array.shape[0], array.shape[0]), dtype=np.float64)
        alternatives = np.zeros(array.shape[0], dtype=np.float64)
        alpha = 0.3
        beta = -0.15
        s_lambda_max = 0.1
        s_lambda1_max = 0.1
        k = 0
        count = 0
        while MatrixOperations.get2DMatrixTotalSum(array_rank_a) < array.shape[0]:
            lambda_max = MatrixOperations.getMaxValueInRowSorting(
                MatrixOperations.getMaxValueInColumn(array_a)
            )
            for j in range(array_a.shape[1]):
                for i in range(array_a.shape[0]):
                    if array_a[i, j] < lambda_max - s_lambda_max:
                        array_l1[i, j] = array_a[i, j]
                    else:
                        array_l1[i, j] = 0.0
                    if i == j:
                        array_l1[i, j] = 0.0
            lambda1_max = MatrixOperations.getMaxValueInRowSorting(
                MatrixOperations.getMaxValueInColumn(array_l1)
            )
            for j in range(array_a.shape[1]):
                for i in range(array_a.shape[0]):
                    if array_a[i, j] > lambda1_max and array_a[i, j] > (
                        array_a[j, i] + alpha + beta * array_a[i, j]
                    ):
                        array_q[i, j] = 1.0
                    else:
                        array_q[i, j] = 0.0
                    if i == j:
                        array_q[i, j] = 0.0
            for i in range(array.shape[0]):
                if array_total[i, 0] != 10001:
                    array_total[i, 0] = MatrixOperations.getWeightsSum(array_q[i])
                if array_total[i, 1] != 10001:
                    array_total[i, 1] = MatrixOperations.getCriterionSum(array_q, i)
                if array_total[i, 2] != 10001:
                    array_total[i, 2] = array_total[i, 0] - array_total[i, 1]
            min_total = MatrixOperations.getMinValueInColumnJ(array_total, 2)
            count = 0
            for i1 in range(array.shape[0]):
                if array_total[i1, 2] == min_total:
                    count += 1
                    alternatives[i1] = 1.0
                else:
                    alternatives[i1] = 0.0
            if count == 1:
                for i1 in range(array.shape[0]):
                    if array_total[i1, 2] == min_total:
                        array_rank_a[k, i1] = 1.0
                        array_total[i1, 0] = 10001
                        array_total[i1, 1] = 10001
                        array_total[i1, 2] = 10001
                        for remove in range(array.shape[0]):
                            array_a[i1, remove] = 0.0
                            array_a[remove, i1] = 0.0
            if count > 1:
                array_atie[:, :] = 0.0
                for j2 in range(alternatives.shape[0]):
                    if alternatives[j2] == 1.0:
                        for i2 in range(array_atie.shape[0]):
                            if alternatives[i2] == 1.0:
                                array_atie[i2, j2] = array_a[i2, j2]
                for j2 in range(array_atie.shape[1]):
                    for i2 in range(array_atie.shape[0]):
                        if array_atie[i2, j2] < lambda1_max - s_lambda1_max:
                            array_l2[i2, j2] = array_atie[i2, j2]
                        else:
                            array_l2[i2, j2] = 0.0
                        if i2 == j2:
                            array_l2[i2, j2] = 0.0
                lambda2_max = MatrixOperations.getMaxValueInRowSorting(
                    MatrixOperations.getMaxValueInColumn(array_l2)
                )
                for j2 in range(array_atie.shape[1]):
                    for i2 in range(array_atie.shape[0]):
                        if array_atie[i2, j2] < lambda2_max - s_lambda1_max:
                            array_l2[i2, j2] = array_atie[i2, j2]
                        else:
                            array_l2[i2, j2] = 0.0
                        if i2 == j2:
                            array_l2[i2, j2] = 0.0
                lambda2_max = MatrixOperations.getMaxValueInRowSorting(
                    MatrixOperations.getMaxValueInColumn(array_l2)
                )
                for j2 in range(array_atie.shape[1]):
                    for i2 in range(array_atie.shape[0]):
                        if array_atie[i2, j2] > lambda2_max and array_atie[i2, j2] > (
                            array_atie[j2, i2] + alpha + beta * array_atie[i2, j2]
                        ):
                            array_qtie[i2, j2] = 1.0
                        else:
                            array_qtie[i2, j2] = 0.0
                        if i2 == j2:
                            array_qtie[i2, j2] = 0.0
                for i2 in range(array.shape[0]):
                    if alternatives[i2] == 0.0:
                        array_ttie[i2, 0] = 10001
                        array_ttie[i2, 1] = 10001
                        array_ttie[i2, 2] = 10001
                    else:
                        array_ttie[i2, 0] = MatrixOperations.getWeightsSum(array_qtie[i2])
                        array_ttie[i2, 1] = MatrixOperations.getCriterionSum(array_qtie, i2)
                        array_ttie[i2, 2] = array_ttie[i2, 0] - array_ttie[i2, 1]
                min_ttie = MatrixOperations.getMinValueInColumnJ(array_ttie, 2)
                for i2 in range(array.shape[0]):
                    if array_ttie[i2, 2] == min_ttie:
                        array_rank_a[k, i2] = 1.0
                        array_ttie[i2, 0] = 10001
                        array_ttie[i2, 1] = 10001
                        array_ttie[i2, 2] = 10001
                        array_total[i2, 0] = 10001
                        array_total[i2, 1] = 10001
                        array_total[i2, 2] = 10001
                        for remove in range(array.shape[0]):
                            array_a[i2, remove] = 0.0
                            array_a[remove, i2] = 0.0
            k += 1
            count = 0
        p1 = MatrixOperations.getElementCountZero(MatrixOperations.getRowSum(array_rank_a))
        for i in range(array_invert.shape[0] - p1):
            for j in range(array_invert.shape[1]):
                array_invert[array_invert.shape[0] - 1 - p1 - i, j] = array_rank_a[i, j]
        array_rank_a = array_invert
        for i in range(array_rank_a.shape[0]):
            for j in range(array_rank_a.shape[1]):
                array_rank_a[i, j] = array_rank_a[i, j] * (i + 1)
        return array_rank_a

    @staticmethod
    def rankFinal(
        array: np.ndarray,
        p: np.ndarray,
        q: np.ndarray,
        v: np.ndarray,
    ) -> np.ndarray:
        array_rank_a = ELECTRE_IV.rankAscending(array, p, q, v)
        array_rank_d = ELECTRE_IV.rankDescending(array, p, q, v)
        rd = MatrixOperations.getColumnSum(array_rank_d)
        ra = MatrixOperations.getColumnSum(array_rank_a)
        rm = (ra + rd) / 2.0

        array_temp = Credibility.getCredibilityMatrixEIV(array, p, q, v)
        n = array.shape[0]
        array_output1 = ELECTRE_I._build_matrix_block("Credibility Matrix:", array_temp, n)
        array_output1[0, 0] = "Credibility Matrix:"
        for i in range(1, array_output1.shape[0]):
            for j in range(1, array_output1.shape[1]):
                if array_output1[i, j] == "1.0":
                    array_output1[i, j] = "Sq"
                if array_output1[i, j] == "0.8":
                    array_output1[i, j] = "Sc"
                if array_output1[i, j] == "0.6":
                    array_output1[i, j] = "Sp"
                if array_output1[i, j] == "0.4":
                    array_output1[i, j] = "Ss"
                if array_output1[i, j] == "0.2":
                    array_output1[i, j] = "Sv"
                if array_output1[i, j] == "0.0":
                    array_output1[i, j] = ""
                if i == j:
                    array_output1[i, j] = "-"

        rows = max(rd.shape[0], ra.shape[0], rm.shape[0])
        array_output2 = np.full((rows + 2, 7), "", dtype=object)
        array_output2[0, 0] = "Ranking:"
        array_output2[0, 2] = "Ascend."
        array_output2[0, 3] = "Descend."
        array_output2[0, 4] = "Average"
        for i in range(ra.shape[0]):
            array_output2[i + 1, 1] = f"a{i + 1}"
            array_output2[i + 1, 2] = str(round(float(ra[i]) * 10000) / 10000)
            array_output2[i + 1, 3] = str(round(float(rd[i]) * 10000) / 10000)
            array_output2[i + 1, 4] = str(round(float(rm[i]) * 10000) / 10000)

        rf = np.full((array_rank_a.shape[0], array_rank_a.shape[1]), None, dtype=object)
        rg = np.full((array_rank_a.shape[0], array_rank_a.shape[1]), None, dtype=object)
        for i in range(array_rank_a.shape[0]):
            for j in range(array_rank_a.shape[1]):
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
                    rf[i, j] = "-"
                    rg[i, j] = "-"

        array_output3 = np.full((rg.shape[0] + 2, rg.shape[1] + 2), "", dtype=object)
        array_output3[0, 0] = "Dominance Matrix:"
        for i in range(rg.shape[0]):
            for j in range(rg.shape[1]):
                array_output3[0, j + 2] = f"a{j + 1}"
                array_output3[i + 1, 1] = f"a{i + 1}"
                array_output3[i + 1, j + 2] = rg[i, j]

        cols = max(array_output1.shape[1], array_output2.shape[1], array_output3.shape[1])
        array_final = np.full(
            (array_output1.shape[0] + array_output2.shape[0] + array_output3.shape[0], cols + 2),
            " ",
            dtype=object,
        )
        ELECTRE_I._copy_block(array_final, array_output1, 0)
        ELECTRE_I._copy_block(array_final, array_output2, array_output1.shape[0])
        ELECTRE_I._copy_block(
            array_final, array_output3, array_output1.shape[0] + array_output2.shape[0]
        )
        return array_final
