# SPDX-License-Identifier: AGPL-3.0-only
"""Local geometry experiment using injected masks and calibrated metric heights."""

from math import isfinite


def finite(value):
    return type(value) in (int, float) and isfinite(value)


def calibrate_homography(image_points, plane_points_cm):
    """Four non-collinear planar correspondences; solve H with h33=1.

    Lens distortion must be corrected upstream. No relative monocular depth is
    silently interpreted as centimetres. Singular/ill-conditioned fits are rejected.
    """
    if len(image_points) != 4 or len(plane_points_cm) != 4:
        raise ValueError("four calibration pairs required")
    if any(len(p) != 2 or not all(finite(v) for v in p) for p in (*image_points, *plane_points_cm)):
        raise ValueError("finite 2D calibration points required")
    rows = []
    for (x, y), (u, v) in zip(image_points, plane_points_cm):
        rows.extend(([x, y, 1, 0, 0, 0, -u * x, -u * y, u], [0, 0, 0, x, y, 1, -v * x, -v * y, v]))
    for col in range(8):
        pivot = max(range(col, 8), key=lambda r: abs(rows[r][col]))
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        if abs(scale) < 1e-10:
            raise ValueError("degenerate calibration")
        rows[col] = [v / scale for v in rows[col]]
        for r in range(8):
            if r != col:
                factor = rows[r][col]
                rows[r] = [v - factor * w for v, w in zip(rows[r], rows[col])]
    result = tuple(row[-1] for row in rows) + (1.0,)
    if not all(finite(v) for v in result):
        raise ValueError("calibration overflow")
    return result


def project(h, x, y):
    if len(h) != 9 or not all(finite(v) for v in (*h, x, y)):
        raise ValueError("finite homography and coordinates required")
    divisor = h[6] * x + h[7] * y + h[8]
    if abs(divisor) < 1e-10:
        raise ValueError("point at projective horizon")
    point = ((h[0] * x + h[1] * y + h[2]) / divisor, (h[3] * x + h[4] * y + h[5]) / divisor)
    if not all(finite(v) for v in point):
        raise ValueError("projection overflow")
    return point


def volume_cm3(mask, heights_cm, *, cell_area_cm2, metric_calibrated=False):
    """Integrate an already rectified height grid. No image/model access here."""
    if metric_calibrated is not True:
        raise ValueError("metric height calibration required; relative depth is insufficient")
    if not finite(cell_area_cm2) or cell_area_cm2 <= 0 or not mask or not mask[0]:
        raise ValueError("positive area and nonempty rectified grid required")
    width = len(mask[0])
    if len(mask) != len(heights_cm) or any(len(row) != width for row in (*mask, *heights_cm)):
        raise ValueError("matching rectangular grids required")
    if any(type(v) is not bool for row in mask for v in row):
        raise ValueError("binary mask required")
    if any(not finite(v) or v < 0 for row in heights_cm for v in row):
        raise ValueError("finite nonnegative metric heights required")
    result = sum(h for row, heights in zip(mask, heights_cm) for hit, h in zip(row, heights) if hit)
    result *= cell_area_cm2
    if not finite(result):
        raise ValueError("volume overflow")
    return result


def bite_cadence_per_minute(candidate_times):
    """Candidate cadence only; chewing/mouth motion is not confirmed intake."""
    if any(not finite(t) or t < 0 for t in candidate_times):
        raise ValueError("finite nonnegative timestamps required")
    if any(b <= a for a, b in zip(candidate_times, candidate_times[1:])):
        raise ValueError("strictly increasing candidate times required")
    if len(candidate_times) < 2:
        return None
    return 60 * (len(candidate_times) - 1) / (candidate_times[-1] - candidate_times[0])
