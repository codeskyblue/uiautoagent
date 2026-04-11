"""AI-based UI element detection module."""

from uiautoagent.detector.bbox_detector import (
    BBox,
    DetectionResult,
    detect_element,
    draw_bbox,
)

__all__ = ["BBox", "DetectionResult", "detect_element", "draw_bbox"]
