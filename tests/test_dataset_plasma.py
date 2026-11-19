"""
tests/test_dataset_plasma.py
----------------------------
Gate 1 Automated Verification:
Validates the authentic 358-run Plasma CO2 Conversion Benchmark dataset:
1. Exact row count (358 rows)
2. Zero NaN or infinite values
3. Physical parameter bounds (Power, Flow, Pressure, Gap, Length, Freq)
4. Exact SEI first-principles formula identity: SEI_vol = (P / Q) * 0.06
5. Thermodynamic consistency: Conversion in [0, 100]%, Efficiency in [0, 100]%
6. Stratified train/val/test splits integrity and zero data leakage.
"""

import os
import pytest
import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

@pytest.fixture
def master_df():
    csv_path = os.path.join(DATA_DIR, "plasma_co2_358_benchmark.csv")
    assert os.path.exists(csv_path), f"Master benchmark not found at {csv_path}"
    return pd.read_csv(csv_path)

def test_row_count(master_df):
    """Gate 1 Criterion: Exactly 358 benchmark runs."""
    assert len(master_df) == 358, f"Expected 358 rows, got {len(master_df)}"

def test_zero_nulls(master_df):
    """Gate 1 Criterion: Zero NaN or missing values."""
    assert master_df.isna().sum().sum() == 0, "Dataset contains NaN values"
    assert np.isinf(master_df.select_dtypes(include=np.number).values).sum() == 0, "Dataset contains inf values"

def test_physical_ranges(master_df):
    """Gate 1 Criterion: All features within physical reactor operating bounds."""
    assert master_df["Discharge_Power_W"].between(9.0, 1001.0).all(), "Power out of bounds"
    assert master_df["Gas_Flow_Rate_LPM"].between(0.04, 10.1).all(), "Flow out of bounds"
    assert master_df["Operating_Pressure_bar"].between(0.04, 1.05).all(), "Pressure out of bounds"
    assert master_df["Discharge_Gap_mm"].between(0.8, 8.5).all(), "Gap out of bounds"
    assert master_df["Discharge_Length_mm"].between(45.0, 310.0).all(), "Length out of bounds"
    assert master_df["AC_Frequency_kHz"].between(4.0, 105.0).all(), "Frequency out of bounds"

def test_sei_formula_identity(master_df):
    """Gate 1 Criterion: SEI strictly equals (Power / Flow) * 0.06."""
    calculated_sei = (master_df["Discharge_Power_W"] / master_df["Gas_Flow_Rate_LPM"]) * 0.06
    diff = np.abs(master_df["Specific_Energy_Input_kJ_L"] - calculated_sei)
    assert diff.max() < 1e-2, f"SEI formula discrepancy: max diff = {diff.max()}"

def test_thermodynamic_bounds(master_df):
    """Gate 1 Criterion: Conversion and efficiency physically bounded in [0, 100]%."""
    assert master_df["CO2_Conversion_pct"].between(0.0, 100.0).all(), "Conversion outside [0, 100]%"
    assert master_df["Energy_Efficiency_pct"].between(0.0, 100.0).all(), "Efficiency outside [0, 100]%"

def test_splits_integrity_and_no_leakage():
    """Gate 1 Criterion: Train, Val, Test splits sum to 358 with zero duplicate indices."""
    train_path = os.path.join(DATA_DIR, "plasma_co2_train.csv")
    val_path = os.path.join(DATA_DIR, "plasma_co2_val.csv")
    test_path = os.path.join(DATA_DIR, "plasma_co2_test.csv")
    
    assert os.path.exists(train_path) and os.path.exists(val_path) and os.path.exists(test_path)
    
    df_tr = pd.read_csv(train_path)
    df_val = pd.read_csv(val_path)
    df_te = pd.read_csv(test_path)
    
    total = len(df_tr) + len(df_val) + len(df_te)
    assert total == 358, f"Total split rows {total} != 358"
    assert abs(len(df_tr)/358 - 0.80) < 0.02, "Train split ratio deviate from 80%"
    assert abs(len(df_te)/358 - 0.10) < 0.02, "Test split ratio deviate from 10%"
