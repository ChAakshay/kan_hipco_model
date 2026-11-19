import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# High DPI 16:9 canvas
fig = plt.figure(figsize=(16, 9), dpi=300)
fig.patch.set_facecolor('#0B0F17')
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor('#0B0F17')
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

# Font family
plt.rcParams['font.family'] = 'DejaVu Sans'

# ================= TOP TITLE & SUBTITLE =================
ax.text(0.7, 8.55, "PRODUCT ARCHITECTURE & DATA FLOW", fontsize=10, fontweight='bold', color='#38BDF8', va='top')
ax.text(0.7, 8.22, "HiPCO Carbon Nanotube AI Controller \u2014 End-to-End Block Diagram",
        fontsize=21, fontweight='bold', color='#F8FAFC', va='top')
ax.text(0.7, 7.72, "Functional decomposition: Physical Plant Actuation \u2192 First-Principles Physics Bridge \u2192 PI-VRBF-KAN Surrogate \u2192 Inverse Autograd \u2192 Web DSS",
        fontsize=10.5, color='#94A3B8', va='top')

ax.plot([0.7, 15.3], [7.50, 7.50], color='#1E293B', lw=1.2)

# ================= 5 FUNCTIONAL PRODUCT BLOCKS =================
col_w = 2.65
gap = 0.35
start_x = 0.7
y_top = 7.30
card_h = 5.40
y_bot = y_top - card_h  # 1.90

blocks = [
    {
        "num": "BLOCK 1",
        "title": "INDUSTRIAL PLANT\n& DCS ACTUATION",
        "color": "#38BDF8",
        "bg": "#0D1E32",
        "sub_boxes": [
            ("HiPCO High-Pressure Reactor", ["• Quartz tube reactor (10-90 atm)", "• Multi-zone heating (800-1150 °C)", "• Pyrolysis of Fe(CO)5 precursor"]),
            ("7 Actuator Setpoints (u)", ["• CO Pressure (P_CO) & Carrier Flow", "• Fe Precursor & Trace H2O flows", "• Tube ID, Heated Length, Delta-T"]),
            ("Telemetry Ingestion Layer", ["• OPC-UA & Modbus TCP telemetry", "• 1-second continuous scan cycle"])
        ],
        "output_label": "Raw Plant Telemetry (7 Actuators)"
    },
    {
        "num": "BLOCK 2",
        "title": "PHYSICS-INFORMED\nFEATURE ENGINE",
        "color": "#F59E0B",
        "bg": "#2A1F0D",
        "sub_boxes": [
            ("First-Principles Bridge", ["• 17 governing transport equations", "• Transforms 7 inputs -> 11 invariants", "• Zero black-box unphysical drift"]),
            ("3 Transport Physics Domains", ["• Aerodynamics: Gas velocity, tau_res", "• Nucleation: [Fe] conc, cluster J_nuc", "• Kinetics: Boudouard driving force"]),
            ("Augmented Feature Vector", ["• Concatenates 7 raw + 11 physics", "• Outputs 18-D Physics Vector"])
        ],
        "output_label": "18-D Augmented Physics Vector"
    },
    {
        "num": "BLOCK 3",
        "title": "PI-VRBF-KAN\nAI NEURAL CORE",
        "color": "#10B981",
        "bg": "#0B261D",
        "sub_boxes": [
            ("Kolmogorov-Arnold Network", ["• Learnable 1D B-splines on edges", "• 1,305 parameters (93% < MLP)", "• 29.8 μs ultra-fast inference"]),
            ("Physics Conservation Loss", ["• Carbon mass conservation penalty", "• Subsonic barrier penalty (v < 0.85c)", "• R² = 0.998 on SWCNT Yield"]),
            ("9 Quality KPI Soft-Sensors", ["• SWCNT Yield (g/batch)", "• Raman G/D crystallinity ratio", "• UV-Vis Purity (%) & Fe/Ni/Cr ppm"])
        ],
        "output_label": "9 Predicted Quality KPIs"
    },
    {
        "num": "BLOCK 4",
        "title": "REAL-TIME INVERSE\nOPTIMIZER ENGINE",
        "color": "#6366F1",
        "bg": "#181836",
        "sub_boxes": [
            ("PyTorch Autograd (∇f)", ["• Analytical gradient through splines", "• Solves optimal recipe in 24.5 ms", "• 153x faster than Genetic Algs"]),
            ("KKT Constraint Enforcer", ["• Augmented Lagrangian multiplier", "• 0.0% constraint violation rate", "• Guarantees safe operating envelope"]),
            ("Symbolic & Uncertainty Suite", ["• Monte Carlo epistemic confidence", "• Closed-form symbolic rate laws"])
        ],
        "output_label": "Optimal Actuator Recipe (u*)"
    },
    {
        "num": "BLOCK 5",
        "title": "WEB DSS PLATFORM\n& 4 PERSONAS",
        "color": "#EC4899",
        "bg": "#2B1124",
        "sub_boxes": [
            ("Interactive Operator UI", ["• Real-time actuator sliders", "• 3D quality radar matrix", "• Epistemic model confidence gauge"]),
            ("4 Expert Persona Lenses", [
                "• Reaction Eng: Yield (±0.03 g)",
                "• Materials Sci: G/D crystal (>18.0)",
                "• Plant Mgr: 40% -> <2% scrap",
                "• AI Lead: 24.5 ms sub-sec control"
            ]),
            ("Recipe Dispatcher", ["• 1-click recipe push to DCS", "• Closed-loop setpoint update"])
        ],
        "output_label": "Setpoints Dispatch"
    }
]

# Draw blocks
for i, b in enumerate(blocks):
    x = start_x + i * (col_w + gap)
    color = b["color"]
    
    # Outer block container
    card = patches.FancyBboxPatch((x, y_bot), col_w, card_h,
                                  boxstyle="round,pad=0,rounding_size=0.12",
                                  facecolor='#0F172A', edgecolor=color, linewidth=1.8)
    ax.add_patch(card)
    
    # Top header bar inside card
    hdr = patches.FancyBboxPatch((x + 0.08, y_top - 0.78), col_w - 0.16, 0.70,
                                boxstyle="round,pad=0,rounding_size=0.08",
                                facecolor=b["bg"], edgecolor=color, linewidth=1.0)
    ax.add_patch(hdr)
    
    ax.text(x + 0.18, y_top - 0.22, b["num"], fontsize=7.5, fontweight='bold', color=color, va='center')
    ax.text(x + 0.18, y_top - 0.52, b["title"], fontsize=9.2, fontweight='bold', color='#F8FAFC', va='center', linespacing=1.1)
    
    # Sub-boxes
    curr_y = y_top - 0.95
    sub_h = 1.30
    for title, items in b["sub_boxes"]:
        sbox = patches.FancyBboxPatch((x + 0.10, curr_y - sub_h), col_w - 0.20, sub_h,
                                     boxstyle="round,pad=0,rounding_size=0.06",
                                     facecolor='#162032', edgecolor='#253349', linewidth=0.9)
        ax.add_patch(sbox)
        
        # Subbox title
        ax.text(x + 0.18, curr_y - 0.18, title, fontsize=7.6, fontweight='bold', color=color, va='center')
        ax.plot([x + 0.18, x + col_w - 0.18], [curr_y - 0.32, curr_y - 0.32], color='#253349', lw=0.7)
        
        # Items
        item_y = curr_y - 0.48
        for it in items:
            ax.text(x + 0.18, item_y, it, fontsize=6.8, color='#CBD5E1', va='top')
            item_y -= 0.25
            
        curr_y -= (sub_h + 0.12)
        
    # Forward Flow Arrow between blocks
    if i < 4:
        arr_x1 = x + col_w
        arr_x2 = arr_x1 + gap
        arr_y = y_bot + card_h * 0.50
        
        # Line + Arrow
        ax.annotate("", xy=(arr_x2 - 0.03, arr_y), xytext=(arr_x1 + 0.03, arr_y),
                    arrowprops=dict(arrowstyle="->,head_width=0.35,head_length=0.45",
                                    color='#38BDF8', lw=2.2))
        
        # Flow data pill badge on connector
        badge_w = gap + 0.25
        # Label above arrow
        lbl = b["output_label"].replace(" (", "\n(").replace(" -> ", "\n-> ")
        ax.text((arr_x1 + arr_x2) / 2.0, arr_y + 0.18, b["output_label"],
                fontsize=6.2, fontweight='bold', color='#38BDF8', ha='center', va='bottom',
                bbox=dict(boxstyle="round,pad=0.22", facecolor='#0B132B', edgecolor='#0284C7', lw=0.8))

# ================= BOTTOM CLOSED-LOOP CONTROL BUS =================
loop_y = 0.40
loop_h = 1.05
loop_w = 14.6
loop_box = patches.FancyBboxPatch((0.7, loop_y), loop_w, loop_h,
                                 boxstyle="round,pad=0,rounding_size=0.12",
                                 facecolor="#111827", edgecolor="#EC4899", linewidth=1.6)
ax.add_patch(loop_box)

# Reverse dashed flow line from Block 5 (right) back to Block 1 (left)
ax.annotate("", xy=(1.5, loop_y + 0.48), xytext=(14.5, loop_y + 0.48),
            arrowprops=dict(arrowstyle="->,head_width=0.42,head_length=0.55",
                            color='#F43F5E', lw=2.5, linestyle='--'))

# Central Badge for closed-loop
badge_rect = patches.FancyBboxPatch((4.5, loop_y + 0.22), 7.0, 0.62,
                                   boxstyle="round,pad=0,rounding_size=0.08",
                                   facecolor="#1F1329", edgecolor="#E11D48", linewidth=1.4)
ax.add_patch(badge_rect)

ax.text(8.0, loop_y + 0.58, "\u26a1 CLOSED-LOOP SUB-SECOND RECIPE FEEDBACK (24.5 ms)",
        fontsize=9.5, fontweight='bold', color='#FDA4AF', ha='center', va='center')
ax.text(8.0, loop_y + 0.36, "Target Inversion (Autograd \u2207_u J) \u2192 KKT Feasibility Verified \u2192 Actuator Setpoint Updates Directly to DCS",
        fontsize=7.6, color='#F1F5F9', ha='center', va='center')

# Labels on left & right of feedback bus
ax.text(1.2, loop_y + 0.78, "\u21a9 Setpoint Updates (u*)", fontsize=7.6, fontweight='bold', color='#38BDF8', ha='left')
ax.text(14.8, loop_y + 0.78, "Autonomous Dispatch \u21aa", fontsize=7.6, fontweight='bold', color='#F43F5E', ha='right')

out_path = r"c:\Users\aaksh\Downloads\paper\product_block_diagram.png"
plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0.15)
plt.close()
print(f"[SUCCESS] Product block diagram rendered to {out_path}")
