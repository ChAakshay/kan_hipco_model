"""
nopo_paper_pkg / restore_original_inputs.py
-------------------------------------------
Restores the exact original input factor labels, nominal baselines, units, and ranges:
1. P_CO: 60.0 atm (10 - 90 atm)
2. T_rxn: 950 °C (800 - 1150 °C)
3. T_spread: 25.0 °C (0 - 80 °C)
4. Q_CO: 600 SLPM (100 - 1000 SLPM)
5. Q_Fe: 190 SLPM (10 - 350 SLPM)
6. Q_H2O: 30.0 ppmv (1 - 50 ppmv)
7. Zone_Dev: -5.0 °C (-35 - 15 °C)
"""

import os

pkg_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(pkg_dir)
html_path = os.path.join(root_dir, "hipco_kan_dss_app.html")
builder_path = os.path.join(pkg_dir, "build_upgraded_gui.py")

with open(builder_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update Sliders HTML markup in builder script
old_sliders_html = """                    <!-- ZONE 1 -->
                    <div class="zone-header">Zone 1: Primary Gas Dynamics</div>
                    <div class="slider-group">
                        <div class="slider-header">
                            <span class="slider-name">P_CO (Pressure)</span>
                            <div><span id="val_P_CO" class="slider-val">60.0</span> atm <span id="delta_P_CO" class="delta-chip">Δ 0.0</span></div>
                        </div>
                        <input type="range" class="slider" id="sp_P_CO" min="10" max="90" step="0.5" value="60.0" oninput="updateSimulation()">
                    </div>
                    <div class="slider-group">
                        <div class="slider-header">
                            <span class="slider-name">Q_CO (Carrier Flow)</span>
                            <div><span id="val_Q_CO" class="slider-val">500</span> SLPM <span id="delta_Q_CO" class="delta-chip">Δ 0.0</span></div>
                        </div>
                        <input type="range" class="slider" id="sp_Q_CO" min="100" max="1000" step="10" value="500" oninput="updateSimulation()">
                    </div>

                    <!-- ZONE 2 -->
                    <div class="zone-header">Zone 2: Thermal Profile</div>
                    <div class="slider-group">
                        <div class="slider-header">
                            <span class="slider-name">T_rxn (Mean Growth)</span>
                            <div><span id="val_T_rxn" class="slider-val">1050</span> °C <span id="delta_T_rxn" class="delta-chip">Δ 0.0</span></div>
                        </div>
                        <input type="range" class="slider" id="sp_T_rxn" min="800" max="1150" step="5" value="1050" oninput="updateSimulation()">
                    </div>
                    <div class="slider-group">
                        <div class="slider-header">
                            <span class="slider-name">T_spread (Gradient)</span>
                            <div><span id="val_T_spread" class="slider-val">25.0</span> °C</div>
                        </div>
                        <input type="range" class="slider" id="sp_T_spread" min="0" max="80" step="1" value="25.0" oninput="updateSimulation()">
                    </div>
                    <div class="slider-group">
                        <div class="slider-header">
                            <span class="slider-name">Zone SP Deviation</span>
                            <div><span id="val_Zone_Dev" class="slider-val">-5.0</span> °C</div>
                        </div>
                        <input type="range" class="slider" id="sp_Zone_Dev" min="-35" max="15" step="1" value="-5.0" oninput="updateSimulation()">
                    </div>

                    <!-- ZONE 3 -->
                    <div class="zone-header">Zone 3: Precursor & Catalyst</div>
                    <div class="slider-group">
                        <div class="slider-header">
                            <span class="slider-name">Q_Fe (Fe Precursor)</span>
                            <div><span id="val_Q_Fe" class="slider-val">180</span> SLPM <span id="delta_Q_Fe" class="delta-chip">Δ 0.0</span></div>
                        </div>
                        <input type="range" class="slider" id="sp_Q_Fe" min="10" max="350" step="5" value="180" oninput="updateSimulation()">
                    </div>
                    <div class="slider-group">
                        <div class="slider-header">
                            <span class="slider-name">Q_H2O (Trace Water)</span>
                            <div><span id="val_Q_H2O" class="slider-val">20.0</span> ppmv</div>
                        </div>
                        <input type="range" class="slider" id="sp_Q_H2O" min="1" max="50" step="0.5" value="20.0" oninput="updateSimulation()">
                    </div>"""

new_sliders_html = """                    <!-- ZONE 1 -->
                    <div class="zone-header">Zone 1: Primary Gas Dynamics</div>
                    <div class="slider-group">
                        <div class="slider-header">
                            <span class="slider-name">CO Reactor Pressure (P_CO)</span>
                            <div><span id="val_P_CO" class="slider-val">60.0 atm</span> <span id="delta_P_CO" class="delta-chip">Δ 0.0</span></div>
                        </div>
                        <input type="range" class="slider" id="sp_P_CO" min="10" max="90" step="0.5" value="60.0" oninput="updateSimulation()">
                    </div>
                    <div class="slider-group">
                        <div class="slider-header">
                            <span class="slider-name">CO Gas Flow (Q_CO)</span>
                            <div><span id="val_Q_CO" class="slider-val">600 SLPM</span> <span id="delta_Q_CO" class="delta-chip">Δ 0</span></div>
                        </div>
                        <input type="range" class="slider" id="sp_Q_CO" min="100" max="1000" step="10" value="600" oninput="updateSimulation()">
                    </div>

                    <!-- ZONE 2 -->
                    <div class="zone-header">Zone 2: Thermal Profile</div>
                    <div class="slider-group">
                        <div class="slider-header">
                            <span class="slider-name">Growth Temp (T_rxn)</span>
                            <div><span id="val_T_rxn" class="slider-val">950 °C</span> <span id="delta_T_rxn" class="delta-chip">Δ 0</span></div>
                        </div>
                        <input type="range" class="slider" id="sp_T_rxn" min="800" max="1150" step="1" value="950" oninput="updateSimulation()">
                    </div>
                    <div class="slider-group">
                        <div class="slider-header">
                            <span class="slider-name">Thermal Spread (T_spread)</span>
                            <div><span id="val_T_spread" class="slider-val">25.0 °C</span> <span id="delta_T_spread" class="delta-chip">Δ 0.0</span></div>
                        </div>
                        <input type="range" class="slider" id="sp_T_spread" min="0" max="80" step="0.5" value="25.0" oninput="updateSimulation()">
                    </div>
                    <div class="slider-group">
                        <div class="slider-header">
                            <span class="slider-name">Zone SP Deviation (Zone_Dev)</span>
                            <div><span id="val_Zone_Dev" class="slider-val">-5.0 °C</span> <span id="delta_Zone_Dev" class="delta-chip">Δ 0.0</span></div>
                        </div>
                        <input type="range" class="slider" id="sp_Zone_Dev" min="-35" max="15" step="1" value="-5.0" oninput="updateSimulation()">
                    </div>

                    <!-- ZONE 3 -->
                    <div class="zone-header">Zone 3: Precursor & Catalyst</div>
                    <div class="slider-group">
                        <div class="slider-header">
                            <span class="slider-name">Fe Precursor Flow (Q_Fe)</span>
                            <div><span id="val_Q_Fe" class="slider-val">190 SLPM</span> <span id="delta_Q_Fe" class="delta-chip">Δ 0</span></div>
                        </div>
                        <input type="range" class="slider" id="sp_Q_Fe" min="10" max="350" step="5" value="190" oninput="updateSimulation()">
                    </div>
                    <div class="slider-group">
                        <div class="slider-header">
                            <span class="slider-name">Trace Water Vapor (Q_H2O)</span>
                            <div><span id="val_Q_H2O" class="slider-val">30.0 ppmv</span> <span id="delta_Q_H2O" class="delta-chip">Δ 0.0</span></div>
                        </div>
                        <input type="range" class="slider" id="sp_Q_H2O" min="1" max="50" step="0.5" value="30.0" oninput="updateSimulation()">
                    </div>"""

assert old_sliders_html in text, "old_sliders_html not found"
text = text.replace(old_sliders_html, new_sliders_html)

# 2. Update updateSimulation() delta calculations and nominals in builder script
old_sim_code = """    // Update Slider Displays
    document.getElementById('val_P_CO').innerText = P_CO.toFixed(1);
    document.getElementById('val_T_rxn').innerText = T_rxn.toFixed(0);
    document.getElementById('val_T_spread').innerText = T_spread.toFixed(1);
    document.getElementById('val_Q_CO').innerText = Q_CO.toFixed(0);
    document.getElementById('val_Q_Fe').innerText = Q_Fe.toFixed(0);
    document.getElementById('val_Q_H2O').innerText = Q_H2O.toFixed(1);
    document.getElementById('val_Zone_Dev').innerText = Zone_Dev.toFixed(1);

    // Update Deltas vs Nominal Baseline
    document.getElementById('delta_P_CO').innerText = (P_CO - 60.0 >= 0 ? '+' : '') + (P_CO - 60.0).toFixed(1);
    document.getElementById('delta_T_rxn').innerText = (T_rxn - 1050 >= 0 ? '+' : '') + (T_rxn - 1050).toFixed(0);
    document.getElementById('delta_Q_CO').innerText = (Q_CO - 500 >= 0 ? '+' : '') + (Q_CO - 500).toFixed(0);
    document.getElementById('delta_Q_Fe').innerText = (Q_Fe - 180 >= 0 ? '+' : '') + (Q_Fe - 180).toFixed(0);"""

new_sim_code = """    const baselineSetpoints = {{ P_CO: 60.0, T_rxn: 950.0, T_spread: 25.0, Q_CO: 600.0, Q_Fe: 190.0, Q_H2O: 30.0, Zone_Dev: -5.0 }};

    // Update Slider Displays
    document.getElementById('val_P_CO').innerText = P_CO.toFixed(1) + ' atm';
    document.getElementById('val_T_rxn').innerText = T_rxn.toFixed(0) + ' °C';
    document.getElementById('val_T_spread').innerText = T_spread.toFixed(1) + ' °C';
    document.getElementById('val_Q_CO').innerText = Q_CO.toFixed(0) + ' SLPM';
    document.getElementById('val_Q_Fe').innerText = Q_Fe.toFixed(0) + ' SLPM';
    document.getElementById('val_Q_H2O').innerText = Q_H2O.toFixed(1) + ' ppmv';
    document.getElementById('val_Zone_Dev').innerText = Zone_Dev.toFixed(1) + ' °C';

    // Update Deltas vs Original Nominal Baseline
    document.getElementById('delta_P_CO').innerText = (P_CO - baselineSetpoints.P_CO >= 0 ? '+' : '') + (P_CO - baselineSetpoints.P_CO).toFixed(1);
    document.getElementById('delta_T_rxn').innerText = (T_rxn - baselineSetpoints.T_rxn >= 0 ? '+' : '') + Math.round(T_rxn - baselineSetpoints.T_rxn);
    if (document.getElementById('delta_T_spread')) document.getElementById('delta_T_spread').innerText = (T_spread - baselineSetpoints.T_spread >= 0 ? '+' : '') + (T_spread - baselineSetpoints.T_spread).toFixed(1);
    document.getElementById('delta_Q_CO').innerText = (Q_CO - baselineSetpoints.Q_CO >= 0 ? '+' : '') + Math.round(Q_CO - baselineSetpoints.Q_CO);
    document.getElementById('delta_Q_Fe').innerText = (Q_Fe - baselineSetpoints.Q_Fe >= 0 ? '+' : '') + Math.round(Q_Fe - baselineSetpoints.Q_Fe);
    if (document.getElementById('delta_Q_H2O')) document.getElementById('delta_Q_H2O').innerText = (Q_H2O - baselineSetpoints.Q_H2O >= 0 ? '+' : '') + (Q_H2O - baselineSetpoints.Q_H2O).toFixed(1);
    if (document.getElementById('delta_Zone_Dev')) document.getElementById('delta_Zone_Dev').innerText = (Zone_Dev - baselineSetpoints.Zone_Dev >= 0 ? '+' : '') + (Zone_Dev - baselineSetpoints.Zone_Dev).toFixed(1);"""

assert old_sim_code in text, "old_sim_code not found"
text = text.replace(old_sim_code, new_sim_code)

# 3. Update loadPreset('reset')
old_reset_code = """    }} else if (mode === 'reset') {{
        document.getElementById('sp_P_CO').value = 60.0;
        document.getElementById('sp_T_rxn').value = 1050;
        document.getElementById('sp_T_spread').value = 25.0;
        document.getElementById('sp_Q_CO').value = 500;
        document.getElementById('sp_Q_Fe').value = 180;
        document.getElementById('sp_Q_H2O').value = 20.0;
        document.getElementById('sp_Zone_Dev').value = -5.0;
        document.getElementById('paretoSlider').value = 50;
        updateSimulation();
        return;
    }}"""

new_reset_code = """    }} else if (mode === 'reset') {{
        document.getElementById('sp_P_CO').value = 60.0;
        document.getElementById('sp_T_rxn').value = 950;
        document.getElementById('sp_T_spread').value = 25.0;
        document.getElementById('sp_Q_CO').value = 600;
        document.getElementById('sp_Q_Fe').value = 190;
        document.getElementById('sp_Q_H2O').value = 30.0;
        document.getElementById('sp_Zone_Dev').value = -5.0;
        document.getElementById('paretoSlider').value = 50;
        updateSimulation();
        return;
    }}"""

assert old_reset_code in text, "old_reset_code not found"
text = text.replace(old_reset_code, new_reset_code)

with open(builder_path, "w", encoding="utf-8") as f:
    f.write(text)

print("[SUCCESS] Restored original input factor labels, nominals, and ranges in build_upgraded_gui.py")
