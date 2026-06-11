# InterfaceElectre UI → FastAPI mapping

This document explains the Java Swing UI (guiELECTRE/InterfaceElectre.java) inputs, parameters, buttons, outputs and how each UI action maps to the FastAPI endpoints added to this repository.

---

## High-level
- The GUI stores the current algorithm in `InterfaceElectre.electre` (values 1..8).
- Main editable input: `JTable table` (single editable grid). Output display: `JTable table_1`.
- Many JSpinner controls provide algorithm thresholds and parameters.
- When the user clicks Solve the GUI:
  - reads numbers from `table` and `JSpinner`s,
  - calls the Java algorithm implementation (ELECTRE_* classes),
  - writes JS files via `jsElectre.writeFile_*` into `graph/`, and populates `table_1` with formatted output.

---

## User input fields (UI controls)

- JTable `table` (editable matrix). The GUI arranges the top rows and left column for parameter labels and the rest for numerical inputs. Which rows/columns are used depends on the selected `electre` variant.
- JTable `table_1` — output/result table filled by Solve.
- Spinners (selected names and default models):
  - `spinnerEIQ` (lblEIQ): EI Q, SpinnerNumberModel(0,0,1,0.01) default 0.0
  - `spinnerEIP` (lblEIP): EI P, SpinnerNumberModel(0,0,1,0.01) default 0.0
  - `spinnerEI_sLambda` (lblEI_sLambda): EI_s Lambda, SpinnerNumberModel(0.5,0.5,1,0.01) default 0.5
  - `spinnerEI_vQ` / `spinnerEI_vP`: EI_v thresholds (defaults 0)
  - `spinnerEIICm`, `spinnerEIIC`, `spinnerEIICp`: EII c-, c, c+ parameters (defaults 0.5 in UI)
  - `spinnerEIId1`, `spinnerEIId2`: EII d- / d+ (defaults 0.0)
  - `spinnerETriB`: ETri classes (SpinnerNumberModel(2,2,100,1)) default 2
  - `spinnerETriMeB`, `spinnerETriMeE`: ETri-ME classes & evaluators
  - `spinnerETri_Lambda`, `spinnerETriMe_Lambda`: ETri lambda defaults 0.5
  - `spinnerEI_sCycles`, `spinnerEIICycles`: cycle counts (default 30)
  - `spinnerA`: number of alternatives (actions) (default 2)
  - `spinnerC`: number of criteria (default 2)

The Java code replaces commas with dots and parses table cell strings into doubles.

---

## Algorithm parameters (where set/read)

- ELECTRE I (electre == 1):
  - weights: row 0, cols 1..p
  - performance: rows 1..q, cols 1..p
  - thresholds: `spinnerEIP` (ei_p), `spinnerEIQ` (ei_q)

- ELECTRE I_s (electre == 2):
  - weights: table row 3
  - v: table row 2
  - p: table row 1
  - q: table row 0
  - performance: rows 4.. (alternatives start at row index 4)
  - `spinnerEI_sLambda` and `spinnerEI_sCycles`

- ELECTRE I_v (electre == 3):
  - weights: table row 1
  - v: table row 0
  - performance: rows starting at index 2
  - `spinnerEI_vP` and `spinnerEI_vQ`

- ELECTRE II (electre == 4):
  - weights: table row 0
  - performance: rows 1..q
  - EII parameters from spinners: `spinnerEIICm`, `spinnerEIIC`, `spinnerEIICp`, `spinnerEIId1`, `spinnerEIId2`, `spinnerEIICycles`

- ELECTRE III (electre == 5):
  - weights: table row 3
  - v: row 2, p: row 1, q: row 0
  - performance: rows 4.. (alternatives)

- ELECTRE IV (electre == 6):
  - performance: rows starting at index 2
  - v: row 2, p: row 1, q: row 0

- ELECTRE Tri (electre == 7):
  - `spinnerETriB` determines number of profile rows (`e_bh`). The first `e_bh - 1` rows of the table are the profile `bh` matrix.
  - alternatives appear after the profile rows and header rows; weights, p,q,v are read from offsets computed in code.
  - `spinnerETri_Lambda` (ETri_Lambda)

- ELECTRE Tri-ME (electre == 8):
  - Like ETri but p is multiplied by `ETriMe_Evaluators` and columns are grouped per evaluator.

---

## Buttons and actions

- `btnBuildMatrix` (Matrix): configure `table` shape (rows/columns and header labels) depending on selected `electre` and values of `spinnerA` (alternatives) and `spinnerC` (criteria).
- `buttonSolve` (Solve): main action. Implementation does:
  1. Reads spinner values (thresholds/params)
  2. Reads table cells (weights, performance, p/q/v as required)
  3. Calls Java algorithm (ELECTRE_I.e_I_Algorithm, ELECTRE_I_s.e_I_s_Algorithm, etc.)
  4. Extracts specific output blocks (dominance matrix, kernel, ranking, cycles, classification) from the returned formatted 2D string arrays
  5. Calls `jsElectre.writeFile_*` to write graph JS files under `graph/` and populates `table_1` with the returned output

- `buttonGraph` (Graph): opens the appropriate HTML page under `graph/` (each HTML loads the JS written by `jsElectre`).
- `buttonSave` (Save): writes table_1 to a text file via `Export.xt` (local save).

---

## Output tables and contents

- `table_1` is set to display the formatted result returned by the ELECTRE methods. Typical blocks included:
  - Concordance matrix (or per-criterion concordance)
  - Discordance matrix (or per-criterion discordance)
  - Credibility matrix
  - Dominance / kernel / dominated (ELECTRE I variants)
  - Cycles (ELECTRE I_s)
  - Ranking blocks (ELECTRE II/III/IV: ascend/descend/average)
  - Classification and projection for ETri/ETri-ME

The Java code expects the algorithm functions to return formatted arrays of strings (with labels). The API endpoints added to the Python port currently return the algorithm outputs as lists — those outputs may be mixed strings and numbers.

---

## Graph files and mapping

- jsElectre writes JS files and the GUI opens HTML pages. Mapping is:
  - electre == 1 -> `graph/electre_i.js` + HTML `graph_01_e_i_.html`
  - electre == 2 -> `graph/electre_i_s.js` + HTML `graph_01_e_i_s.html`
  - electre == 3 -> `graph/electre_i_v.js` + HTML `graph_01_e_i_v.html`
  - electre == 4 -> `graph/electre_ii.js`  + HTML `graph_02_e_ii_.html`
  - electre == 5 -> `graph/electre_iii.js` + HTML `graph_03_e_iii_.html`
  - electre == 6 -> `graph/electre_iv.js`  + HTML `graph_04_e_iv_.html`
  - electre == 7 -> `graph/electre_tri.js` + HTML `graph_05_e_tri_.html`
  - electre == 8 -> `graph/electre_tri_me.js` + HTML `graph_05_e_tri_me.html`

Each HTML uses Sigma.js to present nodes (alternatives) and directed edges derived from the dominance matrix. Kernel alternatives are colored differently.

---

## UI action → FastAPI endpoint mapping

The FastAPI endpoints implemented in `main.py` and the request models in `api_models.py` are the target back-end equivalents for the Java Solve actions.

- ELECTRE I (Solve) → POST `/electre/i` (ElectreIRequest)
  - performance: alternatives × criteria (from table rows 1..q)
  - weights: from table row 0
  - ei_p, ei_q: from `spinnerEIP`, `spinnerEIQ`

- ELECTRE I_s → POST `/electre/i_s` (ElectreISRequest)
  - performance: alternatives × criteria (rows start at index 4 in GUI)
  - weights: table row 3
  - p, q, v: table rows 1, 0, 2 respectively
  - ei_s_lambda, maximum_cycles: spinner values

- ELECTRE I_v → POST `/electre/i_v` (ElectreIVLikeRequest expected fields)
  - performance: alternatives × criteria (rows starting at index 2)
  - weights: table row 1
  - v: table row 0
  - thresholds: provided using `eii_cp`/`eii_c` fields in the server model (convention used in Python port)

- ELECTRE II → POST `/electre/ii` (ElectreIVLikeRequest with EII params)
  - performance: table rows 1..q
  - weights: table row 0
  - eii_cp, eii_c, eii_cm, eii_d1, eii_d2, maximum_cycles: from spinners

- ELECTRE III → POST `/electre/iii` (ElectreIVLikeRequest)
  - performance: table rows 4.. (depending on GUI layout)
  - weights & p,q,v read as in GUI mapping above

- ELECTRE IV → POST `/electre/iv` (ElectreIVRequest)
  - performance: table rows starting at index 2
  - p,q,v from top rows

- ELECTRE Tri / Tri-ME → POST `/electre/tri` (ElectreTriRequest)
  - x: performance matrix (alternatives × criteria)
  - w, p, q, v: from GUI offsets described above
  - bh: profile matrix (first `e_bh - 1` rows from the table)
  - electre: 7 or 8
  - cut_off: cutoff value used by classification (GUI provides this value at algorithm call site)
  - num_criteria, tri_me_evaluators: spinner values

---

## Notes, caveats and recommended next steps

- The Java GUI expects formatted string outputs (blocks). The Python endpoints return algorithm outputs converted to lists; some output can mix strings and numbers. If you want a more structured, typed OpenAPI schema, add per-endpoint response models that separate numeric matrices (concordance/discordance/credibility) and metadata (kernel vector, cycles, ranking tables).
- To fully replicate the Java graph flow in a web UI: either:
  1. Let the server return the graph arrays (dominance matrix and kernel vector) — add endpoints to return specifically the graph data (instead of writing JS files to disk), or
  2. Keep the file-based approach (`jsElectre.writeFile_*`) but have the server produce those JS resources and expose them statically.

If you want, I can:
- Add example JSON payloads for each electre variant built from the exact GUI offsets.
- Add specialized response models so OpenAPI documents typed response structures for each method.
- Add endpoints that return the graph arrays (dominance matrix + kernel vector) so a web client can fetch and render graphs directly.

---

Generated from: `guiELECTRE/InterfaceElectre.java` (analysis of the Solve, Build Matrix and Graph flows).
