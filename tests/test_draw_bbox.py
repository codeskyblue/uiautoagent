"""Tests for draw_bbox function."""

from PIL import Image
from uiautoagent.detector import BBox, DetectionResult, draw_bbox


def test_draw_bbox_with_result(tmp_path):
    """Test draw_bbox with a valid detection result."""
    # Create a test image
    test_image_path = tmp_path / "test_input.png"
    output_path = tmp_path / "test_output.png"

    # Create a simple white image
    img = Image.new("RGB", (500, 500), color="white")
    img.save(test_image_path)

    # Create a detection result
    bbox = BBox(x1=100, y1=100, x2=300, y2=200)
    result = DetectionResult(
        found=True, bbox=bbox, description="测试按钮", thought="找到测试按钮"
    )

    # Draw bbox
    result_img = draw_bbox(test_image_path, result, output_path)

    # Verify the image was modified
    assert result_img is not None
    assert result_img.mode == "RGB"
    assert result_img.size == (500, 500)

    # Verify output file was created
    assert output_path.exists()


def test_draw_bbox_without_description(tmp_path):
    """Test draw_bbox without description text."""
    test_image_path = tmp_path / "test_input_no_desc.png"
    output_path = tmp_path / "test_output_no_desc.png"

    # Create a test image
    img = Image.new("RGB", (500, 500), color="white")
    img.save(test_image_path)

    # Create a detection result without description
    bbox = BBox(x1=50, y1=50, x2=150, y2=150)
    result = DetectionResult(
        found=True, bbox=bbox, description=None, thought="找到目标"
    )

    # Draw bbox
    result_img = draw_bbox(test_image_path, result, output_path)

    # Verify the image was created
    assert result_img is not None
    assert output_path.exists()


def test_draw_bbox_not_found(tmp_path):
    """Test draw_bbox when element is not found."""
    test_image_path = tmp_path / "test_input_not_found.png"

    # Create a test image
    img = Image.new("RGB", (500, 500), color="white")
    img.save(test_image_path)

    # Create a detection result with no bbox
    result = DetectionResult(
        found=False, bbox=None, description=None, thought="未找到元素"
    )

    # Draw bbox (should not draw anything)
    result_img = draw_bbox(test_image_path, result)

    # Verify the image was returned unchanged
    assert result_img is not None
    assert result_img.mode == "RGB"
    assert result_img.size == (500, 500)


def test_draw_bbox_no_output_file(tmp_path):
    """Test draw_bbox without saving to file."""
    test_image_path = tmp_path / "test_input_no_save.png"

    # Create a test image
    img = Image.new("RGB", (500, 500), color="white")
    img.save(test_image_path)

    # Create a detection result
    bbox = BBox(x1=100, y1=100, x2=300, y2=200)
    result = DetectionResult(
        found=True, bbox=bbox, description="按钮", thought="找到按钮"
    )

    # Draw bbox without output path
    result_img = draw_bbox(test_image_path, result, output=None)

    # Verify the image was returned but not saved
    assert result_img is not None
    assert not (tmp_path / "test_output_no_save.png").exists()
