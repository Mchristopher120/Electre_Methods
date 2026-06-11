"""Johnson elementary cycle search."""

from __future__ import annotations

from typing import List, Optional

from my_cycles.johnson_algorithm_adjacency_list import JohnsonAlgorithm_AdjacencyList
from my_cycles.johnson_algorithm_strong_connected_components import JohnsonAlgorithm_StrongConnectedComponents


class JohnsonAlgorithm_ElementaryCyclesSearch:
    def __init__(
        self,
        matrix: List[List[bool]],
        graph_nodes: List[object],
        maximum_cycles: int = 15,
    ) -> None:
        self.graph_nodes: List[object] = graph_nodes
        self.adj_list: List[List[int]] = JohnsonAlgorithm_AdjacencyList.getAdjacencyList(matrix)
        self.maximum_cycles: int = maximum_cycles
        self.cycles: List[List[object]] = []
        self.blocked: List[bool] = []
        self.b_lists: List[List[int]] = []
        self.stack: List[int] = []

    def getElementaryCycles(self) -> List[List[object]]:
        self.cycles = []
        self.blocked = [False] * len(self.adj_list)
        self.b_lists = [[] for _ in range(len(self.adj_list))]
        self.stack = []
        sccs = JohnsonAlgorithm_StrongConnectedComponents(self.adj_list)
        s = 0

        while True:
            scc_result = sccs.getAdjacencyList(s)
            if scc_result is not None and scc_result.getAdjList() is not None:
                scc = scc_result.getAdjList()
                s = scc_result.getLowestNodeId()
                for j in range(len(scc)):
                    if scc[j] is not None and len(scc[j]) > 0:
                        self.blocked[j] = False
                        self.b_lists[j] = []
                self._find_cycles(s, s, scc)
                s += 1
            else:
                break
        return self.cycles

    def _find_cycles(self, v: int, s: int, adj_list: List[List[int]]) -> bool:
        f = False
        self.stack.append(v)
        self.blocked[v] = True
        for w in adj_list[v]:
            if w == s:
                cycle = [self.graph_nodes[index] for index in self.stack]
                if len(self.cycles) + 1 > self.maximum_cycles:
                    break
                self.cycles.append(cycle)
                f = True
            elif not self.blocked[w]:
                if self._find_cycles(w, s, adj_list):
                    f = True
        if f:
            self._unblock(v)
        else:
            for w in adj_list[v]:
                if v not in self.b_lists[w]:
                    self.b_lists[w].append(v)
        self.stack.remove(v)
        return f

    def _unblock(self, node: int) -> None:
        self.blocked[node] = False
        b_node = self.b_lists[node]
        while len(b_node) > 0:
            w = b_node.pop(0)
            if self.blocked[w]:
                self._unblock(w)
