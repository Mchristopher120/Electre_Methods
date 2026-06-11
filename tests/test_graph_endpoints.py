import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def basic_performance(n=2,m=2):
    return [[1.0 for _ in range(m)] for __ in range(n)]

def test_graph_ei():
    body = {"performance": basic_performance(), "weights": [1.0, 1.0], "ei_p": 0.5, "ei_q": 0.2}
    r = client.post('/graph/data/ei', json=body)
    assert r.status_code == 200
    data = r.json()
    assert 'nodes' in data and 'edges' in data

def test_graph_ii():
    body = {"performance": basic_performance(), "weights": [1.0,1.0], "eii_cp":0.5, "eii_c":0.5}
    r = client.post('/graph/data/ii', json=body)
    assert r.status_code == 200
    data = r.json()
    assert 'concordance' in data and 'credibility' in data

def test_graph_tri():
    body = {"x": basic_performance(), "p":[0.0,0.0], "q":[0.0,0.0], "v":[0.0,0.0], "w":[1.0,1.0], "bh":[[0.5,0.5]], "electre":7, "cut_off":0.5, "num_criteria":2, "tri_me_evaluators":2}
    r = client.post('/graph/data/tri', json=body)
    assert r.status_code == 200
    data = r.json()
    assert 'nodes' in data and 'rankings' in data
