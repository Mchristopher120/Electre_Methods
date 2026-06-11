"""Discordance matrix computations for ELECTRE methods."""

from __future__ import annotations

import numpy as np

from matrix_electre.concordance import Concordance
from matrix_electre.matrix_operations import MatrixOperations


class Discordance:
    @staticmethod
    def getDiscordanceMatrixEI(array: np.ndarray) -> np.ndarray:
        n = array.shape[0]
        array_dm = np.zeros((n, n), dtype=np.float64)
        array_dm_temp = np.zeros(array.shape[1], dtype=np.float64)
        array_delta = MatrixOperations.getDelta(array)
        delta = MatrixOperations.getMaxValueInRowNonSorting(array_delta)
        for j in range(array.shape[0]):
            for i in range(array.shape[0]):
                if i == j:
                    array_dm[i, j] = 0.0
                else:
                    for k in range(array.shape[1]):
                        array_dm_temp[k] = array[j, k] - array[i, k]
                    array_dm_temp = np.sort(array_dm_temp)
                    if array_dm_temp[-1] >= 0:
                        array_dm[i, j] = array_dm_temp[-1] / delta
                    else:
                        array_dm[i, j] = 0.0
        return array_dm

    @staticmethod
    def getDiscordanceMatrixEI_s(
        c: float,
        array: np.ndarray,
        weights: np.ndarray,
        p: np.ndarray,
        q: np.ndarray,
        v: np.ndarray,
        k: int,
        ei_s_lambda: float,
    ) -> np.ndarray:
        n = array.shape[0]
        array_dmj = np.zeros((n, n), dtype=np.float64)
        array_cm = Concordance.getConcordanceMatrixEI_s(array, weights, p, q)
        array_w = MatrixOperations.getNormalizedWeigths(weights)
        c = ei_s_lambda
        for i in range(array.shape[0]):
            for j in range(array.shape[0]):
                if array[j, k] - array[i, k] < v[k] - q[k] * (
                    (1 - array_cm[i, j]) - array_w[k]
                ) / (1 - c - array_w[k]):
                    array_dmj[i, j] = 0.0
                else:
                    array_dmj[i, j] = 1.0
        return array_dmj

    @staticmethod
    def getDiscordanceMatrixEI_v(array: np.ndarray, v: np.ndarray) -> np.ndarray:
        n = array.shape[0]
        array_dm = np.zeros((n, n), dtype=np.float64)
        for i in range(array.shape[0]):
            for j in range(array.shape[0]):
                if i == j:
                    array_dm[i, j] = 0.0
                else:
                    for k in range(array.shape[1]):
                        if array[j, k] - array[i, k] >= v[k]:
                            array_dm[i, j] = 1.0
                            break
        return array_dm

    @staticmethod
    def getDiscordanceMatrixEII(array: np.ndarray) -> np.ndarray:
        array_dm_temp = np.zeros(array.shape[1], dtype=np.float64)
        n = array.shape[0]
        array_dm = np.zeros((n, n), dtype=np.float64)
        array_delta = MatrixOperations.getDelta(array)
        delta = MatrixOperations.getMaxValueInRowSorting(array_delta)
        for j in range(array.shape[0]):
            for i in range(array.shape[0]):
                if i == j:
                    array_dm[i, j] = 0.0
                else:
                    for k in range(array.shape[1]):
                        array_dm_temp[k] = array[j, k] - array[i, k]
                    array_dm_temp = np.sort(array_dm_temp)
                    if array_dm_temp[-1] >= 0:
                        array_dm[i, j] = array_dm_temp[-1] / delta
                    else:
                        array_dm[i, j] = 0.0
        return array_dm

    @staticmethod
    def getDiscordanceMatrixEIII(
        array: np.ndarray,
        p: np.ndarray,
        v: np.ndarray,
        k: int,
    ) -> np.ndarray:
        n = array.shape[0]
        array_dmj = np.zeros((n, n), dtype=np.float64)
        dm_temp = 0.0
        for i in range(array.shape[0]):
            for j in range(array.shape[0]):
                if i == j:
                    array_dmj[i, j] = 0.0
                else:
                    if array[j, k] <= p[k] + array[i, k]:
                        dm_temp = 0.0
                    if array[j, k] >= v[k] + array[i, k]:
                        dm_temp = 1.0
                    if (array[j, k] - array[i, k]) > p[k] and (array[j, k] - array[i, k]) < v[k]:
                        dm_temp = ((array[j, k] - array[i, k]) - p[k]) / (v[k] - p[k])
                    array_dmj[i, j] = dm_temp
        return array_dmj

    @staticmethod
    def getDiscordanceMatrix_x_bh_ETri(
        x: np.ndarray,
        p: np.ndarray,
        v: np.ndarray,
        w: np.ndarray,
        bh: np.ndarray,
    ) -> np.ndarray:
        array_dm = np.zeros((x.shape[0] * bh.shape[0], x.shape[1]), dtype=np.float64)
        k = 0
        for profile in range(bh.shape[0]):
            k = k * x.shape[0]
            for i in range(x.shape[0]):
                for j in range(x.shape[1]):
                    if bh[profile, j] - x[i, j] < p[j]:
                        array_dm[i + k, j] = 0.0
                    elif bh[profile, j] - x[i, j] >= v[j]:
                        array_dm[i + k, j] = 1.0
                    else:
                        array_dm[i + k, j] = (-p[j] + bh[profile, j] - x[i, j]) / (v[j] - p[j])
            k = profile + 1
        return array_dm

    @staticmethod
    def getDiscordanceMatrix_bh_x_ETri(
        x: np.ndarray,
        p: np.ndarray,
        v: np.ndarray,
        w: np.ndarray,
        bh: np.ndarray,
    ) -> np.ndarray:
        array_dm = np.zeros((x.shape[0] * bh.shape[0], x.shape[1]), dtype=np.float64)
        k = 0
        for profile in range(bh.shape[0]):
            k = k * x.shape[0]
            for i in range(x.shape[0]):
                for j in range(x.shape[1]):
                    if x[i, j] - bh[profile, j] < p[j]:
                        array_dm[i + k, j] = 0.0
                    elif x[i, j] - bh[profile, j] >= v[j]:
                        array_dm[i + k, j] = 1.0
                    else:
                        array_dm[i + k, j] = (-p[j] + x[i, j] - bh[profile, j]) / (v[j] - p[j])
            k = profile + 1
        return array_dm
