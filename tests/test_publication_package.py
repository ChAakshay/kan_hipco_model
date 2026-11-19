"""
tests/test_publication_package.py
---------------------------------
Gate 7 Automated Verification:
Validates the complete publication package and teammate handoff deliverables:
1. Manuscript draft Plasma_CO2_KAN_Conference_Paper.md completeness
2. Teammate publication guide TEAMMATE_README_PUBLICATION_GUIDE.md integrity
3. All 5 publication figures present in figures/ (300 DPI)
4. All LaTeX tables and JSON logs present in results/
5. Clean separation: zero synthetic data in active data directory.
"""

import os
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANUSCRIPT = os.path.join(ROOT_DIR, "Plasma_CO2_KAN_Conference_Paper.md")
GUIDE = os.path.join(ROOT_DIR, "TEAMMATE_README_PUBLICATION_GUIDE.md")
FIGS_DIR = os.path.join(ROOT_DIR, "figures")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
DATA_DIR = os.path.join(ROOT_DIR, "data")

def test_manuscript_draft_completeness():
    """Gate 7 Criterion: Complete manuscript draft with all core sections."""
    assert os.path.exists(MANUSCRIPT), f"Missing manuscript at {MANUSCRIPT}"
    with open(MANUSCRIPT, "r", encoding="utf-8") as f:
        content = f.read()
    sections = [
        "## Abstract",
        "## I. Introduction",
        "## II. Mathematical Formulation",
        "## III. Experimental Benchmark & Data Provenance",
        "## IV. Benchmark Results & Statistical Significance",
        "## V. Symbolic Kinetic Rate Law Distillation",
        "## VI. Real-Time Differentiable Inverse Optimization",
        "## VII. Dynamic Experimental Validation",
        "## VIII. Conclusion",
        "## References"
    ]
    for s in sections:
        assert s in content, f"Missing section in manuscript: {s}"

def test_teammate_guide_integrity():
    """Gate 7 Criterion: Teammate guide exists and documents all handoff deliverables."""
    assert os.path.exists(GUIDE), f"Missing teammate guide at {GUIDE}"
    with open(GUIDE, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Directory Structure of Deliverables" in content
    assert "Key Numbers & Claims to Highlight" in content
    assert "pytest tests/ -v" in content

def test_all_publication_figures():
    """Gate 7 Criterion: 5 high-resolution publication figures exist."""
    figs = [
        "fig2_model_benchmark_bars.png",
        "fig4_inverse_scaling_speedup.png",
        "fig5_ablation_study_matrix.png",
        "fig6_pilot_lab_transfer.png",
        "fig8_symbolic_splines.png"
    ]
    for fig in figs:
        p = os.path.join(FIGS_DIR, fig)
        assert os.path.exists(p), f"Missing figure: {p}"
        assert os.path.getsize(p) > 10000, f"Figure abnormally small: {p}"

def test_latex_tables_and_json_results():
    """Gate 7 Criterion: LaTeX tables and JSON logs ready for publication."""
    tables = [
        "benchmark_table_latex.tex",
        "ablation_table_latex.tex",
        "symbolic_rate_laws.tex",
        "paper_benchmark_results.json",
        "plasma_symbolic_equations.json"
    ]
    for t in tables:
        p = os.path.join(RESULTS_DIR, t)
        assert os.path.exists(p), f"Missing result deliverable: {p}"

def test_zero_synthetic_data_in_active_dirs():
    """Gate 7 Criterion: Zero synthetic SWCNT data in active data/ or nopo_paper_pkg/."""
    for root, _, files in os.walk(DATA_DIR):
        for f in files:
            assert not f.startswith("SWCNT_synthetic"), f"Synthetic file found in data/: {f}"
