"""Matrix utility operations for ELECTRE algorithms."""

from __future__ import annotations

import numpy as np


class MatrixOperations:
    @staticmethod
    def getWeightsSum(array: np.ndarray) -> float:
        return float(np.sum(array))

    @staticmethod
    def getCriterionSum(array: np.ndarray, j: int) -> float:
        sum_val = 0.0
        for i in range(array.shape[1]):
            sum_val += array[i, j]
        return sum_val

    @staticmethod
    def getNormalizedWeigths(array: np.ndarray) -> np.ndarray:
        array_nw = np.zeros(array.shape, dtype=np.float64)
        sum_val = MatrixOperations.getWeightsSum(array)
        for i in range(array.shape[0]):
            array_nw[i] = array[i] / sum_val
        return array_nw

    @staticmethod
    def getColumnSum(array: np.ndarray) -> np.ndarray:
        array_c = np.zeros(array.shape[1], dtype=np.float64)
        for j in range(array.shape[1]):
            for i in range(array.shape[0]):
                array_c[j] += array[i, j]
        return array_c

    @staticmethod
    def getRowSum(array: np.ndarray) -> np.ndarray:
        array_r = np.zeros(array.shape[0], dtype=np.float64)
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                array_r[i] += array[i, j]
        return array_r

    @staticmethod
    def getNormalizedPerformanceMatrix(array: np.ndarray) -> np.ndarray:
        array_npm = np.zeros(array.shape, dtype=np.float64)
        a = MatrixOperations.getColumnSum(array)
        for j in range(array.shape[1]):
            for i in range(array.shape[0]):
                array_npm[i, j] = array[i, j] / a[j]
        return array_npm

    @staticmethod
    def getMaxValueInColumn(array: np.ndarray) -> np.ndarray:
        array_max = np.zeros(array.shape[1], dtype=np.float64)
        for j in range(array.shape[1]):
            max_val = array[0, j]
            for i in range(array.shape[0]):
                if array[i, j] >= max_val:
                    max_val = array[i, j]
                    array_max[j] = array[i, j]
        return array_max

    @staticmethod
    def getMaxValueInColumnJ(array: np.ndarray, j: int) -> float:
        max_val = -100001.0
        for i in range(array.shape[0]):
            if array[i, j] >= max_val:
                max_val = array[i, j]
        return max_val

    @staticmethod
    def getMinValueInColumn(array: np.ndarray) -> np.ndarray:
        array_min = np.zeros(array.shape[1], dtype=np.float64)
        for j in range(array.shape[1]):
            min_val = array[0, j]
            for i in range(array.shape[0]):
                if array[i, j] <= min_val:
                    min_val = array[i, j]
                    array_min[j] = array[i, j]
        return array_min

    @staticmethod
    def getMinValueInColumnJ(array: np.ndarray, j: int) -> float:
        min_val = 100001.0
        for i in range(array.shape[0]):
            if array[i, j] <= min_val:
                min_val = array[i, j]
        return min_val

    @staticmethod
    def getMaxValueInRowSorting(array: np.ndarray) -> float:
        sorted_array = np.sort(array.copy())
        return float(sorted_array[-1])

    @staticmethod
    def getMaxValueInRowNonSorting(array: np.ndarray) -> float:
        max_val = -100001.0
        if array.shape[0] == 1:
            max_val = float(array[0])
        for i in range(array.shape[0]):
            if max_val < array[i]:
                max_val = float(array[i])
        return max_val

    @staticmethod
    def getMinValueInRowNonSorting(array: np.ndarray) -> float:
        min_val = 100001.0
        for i in range(array.shape[0]):
            if min_val > array[i]:
                min_val = float(array[i])
        return min_val

    @staticmethod
    def getDelta(array: np.ndarray) -> np.ndarray:
        a = MatrixOperations.getMaxValueInColumn(array)
        b = MatrixOperations.getMinValueInColumn(array)
        array_delta = np.zeros(array.shape[1], dtype=np.float64)
        for i in range(array.shape[1]):
            array_delta[i] = a[i] - b[i]
        return array_delta

    @staticmethod
    def getElementCountZero(array: np.ndarray) -> int:
        elementcount = 0
        for i in range(array.shape[0]):
            if array[i] == 0:
                elementcount += 1
        return elementcount

    @staticmethod
    def get2DElementCountSpecificValue(array: np.ndarray, b: float) -> int:
        elementcount = 0
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                if array[i, j] == b:
                    elementcount += 1
        return elementcount

    @staticmethod
    def getTransposed2DMatrix(array: np.ndarray) -> np.ndarray:
        array_t2d = np.zeros((array.shape[1], array.shape[0]), dtype=np.float64)
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                array_t2d[j, i] = array[i, j]
        return array_t2d

    @staticmethod
    def get2DMatrixSum(array1: np.ndarray, array2: np.ndarray) -> np.ndarray:
        array_s2d = np.zeros(array1.shape, dtype=np.float64)
        for i in range(array1.shape[0]):
            for j in range(array1.shape[1]):
                array_s2d[i, j] = array1[i, j] + array2[i, j]
        return array_s2d

    @staticmethod
    def get2DMatrixTotalSum(array: np.ndarray) -> float:
        total = 0.0
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                total += array[i, j]
        return total

    @staticmethod
    def get2DDirectMatrixMult(array1: np.ndarray, array2: np.ndarray) -> np.ndarray:
        array_m2d = np.zeros((array1.shape[0], array1.shape[0]), dtype=np.float64)
        for i in range(array1.shape[0]):
            for j in range(array1.shape[1]):
                array_m2d[i, j] = array1[i, j] * array2[i, j]
        return array_m2d

    @staticmethod
    def get2DRemoveRow(array1: np.ndarray, row: int) -> np.ndarray:
        array_rd = np.zeros((array1.shape[0] - 1, array1.shape[1]), dtype=np.float64)
        p = 0
        for i in range(array1.shape[0]):
            if i == row:
                continue
            q = 0
            for j in range(array1.shape[1]):
                array_rd[p, q] = array1[i, j]
                q += 1
            p += 1
        return array_rd

    @staticmethod
    def get2DSearchString(r: str, c: str, array: list[list[str]]) -> str:
        value = "Not Found!"
        for i in range(1, len(array)):
            for j in range(1, len(array[0])):
                if array[i][0] == r and array[0][j] == c:
                    return array[i][j]
        return value

    @staticmethod
    def get2DSearchStringUpper(r: str, c: str, array: list[list[str]]) -> str:
        value = "Not Found!"
        for i in range(1, len(array)):
            for j in range(i + 1, len(array[0])):
                if array[i][0] == r and array[0][j] == c:
                    return array[i][j]
        return value

    @staticmethod
    def get2DRemoveColumn(array1: np.ndarray, column: int) -> np.ndarray:
        array_rd = np.zeros((array1.shape[0], array1.shape[1] - 1), dtype=np.float64)
        p = 0
        for i in range(array1.shape[0]):
            q = 0
            for j in range(array1.shape[1]):
                if j == column:
                    continue
                array_rd[p, q] = array1[i, j]
                q += 1
            p += 1
        return array_rd

    @staticmethod
    def get2DRemoveColumnString(array1: list[list[str]], column: int) -> list[list[str]]:
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

    @staticmethod
    def get2DRemoveRowString(array1: list[list[str]], row: int) -> list[list[str]]:
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
