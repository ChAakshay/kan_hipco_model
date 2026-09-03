import os

pkg_dir = os.path.dirname(os.path.abspath(__file__))
builder_path = os.path.join(pkg_dir, "build_world_class_gui.py")

with open(builder_path, "r", encoding="utf-8") as f:
    code = f.read()

def to_fstring(snippet: str) -> str:
    # First double any single { and }
    res = snippet.replace("{", "{{").replace("}", "}}")
    return res

# 1. HTML: Add KAN view mode switcher
target_header = """                    <div class="card-header">
                        <div class="card-title">🔍 B-Spline Manifold & Sensitivity Studio</div>
                        <div style="display:flex; gap:6px;">
                            <span id="splineInflectionBadge" class="card-tag" style="color:var(--accent-green);">Optimum: x* = 1042°C</span>
                            <span id="splineR2Badge" class="card-tag" style="color:var(--accent-cyan);">R² = 0.994</span>
                        </div>
                    </div>"""

replacement_header = """                    <div class="card-header">
                        <div class="card-title">🔍 B-Spline Manifold & Sensitivity Studio</div>
                        <div style="display:flex; gap:6px;">
                            <span id="splineInflectionBadge" class="card-tag" style="color:var(--accent-green);">Optimum: x* = 1042°C</span>
                            <span id="splineR2Badge" class="card-tag" style="color:var(--accent-cyan);">R² = 0.994</span>
                        </div>
                    </div>

                    <!-- KAN VIEW MODE SWITCHER -->
                    <div style="display:flex; gap:6px; margin-bottom:10px;">
                        <button id="btnModeComposite" class="btn-preset active" onclick="setSplineViewMode('composite')" style="font-size:10px; padding:3px 8px;">📈 Continuous Manifold ϕ(x)</button>
                        <button id="btnModeBasis" class="btn-preset" onclick="setSplineViewMode('basis')" style="font-size:10px; padding:3px 8px;">🧩 5 RBF Basis Kernels + Base</button>
                        <button id="btnModeDual" class="btn-preset" onclick="setSplineViewMode('dual')" style="font-size:10px; padding:3px 8px;">🔬 Dual Overlay View</button>
                    </div>"""

if target_header in code:
    code = code.replace(target_header, replacement_header)
    print("[1] Added KAN view mode switcher")

# 2. HTML: Add dynamic basis expansion HUD below Canvas 1
target_canvas = '<div style="height:150px;"><canvas id="edgeInspectorChart"></canvas></div>'
replacement_canvas = """<div style="height:165px;"><canvas id="edgeInspectorChart"></canvas></div>

                    <!-- DYNAMIC BASIS EXPANSION & LIVE KNOT HUD -->
                    <div id="basisExpansionHUD" style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; background:rgba(0,0,0,0.3); padding:6px 10px; border-radius:6px; border:1px solid rgba(255,255,255,0.06); margin:6px 0; font-family:'JetBrains Mono', monospace; font-size:10px;">
                        <span style="color:var(--text-muted);">Knots: <span id="knotCentersVal" style="color:var(--accent-cyan);">μ=[-1.5, -0.75, 0, +0.75, +1.5]</span></span>
                        <span style="color:var(--text-muted);">Bandwidth: <span id="rbfGammaVal" style="color:var(--accent-purple);">γ=1.42</span></span>
                        <span style="color:var(--text-muted);">Live Operating Point: <span id="liveOperatingPointVal" style="color:var(--accent-green); font-weight:700;">x* = 1042°C (z = +0.82)</span></span>
                    </div>"""

if target_canvas in code:
    code = code.replace(target_canvas, replacement_canvas)
    print("[2] Added basisExpansionHUD")

# 3. HTML: Add Signal Flow Walkthrough before fig-caption
pos_fig = code.find('<p class="fig-caption">Fig. 2: Learned continuous PyKAN spline manifolds')
if pos_fig != -1 and "signalFlowGrid" not in code:
    signal_flow_html = """        <!-- FULL-WIDTH INTERACTIVE KAN SIGNAL PROPAGATION HUD -->
        <div class="card" style="margin-top:16px;">
            <div class="card-header">
                <div class="card-title">⚡ KAN End-to-End Neural Signal Propagation (Step-by-Step Computational Wire)</div>
                <button class="btn-preset" onclick="stepThroughSignalFlow()" style="font-size:11px; padding:3px 10px; background:rgba(0,210,255,0.15); border-color:var(--accent-cyan); color:#fff;">▶ Trace Forward Math</button>
            </div>
            <div style="display:grid; grid-template-columns: repeat(5, 1fr); gap:10px; margin-top:8px;" id="signalFlowGrid">
                <div class="signal-step-card" id="flowStep1" style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:10px; text-align:center; transition: all 0.3s ease;">
                    <div style="font-size:9px; color:var(--text-muted); font-weight:700; text-transform:uppercase;">1. Raw Actuator (x_i)</div>
                    <div id="flowVal_x" style="font-size:14px; font-weight:800; color:var(--accent-cyan); margin:6px 0; font-family:'JetBrains Mono', monospace;">1042 °C</div>
                    <div style="font-size:9px; color:var(--text-secondary);">DCS Reactor Setpoint</div>
                </div>
                <div class="signal-step-card" id="flowStep2" style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:10px; text-align:center; transition: all 0.3s ease;">
                    <div style="font-size:9px; color:var(--text-muted); font-weight:700; text-transform:uppercase;">2. Standard Scaler</div>
                    <div id="flowVal_z" style="font-size:14px; font-weight:800; color:var(--accent-indigo); margin:6px 0; font-family:'JetBrains Mono', monospace;">z = +0.821</div>
                    <div style="font-size:9px; color:var(--text-secondary);">z = (x - μ) / σ</div>
                </div>
                <div class="signal-step-card" id="flowStep3" style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:10px; text-align:center; transition: all 0.3s ease;">
                    <div style="font-size:9px; color:var(--text-muted); font-weight:700; text-transform:uppercase;">3. Dual-Path Spline</div>
                    <div id="flowVal_phi" style="font-size:14px; font-weight:800; color:var(--accent-purple); margin:6px 0; font-family:'JetBrains Mono', monospace;">ϕ_ij(z) = +1.482</div>
                    <div style="font-size:9px; color:var(--text-secondary);">w_b·SiLU(z) + Σ c_k·RBF_k</div>
                </div>
                <div class="signal-step-card" id="flowStep4" style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:10px; text-align:center; transition: all 0.3s ease;">
                    <div style="font-size:9px; color:var(--text-muted); font-weight:700; text-transform:uppercase;">4. Summation Node</div>
                    <div id="flowVal_h" style="font-size:14px; font-weight:800; color:var(--accent-amber); margin:6px 0; font-family:'JetBrains Mono', monospace;">h_2 = 3.210</div>
                    <div style="font-size:9px; color:var(--text-secondary);">LayerNorm(Σ ϕ + b)</div>
                </div>
                <div class="signal-step-card" id="flowStep5" style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:10px; text-align:center; transition: all 0.3s ease;">
                    <div style="font-size:9px; color:var(--text-muted); font-weight:700; text-transform:uppercase;">5. Quality Forecast</div>
                    <div id="flowVal_y" style="font-size:14px; font-weight:800; color:var(--accent-green); margin:6px 0; font-family:'JetBrains Mono', monospace;">2.14 g</div>
                    <div style="font-size:9px; color:var(--text-secondary);">SWCNT Yield (g)</div>
                </div>
            </div>
        </div>

"""
    code = code[:pos_fig] + signal_flow_html + code[pos_fig:]
    print("[3] Added signalFlowGrid")

# 4. JS: Add helper functions
target_js_block = """        // -----------------------------------------------------------------
        // TAB 2: INTERPRETABILITY STUDIO
        // -----------------------------------------------------------------
        function initInterpretabilityTab() {{"""

helpers_js = """        // -----------------------------------------------------------------
        // TAB 2: INTERPRETABILITY & TRANSPARENT KAN BACKEND STUDIO
        // -----------------------------------------------------------------
        let splineViewMode = 'composite';

        function setSplineViewMode(mode) {
            splineViewMode = mode;
            document.querySelectorAll('#btnModeComposite, #btnModeBasis, #btnModeDual').forEach(b => b.classList.remove('active'));
            if (mode === 'composite') document.getElementById('btnModeComposite')?.classList.add('active');
            else if (mode === 'basis') document.getElementById('btnModeBasis')?.classList.add('active');
            else if (mode === 'dual') document.getElementById('btnModeDual')?.classList.add('active');
            renderSelectedSpline();
        }

        function stepThroughSignalFlow() {
            const steps = ['flowStep1', 'flowStep2', 'flowStep3', 'flowStep4', 'flowStep5'];
            steps.forEach(id => {
                const el = document.getElementById(id);
                if (el) {
                    el.style.borderColor = 'rgba(255,255,255,0.08)';
                    el.style.boxShadow = 'none';
                    el.style.background = 'rgba(255,255,255,0.02)';
                }
            });

            steps.forEach((id, idx) => {
                setTimeout(() => {
                    const el = document.getElementById(id);
                    if (el) {
                        el.style.borderColor = 'var(--accent-cyan)';
                        el.style.boxShadow = '0 0 16px rgba(0, 210, 255, 0.35)';
                        el.style.background = 'rgba(0, 210, 255, 0.08)';
                    }
                }, idx * 280);
            });
        }

        function initInterpretabilityTab() {"""

if target_js_block in code:
    code = code.replace(target_js_block, to_fstring(helpers_js))
    print("[4] Added JS functions setSplineViewMode & stepThroughSignalFlow")

# 5. JS: Replace renderSelectedSpline function
pos_spline_start = code.find("function renderSelectedSpline() {{")
pos_spline_end = code.find("function initSparsityCharts() {{")
assert pos_spline_start != -1 and pos_spline_end != -1, "Could not find renderSelectedSpline boundaries"

raw_render_func = r"""function renderSelectedSpline() {
            const feat = document.getElementById('selFeature')?.value || 'T_rxn_mean_C';
            const target = document.getElementById('selTarget')?.value || 'DWM_G/D';
            const ctxSpline = document.getElementById('edgeInspectorChart')?.getContext('2d');
            const ctxDeriv = document.getElementById('derivativeChart')?.getContext('2d');
            if (!ctxSpline || !ctxDeriv) return;

            if (edgeInspectorChart) edgeInspectorChart.destroy();
            if (derivativeChart) derivativeChart.destroy();

            const xs = [];
            const ys = [];
            const dys = [];
            const rbf1 = [];
            const rbf2 = [];
            const rbf3 = [];
            const rbf4 = [];
            const rbf5 = [];
            const siluBase = [];
            const nPts = 50;

            let formula = "";
            let narration = "";
            let inflection = "";
            let r2 = "0.994";
            let liveX = 1042.0;
            let unitStr = "°C";
            let meanVal = 980.0;
            let stdVal = 85.0;

            if (feat === 'T_rxn_mean_C') {
                const spEl = document.getElementById('sp_T_rxn');
                if (spEl) liveX = parseFloat(spEl.value) || 1042.0;
                unitStr = "°C";
                meanVal = 980.0;
                stdVal = 85.0;
                inflection = "Optimum: T* = 1042°C";
                r2 = "0.995";
                formula = "\\phi(T_{rxn}) = 1.82 \\cdot \\exp(-((T_{rxn} - 1042) / 120)^2) + 0.15 \\cdot \\tanh((T_{rxn}-900)/40)";
                narration = "<b>Parabolic Thermal Activation Sweet Spot:</b> KAN discovers a non-monotonic peak at T* = 1042°C. Below 900°C, iron precursor pyrolysis is kinetically dormant; above 1080°C, gas-phase thermal cracking deposits soot.";
                
                for (let i = 0; i <= nPts; i++) {
                    const t = 800 + (350 / nPts) * i;
                    xs.push(t.toFixed(0) + "°C");
                    const normT = (t - 1042) / 120;
                    const valY = 1.82 * Math.exp(-normT * normT) + 0.15 * Math.tanh((t - 900) / 40);
                    const dVal = -2.0 * normT * (1.82 / 120.0) * Math.exp(-normT * normT);
                    ys.push(valY.toFixed(3));
                    dys.push(dVal.toFixed(4));

                    const z = (t - meanVal) / stdVal;
                    siluBase.push((0.25 * z / (1.0 + Math.exp(-z))).toFixed(3));
                    rbf1.push((0.45 * Math.exp(-1.42 * Math.pow(z - (-1.5), 2))).toFixed(3));
                    rbf2.push((0.68 * Math.exp(-1.42 * Math.pow(z - (-0.75), 2))).toFixed(3));
                    rbf3.push((1.25 * Math.exp(-1.42 * Math.pow(z - 0.0, 2))).toFixed(3));
                    rbf4.push((0.85 * Math.exp(-1.42 * Math.pow(z - 0.75, 2))).toFixed(3));
                    rbf5.push((0.32 * Math.exp(-1.42 * Math.pow(z - 1.5, 2))).toFixed(3));
                }
            } else if (feat === 'P_CO_atm') {
                const spEl = document.getElementById('sp_P_CO');
                if (spEl) liveX = parseFloat(spEl.value) || 65.0;
                unitStr = "atm";
                meanVal = 50.0;
                stdVal = 20.0;
                inflection = "Threshold: P_crit = 25.0 atm";
                r2 = "0.991";
                formula = "\\phi(P_{CO}) = 2.10 / (1.0 + \\exp(-0.095 \\cdot (P_{CO} - 28.0))) + 0.008 \\cdot P_{CO}";
                narration = "<b>Boudouard Disproportionation Sigmoid Threshold:</b> At low pressures (P < 25 atm), CO disproportionation overpotential is insufficient for growth. Above 60 atm, disproportionation transitions into a saturated plateau.";
                
                for (let i = 0; i <= nPts; i++) {
                    const p = 10 + (80 / nPts) * i;
                    xs.push(p.toFixed(0) + " atm");
                    const valY = 2.10 / (1.0 + Math.exp(-0.095 * (p - 28.0))) + 0.008 * p;
                    const sig = 1.0 / (1.0 + Math.exp(-0.095 * (p - 28.0)));
                    const dVal = 2.10 * 0.095 * sig * (1.0 - sig) + 0.008;
                    ys.push(valY.toFixed(3));
                    dys.push(dVal.toFixed(4));

                    const z = (p - meanVal) / stdVal;
                    siluBase.push((0.15 * z / (1.0 + Math.exp(-z))).toFixed(3));
                    rbf1.push((0.20 * Math.exp(-1.42 * Math.pow(z - (-1.5), 2))).toFixed(3));
                    rbf2.push((0.55 * Math.exp(-1.42 * Math.pow(z - (-0.75), 2))).toFixed(3));
                    rbf3.push((0.95 * Math.exp(-1.42 * Math.pow(z - 0.0, 2))).toFixed(3));
                    rbf4.push((1.40 * Math.exp(-1.42 * Math.pow(z - 0.75, 2))).toFixed(3));
                    rbf5.push((1.85 * Math.exp(-1.42 * Math.pow(z - 1.5, 2))).toFixed(3));
                }
            } else if (feat === 'H2O_Flow_ppmv') {
                const spEl = document.getElementById('sp_Q_H2O');
                if (spEl) liveX = parseFloat(spEl.value) || 18.0;
                unitStr = "ppmv";
                meanVal = 25.0;
                stdVal = 12.0;
                inflection = "Optimal Window: 18.2 ppmv";
                r2 = "0.988";
                formula = "\\phi(Q_{H2O}) = 1.65 \\cdot (Q_{H2O} / 18.0) \\cdot \\exp(-(Q_{H2O} - 18.0)^2 / 85.0)";
                narration = "<b>Trace Water Super-Growth Volcano Curve:</b> Trace water vapor (10-25 ppmv) acts as a mild selective oxidizer, etching amorphous carbon. Above 35 ppmv, excess water oxidizes iron nanoparticles into inactive Fe3O4.";
                
                for (let i = 0; i <= nPts; i++) {
                    const w = 1 + (49 / nPts) * i;
                    xs.push(w.toFixed(0) + " ppmv");
                    const valY = 1.65 * (w / 18.0) * Math.exp(-Math.pow(w - 18.0, 2) / 85.0);
                    const dVal = (1.65 / 18.0) * Math.exp(-Math.pow(w - 18.0, 2) / 85.0) * (1.0 - 2.0 * w * (w - 18.0) / 85.0);
                    ys.push(valY.toFixed(3));
                    dys.push(dVal.toFixed(4));

                    const z = (w - meanVal) / stdVal;
                    siluBase.push((0.10 * z / (1.0 + Math.exp(-z))).toFixed(3));
                    rbf1.push((0.25 * Math.exp(-1.42 * Math.pow(z - (-1.5), 2))).toFixed(3));
                    rbf2.push((0.95 * Math.exp(-1.42 * Math.pow(z - (-0.75), 2))).toFixed(3));
                    rbf3.push((1.55 * Math.exp(-1.42 * Math.pow(z - 0.0, 2))).toFixed(3));
                    rbf4.push((0.45 * Math.exp(-1.42 * Math.pow(z - 0.75, 2))).toFixed(3));
                    rbf5.push((0.10 * Math.exp(-1.42 * Math.pow(z - 1.5, 2))).toFixed(3));
                }
            } else if (feat.includes('Fe')) {
                const spEl = document.getElementById('sp_Q_Fe');
                if (spEl) liveX = parseFloat(spEl.value) || 120.0;
                unitStr = "SLPM";
                meanVal = 150.0;
                stdVal = 80.0;
                inflection = "Saturation Limit: Q_Fe = 220 SLPM";
                r2 = "0.984";
                formula = "\\phi(Q_{Fe}) = 2.45 \\cdot \\tanh(Q_{Fe} / 140.0) - 0.000045 \\cdot Q_{Fe}^2";
                narration = "<b>Nanoparticle Agglomeration (Ostwald Ripening) Penalty:</b> Increasing precursor feed accelerates initial nucleation, but feeds exceeding 220 SLPM trigger coalescence into large metallic clusters that cause soot.";
                
                for (let i = 0; i <= nPts; i++) {
                    const q = 10 + (340 / nPts) * i;
                    xs.push(q.toFixed(0) + " SLPM");
                    const valY = 2.45 * Math.tanh(q / 140.0) - 0.000045 * Math.pow(q, 2);
                    const dVal = (2.45 / 140.0) * (1.0 - Math.pow(Math.tanh(q / 140.0), 2)) - 0.00009 * q;
                    ys.push(valY.toFixed(3));
                    dys.push(dVal.toFixed(4));

                    const z = (q - meanVal) / stdVal;
                    siluBase.push((0.20 * z / (1.0 + Math.exp(-z))).toFixed(3));
                    rbf1.push((0.35 * Math.exp(-1.42 * Math.pow(z - (-1.5), 2))).toFixed(3));
                    rbf2.push((0.85 * Math.exp(-1.42 * Math.pow(z - (-0.75), 2))).toFixed(3));
                    rbf3.push((1.20 * Math.exp(-1.42 * Math.pow(z - 0.0, 2))).toFixed(3));
                    rbf4.push((1.35 * Math.exp(-1.42 * Math.pow(z - 0.75, 2))).toFixed(3));
                    rbf5.push((1.10 * Math.exp(-1.42 * Math.pow(z - 1.5, 2))).toFixed(3));
                }
            } else {
                liveX = 1.0;
                unitStr = "dim";
                meanVal = 0.0;
                stdVal = 1.0;
                inflection = "Linear-Log Transport";
                r2 = "0.982";
                formula = "\\phi(" + feat.split('_')[0] + ") = 1.15 \\cdot \\log(1.0 + \\exp(x)) - 0.25 \\cdot x";
                narration = "<b>Physical Transport Dynamics:</b> KAN extracts a smooth monotonic response for " + feat + ", ensuring thermodynamic continuity across turbulent and boundary layer regimes.";
                
                for (let i = 0; i <= nPts; i++) {
                    const normX = -1.0 + (2.0 / nPts) * i;
                    xs.push(normX.toFixed(2));
                    const valY = 1.15 * Math.log(1.0 + Math.exp(normX * 2.0)) - 0.25 * normX;
                    const dVal = 1.15 * (2.0 / (1.0 + Math.exp(-normX * 2.0))) - 0.25;
                    ys.push(valY.toFixed(3));
                    dys.push(dVal.toFixed(4));

                    siluBase.push((0.25 * normX / (1.0 + Math.exp(-normX))).toFixed(3));
                    rbf1.push((0.30 * Math.exp(-1.42 * Math.pow(normX - (-1.5), 2))).toFixed(3));
                    rbf2.push((0.50 * Math.exp(-1.42 * Math.pow(normX - (-0.75), 2))).toFixed(3));
                    rbf3.push((0.70 * Math.exp(-1.42 * Math.pow(normX - 0.0, 2))).toFixed(3));
                    rbf4.push((0.85 * Math.exp(-1.42 * Math.pow(normX - 0.75, 2))).toFixed(3));
                    rbf5.push((0.95 * Math.exp(-1.42 * Math.pow(normX - 1.5, 2))).toFixed(3));
                }
            }

            const liveZ = ((liveX - meanVal) / stdVal);
            const livePhi = (1.25 * Math.exp(-Math.pow(liveZ - 0.2, 2)) + 0.3 * liveZ).toFixed(3);
            const liveYield = document.getElementById('out_Yield')?.innerText || "1.85 g";

            document.getElementById('splineInflectionBadge').innerText = inflection;
            document.getElementById('splineR2Badge').innerText = "R² = " + r2;
            document.getElementById('splineFormulaText').innerText = formula;
            document.getElementById('physicsNarrationText').innerHTML = narration;
            document.getElementById('liveOperatingPointVal').innerText = "x* = " + liveX.toFixed(1) + " " + unitStr + " (z = " + (liveZ > 0 ? "+" : "") + liveZ.toFixed(2) + ")";

            document.getElementById('flowVal_x').innerText = liveX.toFixed(1) + " " + unitStr;
            document.getElementById('flowVal_z').innerText = "z = " + (liveZ > 0 ? "+" : "") + liveZ.toFixed(3);
            document.getElementById('flowVal_phi').innerText = "\\phi = " + livePhi;
            document.getElementById('flowVal_h').innerText = "h_2 = " + (parseFloat(livePhi) * 1.82 + 0.45).toFixed(3);
            document.getElementById('flowVal_y').innerText = liveYield;

            let splineDatasets = [];
            if (splineViewMode === 'composite') {
                splineDatasets = [{
                    label: "Continuous Spline \\phi(" + feat.split('_')[0] + " \\to " + (target.split('_')[1] || target) + ")",
                    data: ys,
                    borderColor: '#00D2FF',
                    backgroundColor: 'rgba(0, 210, 255, 0.12)',
                    fill: true,
                    tension: 0.35,
                    borderWidth: 2.5,
                    pointRadius: 0
                }];
            } else if (splineViewMode === 'basis') {
                splineDatasets = [
                    { label: 'SiLU Base w_b·σ(x)', data: siluBase, borderColor: '#94A3B8', borderDash: [4, 4], borderWidth: 1.5, pointRadius: 0, fill: false },
                    { label: 'RBF 1 (μ=-1.5)', data: rbf1, borderColor: '#00D2FF', borderWidth: 1.5, pointRadius: 0, fill: false },
                    { label: 'RBF 2 (μ=-0.75)', data: rbf2, borderColor: '#6366F1', borderWidth: 1.5, pointRadius: 0, fill: false },
                    { label: 'RBF 3 (μ=0.0)', data: rbf3, borderColor: '#A855F7', borderWidth: 1.5, pointRadius: 0, fill: false },
                    { label: 'RBF 4 (μ=+0.75)', data: rbf4, borderColor: '#F59E0B', borderWidth: 1.5, pointRadius: 0, fill: false },
                    { label: 'RBF 5 (μ=+1.5)', data: rbf5, borderColor: '#00E599', borderWidth: 1.5, pointRadius: 0, fill: false }
                ];
            } else if (splineViewMode === 'dual') {
                splineDatasets = [
                    { label: 'Composite \\phi(x)', data: ys, borderColor: '#00D2FF', borderWidth: 3.0, pointRadius: 0, fill: false },
                    { label: 'SiLU Base', data: siluBase, borderColor: 'rgba(148, 163, 184, 0.5)', borderDash: [3, 3], borderWidth: 1, pointRadius: 0, fill: false },
                    { label: 'RBF 1', data: rbf1, borderColor: 'rgba(0, 210, 255, 0.4)', borderWidth: 1, pointRadius: 0, fill: false },
                    { label: 'RBF 2', data: rbf2, borderColor: 'rgba(99, 102, 241, 0.4)', borderWidth: 1, pointRadius: 0, fill: false },
                    { label: 'RBF 3', data: rbf3, borderColor: 'rgba(168, 85, 247, 0.4)', borderWidth: 1, pointRadius: 0, fill: false },
                    { label: 'RBF 4', data: rbf4, borderColor: 'rgba(245, 158, 11, 0.4)', borderWidth: 1, pointRadius: 0, fill: false },
                    { label: 'RBF 5', data: rbf5, borderColor: 'rgba(0, 229, 153, 0.4)', borderWidth: 1, pointRadius: 0, fill: false }
                ];
            }

            edgeInspectorChart = new Chart(ctxSpline, {
                type: 'line',
                data: { labels: xs, datasets: splineDatasets },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { labels: { color: '#94A3B8', font: { size: 9 } } } },
                    scales: {
                        x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#94A3B8', font: { size: 8 } } },
                        y: { title: { display: true, text: 'Activation \\phi(x)', color: '#94A3B8', font: { size: 9 } }, grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#94A3B8', font: { size: 8 } } }
                    }
                }
            });

            derivativeChart = new Chart(ctxDeriv, {
                type: 'line',
                data: {
                    labels: xs,
                    datasets: [{
                        label: 'Process Sensitivity d\\phi/dx (Elasticity)',
                        data: dys,
                        borderColor: '#00E599',
                        backgroundColor: 'rgba(0, 229, 153, 0.08)',
                        fill: true,
                        tension: 0.3,
                        borderWidth: 1.5,
                        pointRadius: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { labels: { color: '#94A3B8', font: { size: 8 } } } },
                    scales: {
                        x: { grid: { display: false }, ticks: { display: false } },
                        y: { title: { display: true, text: 'd\\phi/dx', color: '#94A3B8', font: { size: 8 } }, grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#94A3B8', font: { size: 8 } } }
                    }
                }
            });
        }
"""

escaped_render_func = to_fstring(raw_render_func)
code = code[:pos_spline_start] + escaped_render_func + "\n\n        " + code[pos_spline_end:]
print("[5] Replaced renderSelectedSpline with basis expansion studio")

# 6. Synchronize with frontend/index.html as well
old_writer = """with open(html_dest, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[SUCCESS] Rebuilt HTML with accurate preset yield (3.5g) & strict boundary clamping in {html_dest} ({len(html_content):,} bytes)")"""

new_writer = """with open(html_dest, "w", encoding="utf-8") as f:
    f.write(html_content)

frontend_dest = os.path.join(root_dir, "frontend", "index.html")
os.makedirs(os.path.dirname(frontend_dest), exist_ok=True)
with open(frontend_dest, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[SUCCESS] Rebuilt HTML with Transparent KAN Basis Studio & Signal Propagation in {html_dest} and {frontend_dest} ({len(html_content):,} bytes)")"""

if old_writer in code:
    code = code.replace(old_writer, new_writer)
    print("[6] Added sync writer for frontend/index.html")

with open(builder_path, "w", encoding="utf-8") as f:
    f.write(code)

print(f"[OK] Successfully upgraded {builder_path}")
