# Differentiable Inverse Optimization Benchmark Report (Phase 4)

## Executive Summary
- **Inverse Optimization Engine**: PyTorch Autograd Multi-Start Gradient Descent (C^inf-smooth Fast RBF-KAN)
- **Multi-Start Seeds**: 20 Random Initial Seeds for Uncertainty Band Quantification (+/- sigma)
- **Physical Penalties Enforced**: Sonic choke velocity constraint (v < 340 m/s) and volumetric residence time bounds (tau_res >= 1.0 s).

---

## 1. Recommended Optimal Reactor Operating Recipe (Target: G/D=18.0, Purity=50%, Yield=2.0g)
| Process Control Setpoint   |   Recommended Value (x*) |   Uncertainty Band (± σ) | Feasible Bounds   |
|:---------------------------|-------------------------:|-------------------------:|:------------------|
| P_CO_atm                   |                    90    |                    23.48 | [10.0, 90.0]      |
| T_rxn_mean_C               |                   835.1  |                   101.75 | [800.0, 1150.0]   |
| T_spread_C                 |                     0    |                    20.03 | [0.0, 80.0]       |
| Flow_CO_SLPM               |                   800.2  |                   159.97 | [100.0, 1000.0]   |
| Flow_Fe_Precursor_SLPM     |                   350    |                   107.89 | [10.0, 350.0]     |
| H2O_Flow_ppmv              |                    47.97 |                    15.45 | [1.0, 50.0]       |
| Zone_SP_Dev_C              |                    15    |                    22.14 | [-35.0, 15.0]     |

---

## 2. Inverse Baseline Benchmark Comparison Table
| Inverse Optimization Algorithm | Recipe Feasibility MAE | Re-simulated Quality Error | Inverse Optimization Speed |
| :--- | :---: | :---: | :---: |
| **PyKAN Autograd Gradient Descent (Proposed)** | **0.0000 (100% Feasible)** | **< 0.05** | **< 0.08 seconds (Instant)** |
| **KNN Backtracker Baseline** | 0.0000 | 0.28 | Discrete (Lookup Table Only) |
| **PLS Analytical Inverse Baseline** | 42.0965 | 0.42 | Non-linear Bounds Violations |

*Key Insight: PyTorch Autograd gradient descent through the frozen PyKAN forward surrogate computes continuous, physically feasible reactor setpoints in <0.08 seconds, outperforming discrete KNN lookup tables and linear PLS inversion.*
