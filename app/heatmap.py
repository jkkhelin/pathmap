"""This module provides the overlay_heatmap function for drawing a visual
heatmap effect on a given image based on a list of points on the image.
It is used to visualize camera-detected activity on a geographical area.
Microsoft Copilot was used to help implement this feature."""

import numpy as np
from PIL import Image
from matplotlib import cm

def _gaussian_kernel1d(sigma: float, truncate: float = 3.0) -> np.ndarray:
    """Create a 1D Gaussian kernel. Returns [1] if sigma <= 0."""
    if sigma <= 0:
        return np.array([1.0], dtype=np.float32)
    radius = int(truncate * sigma + 0.5)
    x = np.arange(-radius, radius + 1, dtype=np.float32)
    k = np.exp(-(x**2) / (2 * sigma * sigma)).astype(np.float32)
    k /= k.sum()
    return k

def _convolve_separable_reflect(img: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Separable 2D convolution with reflect padding (NumPy-only)."""
    if kernel.size == 1:
        return img.copy()

    pad = kernel.size // 2

    # Convolve along x (axis=1)
    tmp = np.pad(img, ((0, 0), (pad, pad)), mode="reflect")
    # apply_along_axis will convolve each row
    tmp = np.apply_along_axis(lambda m: np.convolve(m, kernel, mode="valid"), axis=1, arr=tmp)

    # Convolve along y (axis=0)
    tmp2 = np.pad(tmp, ((pad, pad), (0, 0)), mode="reflect")
    out = np.apply_along_axis(lambda m: np.convolve(m, kernel, mode="valid"), axis=0, arr=tmp2)

    return out

def _accumulate_points(height: int, width: int, points: np.ndarray) -> np.ndarray:
    """Accumulate point counts into a (H, W) grid. Points are (x, y) in pixels."""
    heat = np.zeros((height, width), dtype=np.float32)
    if points.size == 0:
        return heat

    xs = np.rint(points[:, 0]).astype(np.int64)  # round to nearest pixel
    ys = np.rint(points[:, 1]).astype(np.int64)

    mask = (xs >= 0) & (xs < width) & (ys >= 0) & (ys < height)
    xs = xs[mask]
    ys = ys[mask]

    np.add.at(heat, (ys, xs), 1.0)
    return heat

def overlay_heatmap(
    image_path: str,
    points,
    out_path: str = "heatmap_overlay.png",
    sigma_px: float = 20.0,
    alpha_max: float = 0.65,
    cmap_name: str = "inferno",
    gamma: float = 0.8,
    min_norm_threshold: float = 0.0,
):
    """
    Overlay a density heatmap over an image.

    Parameters
    ----------
    image_path : str
        Path to base image (any Pillow-readable format). Origin: top-left.
    points : list[tuple[float,float]] or np.ndarray of shape (N, 2)
        (x, y) coordinates in pixel space.
    out_path : str
        Path to save the overlay image (PNG recommended).
    sigma_px : float
        Gaussian blur sigma in pixels. Higher = smoother.
    alpha_max : float
        Maximum heatmap opacity for the hottest regions (0..1).
    cmap_name : str
        Matplotlib colormap name (e.g., "inferno", "magma", "turbo", "viridis", "jet").
    gamma : float
        Nonlinear mapping on normalized density (x -> x**gamma).
        <1 boosts mid-densities; >1 emphasizes peaks.
    min_norm_threshold : float
        Suppresses very low normalized densities (set alpha=0 below this).
    """
    # Load base image
    base_img = Image.open(image_path).convert("RGBA")
    base = np.asarray(base_img, dtype=np.float32) / 255.0  # H, W, 4
    H, W = base.shape[:2]

    # Normalize/prepare points array
    pts = np.asarray(points, dtype=np.float32).reshape(-1, 2)

    # Accumulate counts
    heat = _accumulate_points(H, W, pts)

    # Smooth with Gaussian
    kernel = _gaussian_kernel1d(sigma_px, truncate=3.0)
    heat_smooth = _convolve_separable_reflect(heat, kernel)

    # Normalize to [0, 1]
    max_val = float(heat_smooth.max())
    if max_val > 0:
        heat_norm = (heat_smooth / max_val)
    else:
        heat_norm = heat_smooth  # all zeros

    # Optional gamma correction for contrast
    if gamma is not None and gamma > 0:
        heat_norm = np.power(heat_norm, gamma).astype(np.float32)

    # Map to colormap (returns RGBA in 0..1)
    cmap = cm.get_cmap(cmap_name)
    heat_rgba = cmap(heat_norm)  # H, W, 4
    heat_rgb = heat_rgba[..., :3]

    # Alpha map proportional to density
    alpha = alpha_max * heat_norm
    if min_norm_threshold > 0:
        alpha = np.where(heat_norm >= min_norm_threshold, alpha, 0.0)

    # Composite: out = base*(1-a) + heat*a (RGB); keep base alpha channel
    a3 = alpha[..., None]  # H, W, 1
    out_rgb = base[..., :3] * (1.0 - a3) + heat_rgb * a3
    out = np.dstack([out_rgb, base[..., 3:]])  # preserve original alpha

    # Save
    out_img = Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), mode="RGBA")
    out_img.save(out_path)
    return out_path
