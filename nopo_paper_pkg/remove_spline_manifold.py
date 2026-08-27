"""
nopo_paper_pkg / remove_spline_manifold.py
-------------------------------------------
Removes the "Learned B-Spline Manifold" card from Tab 1 in build_upgraded_gui.py and verify_gui.py.
"""

import os

pkg_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(pkg_dir)
builder_path = os.path.join(pkg_dir, "build_upgraded_gui.py")
verify_path = os.path.join(pkg_dir, "verify_gui.py")

with open(builder_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Remove the B-Spline Manifold card from Tab 1 HTML
old_spline_card = """                <!-- B-SPLINE LINE PLOT CARD -->
                <div class="card">
                    <div class="card-title">
                        <span>📈 Learned B-Spline Manifold (\\phi(T_rxn))</span>
                        <span style="color:var(--accent-cyan); font-size:10px;">Autograd Active</span>
                    </div>
                    <div style="height:170px;"><canvas id="splineChart"></canvas></div>
                </div>"""

if old_spline_card in text:
    text = text.replace(old_spline_card, "")
else:
    # Try alternate variant if braces differ
    import re
    text = re.sub(r'<!-- B-SPLINE LINE PLOT CARD -->.*?</div>\s*</div>\s*</div>', '</div>', text, flags=re.DOTALL)

with open(builder_path, "w", encoding="utf-8") as f:
    f.write(text)

# 2. Update verify_gui.py to remove splineChart from required_ids
with open(verify_path, "r", encoding="utf-8") as f:
    v_text = f.read()

v_text = v_text.replace(", 'splineChart'", "").replace("'splineChart',", "").replace("'splineChart'", "")

with open(verify_path, "w", encoding="utf-8") as f:
    f.write(v_text)

print("[SUCCESS] Removed Learned B-Spline Manifold card from Tab 1 and updated verify_gui.py")
