"""Credibility matrix computations for ELECTRE methods."""

from __future__ import annotations

import numpy as np

from matrix_electre.concordance import Concordance
from matrix_electre.discordance import Discordance
from matrix_electre.matrix_operations import MatrixOperations


class Credibility:
    @staticmethod
    def getCredibilityMatrixEI(
        array: np.ndarray,
        weights: np.ndarray,
        ei_p: float,
        ei_q: float,
    ) -> np.ndarray:
        n = array.shape[0]
        array_cred_m = np.zeros((n, n), dtype=np.float64)
        array_cm = Concordance.getConcordanceMatrixEI(array, weights)
        array_dm = Discordance.getDiscordanceMatrixEI(array)
        for j in range(array.shape[0]):
            for i in range(array.shape[0]):
                if i == j:
                    array_cred_m[i, j] = 0.0
                else:
                    if array_cm[i, j] >= ei_p and array_dm[i, j] <= ei_q:
                        array_cred_m[i, j] = 1.0
                    else:
                        array_cred_m[i, j] = 0.0
        return array_cred_m

    @staticmethod
    def getCredibilityMatrixEI_s(
        array: np.ndarray,
        weights: np.ndarray,
        p: np.ndarray,
        q: np.ndarray,
        v: np.ndarray,
        ei_s_lambda: float,
    ) -> np.ndarray:
        n = array.shape[0]
        array_cred_m = np.zeros((n, n), dtype=np.float64)
        n = array.shape[0]
        array_dm = np.zeros((n, n), dtype=np.float64)
        array_cm = Concordance.getConcordanceMatrixEI_s(array, weights, p, q)
        c = ei_s_lambda
        for k in range(array.shape[1]):
            array_dmj = Discordance.getDiscordanceMatrixEI_s(
                c, array, weights, p, q, v, k, ei_s_lambda
            )
            array_dm = MatrixOperations.get2DMatrixSum(array_dm, array_dmj)
        for j in range(array.shape[0]):
            for i in range(array.shape[0]):
                if i == j:
                    array_dm[i, j] = 0.0
        for j in range(array.shape[0]):
            for i in range(array.shape[0]):
                if array_dm[i, j] > 0:
                    array_dm[i, j] = 1.0
                else:
                    array_dm[i, j] = 0.0
        for j in range(array.shape[0]):
            for i in range(array.shape[0]):
                if array_cm[i, j] >= c and array_dm[i, j] == 0:
                    array_cred_m[i, j] = 1.0
                else:
                    array_cred_m[i, j] = 0.0
        for j in range(array.shape[0]):
            for i in range(array.shape[0]):
                if i == j:
                    array_cred_m[i, j] = 0.0
        return array_cred_m

    @staticmethod
    def getCredibilityMatrixEI_v(
        array: np.ndarray,
        v: np.ndarray,
        weights: np.ndarray,
        ei_v_p: float,
        ei_v_q: float,
    ) -> np.ndarray:
        n = array.shape[0]
        array_cred_m = np.zeros((n, n), dtype=np.float64)
        array_cm = Concordance.getConcordanceMatrixEI_v(array, weights)
        array_dm = Discordance.getDiscordanceMatrixEI_v(array, v)
        for j in range(array.shape[0]):
            for i in range(array.shape[0]):
                if i == j:
                    array_cred_m[i, j] = 0.0
                else:
                    if array_cm[i, j] >= ei_v_p and array_dm[i, j] <= ei_v_q:
                        array_cred_m[i, j] = 1.0
                    else:
                        array_cred_m[i, j] = 0.0
        return array_cred_m

    @staticmethod
    def getCredibilityMatrixEII(
        array: np.ndarray,
        weights: np.ndarray,
        eii_cp: float,
        eii_c: float,
        eii_cm: float,
        eii_d1: float,
        eii_d2: float,
    ) -> np.ndarray:
        n = array.shape[0]
        array_cred_ms = np.zeros((n, n), dtype=np.float64)
        array_cred_mw = np.zeros((n, n), dtype=np.float64)
        array_cm = Concordance.getConcordanceMatrixEII(array, weights)
        array_dm = Discordance.getDiscordanceMatrixEII(array)
        for j in range(array.shape[0]):
            for i in range(array.shape[0]):
                if i == j:
                    array_cred_ms[i, j] = 0.0
                else:
                    if (
                        array_cm[i, j] >= eii_cp
                        and array_dm[i, j] <= eii_d2
                        and array_cm[i, j] >= array_cm[j, i]
                    ) or (
                        array_cm[i, j] >= eii_c
                        and array_dm[i, j] <= eii_d1
                        and array_cm[i, j] >= array_cm[j, i]
                    ):
                        array_cred_ms[i, j] = 1.0
                    else:
                        array_cred_ms[i, j] = 0.0
        for j in range(array.shape[0]):
            for i in range(array.shape[0]):
                if i == j:
                    array_cred_mw[i, j] = 0.0
                else:
                    if (
                        array_cm[i, j] >= eii_cm
                        and array_dm[i, j] <= eii_d2
                        and array_cm[i, j] >= array_cm[j, i]
                    ):
                        array_cred_mw[i, j] = 1.0
                    else:
                        array_cred_mw[i, j] = 0.0
        return MatrixOperations.get2DMatrixSum(array_cred_ms, array_cred_mw)

    @staticmethod
    def getCredibilityMatrixEIII(
        array: np.ndarray,
        weights: np.ndarray,
        p: np.ndarray,
        q: np.ndarray,
        v: np.ndarray,
    ) -> np.ndarray:
        n = array.shape[0]
        array_cred_m = np.ones((n, n), dtype=np.float64)
        array_cm = Concordance.getConcordanceMatrixEIII(array, weights, p, q)
        for k in range(array.shape[1]):
            array_dm = Discordance.getDiscordanceMatrixEIII(array, p, v, k)
            for j in range(array.shape[0]):
                for i in range(array.shape[0]):
                    if i != j:
                        if array_dm[i, j] <= array_cm[i, j]:
                            array_dm[i, j] = 1.0
                        else:
                            array_dm[i, j] = (1 - array_dm[i, j]) / (1 - array_cm[i, j])
                        array_cred_m[i, j] = array_cred_m[i, j] * array_dm[i, j]
                    else:
                        array_cred_m[i, j] = 0.0
        return MatrixOperations.get2DDirectMatrixMult(array_cred_m, array_cm)

    @staticmethod
    def getCredibilityMatrixEIV(
        array: np.ndarray,
        p: np.ndarray,
        q: np.ndarray,
        v: np.ndarray,
    ) -> np.ndarray:
        sq = 1.0
        sc = 0.8
        sp = 0.6
        ss = 0.4
        sv = 0.2
        k = 0
        a_comparison = np.zeros((array.shape[0] * array.shape[0], array.shape[1]), dtype=np.float64)
        a_veto = np.zeros((array.shape[0] * array.shape[0], array.shape[1]), dtype=np.float64)
        n = array.shape[0]
        array_mp_ab = np.zeros((n, n), dtype=np.float64)
        array_mq_ab = np.zeros((n, n), dtype=np.float64)
        array_mi_ab = np.zeros((n, n), dtype=np.float64)
        array_mo = np.zeros((n, n), dtype=np.float64)
        array_veto = np.zeros((n, n), dtype=np.float64)
        array_s = np.zeros((n, n), dtype=np.float64)
        array_m = np.zeros((n, n), dtype=np.float64)
        array_cred_m = np.zeros((n, n), dtype=np.float64)
        mp = 0.0
        mq = 0.0
        mi = 0.0
        mo = 0.0

        for i in range(array.shape[0]):
            for j in range(array.shape[0]):
                for r in range(array.shape[1]):
                    a_comparison[k, r] = array[j, r] - array[i, r]
                    a_veto[k, r] = array[j, r] - array[i, r]
                k += 1
        k = 0

        for i in range(array.shape[0]):
            for j in range(array.shape[0]):
                for r in range(array.shape[1]):
                    if a_comparison[k, r] > p[r]:
                        mp += 1
                k += 1
                array_mp_ab[i, j] = mp
                mp = 0.0
        k = 0

        for i in range(array.shape[0]):
            for j in range(array.shape[0]):
                for r in range(array.shape[1]):
                    if a_comparison[k, r] > q[r] and a_comparison[k, r] <= p[r]:
                        mq += 1
                k += 1
                array_mq_ab[i, j] = mq
                mq = 0.0
        k = 0

        for i in range(array.shape[0]):
            for j in range(array.shape[0]):
                for r in range(array.shape[1]):
                    if a_comparison[k, r] >= -q[r] and a_comparison[k, r] <= q[r] and a_comparison[k, r] > 0:
                        mi += 1
                k += 1
                array_mi_ab[i, j] = mi
                mi = 0.0
        k = 0

        for i in range(array.shape[0]):
            for j in range(array.shape[0]):
                for r in range(array.shape[1]):
                    if a_comparison[k, r] == 0:
                        mo += 1
                k += 1
                array_mo[j, i] = mo
                array_mo[i, j] = 0.0
                mo = 0.0
        k = 0

        for i in range(array.shape[0]):
            for j in range(array.shape[0]):
                for r in range(array.shape[1]):
                    if a_veto[k, r] >= -v[r]:
                        a_veto[k, r] = 1.0
                        if i != j:
                            array_veto[i, j] = 1.0
                k += 1
        k = 0

        array_mp_ba = MatrixOperations.getTransposed2DMatrix(array_mp_ab)
        array_mq_ba = MatrixOperations.getTransposed2DMatrix(array_mq_ab)
        array_mi_ba = MatrixOperations.getTransposed2DMatrix(array_mi_ab)

        for i in range(array.shape[0]):
            for j in range(array.shape[0]):
                array_s[i, j] = array_mp_ab[i, j] + array_mq_ab[i, j] + array_mi_ab[i, j] + array_mo[i, j]
        for i in range(array.shape[0]):
            for j in range(array.shape[0]):
                array_m[i, j] = array_s[i, j] + array_s[j, i]

        for i in range(array.shape[0]):
            for j in range(array.shape[0]):
                if array_mp_ab[i, j] == 0 or (
                    array_mp_ab[i, j] == 1
                    and array_mp_ba[i, j] >= array.shape[1] / 2
                    and array_veto[i, j] >= 1
                ):
                    array_cred_m[i, j] = sv
                if array_mp_ab[i, j] == 0:
                    array_cred_m[i, j] = ss
                if array_mp_ab[i, j] == 0 and array_mq_ab[i, j] <= array_mp_ba[i, j] + array_mq_ba[i, j]:
                    array_cred_m[i, j] = sp
                if (
                    array_mp_ab[i, j] == 0
                    and array_mq_ab[i, j] <= array_mq_ba[i, j]
                    and array_mq_ab[i, j] + array_mi_ab[i, j] <= array_mp_ba[i, j] + array_mq_ba[i, j] + array_mi_ba[i, j]
                ):
                    array_cred_m[i, j] = sc
                if (
                    array_mp_ab[i, j] + array_mq_ab[i, j] == 0
                    and array_mi_ab[i, j] <= array_mp_ba[i, j] + array_mq_ba[i, j] + array_mi_ba[i, j]
                ):
                    array_cred_m[i, j] = sq
                if i == j:
                    array_cred_m[i, j] = 0.0
        return array_cred_m

    @staticmethod
    def getCredibilityMatrixETri_x_bh(
        x: np.ndarray,
        p: np.ndarray,
        q: np.ndarray,
        v: np.ndarray,
        w: np.ndarray,
        bh: np.ndarray,
    ) -> np.ndarray:
        array_cm_x_bh = Concordance.getConcordanceMatrix_x_bh_ETri(x, p, q, w, bh)
        array_dm_x_bh = Discordance.getDiscordanceMatrix_x_bh_ETri(x, p, v, w, bh)
        array_temp_x_bh = np.zeros((x.shape[0] * bh.shape[0], x.shape[1]), dtype=np.float64)
        product_dm = np.zeros(x.shape[0] * bh.shape[0], dtype=np.float64)
        array_cred_m_x_bh = np.zeros(x.shape[0] * bh.shape[0], dtype=np.float64)
        for i in range(array_dm_x_bh.shape[0]):
            for j in range(array_dm_x_bh.shape[1]):
                if array_dm_x_bh[i, j] > array_cm_x_bh[i, array_dm_x_bh.shape[1]]:
                    array_temp_x_bh[i, j] = (
                        1 - array_dm_x_bh[i, j]
                    ) / (1 - array_cm_x_bh[i, array_dm_x_bh.shape[1]])
                else:
                    array_temp_x_bh[i, j] = 1.0
        for i in range(array_temp_x_bh.shape[0]):
            product_dm[i] = array_temp_x_bh[i, 0]
            for j in range(1, array_temp_x_bh.shape[1]):
                product_dm[i] = product_dm[i] * array_temp_x_bh[i, j]
        for i in range(array_dm_x_bh.shape[0]):
            for j in range(array_dm_x_bh.shape[1]):
                if array_dm_x_bh[i, j] > array_cm_x_bh[i, array_dm_x_bh.shape[1]]:
                    array_cred_m_x_bh[i] = array_cm_x_bh[i, array_dm_x_bh.shape[1]] * product_dm[i]
                    break
                else:
                    array_cred_m_x_bh[i] = array_cm_x_bh[i, array_dm_x_bh.shape[1]]
        return array_cred_m_x_bh

    @staticmethod
    def getCredibilityMatrixETri_bh_x(
        x: np.ndarray,
        p: np.ndarray,
        q: np.ndarray,
        v: np.ndarray,
        w: np.ndarray,
        bh: np.ndarray,
    ) -> np.ndarray:
        array_cm_bh_x = Concordance.getConcordanceMatrix_bh_x_ETri(x, p, q, w, bh)
        array_dm_bh_x = Discordance.getDiscordanceMatrix_bh_x_ETri(x, p, v, w, bh)
        array_temp_bh_x = np.zeros((x.shape[0] * bh.shape[0], x.shape[1]), dtype=np.float64)
        product_dm = np.zeros(x.shape[0] * bh.shape[0], dtype=np.float64)
        array_cred_m_bh_x = np.zeros(x.shape[0] * bh.shape[0], dtype=np.float64)
        for i in range(array_dm_bh_x.shape[0]):
            for j in range(array_dm_bh_x.shape[1]):
                if array_dm_bh_x[i, j] > array_cm_bh_x[i, array_dm_bh_x.shape[1]]:
                    array_temp_bh_x[i, j] = (
                        1 - array_dm_bh_x[i, j]
                    ) / (1 - array_cm_bh_x[i, array_dm_bh_x.shape[1]])
                else:
                    array_temp_bh_x[i, j] = 1.0
        for i in range(array_temp_bh_x.shape[0]):
            product_dm[i] = array_temp_bh_x[i, 0]
            for j in range(1, array_temp_bh_x.shape[1]):
                product_dm[i] = product_dm[i] * array_temp_bh_x[i, j]
        for i in range(array_dm_bh_x.shape[0]):
            for j in range(array_dm_bh_x.shape[1]):
                if array_dm_bh_x[i, j] > array_cm_bh_x[i, array_dm_bh_x.shape[1]]:
                    array_cred_m_bh_x[i] = array_cm_bh_x[i, array_dm_bh_x.shape[1]] * product_dm[i]
                    break
                else:
                    array_cred_m_bh_x[i] = array_cm_bh_x[i, array_dm_bh_x.shape[1]]
        return array_cred_m_bh_x
