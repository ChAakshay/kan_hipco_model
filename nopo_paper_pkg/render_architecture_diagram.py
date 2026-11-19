import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Styling
plt.rcParams['font.family'] = 'DejaVu Sans'

# 16:9 Widescreen (16 x 9 inches) at 300 DPI
fig = plt.figure(figsize=(16, 9), dpi=300)
fig.patch.set_facecolor('#07090E')
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor('#07090E')
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

# ================= TOP HEADER =================
ax.text(0.7, 8.58, "SYSTEM ARCHITECTURE  \u2022  CYBER-PHYSICAL DIGITAL TWIN & INVERSE CONTROL",
        fontsize=10.5, fontweight='bold', color='#00F2FE', va='top')
ax.text(0.7, 8.24, "HiPCO KAN End-to-End System Architecture",
        fontsize=22, fontweight='bold', color='#F8FAFC', va='top')
ax.text(0.7, 7.74, "Hierarchical Integration of Industrial DCS Actuation, First-Principles Physics Bridge, Kolmogorov-Arnold Neural Networks, and Real-Time Autograd Inversion",
        fontsize=11.0, color='#94A3B8', va='top')

# Accent top line
ax.plot([0.7, 15.3], [7.50, 7.50], color='#1E293B', lw=1.5)

# ================= 5 MAIN ARCHITECTURAL PILLARS =================
col_w = 2.65
gap = 0.34
start_x = 0.7
y_top = 7.30
card_h = 5.55
y_bot = y_top - card_h  # 1.75

cols_data = [
    {
        "id": "LAYER 1",
        "title": "PLANT ACTUATION &\nDCS INGESTION",
        "subtitle": "Raw Industrial Control & Sensors",
        "color": "#38BDF8", # Sky Cyan
        "bg_badge": "#0369A1",
        "items": [
            ("7 Primary Plant Actuators", [
                "• CO Gas Pressure (P_CO: 10\u201390 atm)",
                "• Reaction Temp (T_rxn: 800\u20131150 \u00b0C)",
                "• Thermal Spread (\u0394T: 0\u201380 \u00b0C)",
                "• CO Carrier Flow (Q_CO: 100\u20131000 SLPM)",
                "• Fe Precursor Flow (Q_Fe: 10\u2013350 SLPM)",
                "• Trace Water Flow (Q_H2O: 1\u201350 ppmv)",
                "• Zone Setpoint Deviation (\u0394T_zone)"
            ]),
            ("Industrial Field Protocols", [
                "• OPC-UA & Modbus TCP Ingestion",
                "• 1-Second DCS Scan Rate Cycle",
                "• Emerson DeltaV / Yokogawa Historian"
            ])
        ]
    },
    {
        "id": "LAYER 2",
        "title": "17-EQUATION\nPHYSICS BRIDGE",
        "subtitle": "Transport & Kinetic Invariants",
        "color": "#F59E0B", # Amber
        "bg_badge": "#B45309",
        "items": [
            ("Fluid Dynamics & Aerodynamics", [
                "• Ideal Gas Volume Expansion (Q_actual)",
                "• Linear Gas Velocity (v_gas: 20\u2013180 m/s)",
                "• Hot-Zone Transit Time (\u03c4_res = L / v_gas)",
                "• Reynolds Number (Re: Laminar vs Turb)"
            ]),
            ("Precursor Pyrolysis & Aerosol", [
                "• Active Gas Iron Conc. ([Fe] ppm)",
                "• Homogeneous Nucleation Rate (J_nuc)",
                "• Thermal Boundary Layer (\u03b4_th mm)"
            ]),
            ("Boudouard Chemical Kinetics", [
                "• Driving Force (\u0394G \u221d K_eq \u00b7 P_CO\u00b2 / P_CO2)",
                "• Water-to-Carbon Etching Ratio (\u03c7_H2O)"
            ])
        ]
    },
    {
        "id": "LAYER 3",
        "title": "PI-VRBF-KAN\nNEURAL CORE",
        "subtitle": "Physics-Informed Spline Manifold",
        "color": "#818CF8", # Indigo
        "bg_badge": "#4338CA",
        "items": [
            ("Kolmogorov-Arnold Architecture", [
                "• 18 Inputs \u2192 Shared Hidden \u2192 9 Outputs",
                "• Learnable Univariate 1D Edge Splines",
                "• \u03d5(x) = w_b\u00b7SiLU(x) + w_s\u00b7\u2211 c_m B_m(x)",
                "• 1,305 Parameters (93.6% < MLPs)"
            ]),
            ("Physics-Informed Loss (PINN)", [
                "• L_total = L_MSE + \u03bb\u2081 L_carbon + \u03bb\u2082 L_sonic",
                "• Carbon Mass Balance Conservation",
                "• Subsonic Penalty Barrier (v < 0.85 c)"
            ]),
            ("Computational Performance", [
                "• 29.8 \u03bcs Forward Inference Latency",
                "• Continuous C\u00b2 Analytical Derivatives"
            ])
        ]
    },
    {
        "id": "LAYER 4",
        "title": "SCIENTIFIC AI\nMICROSERVICES",
        "subtitle": "Active Intelligence & Soft-Sensing",
        "color": "#34D399", # Emerald
        "bg_badge": "#047857",
        "items": [
            ("Multi-Target Soft-Sensing (9 KPIs)", [
                "• SWCNT Yield (g/batch, R\u00b2=0.998)",
                "• Raman G/D Crystallinity (R\u00b2=0.999)",
                "• UV-Vis Optical Purity (R\u00b2=0.999)",
                "• Fe, Ni, Cr Axial & Radial ppm"
            ]),
            ("Uncertainty & Discovery", [
                "• Monte Carlo Epistemic Gauge (\u03c3_epistemic)",
                "• Fast Permutation SHAP Attributions",
                "• Closed-Form Symbolic Rate Law Extraction",
                "• Active Learning Campaign Recommender"
            ])
        ]
    },
    {
        "id": "LAYER 5",
        "title": "WEB DECISION SUPPORT\n& INVERSE CONTROL",
        "subtitle": "Closed-Loop Cyber-Physical UX",
        "color": "#E879F9", # Fuchsia
        "bg_badge": "#A21CAF",
        "items": [
            ("Interactive Operator UI (Port 8050)", [
                "• 7 Responsive Actuator Sliders",
                "• 3D Spider Radar Quality Matrix",
                "• Live Physics Telemetry HUD Tiles",
                "• Real-Time Pareto Frontier Visualizer"
            ]),
            ("KKT Autograd Recipe Solver", [
                "• Projected PyTorch Gradient Descent",
                "• Solves Recipes in 24.5 ms (153x faster)",
                "• 0.0% Constraint / Boundary Violations"
            ])
        ]
    }
]

for i, col in enumerate(cols_data):
    x = start_x + i * (col_w + gap)
    color = col["color"]
    
    # Pillar Container Card
    box = patches.FancyBboxPatch((x, y_bot), col_w, card_h,
                                 boxstyle="round,pad=0,rounding_size=0.14",
                                 facecolor="#0F172A", edgecolor=color, linewidth=1.6)
    ax.add_patch(box)
    
    # Layer ID Badge
    badge_bg = patches.FancyBboxPatch((x + 0.16, y_top - 0.36), 0.95, 0.22,
                                     boxstyle="round,pad=0,rounding_size=0.06",
                                     facecolor=col["bg_badge"], edgecolor='none')
    ax.add_patch(badge_bg)
    ax.text(x + 0.635, y_top - 0.25, col["id"],
            fontsize=7.8, fontweight='bold', color='#FFFFFF', ha='center', va='center')
    
    # Pillar Header (2-line title support)
    ax.text(x + 0.16, y_top - 0.50, col["title"],
            fontsize=8.8, fontweight='bold', color=color, va='top', linespacing=1.15)
    ax.text(x + 0.16, y_top - 0.92, col["subtitle"],
            fontsize=7.2, color='#94A3B8', va='top')
    
    ax.plot([x + 0.16, x + col_w - 0.16], [y_top - 1.06, y_top - 1.06], color='#1E293B', lw=1.0)
    
    # Content Sections
    curr_y = y_top - 1.18
    for sec_title, bullets in col["items"]:
        # Section title tag
        sec_box = patches.FancyBboxPatch((x + 0.12, curr_y - 0.18), col_w - 0.24, 0.21,
                                         boxstyle="round,pad=0,rounding_size=0.04",
                                         facecolor='#1E293B', edgecolor='none')
        ax.add_patch(sec_box)
        ax.text(x + 0.18, curr_y - 0.08, sec_title,
                fontsize=7.4, fontweight='bold', color='#F1F5F9', va='center')
        curr_y -= 0.28
        
        for b in bullets:
            ax.text(x + 0.16, curr_y, b, fontsize=6.9, color='#CBD5E1', va='top')
            curr_y -= 0.195
        curr_y -= 0.08

    # Clean forward connector arrow in the gap between pillars
    if i < 4:
        arr_x = x + col_w + 0.05
        arr_target = arr_x + gap - 0.10
        arr_y = y_bot + card_h * 0.58
        ax.annotate("", xy=(arr_target, arr_y), xytext=(arr_x, arr_y),
                    arrowprops=dict(arrowstyle="->,head_width=0.32,head_length=0.40",
                                    color='#38BDF8', lw=2.0))
        ax.text((arr_x + arr_target)/2.0, arr_y + 0.14, "Forward",
                fontsize=6.8, fontweight='bold', color='#38BDF8', ha='center', va='bottom')

# ================= BOTTOM CLOSED-LOOP FEEDBACK CHANNEL =================
loop_box = patches.FancyBboxPatch((0.7, 0.38), 14.6, 1.05,
                                 boxstyle="round,pad=0,rounding_size=0.12",
                                 facecolor="#111827", edgecolor="#00F2FE", linewidth=1.5)
ax.add_patch(loop_box)

# Reverse dashed flow line from Layer 5 to Layer 1
ax.annotate("", xy=(1.5, 0.65), xytext=(14.5, 0.65),
            arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.5",
                            color='#E879F9', lw=2.2, linestyle='--'))

# Badge in center of bottom loop
loop_badge = patches.FancyBboxPatch((4.8, 0.76), 6.4, 0.52,
                                   boxstyle="round,pad=0,rounding_size=0.08",
                                   facecolor="#1E1B4B", edgecolor='#A855F7', linewidth=1.2)
ax.add_patch(loop_badge)

ax.text(8.0, 1.04, "\u26a1 CLOSED-LOOP AUTOGRAD INVERSE OPTIMIZATION (\u2207_u J) IN 24.5 ms",
        fontsize=9.2, fontweight='bold', color='#F0ABFC', ha='center', va='center')
ax.text(8.0, 0.88, "Operator Target Constraints \u2192 Instant KKT Projected Setpoint Synthesis \u2192 DCS Actuation Feedback Loop",
        fontsize=7.8, color='#CBD5E1', ha='center', va='center')

# Left return badge
ax.text(1.2, 0.95, "\u21a9 Actuator Setpoint Updates", fontsize=7.6, fontweight='bold', color='#38BDF8', ha='left')
# Right origin badge
ax.text(14.8, 0.95, "Optimal Recipes \u21aa", fontsize=7.6, fontweight='bold', color='#E879F9', ha='right')

out_path = r"c:\Users\aaksh\Downloads\paper\system_architecture_diagram.png"
plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0.12)
plt.close()
print(f"[SUCCESS] Polished architecture diagram saved to: {out_path}")
