# 📚 Key Papers Guide: Physics-Informed KAN for Plasma CO₂ Conversion

This directory contains the reading guides and download links for the three foundational papers underpinning this research project.

---

## 1. Paper 1 (AI & Machine Learning Architecture)
* **Title:** *KAN: Kolmogorov-Arnold Networks*
* **Authors:** Ziming Liu, Yixuan Wang, Sachin Vaidya, Fabian Ruehle, James Halverson, Marin Soljačić, Thomas Y. Hou, Max Tegmark (MIT, Caltech)
* **Preprint / Year:** arXiv:2404.19756 (2024)
* **Local PDF File:** [`Paper1_KAN_Liu_Tegmark_2024.pdf`](Paper1_KAN_Liu_Tegmark_2024.pdf) *(12.23 MB, fully downloaded in this folder)*
* **Online Direct PDF:** [https://arxiv.org/pdf/2404.19756.pdf](https://arxiv.org/pdf/2404.19756.pdf)
* **arXiv Abstract:** [https://arxiv.org/abs/2404.19756](https://arxiv.org/abs/2404.19756)

### What to Read:
1. **Section 2 (KAN Architecture):** Explains how KAN replaces fixed scalar weight matrices ($W \cdot x$) with learnable continuous 1D B-splines directly on the graph edges ($\phi(x)$).
2. **Section 3.1 & 3.2 (Symbolic Discovery & Interpretability):** Shows how trained 1D splines collapse into closed-form algebraic equations (the technique we used in `nopo_paper_pkg/symbolic_extractor.py`).
3. **Figure 2.1 & Figure 3.1:** Compare them directly to Tab 2 of your web application (`plasma_kan_dss_app.html`).

---

## 2. Paper 2 (Experimental Benchmark & 358-Run Database)
* **Title:** *Machine learning to predict plasma-based CO₂ conversion in dielectric barrier discharge reactors*
* **Authors:** Jiayin Li, Xinpei Lu, Pranav Arun, J. Xu, F. Gallucci, S. Li, and Annemie Bogaerts (PLASMANT, University of Antwerp)
* **Journal:** *Green Chemistry* (2026) / *Journal of CO₂ Utilization*
* **Official DOI:** [https://doi.org/10.1039/d6gc01077f](https://doi.org/10.1039/d6gc01077f)
* **Companion Paper (Glow Discharge ML):** [https://doi.org/10.1039/d5gc00301f](https://doi.org/10.1039/d5gc00301f)
* **Data Repository Source:** [https://data.4tu.nl](https://data.4tu.nl) / [Zenodo](https://zenodo.org)

### What to Read:
1. **Experimental Setup & Curation:** Explains the physical bounds of the 358 DBD reactor runs logged in your `data/plasma_co2_358_benchmark.csv`.
2. **Feature Mapping:** Specific Energy Input identity $\text{SEI} = \frac{P}{Q} \times 0.06\text{ kJ/L}$.
3. **Why Your Paper Beats Theirs:** Li et al. utilized classical black-box models (Random Forest, XGBoost, standard MLPs) which exhibit up to $14.96\%$ physical violations. Your paper introduces PI-VRBF-KAN to enforce monotonicity and eliminate violations ($0.00\%$).

---

## 3. Paper 3 (The Plasma Chemistry & Physics Mechanism)
* **Title:** *Plasma technology – a novel solution for CO₂ conversion?*
* **Authors:** Ramses Snoeckx and Annemie Bogaerts (PLASMANT Research Group, University of Antwerp)
* **Journal:** *Chemical Society Reviews*, 2017, 46, 5805–5863 (Royal Society of Chemistry)
* **Official DOI Link:** [https://doi.org/10.1039/C6CS00066E](https://doi.org/10.1039/C6CS00066E)
* **Publisher Article Page:** [https://pubs.rsc.org/en/content/articlelanding/2017/cs/c6cs00066e](https://pubs.rsc.org/en/content/articlelanding/2017/cs/c6cs00066e)
* **PubMed / Europe PMC:** [https://pubmed.ncbi.nlm.nih.gov/28825736/](https://pubmed.ncbi.nlm.nih.gov/28825736/)

### What to Read:
1. **Section 3 (Thermodynamic Fundamentals & Efficiency):** Explains why standard thermal conversion requires $>2000\text{ K}$, whereas non-thermal plasma exploits electron-impact vibrational excitation ($\text{CO}_2(v)$).
2. **The Reaction Energy Bound:** Direct dissociation requires $\Delta H^\circ_{298\text{K}} = 283\text{ kJ/mol} = 2.93\text{ eV/molecule}$, which forms the basis for your Energy Efficiency formula:
   $$\eta_{\text{EE}} = \chi_{\text{CO}_2} \times \frac{2.93\text{ eV}}{\text{SEI}_{\text{mol}}}$$
3. **The Trade-Off (Pareto Frontier):** Explains why high SEI leads to vibrational-translational ($V\text{-}T$) relaxation (gas heating losses), justifying your dashboard's **⭐ Optimal Trade-Off Preset** at $\text{SEI} \approx 16.2\text{ kJ/L}$.
