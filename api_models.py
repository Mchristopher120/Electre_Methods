from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field


Matrix = List[List[float]]


class ElectreResponse(BaseModel):
    result: List[List[Any]]


class GraphNode(BaseModel):
    id: str
    label: Optional[str] = None
    position: Optional[dict] = None  # {'x': float, 'y': float}
    metadata: Optional[dict] = None


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    weight: Optional[float] = None
    label: Optional[str] = None
    metadata: Optional[dict] = None


class GraphData(BaseModel):
    method: str
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    positions: Optional[List[List[float]]] = None
    dominance: Optional[Matrix] = None
    concordance: Optional[Matrix] = None
    discordance: Optional[Matrix] = None
    credibility: Optional[Matrix] = None
    rankings: Optional[List[dict]] = None  # e.g. [{'alt':'a1','rank':1,'value':0.5}, ...]
    metadata: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "method": "ii",
                "nodes": [{"id": "a1", "label": "a1"}, {"id": "a2", "label": "a2"}],
                "edges": [{"id": "e0_1", "source": "a1", "target": "a2", "weight": 1.0}],
                "dominance": [[0, 1], [0, 0]],
                "concordance": [[0.0, 0.6], [0.5, 0.0]],
                "discordance": [[0.0, 0.2], [0.1, 0.0]],
                "credibility": [[0, 1], [0, 0]],
                "rankings": [{"alt": "a1", "avg": 0.8}, {"alt": "a2", "avg": 0.2}],
                "metadata": {}
            }
        }


class ElectreIRequest(BaseModel):
    performance: Matrix = Field(..., description="Performance matrix (alternatives x criteria)")
    weights: List[float] = Field(..., description="Weights for criteria")
    ei_p: float = Field(..., description="ELECTRE I p threshold")
    ei_q: float = Field(..., description="ELECTRE I q threshold")


class ElectreISRequest(BaseModel):
    performance: Matrix
    weights: List[float]
    p: List[float]
    q: List[float]
    v: List[float]
    ei_s_lambda: float = 0.5
    maximum_cycles: int = 15


class ElectreIVRequest(BaseModel):
    performance: Matrix
    p: List[float]
    q: List[float]
    v: List[float]


class ElectreIVLikeRequest(BaseModel):
    performance: Matrix
    weights: Optional[List[float]] = None
    p: Optional[List[float]] = None
    q: Optional[List[float]] = None
    v: Optional[List[float]] = None
    # params for EII
    eii_cp: Optional[float] = None
    eii_c: Optional[float] = None
    eii_cm: Optional[float] = None
    eii_d1: Optional[float] = None
    eii_d2: Optional[float] = None
    maximum_cycles: int = 15


class ElectreTriRequest(BaseModel):
    x: Matrix
    p: List[float]
    q: List[float]
    v: List[float]
    w: List[float]
    bh: List[List[float]]
    electre: int = Field(..., description="7 for ETri, 8 for ETri-ME")
    cut_off: float
    num_criteria: int
    tri_me_evaluators: int = 2


# Pydantic v2: ensure any postponed/resolved forward refs are rebuilt for OpenAPI generation
try:
    for _m in (
        ElectreResponse,
        GraphData,
        ElectreIRequest,
        ElectreISRequest,
        ElectreIVRequest,
        ElectreIVLikeRequest,
        ElectreTriRequest,
    ):
        model_rebuild = getattr(_m, "model_rebuild", None)
        if callable(model_rebuild):
            _m.model_rebuild()
except Exception:
    # Best-effort; if pydantic version doesn't support model_rebuild this is a no-op
    pass
