from typing import Union
import numpy as np

def apply_homography(H: np.ndarray, x: float, y: float) -> tuple[float, float]:
    """Apply projective transformation given by homography H
    to the video point (x1, y1).
    
    Args:
        H: The homography to apply. Depends on the camera.
        x: The x coordinate of the video point.
        y: The y coordinate of the video point.

    Returns:
        The resulting map point (x2, y2).
    """
    homogeneous_coords = np.array([x, y, 1])
    x_prime, y_prime, w_prime = H @ homogeneous_coords
    x2, y2 = x_prime / w_prime, y_prime / w_prime
    return x2, y2

def estimate_homography(points1: Union[list, np.ndarray],
                        points2: Union[list, np.ndarray]) -> np.ndarray:
    """
    Compute the homography that defines the projective transformation
    between the video and map surfaces.

    Args:
        points1: List of points in the camera video.
        points2: List of corresponding points on the map.

    Returns:
        The homography that allows transforming between video and map points.
    """
    points1 = np.array(points1)
    points2 = np.array(points2)

    n = points1.shape[0]
    if n < 4:
        raise ValueError('At least 4 points are required.')
    if points1.shape != points2.shape:
        raise ValueError('Both point lists must be of equal length')
    
    # This block solves a linear system of equations
    # to get the components of H
    A = np.zeros([2 * n, 9])
    for i, ((x1, y1), (x2, y2)) in enumerate(zip(points1, points2)):
        A[2 * i + 0] = [x1, y1, 1, 0, 0, 0, -x1 * x2, -y1 * x2, -x2]
        A[2 * i + 1] = [0, 0, 0, x1, y1, 1, -x1 * y2, -y1 * y2, -y2]
    U, E, V = np.linalg.svd(A)
    H = V[-1].reshape(3, 3)

    # All scaled H represent the same projection, so we divide by
    # H[2, 2] to get a deterministic result. This ensures the last
    # element of H is always 1.
    H = H / H[2, 2]

    return H