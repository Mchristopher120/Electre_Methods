"""ELECTRE Tri / Tri-ME classification algorithm."""

from __future__ import annotations

import numpy as np

from matrix_electre.concordance import Concordance
from matrix_electre.credibility import Credibility
from matrix_electre.discordance import Discordance
from matrix_electre.electre_i import ELECTRE_I


class ELECTRE_Tri:
    @staticmethod
    def e_Tri_Algorithm(
        x: np.ndarray,
        p: np.ndarray,
        q: np.ndarray,
        v: np.ndarray,
        w: np.ndarray,
        bh: np.ndarray,
        electre: int,
        cut_off: float,
        num_criteria: int,
        tri_me_evaluators: int = 2,
        maximum_cycles: int = 15,
    ) -> np.ndarray:
        del maximum_cycles  # reserved for parity with interface signature
        array_cred_m_x_bh = Credibility.getCredibilityMatrixETri_x_bh(x, p, q, v, w, bh)
        array_cred_m_bh_x = Credibility.getCredibilityMatrixETri_bh_x(x, p, q, v, w, bh)
        array_cr = np.zeros((x.shape[0] * bh.shape[0], 2), dtype=np.float64)
        array_pr = np.full((x.shape[0], bh.shape[0]), "", dtype=object)
        array_cl = np.full((x.shape[0] + 1, 2), "", dtype=object)

        for j in range(array_cred_m_x_bh.shape[0]):
            array_cr[j, 0] = array_cred_m_x_bh[j]
            array_cr[j, 1] = array_cred_m_bh_x[j]

        k = 0
        for profile in range(bh.shape[0]):
            k = k * x.shape[0]
            for j in range(x.shape[0]):
                if array_cr[j + k, 0] >= cut_off and array_cr[j + k, 1] >= cut_off:
                    array_pr[j, profile] = "I"
                elif array_cr[j + k, 0] >= cut_off and array_cr[j + k, 1] < cut_off:
                    array_pr[j, profile] = ">"
                elif array_cr[j + k, 0] < cut_off and array_cr[j + k, 1] >= cut_off:
                    array_pr[j, profile] = "<"
                else:
                    array_pr[j, profile] = "R"
            k = profile + 1

        array_cl[0, 0] = "Pessimist"
        array_cl[0, 1] = "Optimist"
        for i in range(1, array_cl.shape[0]):
            array_cl[i, 0] = chr(bh.shape[0] + ord("A"))
            array_cl[i, 1] = chr(ord("A"))

        for i in range(array_pr.shape[0]):
            l_val = 0
            for profile in range(bh.shape[0]):
                l_val += 1
                if array_pr[i, bh.shape[0] - profile - 1] == ">":
                    array_cl[i + 1, 0] = chr((bh.shape[0] - l_val) + ord("A"))

        for i in range(array_pr.shape[0]):
            m_val = 0
            for profile in range(bh.shape[0]):
                m_val += 1
                if array_pr[i, profile] == "<":
                    array_cl[i + 1, 1] = chr(m_val + ord("A"))

        array_temp = Concordance.getConcordanceMatrix_x_bh_ETri(x, p, q, w, bh)
        array_output1 = ELECTRE_Tri._build_tri_concordance_output(
            array_temp, x, bh, electre, num_criteria, tri_me_evaluators, "Concordance c( ai;bh ):", "ai;bh"
        )
        array_temp = Concordance.getConcordanceMatrix_bh_x_ETri(x, p, q, w, bh)
        array_output2 = ELECTRE_Tri._build_tri_concordance_output(
            array_temp, x, bh, electre, num_criteria, tri_me_evaluators, "Concordance c( bh;ai ):", "bh;ai"
        )
        array_temp_d = Discordance.getDiscordanceMatrix_x_bh_ETri(x, p, v, w, bh)
        array_output3 = ELECTRE_Tri._build_tri_discordance_output(
            array_temp_d, x, bh, electre, num_criteria, tri_me_evaluators, "Discordance d( ai;bh ):", "ai;bh"
        )
        array_temp_d = Discordance.getDiscordanceMatrix_bh_x_ETri(x, p, v, w, bh)
        array_output4 = ELECTRE_Tri._build_tri_discordance_output(
            array_temp_d, x, bh, electre, num_criteria, tri_me_evaluators, "Discordance d( bh;ai ):", "bh;ai"
        )

        array_output5 = np.full((array_cred_m_x_bh.shape[0] + 2, 5), "", dtype=object)
        array_output5[0, 0] = "Credibility:"
        array_output5[0, 2] = "( ai;bh )"
        array_output5[0, 4] = "( bh;ai )"
        profilebh = bh.shape[0] + 1
        alt = 0
        for i in range(array_cred_m_x_bh.shape[0]):
            if i % x.shape[0] == 0:
                profilebh -= 1
                alt = 0
            else:
                alt += 1
            array_output5[i + 1, 1] = f"cr(a{alt + 1};b{profilebh})"
            array_output5[i + 1, 3] = f"cr(b{profilebh};a{alt + 1})"
        for i in range(array_cred_m_x_bh.shape[0]):
            array_output5[i + 1, 2] = str(round(float(array_cred_m_x_bh[i]) * 10000) / 10000)
            array_output5[i + 1, 4] = str(round(float(array_cred_m_bh_x[i]) * 10000) / 10000)

        array_output6 = np.full((x.shape[0] + 1, 5), "", dtype=object)
        array_output6[0, 0] = "Classification:"
        array_output6[0, 2] = "Alternative"
        array_output6[0, 3] = "Pessimist"
        array_output6[0, 4] = "Optmist"
        for i in range(x.shape[0]):
            array_output6[i + 1, 2] = f"a{i + 1}"
            array_output6[i + 1, 3] = array_cl[i + 1, 0]
            array_output6[i + 1, 4] = array_cl[i + 1, 1]

        blocks = [array_output1, array_output2, array_output3, array_output4, array_output5, array_output6]
        cols = max(block.shape[1] for block in blocks)
        array_final = np.full((sum(b.shape[0] for b in blocks), cols + 1), " ", dtype=object)
        offset = 0
        for block in blocks:
            ELECTRE_I._copy_block(array_final, block, offset)
            offset += block.shape[0]
        return array_final

    @staticmethod
    def _build_tri_concordance_output(
        array_temp: np.ndarray,
        x: np.ndarray,
        bh: np.ndarray,
        electre: int,
        num_criteria: int,
        tri_me_evaluators: int,
        title: str,
        direction: str,
    ) -> np.ndarray:
        array_output = np.full(
            (array_temp.shape[0] + 2, array_temp.shape[1] + 3), "", dtype=object
        )
        array_output[0, 0] = title
        array_output[0, array_temp.shape[1] + 1] = "C( a;b )" if direction == "ai;bh" else "C( b;a )"
        profilebh = bh.shape[0] + 1
        alt = 0
        f = 0
        e = tri_me_evaluators
        for i in range(array_temp.shape[0]):
            if i % x.shape[0] == 0:
                profilebh -= 1
                alt = 0
            else:
                alt += 1
            for j in range(array_temp.shape[1] - 1):
                if electre == 7:
                    array_output[0, j + 2] = f"g{j + 1}"
                if direction == "ai;bh":
                    array_output[i + 1, 1] = f"c(a{alt + 1};b{profilebh})"
                else:
                    array_output[i + 1, 1] = f"c(b{profilebh};a{alt + 1})"
        if electre == 8:
            for ev in range(1, e + 1):
                for crit in range(1, num_criteria + 1):
                    array_output[0, f + 2] = f"EV{ev}( g{crit} )"
                    if f + 1 <= x.shape[1] - 1:
                        f += 1
        for i in range(array_temp.shape[0]):
            for j in range(array_temp.shape[1] - 1):
                array_output[i + 1, j + 2] = str(round(float(array_temp[i, j]) * 10000) / 10000)
        for i in range(array_temp.shape[0]):
            array_output[i + 1, array_temp.shape[1] + 1] = str(
                round(float(array_temp[i, array_temp.shape[1] - 1]) * 10000) / 10000
            )
        return array_output

    @staticmethod
    def _build_tri_discordance_output(
        array_temp_d: np.ndarray,
        x: np.ndarray,
        bh: np.ndarray,
        electre: int,
        num_criteria: int,
        tri_me_evaluators: int,
        title: str,
        direction: str,
    ) -> np.ndarray:
        array_output = np.full(
            (array_temp_d.shape[0] + 2, array_temp_d.shape[1] + 2), "", dtype=object
        )
        array_output[0, 0] = title
        profilebh = bh.shape[0] + 1
        alt = 0
        f = 0
        e = tri_me_evaluators
        for i in range(array_temp_d.shape[0]):
            if i % x.shape[0] == 0:
                profilebh -= 1
                alt = 0
            else:
                alt += 1
            for j in range(array_temp_d.shape[1]):
                if electre == 7:
                    array_output[0, j + 2] = f"g{j + 1}"
                if direction == "ai;bh":
                    array_output[i + 1, 1] = f"d(a{alt + 1};b{profilebh})"
                else:
                    array_output[i + 1, 1] = f"d(b{profilebh};a{alt + 1})"
        if electre == 8:
            for ev in range(1, e + 1):
                for crit in range(1, num_criteria + 1):
                    array_output[0, f + 2] = f"EV{ev}( g{crit} )"
                    if f + 1 <= x.shape[1] - 1:
                        f += 1
        for i in range(array_temp_d.shape[0]):
            for j in range(array_temp_d.shape[1]):
                array_output[i + 1, j + 2] = str(round(float(array_temp_d[i, j]) * 10000) / 10000)
        return array_output
