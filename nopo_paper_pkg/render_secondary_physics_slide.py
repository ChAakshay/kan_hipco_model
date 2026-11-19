import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Global font styling
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['mathtext.fontset'] = 'dejavusans'

# 16:9 Widescreen (16 x 9 inches) at 300 DPI
fig = plt.figure(figsize=(16, 9), dpi=300)
fig.patch.set_facecolor('#080B10')
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor('#080B10')
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

# Top Banner Header
ax.text(0.8, 8.55, "SLIDE 21  •  FEATURE TRANSCENDENCE & THE PHYSICS BRIDGE  •  [17 FIRST-PRINCIPLES TRANSPORT LAWS]",
        fontsize=11, fontweight='bold', color='#00D2FF', va='top')

ax.text(0.8, 8.20, "Deriving Secondary Physics Transport Parameters",
        fontsize=24, fontweight='bold', color='#F3F4F6', va='top')

ax.text(0.8, 7.68, "Transforming 7 Raw Plant DCS Actuators into 11 Internal Aerodynamic, Thermal & Kinetic State Invariants",
        fontsize=12.5, color='#94A3B8', va='top')

ax.plot([0.8, 15.2], [7.42, 7.42], color='#1E283C', lw=1.5)

# 3 Cards Layout
card_w = 4.55
card_h = 6.90
y_top = 7.22
y_bottom = y_top - card_h

cards_config = [
    {
        "x": 0.8,
        "border": "#00D2FF",
        "title": "1. AERODYNAMICS & RESIDENCE TIME",
        "domain": "Navier-Stokes Fluid Dynamics & Gas Expansion",
        "eqs": [
            ("Volumetric Gas Expansion (Ideal Gas):",
             r"$Q_{\mathrm{actual}} = Q_{\mathrm{CO}} \cdot \left(\frac{T_{\mathrm{rxn}} + 273.15}{298.15}\right) \cdot \left(\frac{1}{P_{\mathrm{CO}}}\right)$",
             "Actual gas volume expands with temperature and contracts under pressure."),
            
            ("Linear Gas Velocity (v_gas):",
             r"$v_{\mathrm{gas}} = \frac{4 \cdot Q_{\mathrm{actual}}}{\pi \cdot D_{\mathrm{tube}}^2} \quad \left[20 \text{ to } 180\ \mathrm{m/s}\right]$",
             "Carrier velocity determines boundary-layer shear and aerosol suspension."),
            
            ("Hot-Zone Transit Time (\u03c4_res):",
             r"$\tau_{\mathrm{res}} = \frac{L_{\mathrm{hot\ zone}}}{v_{\mathrm{gas}}} \quad \left[1 \text{ to } 6\ \mathrm{s}\right]$",
             "Exact residence time available for catalyst growth before thermal quench."),
            
            ("Fluid Flow Regime (Reynolds Number):",
             r"$\mathrm{Re} = \frac{\rho(P, T) \cdot v_{\mathrm{gas}} \cdot D_{\mathrm{tube}}}{\mu(T)}$",
             "Governs laminar core stability vs turbulent boundary mixing.")
        ],
        "features": "Derived: Residence_Time_s, Reynolds_Number, Linear_Velocity",
        "takeaways": [
            "Insight: Catalyst clusters only grow while inside the hot zone (1\u20136 s).",
            "Velocity must balance precursor mixing without causing sonic shear."
        ]
    },
    {
        "x": 5.72,
        "border": "#F59E0B",
        "title": "2. CATALYST NUCLEATION & BOUNDARY",
        "domain": "Precursor Pyrolysis & Aerosol Condensation",
        "eqs": [
            ("Active Iron Concentration ([Fe]):",
             r"$[\mathrm{Fe}] = \left(\frac{Q_{\mathrm{Fe}} \cdot P_{\mathrm{sat}}(T_{\mathrm{bubbler}})}{Q_{\mathrm{CO}} \cdot P_{\mathrm{CO}}}\right) \times 10^6 \quad \left[100 \text{ to } 1200\ \mathrm{ppm}\right]$",
             "True gas-phase density of decomposed Fe(CO)5 precursor vapor."),
            
            ("Homogeneous Nucleation Rate (J_nuc):",
             r"$J_{\mathrm{nuc}} = k_0 \cdot [\mathrm{Fe}]^2 \cdot \exp\left(-\frac{\Delta G^*}{R \cdot T_{\mathrm{rxn}}}\right)$",
             "Rate of iron atom condensation into critical 1.2 nm growth seeds."),
            
            ("Thermal Boundary Layer Thickness (\u03b4_th):",
             r"$\delta_{\mathrm{th}} = \frac{D_{\mathrm{tube}}}{\sqrt{\mathrm{Re}}} \cdot \mathrm{Pr}^{-1/3} \quad \left[1 \text{ to } 8\ \mathrm{mm}\right]$",
             "Wall-to-centerline temperature lag across reactor cross-section."),
            
            ("Catalyst Growth vs Deactivation Ratio:",
             r"$\Phi_{\mathrm{cat}} = \frac{\tau_{\mathrm{growth}}}{\tau_{\mathrm{encapsulation}}}$",
             "Competition between continuous tube extrusion and soot poisoning.")
        ],
        "features": "Derived: Fe_Concentration_ppm, Nucleation_Est, Boundary_Layer",
        "takeaways": [
            "Insight: Fe(CO)5 pyrolyzes at 800\u00b0C into atomic Fe active seeds.",
            "Excess temperature triggers Ostwald ripening into dead iron chunks."
        ]
    },
    {
        "x": 10.65,
        "border": "#00E599",
        "title": "3. REACTION THERMODYNAMICS & CHEMISTRY",
        "domain": "Boudouard Equilibrium & Water Volcano Etching",
        "eqs": [
            ("Boudouard Disproportionation Equilibrium:",
             r"$2\,\mathrm{CO}_{(\mathrm{g})} \rightleftharpoons \mathrm{C}_{(\mathrm{SWCNT})} + \mathrm{CO}_{2(\mathrm{g})}, \quad \Delta H^\circ = -172.5\ \mathrm{kJ/mol}$",
             "Exothermic carbon deposition reaction driving nanotube assembly."),
            
            ("Temperature-Dependent Equilibrium (K_eq):",
             r"$\ln K_{\mathrm{eq}}(T) = \frac{20{,}750}{T_{\mathrm{rxn}} + 273.15} - 21.05$",
             "Calculates thermodynamic ceiling via integrated van 't Hoff relation."),
            
            ("Carbon Chemical Driving Force (\u0394G_drive):",
             r"$\Delta G_{\mathrm{drive}} = \frac{K_{\mathrm{eq}}(T) \cdot P_{\mathrm{CO}}^2}{P_{\mathrm{CO2}}} \quad \left(\propto P_{\mathrm{CO}}^2\right)$",
             "Pressure quadratically accelerates carbon deposition rate onto seeds."),
            
            ("Trace-Water Etching Ratio (\u03c7_H2O):",
             r"$\chi_{\mathrm{H2O}} = \frac{Q_{\mathrm{H2O}}}{Q_{\mathrm{CO}}} \quad [\mathrm{ppmv/SLPM}]$",
             "Volcano peak: selectively gasifies amorphous soot without damaging SWCNT.")
        ],
        "features": "Derived: Boudouard_DrivingForce, P_CO2_bar, Water_CO_Ratio",
        "takeaways": [
            "Insight: Pressure (P\u00b2) drives yield; trace water (16\u201324 ppmv) selectively",
            "gasifies defective sp3 carbon, boosting Raman G/D crystallinity."
        ]
    }
]

for card in cards_config:
    x = card["x"]
    border = card["border"]
    
    # Background Card Box
    box = patches.FancyBboxPatch((x, y_bottom), card_w, card_h,
                                 boxstyle="round,pad=0,rounding_size=0.18",
                                 facecolor="#111827", edgecolor=border, linewidth=1.8)
    ax.add_patch(box)
    
    # Card Header
    ax.text(x + 0.22, y_top - 0.28, card["title"],
            fontsize=11.5, fontweight='bold', color=border, va='top')
    ax.text(x + 0.22, y_top - 0.58, card["domain"],
            fontsize=9.2, fontweight='bold', color='#94A3B8', va='top')
    
    ax.plot([x + 0.22, x + card_w - 0.22], [y_top - 0.76, y_top - 0.76], color='#1E283C', lw=1.0)
    
    # Render Equations
    curr_y = y_top - 0.92
    for label, eq_tex, desc in card["eqs"]:
        ax.text(x + 0.22, curr_y, label, fontsize=9.0, fontweight='bold', color='#E2E8F0', va='top')
        curr_y -= 0.24
        
        ax.text(x + 0.26, curr_y, eq_tex, fontsize=10.2, 
                color='#38BDF8' if border == '#00D2FF' else ('#FBBF24' if border == '#F59E0B' else '#34D399'), va='top')
        curr_y -= 0.38
        
        ax.text(x + 0.22, curr_y, desc, fontsize=7.8, color='#94A3B8', style='italic', va='top')
        curr_y -= 0.38
    
    # Feature pill bar
    pill_box = patches.FancyBboxPatch((x + 0.18, y_bottom + 0.82), card_w - 0.36, 0.40,
                                     boxstyle="round,pad=0,rounding_size=0.08",
                                     facecolor="#182234", edgecolor='#2A3B53', linewidth=1.0)
    ax.add_patch(pill_box)
    ax.text(x + card_w / 2.0, y_bottom + 1.02, card["features"],
            fontsize=7.8, fontweight='bold', 
            color='#38BDF8' if border == '#00D2FF' else ('#FBBF24' if border == '#F59E0B' else '#34D399'),
            ha='center', va='center')
    
    # Engineering takeaway box
    takeaway_box = patches.FancyBboxPatch((x + 0.18, y_bottom + 0.12), card_w - 0.36, 0.60,
                                         boxstyle="round,pad=0,rounding_size=0.08",
                                         facecolor="#0B0F17", edgecolor=border, linewidth=0.8)
    ax.add_patch(takeaway_box)
    
    ax.text(x + 0.26, y_bottom + 0.58, card["takeaways"][0], fontsize=7.6, color='#E2E8F0', va='top')
    ax.text(x + 0.26, y_bottom + 0.36, card["takeaways"][1], fontsize=7.6, color='#CBD5E1', va='top')

out_path = r"c:\Users\aaksh\Downloads\paper\secondary_physics_parameters.png"
plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0.1)
plt.close()
print(f"[SUCCESS] High-resolution graphic polished and saved to: {out_path}")
