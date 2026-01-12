import numpy as np
import pytest

from app.homography import apply_homography, estimate_homography

# tests for apply_homography()

def test_identity_homography_returns_same_point():
    """Test if a homography with diagonal ones produces the input point."""
    H = np.eye(3, dtype=np.float64)
    x1, y1 = 1.25, -0.75
    x2, y2 = apply_homography(H, x1, y1)
    assert np.isclose(x1, x2) and np.isclose(y1, y2)

def test_projective_mapping():
    """Test if apply_homography produces the correct result for a
    projective transformation.
    """
    H = np.array([
        [1.0, 0.5, 0.2],
        [0.0, 1.0, -3.0],
        [0.1, -0.2, 1.0]
    ])
    x1, y1 = 0.8, -0.4
    x2, y2 = apply_homography(H, x1, y1)

    x2_prime = 1.0*x1 + 0.5*y1 + 0.2
    y2_prime = 0.0*x1 + 1.0*y1 + -3.0
    w2_prime = 0.1*x1 + -0.2*y1 + 1.0
    x2_correct = x2_prime / w2_prime
    y2_correct = y2_prime / w2_prime

    assert np.isclose(x2, x2_correct) and np.isclose(y2, y2_correct)

# tests for estimate_homography()

def test_produced_homography_reproduces_points():
    """Test if estimate_homography gives the correct
    results for the same points it was built from."""
    points1 = [
        [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]
    ]
    points2 = [
        [0.0, 0.0], [1.2, 0.1], [1.1, 1.3], [-0.1, 0.9]
    ]

    H = estimate_homography(points1, points2)
    for ((x1, y1), (x2, y2)) in zip(points1, points2):
        x2_produced, y2_produced = apply_homography(H, x1, y1)
        assert np.isclose(x2, x2_produced) and np.isclose(y2, y2_produced)

def test_too_few_points_raises_valueerror():
    """Minimum of 4 points are needed to compute a homography.
    Test that fewer points raise ValueError."""
    points1 = [
        [0.0, 0.0], [1.0, 0.0], [1.0, 1.0]
    ]
    points2 = [
        [0.0, 0.0], [1.2, 0.1], [1.1, 1.3]
    ]
    with pytest.raises(ValueError):
        estimate_homography(points1, points2)

def test_wrong_lengths_raises_valueerror():
    """Both point lists must be of equal length.
    Test that wrong lenghts raise ValueError."""
    points1 = [
        [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.5, 1.5]
    ]
    points2 = [
        [0.0, 0.0], [1.2, 0.1], [1.1, 1.3], [-0.1, 0.9]
    ]
    with pytest.raises(ValueError):
        estimate_homography(points1, points2)