import numpy as np

def apply_homography(H: np.ndarray, x: float, y: float) -> tuple[float, float]:
    """Apply projective transformation given by homography H
    to the point (x1, y1).
    
    Args:
        H: The homography to apply.
        x: The x coordinate of the point.
        y: The y coordinate of the point.

    Returns:
        The resulting point (x2, y2).
    """
    homogeneous_coords = np.array([x, y, 1])
    x_prime, y_prime, w_prime = H @ homogeneous_coords
    x2, y2 = x_prime / w_prime, y_prime / w_prime
    return x2, y2

def estimate_homography(points1, points2):
    return np.zeros(3)