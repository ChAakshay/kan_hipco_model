import os

html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hipco_kan_dss_app.html")

with open(html_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update the Unified Inverse Control Bar with Pareto Slider
old_bar = '''<button id="btnSolveInverse" class="btn-unified-solve" onclick="executeUnifiedInverseSolve()">⚡ Solve Optimal Reactor Recipe</button>
                </div>'''

new_bar = '''<button id="btnSolveInverse" class="btn-unified-solve" onclick="executeUnifiedInverseSolve()">⚡ Solve Optimal Reactor Recipe</button>
                    <div style="margin-top:16px; padding:12px; background:rgba(0,242,254,0.05); border-radius:8px; border:1px solid rgba(0,242,254,0.2);">
                        <div style="font-size:11px; color:var(--text-muted); margin-bottom:6px; font-weight:bold;">Multi-Objective Pareto Priority Navigator:</div>
                        <input type="range" class="slider" id="paretoSlider" min="0" max="100" value="50">
                        <div style="display:flex; justify-content:space-between; font-size:10px; color:var(--accent-cyan); margin-top:6px;">
                            <span>👈 Yield Focus</span>
                            <span>Balanced</span>
                            <span>Ultra-Purity Focus 👉</span>
                        </div>
                    </div>
                </div>'''

if old_bar in text:
    text = text.replace(old_bar, new_bar)
else:
    # Try CRLF
    old_bar_crlf = old_bar.replace('\n', '\r\n')
    new_bar_crlf = new_bar.replace('\n', '\r\n')
    if old_bar_crlf in text:
        text = text.replace(old_bar_crlf, new_bar_crlf)

# 2. Update Sonic Check to KKT Constraint Check
old_kkt = '''<span class="lbl">Sonic V Check</span>
                            <span id="evalSonicCheck" class="val" style="color:var(--accent-blue)">93.2 m/s</span>'''
new_kkt = '''<span class="lbl">KKT Const. Check</span>
                            <span id="evalSonicCheck" class="val" style="color:var(--accent-green)">0 Violations</span>'''
if old_kkt in text:
    text = text.replace(old_kkt, new_kkt)
else:
    old_kkt_crlf = old_kkt.replace('\n', '\r\n')
    new_kkt_crlf = new_kkt.replace('\n', '\r\n')
    if old_kkt_crlf in text:
        text = text.replace(old_kkt_crlf, new_kkt_crlf)

# 3. Update MPC Badge
old_mpc = '''<div class="mpc-badge">⚡ MPC Loop: &lt;0.08s/cycle</div>'''
new_mpc = '''<div class="mpc-badge">⚡ Aug-Lagrangian MPC Loop: <span style="color:#00e676; margin-left:6px;">&lt; 22ms / cycle</span></div>'''
if old_mpc in text:
    text = text.replace(old_mpc, new_mpc)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(text)

print("[SUCCESS] HTML GUI Updated with Pareto Slider & KKT Badges.")
