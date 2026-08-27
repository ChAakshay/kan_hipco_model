# Data Card: Physics-Augmented HiPCO Synthetic Dataset

## 1. Dataset Overview
- **Large Training Dataset**: 5000 rows (`SWCNT_synthetic_5000.csv` / `.xlsx`)
- **Matched Validation Dataset**: 50 rows (`SWCNT_synthetic_50_matched.csv` / `.xlsx`, matching real production batch count)
- **Feature Space**: 7 Process Control Setpoints + 11 Secondary Physics Engine Outputs = 18 Total Inputs
- **Quality Target Space**: 9 Nanotube Quality Metrics (Raman $G/D$, UV-Vis Optical Purity %, Batch Yield g, Fe/Ni/Cr Axial & Radial ppm)

---

## 2. Literature-Bounded Input Parameter Ranges
| Parameter Name | Process Variable | Range Min | Range Max | Unit | Citation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `P_CO_atm` | Reactor Pressure | 10.0 | 90.0 | atm | Nikolaev et al. (1999) |
| `T_rxn_mean_C` | Growth Zone Temp | 800.0 | 1150.0 | °C | Bronikowski et al. (2001) |
| `T_spread_C` | Thermal Gradient | 0.0 | 80.0 | °C | HiPCO Reactor Specs |
| `Flow_CO_SLPM` | CO Gas Flow | 100.0 | 1000.0 | SLPM | Dateo et al. (2002) |
| `Flow_Fe_Precursor_SLPM` | Catalyst Carrier Flow | 10.0 | 350.0 | SLPM | Bronikowski et al. (2001) |
| `H2O_Flow_ppmv` | H2O Moderation Flow | 1.0 | 50.0 | ppmv | Dateo et al. (2002) |
| `Zone_SP_Dev_C` | Setpoint Deviation | -35.0 | 15.0 | °C | Production Historian |

---

## 3. Correlation & Noise Models
- **Empirical Correlation Matrix $C \in \mathbb{R}^{7 \times 7}$**: Fitted from real production batch logs (`RX_ML_training.xlsx`). $P_{\text{CO}}$ and $T_{\text{rxn}}$ co-vary ($r = +0.933$).
- **Heteroscedastic Measurement Noise**:
  - Raman $G/D$: $\epsilon \sim \mathcal{N}(0, (0.05 y)^2)$ (5% lab repeatability)
  - UV-Vis Purity: $\epsilon \sim \mathcal{N}(0, (0.04 y)^2)$ (4% spectrophotometer noise)
  - ICP-MS Metals (Fe/Ni/Cr): $\epsilon \sim \mathcal{N}(0, (0.08 y)^2)$ (8% elemental analysis noise)
- **Sensor Calibration Noise**: Thermocouples ($\pm 0.5^\circ$C), Pressure Transmitters ($\pm 0.05$ atm), MFCs ($\pm 0.5\%$ drift).
- **Missingness Pattern**: 15% ICP metals missing, 10% UV purity missing, 5% Raman $G/D$ missing (mirroring real production lab gaps).

---

## 4. Summary Statistics (Large Synthetic Set $N=5000$)
|                                    |             mean |             std |            min |              50% |              max |
|:-----------------------------------|-----------------:|----------------:|---------------:|-----------------:|-----------------:|
| P_CO_atm                           |     59.8249      |    13.587       |    10          |     59.8939      |     90           |
| T_rxn_mean_C                       |    949.281       |    58.1675      |   800          |    949.077       |   1150           |
| T_spread_C                         |     28.1384      |    22.9201      |     0          |     25.7206      |     80           |
| Flow_CO_SLPM                       |    595.298       |   232.243       |   100          |    599.793       |   1000           |
| Flow_Fe_Precursor_SLPM             |    190.953       |    90.3094      |    10          |    191.129       |    350           |
| H2O_Flow_ppmv                      |     29.6669      |     0.77817     |    26.7856     |     29.6697      |     32.4455      |
| Zone_SP_Dev_C                      |     -6.68474     |    11.8174      |   -35          |     -6.49832     |     15           |
| Residence_Time_s                   |     18.9326      |    12.7042      |     5.676      |     15.0935      |    114.476       |
| Reynolds_Number                    | 147203           | 56900.1         | 20578.7        | 149495           | 257943           |
| Fe_Concentration_ppm               |   2321.83        |   479.987       |   320.533      |   2429.38        |   3915.31        |
| CO_Disproportionation_DrivingForce |      0           |     0           |     0          |      0           |      0           |
| Thermal_Loss_kW                    |      2.14634     |     1.13665     |     0.62       |      2.0391      |      4.81986     |
| P_CO2_Partial_bar                  |      0.671931    |     0.216018    |     0.08       |      0.657051    |      1.35        |
| Nucleation_Rate_Est                |      3.39696e+10 |     1.93377e+10 |     3.4193e+08 |      3.14409e+10 |      1.46385e+11 |
| Linear_Gas_Velocity_m_s            |    137.805       |    48.1212      |    18.5372     |    140.595       |    373.866       |
| Catalyst_Growth_Time_Ratio         |      1.0162      |     1.49135     |     0.177896   |      0.59644     |     12.0393      |
| Thermal_Boundary_Thickness_mm      |      0.569108    |     0.29228     |     0.5        |      0.5         |      2.57314     |
| Water_CO_Ratio_ppm                 |     29.6669      |     0.77817     |    26.7856     |     29.6697      |     32.4455      |
| DWM_Yield_g                        |      1.56809     |     0.955692    |     0.05       |      1.50915     |      3.95913     |
| DWM_G/D                            |     15.3079      |     2.38927     |     7.28937    |     15.2561      |     24.6407      |
| DWM_Purity_UV                      |     41.0011      |     7.25168     |    18.729      |     40.9789      |     65           |
| DWM_Ni_ppm_Axial                   |   1256.45        |   277.637       |   508.882      |   1245.99        |   2317.78        |
| DWM_Ni_ppm_Radial                  |   1256.44        |   280.445       |   507.441      |   1246.06        |   2421.8         |
| DWM_Fe_ppm_Axial                   | 303053           | 57109.3         | 50000          | 310679           | 561887           |
| DWM_Fe_ppm_Radial                  | 303016           | 57748.9         | 47590.4        | 310050           | 571397           |
| DWM_Cr_ppm_Axial                   |   1332.39        |   221.378       |   679.443      |   1328.29        |   2317.02        |
| DWM_Cr_ppm_Radial                  |   1332.64        |   224.695       |   695.291      |   1324.25        |   2242.71        |
