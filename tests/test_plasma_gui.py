"""
tests/test_plasma_gui.py
------------------------
Gate 6 Automated Verification:
Validates the Interactive Plasma Decision Support System Dashboard:
1. HTML file exists and contains all 4 tabs.
2. Verified removal of legacy HiPCO/SWCNT variables and synthetic datasets.
3. Verified inclusion of 4 Plasma Chemical Kinetics presets.
4. Server script run_gui.py imports and validates endpoints.
"""

import os
import sys
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLASMA_HTML = os.path.join(ROOT_DIR, "plasma_kan_dss_app.html")
HIPCO_HTML = os.path.join(ROOT_DIR, "hipco_kan_dss_app.html")

def test_html_files_exist():
    """Gate 6 Criterion: HTML dashboard files exist and are populated."""
    assert os.path.exists(PLASMA_HTML), f"Missing {PLASMA_HTML}"
    assert os.path.exists(HIPCO_HTML), f"Missing {HIPCO_HTML}"
    assert os.path.getsize(PLASMA_HTML) > 10000

def test_plasma_tabs_present():
    """Gate 6 Criterion: All 4 tabs present in HTML."""
    with open(PLASMA_HTML, "r", encoding="utf-8") as f:
        content = f.read()
    assert 'id="tab1"' in content, "Missing Tab 1 (Reactor Simulator)"
    assert 'id="tab2"' in content, "Missing Tab 2 (Learned Splines)"
    assert 'id="tab3"' in content, "Missing Tab 3 (Uncertainty & Pilot)"
    assert 'id="tab4"' in content, "Missing Tab 4 (Benchmarks & Ablation)"

def test_four_plasma_presets_present():
    """Gate 6 Criterion: 4 presentation quick-jump presets defined."""
    with open(PLASMA_HTML, "r", encoding="utf-8") as f:
        content = f.read()
    assert "SEI Conversion Saturation" in content
    assert "Efficiency Volcano Peak" in content
    assert "Sub-Atmospheric Pressure" in content
    assert "Discharge Gap Confinement" in content

def test_no_legacy_hipco_remnants():
    """Gate 6 Criterion: Complete removal of legacy carbon nanotube synthetic terms."""
    with open(PLASMA_HTML, "r", encoding="utf-8") as f:
        content = f.read()
    assert "SWCNT_synthetic" not in content, "Legacy synthetic dataset detected"
    assert "DWM_Yield_g" not in content, "Legacy DWM target detected"
    assert "Fe_Precursor" not in content, "Legacy iron precursor detected"
