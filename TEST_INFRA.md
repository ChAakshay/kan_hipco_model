# E2E Test Infra: HiPCO KAN Decision Support System

## Test Philosophy
- Opaque-box, requirement-driven testing derived strictly from `ORIGINAL_REQUEST.md` and user-facing specifications.
- Independent decomposition: tests exercise functional interfaces without coupling to internal private methods.
- Methodology: Category-Partition + Boundary Value Analysis (BVA) + Pairwise Combinatorial + Real-World Workload Testing.

## Feature Inventory Coverage Matrix
| # | Feature Area | Requirement Reference | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---|--------------|-----------------------|:------:|:------:|:------:|:------:|
| 1 | `symbolic_extractor.py` Closed-Form Extraction | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 2 | SymPy Analyticalsnapping (9 Kinetic Classes) | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 3 | Saliency Graph Pruning & Physical Unscaling | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 4 | Effective Activation Energy & Kinetic Derivatives | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 5 | Symbolic Export (LaTeX, SymPy, JSON, Python) | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 6 | Epistemic Uncertainty Estimation ($\sigma_{\text{epistemic}}$) | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 7 | Operator Confidence Metric & OOD Warning | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 8 | Noise Stress-Testing Suite ($\pm 1\% \dots \pm 10\%$) | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 9 | Surrogate Resilience Metrics ($\beta_{\text{deg}}, \text{RI}$) | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 10 | Tri-Objective Trade-Off (Yield vs G/D vs Metals) | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ | ✓ |
| 11 | Batched Weighted Tchebycheff Solver | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ | ✓ |
| 12 | Native NSGA-II Evolutionary Solver | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ | ✓ |
| 13 | 3D Lebesgue Hypervolume & Knee Point Detection | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ | ✓ |
| 14 | Web DSS 3D WebGL Pareto Visualizer | ORIGINAL_REQUEST §R4 | 5 | 5 | ✓ | ✓ |
| 15 | Live Epistemic Confidence Gauges & Sensitivity | ORIGINAL_REQUEST §R4 | 5 | 5 | ✓ | ✓ |
| 16 | KaTeX Symbolic Kinetic Rate Law Viewer | ORIGINAL_REQUEST §R4 | 5 | 5 | ✓ | ✓ |
| 17 | 4-Tab Industrial Dashboard Layout & Presets | ORIGINAL_REQUEST §R4 | 5 | 5 | ✓ | ✓ |
| 18 | Standalone Offline Fallback & REST Backend APIs | ORIGINAL_REQUEST §R4 | 5 | 5 | ✓ | ✓ |

## Test Architecture
- Test Runner: `python nopo_paper_pkg/test_e2e_suite.py`
- Test Framework: Standalone Python `unittest` / programmatic test runner with formatted reporting.
- Pass/Fail Semantics: Exit code 0 on all tests passing; nonzero on failure.

## Real-World Application Scenarios (Tier 4)
| # | Scenario | Features Exercised | Target Physical Goal |
|---|----------|--------------------|---------------------|
| 1 | Electronic-Grade Semiconductor Optimization | F1-F5, F10-F13, F14 | High Crystallinity ($G/D \ge 25$), Fe $< 150,000$ ppm |
| 2 | High-Volume Industrial Bulk Production | F6-F9, F10-F13, F17 | Maximum Yield ($\ge 3.0$ g), Feasible Sonic Velocity ($v \le 340$ m/s) |
| 3 | Sensor Malfunction & Extreme Noise Perturbation | F7-F9, F11, F15 | Robustness under $\pm 10\%$ Flow/Pressure sensor drift |
| 4 | Offline Standalone Field Deployment | F14-F18 | Complete UI execution without backend server connection |
| 5 | Closed-Form Kinetic Parameter Auditing | F1-F5, F16 | Validation of extracted $E_a$ ($60 - 180$ kJ/mol) against literature |

## Minimum Thresholds
- Tier 1: $\ge 90$ test cases ($5 \times 18$ features)
- Tier 2: $\ge 90$ test cases ($5 \times 18$ features)
- Tier 3: $\ge 18$ cross-feature interaction test cases
- Tier 4: $\ge 5$ end-to-end application scenarios
- **Total Minimum**: $\ge 203$ comprehensive test cases.
