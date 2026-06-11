"""Johnson algorithm SCC result container."""

from __future__ import annotations

from typing import List, Set


class JohnsonAlgorithm_SCCResult:
    def __init__(self, adj_list: List[List[int]], lowest_node_id: int) -> None:
        self.adj_list: List[List[int]] = adj_list
        self.lowest_node_id: int = lowest_node_id
        self.node_ids_of_scc: Set[int] = set()
        if self.adj_list is not None:
            for i in range(self.lowest_node_id, len(self.adj_list)):
                if len(self.adj_list[i]) > 0:
                    self.node_ids_of_scc.add(i)

    def getAdjList(self) -> List[List[int]]:
        return self.adj_list

    def getLowestNodeId(self) -> int:
        return self.lowest_node_id
