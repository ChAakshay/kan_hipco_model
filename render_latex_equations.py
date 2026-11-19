import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['DejaVu Serif', 'Times New Roman']

EQ_DIR = r"c:\Users\aaksh\Downloads\paper\nopo_paper_pkg\equations"
os.makedirs(EQ_DIR, exist_ok=True)

# Note: Avoid \left( ... \right) around \sum with limits in Matplotlib cmex10 to prevent glyph substitution artifacts.
DISPLAY_EQUATIONS = [
    (
        "eq1.png",
        r"$2\mathrm{CO} \rightleftharpoons \mathrm{C}_{(\mathrm{SWCNT})} + \mathrm{CO}_2, \qquad \Delta H^{\circ} = -172.5\;\mathrm{kJ/mol}$",
        "(1)"
    ),
    (
        "eq2.png",
        r"$\nabla_{\mathbf{u}} f(\mathbf{u}) = \mathbf{0} \quad \mathrm{for\;Lebesgue\text{-}almost\text{-}every}\; \mathbf{u} \in \mathcal{U}$",
        "(2)"
    ),
    (
        "eq3.png",
        r"$\mathcal{P} = (\mathcal{P}_1, \mathcal{P}_2, \dots, \mathcal{P}_{11})^{\top} : \mathcal{U} \subset \mathbb{R}^{7} \longrightarrow \mathbb{R}^{11}, \qquad \mathbf{z} = \mathcal{P}(\mathbf{u})$",
        "(3)"
    ),
    (
        "eq4.png",
        r"$\tau_{\mathrm{res}} = \frac{V_{\mathrm{rxn}}\, P_{\mathrm{CO}}\, T_{\mathrm{std}}}{(Q_{\mathrm{CO}} + Q_{\mathrm{Fe}})\, P_{\mathrm{std}}\, T_{\mathrm{rxn}}}, \qquad v_{\mathrm{gas}} = \frac{4(Q_{\mathrm{CO}} + Q_{\mathrm{Fe}})\, P_{\mathrm{std}}\, T_{\mathrm{rxn}}}{\pi\, D_{\mathrm{noz}}^{2}\, P_{\mathrm{CO}}\, T_{\mathrm{std}}}$",
        "(4)"
    ),
    (
        "eq5.png",
        r"$u_i^{(k)} = \hat{F}_i^{-1}\left(\Phi\left(\frac{Z_i^{(k)}}{\sqrt{\Sigma_{ii}}}\right)\right), \quad i = 1, \dots, 7, \qquad \mathbf{Z}^{(k)} \sim \mathcal{N}(\mathbf{0},\, \mathbf{\Sigma}_{\mathrm{emp}})$",
        "(5)"
    ),
    (
        "eq6.png",
        r"$\phi_{i,j}(x_i) = w_{b,i,j} \cdot \mathrm{SiLU}(x_i) + \sum_{k=1}^{K} c_{k,i,j} \cdot \exp\left(-\gamma_k (x_i - \mu_k)^{2}\right)$",
        "(6)"
    ),
    (
        "eq7.png",
        r"$\frac{\partial \phi_{i,j}}{\partial x_i} = w_{b,i,j}\,\sigma(x_i)\left[1 + x_i(1 - \sigma(x_i))\right] - 2\sum_{k=1}^{K} c_{k,i,j}\,\gamma_k(x_i - \mu_k)\exp\left(-\gamma_k(x_i - \mu_k)^{2}\right)$",
        "(7)"
    ),
    (
        "eq8.png",
        r"$h_j = \mathrm{LayerNorm}\left[\sum_{i=1}^{18} \phi_{i,j}^{(0)}(x_i) + b_j^{(0)}\right]$",
        "(8)"
    ),
    (
        "eq9.png",
        r"$\hat{y}_m = \sum_{j=1}^{16} \phi_{j,m}^{(1)}(h_j) + b_m^{(1)}, \qquad m = 1, \dots, 9$",
        "(9)"
    ),
    (
        "eq10.png",
        r"$\mathcal{L}_{\mathrm{pre}} = \frac{1}{N_{\mathrm{synth}}} \sum_{n=1}^{N_{\mathrm{synth}}} \Vert \hat{\mathbf{y}}^{(n)} - \mathbf{y}^{(n)} \Vert_{2}^{2} + \lambda_{L_1} \sum_{l,i,j,k} \left| c_{k,i,j}^{(l)} \right|$",
        "(10)"
    ),
    (
        "eq11.png",
        r"$\mathcal{L}_{\mathrm{fine}} = \frac{1}{N} \sum_{n=1}^{N} \Vert \hat{\mathbf{y}}^{(n)} - \mathbf{y}^{(n)} \Vert_{2}^{2} + \lambda_{\mathrm{PINN}} \cdot \mathbb{E}\left[\max\left(0,\, -\frac{\partial \hat{y}_{\mathrm{Yield}}}{\partial P_{\mathrm{CO}}}\right)^{2}\right]$",
        "(11)"
    ),
    (
        "eq12.png",
        r"$\nabla_{\mathbf{u}} \hat{\mathbf{y}} = \frac{\partial f_{\theta}}{\partial \mathbf{u}} + \frac{\partial f_{\theta}}{\partial \mathbf{z}} \cdot \frac{\partial \mathcal{P}}{\partial \mathbf{u}}$",
        "(12)"
    ),
    (
        "eq13.png",
        r"$\mathcal{L}_{A}(\mathbf{u}; \mathbf{\lambda}, \rho) = \sum_{m=1}^{9} w_m \left(\frac{\hat{y}_m(\mathbf{u}) - y_m^{*}}{\sigma_m}\right)^{2} + \lambda_{\mathrm{box}} \sum_{i=1}^{7} \psi_{\mathrm{box}}(u_i) + \frac{1}{2\rho} \sum_{j=1}^{J} \left\{[\max(0,\, \lambda_j + \rho\, g_j(\mathbf{u}))]^{2} - \lambda_j^{2}\right\}$",
        "(13)"
    ),
    (
        "eq14.png",
        r"$\lambda_j^{(t+1)} = \max\left(0,\, \lambda_j^{(t)} + \rho^{(t)}\, g_j(\mathbf{u}^{(t)})\right), \qquad \rho^{(t+1)} = 2\rho^{(t)} \;\mathrm{if}\; \max_j g_j(\mathbf{u}^{(t)}) > \tau_{\mathrm{tol}} \;\mathrm{else}\; \rho^{(t)}$",
        "(14)"
    ),
    (
        "eq15.png",
        r"$\mathbf{\theta}_{t+1} = \mathbf{\theta}_t + \mathbf{w}_t, \quad \mathbf{w}_t \sim \mathcal{N}(\mathbf{0}, \mathbf{Q}), \qquad \mathbf{y}_t = \mathbf{H}_t\,\mathbf{\theta}_t + \mathbf{v}_t, \quad \mathbf{v}_t \sim \mathcal{N}(\mathbf{0}, \mathbf{R})$",
        "(15)"
    ),
    (
        "eq16.png",
        r"$\mathbf{K}_t = \mathbf{P}_{t|t-1}\mathbf{H}_t^{\top}\left(\mathbf{H}_t \mathbf{P}_{t|t-1} \mathbf{H}_t^{\top} + \mathbf{R}\right)^{-1}, \qquad \hat{\mathbf{\theta}}_{t|t} = \hat{\mathbf{\theta}}_{t|t-1} + \mathbf{K}_t\left(\mathbf{y}_t - \mathbf{H}_t \hat{\mathbf{\theta}}_{t|t-1}\right)$",
        "(16)"
    ),
]

TABLE8_EQUATIONS = [
    (
        "sym1.png",
        r"$22.40\,\exp\left(-\frac{(T_{\mathrm{rxn}} - 1042.0)^{2}}{2(42.0)^{2}}\right) - 0.0018\,\max(0,\, T_{\mathrm{rxn}} - 1080.0)^{2}$"
    ),
    (
        "sym2.png",
        r"$\frac{3.32\, P_{\mathrm{CO}}^{2.15}}{25.0^{2.15} + P_{\mathrm{CO}}^{2.15}}$"
    ),
    (
        "sym3.png",
        r"$56.80\,\exp\left(-\frac{(Q_{\mathrm{H2O}} - 18.2)^{2}}{2(9.8)^{2}}\right) - 0.28\, Q_{\mathrm{H2O}} + 12.00$"
    ),
    (
        "sym4.png",
        r"$2.95\left(1 - e^{-Q_{\mathrm{Fe}} / 78.0}\right) - 2.20 \times 10^{-5}\,\max(0,\, Q_{\mathrm{Fe}} - 220.0)^{2.05}$"
    ),
]


def render_display_equations():
    for fname, latex_str, eq_num in DISPLAY_EQUATIONS:
        fs = 10.2 if fname in ("eq7.png", "eq13.png") else 11.0
        fig = plt.figure(figsize=(6.8, 0.52), dpi=600)
        fig.patch.set_facecolor('white')
        fig.text(0.47, 0.5, latex_str, ha='center', va='center', fontsize=fs, color='#000000')
        fig.text(0.98, 0.5, eq_num, ha='right', va='center', fontsize=10.0, color='#000000', family='serif')
        out_path = os.path.join(EQ_DIR, fname)
        fig.savefig(out_path, dpi=600, pad_inches=0.02, facecolor='white')
        plt.close(fig)
        print("Rendered:", fname)

    for fname, latex_str in TABLE8_EQUATIONS:
        fig = plt.figure(figsize=(4.0, 0.50), dpi=600)
        fig.patch.set_facecolor('none')
        fig.text(0.01, 0.5, latex_str, ha='left', va='center', fontsize=11.0, color='#000000')
        out_path = os.path.join(EQ_DIR, fname)
        fig.savefig(out_path, dpi=600, bbox_inches='tight', pad_inches=0.03, transparent=True)
        plt.close(fig)
        print("Rendered:", fname)


if __name__ == '__main__':
    render_display_equations()
