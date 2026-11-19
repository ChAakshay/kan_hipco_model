# Data Card: Curated 358-Run Plasma CO2 Conversion Benchmark

## 1. Dataset Overview
- **Name**: PLASMANT-DIFFER Plasma $\text{CO}_2$ Conversion Benchmark Database
- **Primary Source**: University of Antwerp (PLASMANT Research Group, Prof. Annemie Bogaerts, Jiayin Li et al., *Green Chemistry* 2026, 28, 9804–9821)
- **Secondary Source**: TU Eindhoven & DIFFER Microwave Vacuum Dissociation Datasets (4TU.ResearchData)
- **Total Experimental Runs**: 358 steady-state literature runs across 31 experimental setups + 19-point dynamic transfer test
- **Splits**: 80% Train (288 runs), 10% Validation (35 runs), 10% Test (35 runs)

## 2. Input Features ($D_{\text{in}} = 8$)
1. **`Discharge_Power_W`**: $P \in [14.2, 987.1]\text{ W}$
2. **`Gas_Flow_Rate_LPM`**: $Q \in [0.053, 9.98]\text{ LPM}$
3. **`Operating_Pressure_bar`**: $P_{\text{reactor}} \in [0.05, 1.00]\text{ bar}$ ($50\text{--}1000\text{ mbar}$)
4. **`Discharge_Gap_mm`**: $d_{\text{gap}} \in [1.0, 6.0]\text{ mm}$
5. **`Discharge_Length_mm`**: $L \in [78.7, 251.0]\text{ mm}$
6. **`AC_Frequency_kHz`**: $f \in [14.8, 80.2]\text{ kHz}$
7. **`Specific_Energy_Input_kJ_L`**: $\text{SEI}_{\text{vol}} = \frac{P}{Q} \times 0.06 \in [0.75, 171.4]\text{ kJ/L}$
8. **`Residence_Time_s`**: $\tau_{\text{res}} \in [0.033, 27.87]\text{ s}$

## 3. Target Outputs ($D_{\text{out}} = 3$)
1. **`CO2_Conversion_pct`**: $\chi_{\text{CO}_2} \in [1.2\%, 86.5\%]$ (Mean: 39.0%)
2. **`Energy_Efficiency_pct`**: $\eta_{\text{EE}} \in [0.8\%, 56.4\%]$ (Mean: 45.3%)
3. **`Specific_Energy_Consumption_kJ_mol`**: $\text{SEC} \in [501.8, 28300.0]\text{ kJ/mol}$

## 4. Physics Invariants Enforced
- **Energy Conservation**: $\frac{\partial\chi}{\partial\text{SEI}} \ge 0$
- **Thermodynamic Limit**: $\eta_{\text{EE}} \le 100\%$ and $\eta \le \chi \times \frac{2.93\text{ eV}}{\text{SEI}_{\text{mol}}}$
- **Thermal Overheating Roll-Off**: $\frac{\partial\eta}{\partial\text{SEI}} \le 0$ at elevated $\text{SEI}$
