import numpy as np

from rex import explainability_auc, fidelity, fidelity_curve, random_rotation
from test_models import make_world


def test_fidelity():
    assert fidelity([0, 1, 2, 0], [0, 1, 1, 0]) == 0.75


def test_random_rotation_properties():
    R0 = random_rotation(5, 0.0, seed=0)
    assert np.allclose(R0, np.eye(5))
    R = random_rotation(5, 1.5, seed=0)
    # A rotation: orthogonal, information-preserving.
    assert np.allclose(R @ R.T, np.eye(5), atol=1e-8)


def test_aligned_receiver_dominates_misaligned():
    """Mini version of Exp 1: same labels, same information (rotation is a
    bijection) — only the receiver basis changes, and the explainability
    curve of the aligned receiver dominates."""
    X, y = make_world(n=3000)
    Xtr, Xte, ytr, yte = X[:2500], X[2500:], y[:2500], y[2500:]
    budgets = [4, 8, 16, 32]

    aligned = fidelity_curve(Xtr, ytr, Xte, yte, budgets, basis=None)
    R = random_rotation(5, 1.5, seed=100)
    rotated = fidelity_curve(Xtr, ytr, Xte, yte, budgets, basis=R)

    assert explainability_auc(aligned) > explainability_auc(rotated)
    # Fidelity grows with budget for the aligned receiver.
    assert aligned[-1] >= aligned[0]
