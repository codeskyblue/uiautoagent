"""AI-based UI element detection module."""

from uiautoagent.detector.bbox_detector import (
    BBox,
    DetectionResult,
    detect_element,
    detect_elements,
    draw_bbox,
)
from uiautoagent.detector.content_extractor import ExtractionResult, extract_content

__all__ = [
    "BBox",
    "DetectionResult",
    "detect_element",
    "detect_elements",
    "draw_bbox",
    "ExtractionResult",
    "extract_content",
]
