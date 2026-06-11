"""Tarjan-based strongly connected components for Johnson algorithm."""

from __future__ import annotations

from typing import List, Optional

from my_cycles.johnson_algorithm_scc_result import JohnsonAlgorithm_SCCResult


class JohnsonAlgorithm_StrongConnectedComponents:
    def __init__(self, adj_list: List[List[int]]) -> None:
        self.adj_list_original: List[List[int]] = adj_list
        self.adj_list: List[List[int]] = []
        self.visited: List[bool] = []
        self.stack: List[int] = []
        self.lowlink: List[int] = []
        self.number: List[int] = []
        self.scc_counter: int = 0
        self.current_sccs: List[List[int]] = []

    def getAdjacencyList(self, node: int) -> Optional[JohnsonAlgorithm_SCCResult]:
        self.visited = [False] * len(self.adj_list_original)
        self.lowlink = [0] * len(self.adj_list_original)
        self.number = [0] * len(self.adj_list_original)
        self.stack = []
        self.current_sccs = []

        self._make_adj_list_subgraph(node)

        for i in range(node, len(self.adj_list_original)):
            if not self.visited[i]:
                self._get_strong_connected_components(i)
                nodes = self._get_lowest_id_component()
                if (
                    nodes is not None
                    and node not in nodes
                    and (node + 1) not in nodes
                ):
                    return self.getAdjacencyList(node + 1)
                adjacency_list = self._get_adj_list(nodes)
                if adjacency_list is not None:
                    for j in range(len(self.adj_list_original)):
                        if len(adjacency_list[j]) > 0:
                            return JohnsonAlgorithm_SCCResult(adjacency_list, j)
        return None

    def _make_adj_list_subgraph(self, node: int) -> None:
        self.adj_list = [[] for _ in range(len(self.adj_list_original))]
        for i in range(node, len(self.adj_list)):
            successors: List[int] = []
            for j in self.adj_list_original[i]:
                if j >= node:
                    successors.append(j)
            self.adj_list[i] = successors

    def _get_lowest_id_component(self) -> Optional[List[int]]:
        min_id = len(self.adj_list)
        curr_scc: Optional[List[int]] = None
        for scc in self.current_sccs:
            for node in scc:
                if node < min_id:
                    curr_scc = scc
                    min_id = node
        return curr_scc

    def _get_adj_list(self, nodes: Optional[List[int]]) -> Optional[List[List[int]]]:
        if nodes is None:
            return None
        lowest_id_adjacency_list: List[List[int]] = [[] for _ in range(len(self.adj_list))]
        node_set = set(nodes)
        for node in nodes:
            for succ in self.adj_list[node]:
                if succ in node_set:
                    lowest_id_adjacency_list[node].append(succ)
        return lowest_id_adjacency_list

    def _get_strong_connected_components(self, root: int) -> None:
        self.scc_counter += 1
        self.lowlink[root] = self.scc_counter
        self.number[root] = self.scc_counter
        self.visited[root] = True
        self.stack.append(root)

        for w in self.adj_list[root]:
            if not self.visited[w]:
                self._get_strong_connected_components(w)
                self.lowlink[root] = min(self.lowlink[root], self.lowlink[w])
            elif self.number[w] < self.number[root]:
                if w in self.stack:
                    self.lowlink[root] = min(self.lowlink[root], self.number[w])

        if self.lowlink[root] == self.number[root] and len(self.stack) > 0:
            scc: List[int] = []
            while True:
                next_node = self.stack.pop()
                scc.append(next_node)
                if self.number[next_node] <= self.number[root]:
                    break
            if len(scc) > 1:
                self.current_sccs.append(scc)
