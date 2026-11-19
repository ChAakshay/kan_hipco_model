# Symbolic Distillation Report: Plasma $\text{CO}_2$ Conversion Rate Laws

Closed-form analytical equations distilled directly from the trained Physics-Informed Variational RBF-KAN splines:

| Phenomenon | Symbolic Rate Law | Spline Fidelity ($R^2$) | Physical Mechanism |
| :--- | :--- | :--- | :--- |
| **SEI Dissociation Saturation** | `$\chi_{\text{CO}_2}(\text{SEI}) = 16.23\% + 59.97\% \cdot \left(1 - \exp\left(-0.010 \cdot \text{SEI}^{1.48}\right)\right)$` | **0.9988** | Non-equilibrium electron-impact saturation |
| **Energy Efficiency Roll-Off** | `$\eta_{\text{EE}}(\text{SEI}) = 58.2\% \cdot \left(1 - \exp\left(-1.00\text{SEI}\right)\right) \cdot \exp\left(-0.031\max(0, \text{SEI} - 5.0)\right)$` | **0.9147** | Vibrational excitation peak & thermal gas heating roll-off |
| **Sub-Atmospheric Vacuum Boost** | `$\chi_{\text{CO}_2}(P) = 25.00\% + 31.94(1 - P_{\text{reactor}}) + -25.28(1 - P_{\text{reactor}})^2$` | **0.9551** | Extended electron mean free path and higher $E/N$ |
| **Microgap Field Confinement** | `$\chi_{\text{CO}_2}(d_{\text{gap}}) = 20.74\% + 7.84\left(\frac{1.5\text{ mm}}{d_{\text{gap}}}\right) + -2.50\left(\frac{1.5\text{ mm}}{d_{\text{gap}}}\right)^2$` | **0.8682** | High local electric field strengthening microdischarges |
