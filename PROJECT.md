# Project: HiPCO KAN Decision Support System (DSS)

## Architecture
The HiPCO KAN Decision Support System provides a comprehensive scientific computing and industrial optimization platform for carbon nanotube synthesis. The architecture consists of:
1. **Neural Surrogate Foundation (`kan_model.py`)**: PyTorch `FastRBFKANLinear` Gaussian RBF basis expansion with dual-path SiLU residual connections and forward evaluation.
2. **Symbolic Extraction Engine (`symbolic_extractor.py`)**: Translates trained KAN continuous spline manifolds into explicit, closed-form chemical kinetic rate laws (Arrhenius, Boudouard, Langmuir-Hinshelwood) via SymPy with BIC-based curve snapping, graph pruning, and LaTeX/Python exports.
3. **Inverse Optimizer & Epistemic Uncertainty Engine (`inverse_optimizer.py`)**:
   - Epistemic Uncertainty Quantification ($\sigma_{\text{epistemic}}$ vs $\sigma_{\text{aleatoric}}$) via Monte Carlo ensemble perturbation and Operator Confidence scoring.
   - Comprehensive Noise Stress-Testing Suite ($\pm 1\% \dots \pm 10\%$ OAT, multivariate Monte Carlo, and adversarial perturbations) with Degradation Slope and Robustness Index calculation.
   - Multi-Objective Pareto Frontier Solvers: Batched PyTorch Autograd Weighted Tchebycheff Decomposition with Smooth-Max LogSumExp, native NSGA-II evolutionary algorithm, 3D Lebesgue hypervolume calculation, and automated knee-point detection.
4. **Interactive Web DSS Dashboard (`hipco_kan_dss_app.html`)**:
   - Industrial 4-tab interface featuring Plotly.js 3D WebGL Pareto Frontier visualization with point-click setpoint loading.
   - Live radial epistemic confidence gauges and sensitivity perturbation bands.
   - KaTeX-rendered symbolic chemical rate laws with parameter exploration.
   - Standalone client-side physics fallback + REST API backend synchronization (`run_gui.py`).
5. **Quality Assurance & Verification**: DOM validator (`verify_gui.py`) and full-spectrum E2E test suite (Tiers 1-4 requirement-driven opaque-box testing + Tier 5 adversarial white-box hardening).

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | `FastRBFtoSymPyConverter` | Analytical translation of FastRBFKANLinear weights into SymPy symbolic expression trees | M1 | Survey R1 |
| 2 | `SymbolicSnapper` & 9 Kinetic Classes | Curve fitting of 1D spline activations against 9 kinetic classes (Arrhenius, Boudouard, Langmuir-Hinshelwood, etc.) with BIC selection | M1 | Survey R1 |
| 3 | L1 Node & Edge Graph Pruning | Saliency-based pruning of low-magnitude activation paths ($\theta = 0.05$) to yield compact symbolic expressions | M1 | Survey R1 |
| 4 | Multi-Layer Algebraic Composition | End-to-end composition of Layer 0 and Layer 1 activations with physical unscaling to real reactor units | M1 | Survey R1 |
| 5 | Kinetic Derivative & Energy Extraction | Calculation of effective activation energies ($E_a^{\text{eff}}$), reaction orders ($n_P$), and flow elasticities ($S_Q$) | M1 | Survey R1 |
| 6 | Symbolic Export & CLI | Export of SymPy formulas, LaTeX equations, callable NumPy functions, and JSON dictionaries via `python nopo_paper_pkg/symbolic_extractor.py` | M1 | Survey R1 |
| 7 | Epistemic Uncertainty Estimator | Monte Carlo parameter perturbation and ensemble predictive variance decomposition ($\sigma_{\text{epistemic}}$ vs $\sigma_{\text{aleatoric}}$) | M2 | Survey R2 |
| 8 | Operator Confidence Metric | Dynamic confidence scoring ($0 - 100\%$) and out-of-distribution (OOD) safety warning flags | M2 | Survey R2 |
| 9 | One-At-A-Time (OAT) Stress Suite | Sensitivity sweeps ($\pm 1\% \dots \pm 10\%$) evaluating directional elasticity across all 7 setpoints | M2 | Survey R2 |
| 10 | Multivariate Monte Carlo Noise Stress | $K=1000$ trial multivariate perturbation sweeps measuring MARE, maximum degradation, and physics feasibility retention | M2 | Survey R2 |
| 11 | Worst-Case Adversarial Perturbation | Gradient-directed adversarial perturbation measuring worst-case surrogate degradation | M2 | Survey R2 |
| 12 | Resilience & Robustness Metrics | Calculation of Degradation Slope ($\beta_{\text{deg}}$), Robustness Index ($\text{RI}$), and stress test export tables | M2 | Survey R2 |
| 13 | Conflicting 3-Objective Modeling | Mathematical formulation of tri-objective trade-off: Maximize Yield, Maximize Raman $G/D$, Minimize Metal Residues | M3 | Survey R3 |
| 14 | Batched Weighted Tchebycheff Solver | PyTorch Autograd batched Tchebycheff scalarization with Smooth-Max LogSumExp for real-time (<150ms) Pareto solving | M3 | Survey R3 |
| 15 | Native NSGA-II Evolutionary Solver | Real-coded NSGA-II with SBX crossover, polynomial mutation, and non-dominated crowding distance ranking | M3 | Survey R3 |
| 16 | 3D Hypervolume & Knee-Point Metric | Exact 3D Lebesgue hypervolume measure computation and automated nadir-utopia distance knee-point detection | M3 | Survey R3 |
| 17 | Epistemic-Regularized Inverse Optimizer | Multi-start Adam optimizer incorporating epistemic risk penalty into objective loss | M3 | Survey R3 |
| 18 | Plotly.js 3D WebGL Pareto Visualizer | Interactive 3D scatter plot ($Y$ vs $G/D$ vs Fe) with point-click setpoint injection into reactor sliders | M4 | Survey R4 |
| 19 | Radial Epistemic Confidence Gauges | Live animated gauges showing model confidence %, epistemic variance, and OOD safety status | M4 | Survey R4 |
| 20 | KaTeX Symbolic Kinetic Rate Law Viewer | Interactive equation viewer rendering closed-form chemical rate equations with LaTeX typography and parameter cards | M4 | Survey R4 |
| 21 | 4-Tab Industrial Dashboard Architecture | Organized tab layout (3D Pareto, Digital Twin, Uncertainty & Stress, Symbolic Laws) with industrial presets | M4 | Survey R4 |
| 22 | Standalone Offline & REST Backend API | Offline client-side simulation engine + REST API endpoints (`/api/solve_pareto`, `/api/get_symbolic_laws`, `/api/noise_stress_test`) in `run_gui.py` | M4 | Survey R4 |
| 23 | DOM & GUI Automated Verification | Automated GUI verification harness in `verify_gui.py` validating all element IDs, charts, and interaction handlers | M4 | Survey R4 |
| 24 | E2E Requirement-Driven Test Suite | Comprehensive opaque-box test suite covering Tiers 1-4 (>=11*N test cases) across all modules | M5 | E2E Track |
| 25 | Adversarial Coverage Hardening (Tier 5) | White-box adversarial testing and stress hardening via Challenger-Worker-Reviewer loop | M5 | Final Hardening |

## Milestones
| # | Name | Scope | Dependencies | Status | Sub-Orch ID |
|---|------|-------|-------------|--------|-------------|
| M1 | Symbolic Extraction Engine | Implement `nopo_paper_pkg/symbolic_extractor.py` (Features 1-6) | none | IN_PROGRESS | `805612e2-2340-44fb-b219-911713822d92` |
| M2 | Epistemic Uncertainty & Noise Stress-Testing | Expand `nopo_paper_pkg/inverse_optimizer.py` (Features 7-12) | none | IN_PROGRESS | `604208c8-46f6-44a4-98b0-6354b052e7f6` |
| M3 | Multi-Objective Pareto Frontier Solver | Integrate Pareto Solvers in `nopo_paper_pkg/inverse_optimizer.py` (Features 13-17) | M2 | PLANNED | - |
| M4 | Advanced Web DSS UI Integration | Upgrade `hipco_kan_dss_app.html`, `run_gui.py`, `verify_gui.py` (Features 18-23) | M1, M3 | PLANNED | - |
| M5 | Final Milestone: E2E Verification & Adversarial Hardening | Phase 1: 100% E2E Pass (Tiers 1-4); Phase 2: Tier 5 Adversarial Hardening (Features 24-25) | M1, M2, M3, M4, E2E Track | PLANNED | - |

## Parallel E2E Testing Track
| # | Name | Scope | Dependencies | Status | Sub-Orch ID |
|---|------|-------|-------------|--------|-------------|
| E2E | Opaque-Box Requirement-Driven Test Suite | Build test infrastructure and Tiers 1-4 test cases; publish `TEST_READY.md` | none | IN_PROGRESS | `c194d04b-a994-4663-8ad7-b08aded29b78` |

## Interface Contracts

### M1 (`symbolic_extractor.py`) ↔ M4 (Web DSS & Backend)
- **Functions**:
  - `extract_symbolic_models(checkpoint_path=None) -> Dict[str, Any]`
  - `get_kinetic_rate_laws() -> Dict[str, Dict[str, Union[str, float]]]`
- **JSON Structure**:
  ```json
  {
    "status": "success",
    "equations": {
      "boudouard_rate": {"latex": "...", "text": "...", "r2": 0.964, "ea_kj_mol": 124.8},
      "nucleation_rate": {"latex": "...", "text": "...", "r2": 0.948, "theta_k": 12000.0},
      "gd_ratio": {"latex": "...", "text": "...", "r2": 0.931, "dominant_terms": ["T_rxn", "P_CO"]}
    }
  }
  ```

### M2/M3 (`inverse_optimizer.py`) ↔ M4 (Web DSS & Backend)
- **Functions**:
  - `solve_pareto_frontier(n_points=50, algorithm="tchebycheff") -> Dict[str, Any]`
  - `run_noise_stress_suite(recipe_dict, noise_levels=[0.01, 0.05, 0.10]) -> Dict[str, Any]`
  - `predict_with_epistemic_confidence(setpoints_tensor) -> Tuple[Tensor, Tensor, float]`
- **Pareto JSON Structure**:
  ```json
  {
    "status": "success",
    "hypervolume": 0.842,
    "knee_point_idx": 22,
    "knee_recipe": {"P_CO_atm": 65.0, "T_rxn_mean_C": 980.0, ...},
    "pareto_solutions": [
      {"id": 0, "setpoints": {...}, "yield_g": 2.1, "gd_ratio": 18.5, "fe_ppm": 270000, "confidence": 0.95, "is_knee": true}
    ]
  }
  ```

## Code Layout
```
c:/Users/aaksh/Downloads/paper/
├── .agents/                                 # Agent coordination metadata ONLY
├── hipco_kan_dss_app.html                   # Advanced Web DSS Dashboard (M4)
├── nopo_paper_pkg/
│   ├── kan_model.py                         # PyTorch FastRBFKANLinear neural architecture
│   ├── forward_pipeline.py                  # Phase 3 forward KAN training & benchmarking
│   ├── inverse_optimizer.py                 # Inverse optimizer, Epistemic Uncertainty & Pareto Solvers (M2, M3)
│   ├── symbolic_extractor.py                # Symbolic extraction engine & kinetic laws (M1)
│   ├── synthetic_generator.py               # Phase 2 synthetic dataset generator
│   ├── evaluate_dataset.py                  # Dataset moments & statistical validation
│   ├── run_gui.py                           # HTTP server with REST APIs (M4)
│   ├── verify_gui.py                        # DOM and GUI validation test script (M4)
│   └── test_e2e_suite.py                    # Comprehensive E2E test suite (E2E Track)
```
