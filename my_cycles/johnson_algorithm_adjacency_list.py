"""Adjacency list builder for Johnson algorithm."""

from __future__ import annotations

from typing import List


class JohnsonAlgorithm_AdjacencyList:
    @staticmethod
    def getAdjacencyList(adjacency_matrix: List[List[bool]]) -> List[List[int]]:
        adj_list: List[List[int]] = [[] for _ in range(len(adjacency_matrix))]
        for i in range(len(adjacency_matrix)):
            successors: List[int] = []
            for j in range(len(adjacency_matrix[i])):
                if adjacency_matrix[i][j]:
                    successors.append(j)
            adj_list[i] = successors
        return adj_list
