"""
nopo_paper_pkg / remove_inverse_widget.py
-----------------------------------------
Removes the "INVERSE OPTIMIZER & RECIPE SYNTHESIZER" widget from Tab 1 in build_upgraded_gui.py.
"""

import os
import re

pkg_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(pkg_dir)
builder_path = os.path.join(pkg_dir, "build_upgraded_gui.py")
verify_path = os.path.join(pkg_dir, "verify_gui.py")

with open(builder_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Remove the unified-inverse-bar widget from HTML
pattern = r'<!-- UNIFIED INVERSE CONTROL BAR -->\s*<div class="unified-inverse-bar">.*?</div>\s*</div>'
match = re.search(pattern, text, re.DOTALL)
if match:
    text = text[:match.start()] + text[match.end():]
else:
    # Alternative direct string removal
    old_widget_str = """                <!-- UNIFIED INVERSE CONTROL BAR -->
                <div class="unified-inverse-bar">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <div>
                            <div style="font-size:13px; font-weight:800; color:var(--accent-purple);">⚡ INVERSE OPTIMIZER & RECIPE SYNTHESIZER</div>
                            <div style="font-size:11px; color:var(--text-muted);">Set desired targets below and solve for KKT-guaranteed reactor setpoints</div>
                        </div>
                    </div>
                    
                    <button id="btnSolveInverse" class="btn-unified-solve" onclick="executeUnifiedInverseSolve()">⚡ Solve Optimal Reactor Recipe</button>

                    <div style="margin-top:12px; padding:10px; background:rgba(0,0,0,0.3); border-radius:8px;">
                        <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:4px;">
                            <span style="color:var(--text-muted); font-weight:700;">Multi-Objective Pareto Priority:</span>
                            <span id="paretoModeText" style="color:var(--accent-cyan); font-weight:700;">Balanced Formulation</span>
                        </div>
                        <input type="range" class="slider" id="paretoSlider" min="0" max="100" value="50" oninput="handleParetoChange(this.value)">
                        <div style="display:flex; justify-content:space-between; font-size:10px; color:var(--accent-cyan); margin-top:4px;">
                            <span>👈 Max Yield</span>
                            <span>Balanced</span>
                            <span>Ultra-Purity 👉</span>
                        </div>
                    </div>
                </div>"""
    text = text.replace(old_widget_str, "")

with open(builder_path, "w", encoding="utf-8") as f:
    f.write(text)

# 2. Update verify_gui.py to remove btnSolveInverse
with open(verify_path, "r", encoding="utf-8") as f:
    v_text = f.read()

v_text = v_text.replace("'btnSolveInverse', ", "").replace(", 'btnSolveInverse'", "")

with open(verify_path, "w", encoding="utf-8") as f:
    f.write(v_text)

print("[SUCCESS] Successfully removed Inverse Optimizer & Recipe Synthesizer widget from Tab 1.")
