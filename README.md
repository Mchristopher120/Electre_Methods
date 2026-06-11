# J-ELECTRE — Project Summary

This README gives a concise architecture overview, developer instructions to run the project, test it, and an overview of the work completed during the migration/modernization to a web API + React frontend.

1) Architecture overview
- Backend structure
  - FastAPI application (main.py) implements core API endpoints for ELECTRE methods.
  - matrix_electre/ package contains algorithm implementations (ELECTRE_I, ELECTRE_II, ELECTRE_III, ELECTRE_IV, ELECTRE_Tri and helpers: concordance, discordance, credibility, ranking, matrix operations).
  - api_models.py contains Pydantic request/response models and the new GraphData model used by graph endpoints.
  - tests/ contains pytest tests for graph endpoints.

- Frontend structure
  - frontend/ is a Vite + React application (Material UI) with pages for each ELECTRE method.
  - Pages: src/pages/* (ElectreIPage, ElectreISPage, ElectreIIPage, ElectreIIIPage, ElectreIVPage, ElectreTriPage).
  - Components: MatrixEditor, ParamInputs, ResultsTable, GraphViewCytoscape, Heatmap, and small Recharts-based visual components.

- Data flow
  - User fills matrices/parameters in React UI -> frontend calls REST endpoints (/electre/*) to compute algorithm tables -> frontend displays results table.
  - For visualization, frontend calls /graph/data/{method} to fetch structured GraphData (nodes, edges, positions, concordance/discordance/credibility matrices, rankings) -> GraphViewCytoscape renders graph; Recharts renders ranking/scatter/heatmap visualizations.

2) Backend
- API endpoints (implemented in main.py)
  - POST /electre/i           -> compute ELECTRE I (returns human-readable result block)
  - POST /electre/i_s         -> ELECTRE I_s
  - POST /electre/i_v         -> ELECTRE I_v
  - POST /electre/ii          -> ELECTRE II
  - POST /electre/iii         -> ELECTRE III
  - POST /electre/iv          -> ELECTRE IV
  - POST /electre/tri         -> ELECTRE Tri / Tri-ME
  - POST /graph/data/{method} -> structured graph data (GraphData) for method in [ei, ei_s, ei_v, ii, iii, iv, tri]

- Graph endpoints
  - Return a consistent GraphData JSON schema containing:
    - method: string
    - nodes: [{ id, label, position? }]
    - edges: [{ id, source, target, weight?, label? }]
    - dominance/concordance/discordance/credibility: numeric matrices (when available)
    - rankings: array of objects with numeric scores (asc/desc/avg) when available
    - metadata: free-form additional information (e.g., kernel, cycles)

- Request/response models
  - api_models.py defines Electre*Request models and GraphData, GraphNode, GraphEdge for OpenAPI documentation.

- How to run backend locally
  1. python -m venv .venv
  2. .\.venv\Scripts\activate
  3. pip install -r requirements.txt
  4. uvicorn main:app --reload --host 127.0.0.1 --port 8000
  5. Open http://127.0.0.1:8000/docs to see OpenAPI and example GraphData schema

3) Frontend
- Pages created
  - ElectreIPage, ElectreISPage, ElectreIIPage, ElectreIIIPage, ElectreIVPage, ElectreTriPage (src/pages)

- Components created
  - MatrixEditor.jsx (grid input for matrices)
  - ParamInputs.jsx (small controls for counts and numeric params)
  - ResultsTable.jsx (render result blocks)
  - GraphViewCytoscape.jsx (react-cytoscapejs wrapper consuming GraphData)
  - Heatmap.jsx (simple SVG heatmap with hover tooltips)
  - Recharts usage for ranking bar charts and scatter charts

- Cytoscape integration
  - GraphViewCytoscape posts to /graph/data/{method}, maps nodes/edges/positions to Cytoscape elements, and triggers a layout (uses circle or preset positions when provided).

- Recharts integration
  - Ranking bar charts (vertical layout) for EII/EIII/EIV using GraphData.rankings
  - Scatter chart for ETri (uses GraphData.nodes positions)

- How to run frontend locally
  1. cd frontend
  2. npm install
  3. npm run dev
  4. Open http://localhost:5173 (vite dev server). Vite has a proxy configured to forward /electre and /graph to http://127.0.0.1:8000 by default.

4) Testing
- Existing pytest tests
  - tests/test_graph_endpoints.py contains basic integration-style tests that call /graph/data/ei, /graph/data/ii and /graph/data/tri using FastAPI TestClient and assert structure keys.

- Coverage summary
  - Basic tests cover the graph endpoints for successful responses and key fields. Full unit coverage for all algorithm internals is not included.

- How to execute tests
  1. python -m venv .venv
  2. .\.venv\Scripts\activate
  3. pip install -r requirements.txt
  4. pip install pytest
  5. pytest -q

5) Remaining improvements
- Nice-to-have features
  - Improve rank/graph response with richer metadata (labels, alternative names)
  - Better UI layout and responsive design for small screens
  - Export/save graph images and CSV export for rankings
  - User-friendly presets for common parameter sets and sample datasets

- Performance improvements
  - Move heavy computations to optimized numeric routines (NumPy vectorization) or C extensions where necessary
  - Cache results for repeated requests (same input) and add server-side rate-limiting
  - Paginate or stream very large matrices

- Deployment recommendations
  - Package backend as Docker image and serve with Uvicorn + Gunicorn/Workers behind Nginx
  - Build frontend (npm run build) and serve static files behind CDN or Nginx; or deploy SPA to GitHub Pages while API runs separately
  - Add CI pipeline to run tests (GitHub Actions) and build artifacts

6) Notes and next steps
- Completed in this work:
  - Structured GraphData endpoints with numeric concordance/discordance/credibility/dominance/rankings
  - React SPA with Cytoscape visualizations, Recharts ranking/scatter charts, and Heatmap
  - Basic pytest tests and OpenAPI GraphData example

- Recommended next steps:
  1. Expand tests to cover all methods and edge-cases
  2. Add OpenAPI examples per method (currently GraphData example provided in model)
  3. Final UI polish and documentation (screenshots) before publishing on GitHub

Thank you — if you want, I can now:
- Commit and push these changes to the repository and open a PR (if you provide the remote),
- Or produce a smaller developer quickstart README in frontend/README.md and backend/README sections.
