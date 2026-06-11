"""Ranking matrix operations for ELECTRE II/III/IV."""

from __future__ import annotations

import numpy as np

from matrix_electre.matrix_operations import MatrixOperations


class Ranking:
    @staticmethod
    def matrixRanking(array: np.ndarray) -> np.ndarray:
        array_string = np.full((array.shape[0] + 1, array.shape[0] + 4), "", dtype=object)
        array_count = np.full((array.shape[0], 3), "0", dtype=object)
        array_total = np.full((array.shape[0], 2), "", dtype=object)
        array_double = np.zeros(array.shape[0], dtype=np.float64)
        str_a = ""
        str_b = ""

        for i in range(array.shape[0]):
            elementcount_pp = 0
            elementcount_pm = 0
            for j in range(array.shape[1]):
                if array[i, j] == "P+":
                    elementcount_pp += 1
                    array_count[i, 0] = str(elementcount_pp)
                if array[i, j] == "P-":
                    elementcount_pm += 1
                    array_count[i, 1] = str(elementcount_pm)
                array_count[i, 2] = str(elementcount_pp - elementcount_pm)

        for i in range(array_string.shape[0]):
            if i == 0:
                array_string[0, 0] = ""
            else:
                array_string[i, 0] = f"a{i}"
            for j in range(array_string.shape[1]):
                if j == 0:
                    array_string[0, 0] = ""
                elif j < array.shape[0] + 1:
                    array_string[0, j] = f"a{j}"
                elif j == array.shape[0] + 1:
                    array_string[0, j] = "P+"
                    array_string[0, j + 1] = "P-"
                    array_string[0, j + 2] = "T"
                if i > 0 and j > 0:
                    array_string[i, j] = ""
                if i > 0 and i < array.shape[0] + 1 and j > 0 and j < array.shape[0] + 1:
                    array_string[i, j] = array[i - 1, j - 1]
                if i > 0 and j > array.shape[0]:
                    array_string[i, j] = array_count[i - 1, j - (array.shape[0] + 1)]

        for i in range(array.shape[0]):
            array_double[i] = float(array_string[i + 1, array.shape[0] + 3])
            array_double[i] = array_double[i] + (array_total.shape[0] - 1)

        for i in range(array_total.shape[0]):
            array_total[i, 0] = array_string[i + 1, 0]
            array_total[i, 1] = str(int(array_count[i, 2]) + (array_total.shape[0] - 1))

        elementcount_i = 0
        for i in range(array.shape[0]):
            for j in range(i + 1, array.shape[1]):
                if array[i, j] == "I":
                    elementcount_i += 1

        if elementcount_i > 0:
            for i in range(array.shape[0]):
                for j in range(i + 1, array.shape[1]):
                    if array[i, j] == "I" and array_total[j, 0] != "NA":
                        array_total[i, 0] = array_total[i, 0] + "; " + array_total[j, 0]
                        array_total[j, 0] = "NA"
            for i in range(array_total.shape[0] - 1, -1, -1):
                if array_total[i, 0] == "NA":
                    array_total_list = array_total.tolist()
                    array_total_list = MatrixOperations.get2DRemoveRowString(array_total_list, i)
                    array_total = np.array(array_total_list, dtype=object)

        array_total_list = sorted(array_total.tolist(), key=lambda entry: int(entry[1]))
        array_total_complete = np.full((len(array_total_list), 2), "", dtype=object)
        for i in range(len(array_total_list) - 1, -1, -1):
            array_total_complete[(len(array_total_list) - 1) - i, 0] = array_total_list[i][0]
            array_total_complete[(len(array_total_list) - 1) - i, 1] = str(int(array_total_list[i][1]))

        array_rank_final = np.full(
            (array_total_complete.shape[0] + 1, array_total_complete.shape[0] + 1),
            "0.0",
            dtype=object,
        )
        array_rank_final[0, 0] = ""
        for i in range(array_total_complete.shape[0]):
            array_rank_final[i + 1, 0] = array_total_complete[i, 0]
            array_rank_final[0, i + 1] = array_total_complete[i, 0]

        array_list = np.full(
            (array_rank_final.shape[0] - 1, array_rank_final.shape[1] - 1),
            "",
            dtype=object,
        )
        for i in range(array_rank_final.shape[0] - 1):
            for j in range(array_rank_final.shape[1] - 1):
                array_list[i, j] = array_rank_final[i, j + 1]

        for j in range(array_list.shape[0] - 1):
            count = 0
            for i in range(j + 1, array_list.shape[1]):
                str_a = array_list[0, j]
                if str_a.find(";") >= 0:
                    str_a = str_a[: str_a.index(";")]
                str_b = array_list[0, i]
                if str_b.find(";") >= 0:
                    str_b = str_b[: str_b.index(";")]
                if MatrixOperations.get2DSearchString(str_a, str_b, array_string.tolist()) == "P+":
                    count += 1
                    array_list[count, j] = array_list[0, i]

        for j in range(array_list.shape[1] - 1, -1, -1):
            search = 1
            while search == 1:
                for i in range(array_list.shape[0] - 1, 0, -1):
                    str_a = array_list[i, j]
                    if str_a.find(";") >= 0:
                        str_a = str_a[: str_a.index(";")]
                    if str_a != "0.0":
                        for k in range(i - 1, -1, -1):
                            str_b = array_list[k, j]
                            if str_b.find(";") >= 0:
                                str_b = str_b[: str_b.index(";")]
                            if MatrixOperations.get2DSearchString(str_b, str_a, array_string.tolist()) == "P+":
                                search = 0
                                for m in range(array_rank_final.shape[0]):
                                    for n in range(array_rank_final.shape[1]):
                                        if array_rank_final[m, 0] == array_list[k, j] and array_rank_final[0, n] == array_list[i, j]:
                                            array_rank_final[m, n] = "1.0"
                                for del_idx in range(1, array_list.shape[0]):
                                    if array_list[del_idx, 0] == array_list[i, j]:
                                        array_list[del_idx, 0] = "0.0"
                                    if array_list[del_idx, j] == array_list[i, j]:
                                        array_list[del_idx, j] = "0.0"
                                k = -2
                search = 0
        return array_rank_final

    @staticmethod
    def matrixRanking_XY(array: np.ndarray) -> np.ndarray:
        array_xy = np.full((array.shape[0] - 1, 3), "", dtype=object)
        count = 0
        rank_pos = 0

        for i in range(array_xy.shape[0]):
            array_xy[i, 0] = array[i + 1, 0]
            array_xy[i, 1] = ""
            array_xy[i, 2] = ""

        for j in range(1, array.shape[1]):
            count = 0
            for i in range(1, array.shape[0]):
                if array[i, j] == "1.0":
                    count += 1
                    break
            if count == 0:
                array_xy[j - 1, 2] = f"{rank_pos}.0"
                rank_pos += 1

        for i in range(1, array.shape[0]):
            for j in range(1, array.shape[1]):
                if array[i, j] == "1.0" and array_xy[i - 1, 2] != "":
                    rank_pos = int(array_xy[i - 1, 2][: array_xy[i - 1, 2].index(".")])
                    array_xy[j - 1, 2] = f"{rank_pos + 1}.0"

        rank_pos = 0
        for i in range(1, array.shape[0]):
            for j in range(1, array.shape[1]):
                if array[i, j] == "1.0":
                    array_xy[j - 1, 1] = f"{rank_pos}.0"
                    rank_pos += 1
            if rank_pos > 0:
                break

        for i in range(1, array.shape[0]):
            for j in range(1, array.shape[1]):
                if array[i, j] == "1.0" and array_xy[i - 1, 1] != "":
                    array_xy[j - 1, 1] = array_xy[i - 1, 1]

        for i in range(array_xy.shape[0]):
            if array_xy[i, 1] == "":
                array_xy[i, 1] = "0.0"

        for i in range(array_xy.shape[0] - 1):
            for k in range(i + 1, array_xy.shape[0]):
                if array_xy[i, 1] == array_xy[k, 1] and array_xy[i, 2] == array_xy[k, 2]:
                    array_xy[k, 1] = f"{int(array_xy[i, 1][: array_xy[i, 1].index('.')]) + 1}.0"
        return array_xy
