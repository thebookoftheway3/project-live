# Top-down quantifier

`quantifier.py` accepts injected synthetic arrays, not a camera stream. Homography
maps a plane; it cannot infer food height. Rectify segmentation and calibrated
height grids before integrating area × height in cm³. Relative monocular depth
alone is rejected as a metric input. Nonplanar perspective/occlusion errors remain.

Integration seams are [SAM 2](https://github.com/facebookresearch/sam2) for masks and
[Depth Anything V2](https://github.com/DepthAnything/Depth-Anything-V2) for depth.
No models are included. Pin a model revision, weight digest, preprocessing,
licence and metric calibration before connecting either. Depth Anything V2 model
licences differ by size; do not assume every checkpoint permits OEM use.
Candidate bite cadence is not proof of chewing, swallowing or consumed quantity.
