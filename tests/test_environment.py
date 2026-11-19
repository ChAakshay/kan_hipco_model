"""
tests / test_environment.py
---------------------------
Verification test for Gate 0: Pin and verify environment reproducibility.
Checks installed package versions against requirements-lock.txt.
"""

import os
import sys
import pytest

def get_installed_versions():
    import numpy
    import torch
    import xgboost
    import sklearn
    import sympy
    import pytest as pt
    import pandas
    import scipy
    import matplotlib

    return {
        'numpy': numpy.__version__,
        'torch': torch.__version__,
        'xgboost': xgboost.__version__,
        'scikit-learn': sklearn.__version__,
        'sympy': sympy.__version__,
        'pytest': pt.__version__,
        'pandas': pandas.__version__,
        'scipy': scipy.__version__,
        'matplotlib': matplotlib.__version__,
    }

def test_python_version():
    """Ensure Python version is 3.10+ for reproducibility."""
    assert sys.version_info >= (3, 10), f"Python version {sys.version_info} is below minimum 3.10"

def test_pinned_package_versions():
    """Check each package against pinned requirements-lock.txt."""
    lockfile_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "requirements-lock.txt")
    assert os.path.exists(lockfile_path), f"Missing lockfile: {lockfile_path}"

    pinned = {}
    with open(lockfile_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "==" in line:
                pkg, ver = line.split("==", 1)
                pinned[pkg.strip()] = ver.strip()

    installed = get_installed_versions()

    for pkg, expected_ver in pinned.items():
        assert pkg in installed, f"Package {pkg} not found in installed versions"
        actual_ver = installed[pkg]
        assert actual_ver == expected_ver, (
            f"Version mismatch for {pkg}: expected {expected_ver}, found {actual_ver}"
        )

def test_torch_cpu_or_cuda():
    """Ensure PyTorch is functional and tensor operations work."""
    import torch
    x = torch.randn(5, 5)
    y = x @ x.T
    assert y.shape == (5, 5)
    assert not torch.isnan(y).any()

def test_scikit_learn_metrics():
    """Ensure scikit-learn r2_score works properly."""
    from sklearn.metrics import r2_score
    import numpy as np
    y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y_pred = np.array([1.05, 1.98, 3.02, 3.97, 5.01])
    r2 = r2_score(y_true, y_pred)
    assert r2 > 0.99, f"r2_score test failed: {r2}"
