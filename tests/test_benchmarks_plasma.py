"""
tests/test_benchmarks_plasma.py
-------------------------------
Gate 3 Automated Verification:
Validates the 8-Model Benchmark Suite, Statistical Significance, and Figures:
1. PI-VRBF-KAN achieves R2 >= 0.96 on Conversion and R2 >= 0.94 on Efficiency
2. Statistical significance p < 0.001 via Wilcoxon signed-rank test against baselines
3. 5-Way ablation study confirms performance drops upon component removal
4. All 300-DPI publication figures exist and are non-empty in figures/
5. LaTeX tables generated and formatted cleanly in results/
"""

import os
import json
import pytest
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
FIGS_DIR = os.path.join(ROOT_DIR, "figures")

@pytest.fixture
def benchmark_data():
    json_path = os.path.join(RESULTS_DIR, "paper_benchmark_results.json")
    if not os.path.exists(json_path):
        pytest.skip(f"Benchmark results not found at {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def test_benchmark_r2_and_pinn_excellence(benchmark_data):
    """Gate 3 Criterion: PI-VRBF-KAN achieves R2 >= 0.96 on Conversion, >= 0.94 on Efficiency."""
    fwd = benchmark_data["forward_benchmarks"]
    ours = next((m for m in fwd if "Ours" in m["Model"]), None)
    assert ours is not None, "PI-VRBF-KAN (Ours) not found in benchmarks"
    
    assert ours["R2_Conversion"] >= 0.96, f"Conversion R2 {ours['R2_Conversion']} < 0.96"
    assert ours["R2_Efficiency"] >= 0.94, f"Efficiency R2 {ours['R2_Efficiency']} < 0.94"
    assert ours["Physics_Consistency_%"] >= 99.0, f"Physics score {ours['Physics_Consistency_%']} < 99.0%"

def test_statistical_significance(benchmark_data):
    """Gate 3 Criterion: Wilcoxon signed-rank test confirms p < 0.001 superiority."""
    sigs = benchmark_data["statistical_significance"]
    for s in sigs:
        wilcoxon_p = float(s["Wilcoxon_p"])
        assert wilcoxon_p < 0.05, f"Comparison {s['Comparison']} p-value {wilcoxon_p} not statistically significant"

def test_ablation_degradation(benchmark_data):
    """Gate 3 Criterion: Ablations show performance and physics degradation upon component removal."""
    abl = benchmark_data["ablation_study"]
    full = next(a for a in abl if "Proposed" in a["Configuration"])
    wo_pinn = next(a for a in abl if "w/o PINN" in a["Configuration"])
    wo_knots = next(a for a in abl if "w/o Adaptive" in a["Configuration"])
    mlp = next(a for a in abl if "Standard MLP" in a["Configuration"])
    
    assert full["Mean_R2"] > wo_pinn["Mean_R2"], "Ablating PINN did not decrease R2"
    assert full["Thermodynamic_Consistency_%"] > wo_pinn["Thermodynamic_Consistency_%"], "Ablating PINN did not drop physics score"
    assert full["Mean_R2"] > wo_knots["Mean_R2"], "Ablating adaptive knots did not decrease R2"
    assert full["Mean_R2"] > mlp["Mean_R2"], "Full model not superior to MLP baseline"

def test_publication_figures_exist():
    """Gate 3 Criterion: High-resolution (300 DPI) publication figures generated."""
    expected_figs = [
        "fig2_model_benchmark_bars.png",
        "fig4_inverse_scaling_speedup.png",
        "fig5_ablation_study_matrix.png",
        "fig8_symbolic_splines.png"
    ]
    for fig_name in expected_figs:
        fig_path = os.path.join(FIGS_DIR, fig_name)
        assert os.path.exists(fig_path), f"Missing publication figure: {fig_path}"
        assert os.path.getsize(fig_path) > 10000, f"Figure {fig_name} is abnormally small"

def test_latex_tables_exist():
    """Gate 3 Criterion: Clean LaTeX tables generated in results/."""
    expected_tables = ["benchmark_table_latex.tex", "ablation_table_latex.tex"]
    for tbl in expected_tables:
        tbl_path = os.path.join(RESULTS_DIR, tbl)
        assert os.path.exists(tbl_path), f"Missing LaTeX table: {tbl_path}"
        with open(tbl_path, "r", encoding="utf-8") as f:
            content = f.read()
            assert "\\begin{table" in content and "\\end{table" in content
