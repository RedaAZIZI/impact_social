"""X-57 : test trivial validant que le package s'importe et que la CI tourne."""

import solveur


def test_package_importable() -> None:
    assert solveur.__version__
