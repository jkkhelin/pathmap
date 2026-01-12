import numpy as np

from app.homography import apply_homography

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