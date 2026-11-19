"""
tests/test_symbolic_extractor_plasma.py
---------------------------------------
Gate 5 Automated Verification:
Validates the Symbolic Kinetic Rate Law Distillation Engine:
1. Primary rate law (SEI -> CO2 Conversion) achieves R2 >= 0.98 fidelity
2. All 4 plasma kinetic laws achieve R2 >= 0.85
3. Exported plasma_symbolic_equations.json integrity
4. Exported LaTeX formula file validity.
"""

import os
import json
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(ROOT_DIR, "results")

@pytest.fixture
def symbolic_laws():
    json_path = os.path.join(RESULTS_DIR, "plasma_symbolic_equations.json")
    if not os.path.exists(json_path):
        pytest.skip(f"Symbolic equations file not found at {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def test_four_laws_extracted(symbolic_laws):
    """Gate 5 Criterion: Exactly 4 physical plasma rate laws distilled."""
    assert len(symbolic_laws) == 4, f"Expected 4 laws, got {len(symbolic_laws)}"

def test_primary_conversion_law_r2_fidelity(symbolic_laws):
    """Gate 5 Criterion: Primary SEI -> CO2 conversion law achieves R2 >= 0.98."""
    law1 = next(l for l in symbolic_laws if "SEI -> CO2_Conversion" in l["relationship"])
    assert law1["r2_fidelity"] >= 0.98, f"Primary rate law R2 {law1['r2_fidelity']} < 0.98"

def test_all_laws_r2_fidelity(symbolic_laws):
    """Gate 5 Criterion: All extracted laws have R2 >= 0.85."""
    for l in symbolic_laws:
        assert l["r2_fidelity"] >= 0.85, f"Law {l['relationship']} R2 {l['r2_fidelity']} < 0.85"

def test_latex_export_validity():
    """Gate 5 Criterion: Valid LaTeX file exists in results/."""
    tex_path = os.path.join(RESULTS_DIR, "symbolic_rate_laws.tex")
    assert os.path.exists(tex_path), f"Missing LaTeX export at {tex_path}"
    with open(tex_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "\\begin{equation}" in content and "\\end{equation}" in content
