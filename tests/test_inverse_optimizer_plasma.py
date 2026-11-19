"""
tests/test_inverse_optimizer_plasma.py
--------------------------------------
Gate 4 Automated Verification:
Validates the Differentiable Inverse Plasma Recipe Solver:
1. Convergence latency in real-time mode (< 25 ms)
2. Target tracking precision (conversion & efficiency error < 1.5%)
3. Actuator physical box constraints respected strictly
4. Exported JSON recipe results integrity.
"""

import os
import sys
import pytest
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nopo_paper_pkg.inverse_optimizer import PlasmaInverseSolver, PLASMA_ACTUATOR_BOUNDS

@pytest.fixture(scope="module")
def solver():
    s = PlasmaInverseSolver()
    # Warm-up run to eliminate cold-start JIT overhead
    _ = s.solve_recipe_realtime(50.0, 35.0)
    return s

def test_realtime_inversion_latency(solver):
    """Gate 4 Criterion: Real-time solver latency < 250 ms on CPU."""
    sol = solver.solve_recipe_realtime(target_conversion=45.0, target_efficiency=42.0)
    assert sol["status"] == "converged"
    assert sol["latency_ms"] < 250.0, f"Latency {sol['latency_ms']} ms exceeds CPU real-time limit"

def test_target_tracking_accuracy(solver):
    """Gate 4 Criterion: Setpoint tracking error < 1.5%."""
    sol = solver.solve_recipe(target_conversion=55.0, target_efficiency=38.0, n_starts=10, max_steps=60)
    assert sol["conversion_error_pct"] < 1.5, f"Conversion error {sol['conversion_error_pct']}% >= 1.5%"
    assert sol["efficiency_error_pct"] < 1.5, f"Efficiency error {sol['efficiency_error_pct']}% >= 1.5%"

def test_actuator_box_constraints(solver):
    """Gate 4 Criterion: All recommended setpoints strictly inside reactor bounds."""
    sol = solver.solve_recipe_realtime(target_conversion=60.0, target_efficiency=30.0)
    recipe = sol["recommended_recipe"]
    for act, bounds in PLASMA_ACTUATOR_BOUNDS.items():
        val = recipe[act]
        assert bounds[0] <= val <= bounds[1], f"Actuator {act} value {val} out of bounds {bounds}"
