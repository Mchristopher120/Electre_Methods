"""Concordance matrix computations for ELECTRE methods."""

from __future__ import annotations

import numpy as np

from matrix_electre.matrix_operations import MatrixOperations


class Concordance:
    @staticmethod
    def getConcordanceMatrixEI(array: np.ndarray, weights: np.ndarray) -> np.ndarray:
        n = array.shape[0]
        array_cm = np.zeros((n, n), dtype=np.float64)
        array_nw = MatrixOperations.getNormalizedWeigths(weights)
        for j in range(array.shape[0]):
            for i in range(array.shape[0]):
                if i == j:
                    array_cm[i, j] = 0.0
                else:
                    for k in range(array.shape[1]):
                        if array[i, k] >= array[j, k]:
                            array_cm[i, j] += array_nw[k]
        return array_cm

    @staticmethod
    def getConcordanceMatrixEI_s(
        array: np.ndarray,
        weights: np.ndarray,
        p: np.ndarray,
        q: np.ndarray,
    ) -> np.ndarray:
        n = array.shape[0]
        array_cm = np.zeros((n, n), dtype=np.float64)
        array_cm_temp = np.zeros(array.shape[1], dtype=np.float64)
        for i in range(array.shape[0]):
            for j in range(array.shape[0]):
                if i == j:
                    array_cm[i, j] = 1.0
                else:
                    for k in range(array.shape[1]):
                        if array[j, k] >= p[k] + array[i, k]:
                            array_cm_temp[k] = 0.0 * weights[k]
                        if array[j, k] <= q[k] + array[i, k]:
                            array_cm_temp[k] = 1.0 * weights[k]
                        if (array[j, k] - array[i, k]) < p[k] and (array[j, k] - array[i, k]) > q[k]:
                            array_cm_temp[k] = (
                                ((array[j, k] - array[i, k]) - p[k]) / (q[k] - p[k])
                            ) * weights[k]
                    array_cm[i, j] = (
                        MatrixOperations.getWeightsSum(array_cm_temp)
                        / MatrixOperations.getWeightsSum(weights)
                    )
        return array_cm

    @staticmethod
    def getConcordanceMatrixEI_v(array: np.ndarray, weights: np.ndarray) -> np.ndarray:
        n = array.shape[0]
        array_cm = np.zeros((n, n), dtype=np.float64)
        array_nw = MatrixOperations.getNormalizedWeigths(weights)
        for j in range(array.shape[0]):
            for i in range(array.shape[0]):
                if i == j:
                    array_cm[i, j] = 0.0
                else:
                    for k in range(array.shape[1]):
                        if array[i, k] >= array[j, k]:
                            array_cm[i, j] += array_nw[k]
        return array_cm

    @staticmethod
    def getConcordanceMatrixEII(array: np.ndarray, weights: np.ndarray) -> np.ndarray:
        n = array.shape[0]
        array_cm = np.zeros((n, n), dtype=np.float64)
        array_nw = MatrixOperations.getNormalizedWeigths(weights)
        for j in range(array.shape[0]):
            for i in range(array.shape[0]):
                if i == j:
                    array_cm[i, j] = 0.0
                else:
                    for k in range(array.shape[1]):
                        if array[i, k] >= array[j, k]:
                            array_cm[i, j] += array_nw[k]
        return array_cm

    @staticmethod
    def getConcordanceMatrixEIII(
        array: np.ndarray,
        weights: np.ndarray,
        p: np.ndarray,
        q: np.ndarray,
    ) -> np.ndarray:
        n = array.shape[0]
        array_cm = np.zeros((n, n), dtype=np.float64)
        array_cm_temp = np.zeros(array.shape[1], dtype=np.float64)
        for i in range(array.shape[0]):
            for j in range(array.shape[0]):
                if i == j:
                    array_cm[i, j] = 0.0
                else:
                    for k in range(array.shape[1]):
                        if array[j, k] >= p[k] + array[i, k]:
                            array_cm_temp[k] = 0.0 * weights[k]
                        if array[j, k] <= q[k] + array[i, k]:
                            array_cm_temp[k] = 1.0 * weights[k]
                        if (array[j, k] - array[i, k]) < p[k] and (array[j, k] - array[i, k]) > q[k]:
                            array_cm_temp[k] = (
                                ((array[j, k] - array[i, k]) - p[k]) / (q[k] - p[k])
                            ) * weights[k]
                    array_cm[i, j] = (
                        MatrixOperations.getWeightsSum(array_cm_temp)
                        / MatrixOperations.getWeightsSum(weights)
                    )
        return array_cm

    @staticmethod
    def getConcordanceMatrix_x_bh_ETri(
        x: np.ndarray,
        p: np.ndarray,
        q: np.ndarray,
        w: np.ndarray,
        bh: np.ndarray,
    ) -> np.ndarray:
        array_cm = np.zeros((x.shape[0] * bh.shape[0], x.shape[1] + 1), dtype=np.float64)
        c = 0.0
        k = 0
        for profile in range(bh.shape[0]):
            k = k * x.shape[0]
            for i in range(x.shape[0]):
                for j in range(x.shape[1]):
                    if bh[profile, j] - x[i, j] >= p[j]:
                        array_cm[i + k, j] = 0.0
                    elif bh[profile, j] - x[i, j] < q[j]:
                        array_cm[i + k, j] = 1.0
                    else:
                        array_cm[i + k, j] = (p[j] - bh[profile, j] + x[i, j]) / (p[j] - q[j])
                for count in range(x.shape[1]):
                    c = array_cm[i + k, count] * w[count] + c
                array_cm[i + k, x.shape[1]] = c / MatrixOperations.getWeightsSum(w)
                c = 0.0
            k = profile + 1
        return array_cm

    @staticmethod
    def getConcordanceMatrix_bh_x_ETri(
        x: np.ndarray,
        p: np.ndarray,
        q: np.ndarray,
        w: np.ndarray,
        bh: np.ndarray,
    ) -> np.ndarray:
        array_cm = np.zeros((x.shape[0] * bh.shape[0], x.shape[1] + 1), dtype=np.float64)
        c = 0.0
        k = 0
        for profile in range(bh.shape[0]):
            k = k * x.shape[0]
            for i in range(x.shape[0]):
                for j in range(x.shape[1]):
                    if x[i, j] - bh[profile, j] >= p[j]:
                        array_cm[i + k, j] = 0.0
                    elif x[i, j] - bh[profile, j] < q[j]:
                        array_cm[i + k, j] = 1.0
                    else:
                        array_cm[i + k, j] = (p[j] - x[i, j] + bh[profile, j]) / (p[j] - q[j])
                for count in range(x.shape[1]):
                    c = array_cm[i + k, count] * w[count] + c
                array_cm[i + k, x.shape[1]] = c / MatrixOperations.getWeightsSum(w)
                c = 0.0
            k = profile + 1
        return array_cm
