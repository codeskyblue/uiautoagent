"""Tests for content_extractor module."""

import json
from importlib import import_module
from unittest.mock import MagicMock, patch

import pytest

content_extractor = import_module("uiautoagent.detector.content_extractor")
extract_content = content_extractor.extract_content
ExtractionResult = content_extractor.ExtractionResult


def _make_chat_response(content: str) -> MagicMock:
    """构造 mock 的 chat_completion 返回值"""
    msg = MagicMock()
    msg.content = content
    choice = MagicMock()
    choice.message = msg
    resp = MagicMock()
    resp.choices = [choice]
    return resp


# --- extract_content 测试 ---


@patch("uiautoagent.detector.content_extractor.chat_completion")
def test_extract_content_free_mode(mock_chat, tmp_path):
    """自由模式：不传 example，AI 自主决定 JSON 结构"""
    img = tmp_path / "test.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

    mock_chat.return_value = _make_chat_response(
        json.dumps(
            {
                "thought": "图片中有两个商品",
                "content": [
                    {"name": "苹果", "price": 5.5},
                    {"name": "香蕉", "price": 3.2},
                ],
            }
        )
    )

    result = extract_content(img, "提取所有商品名称和价格")
    assert result.success is True
    assert result.content == [
        {"name": "苹果", "price": 5.5},
        {"name": "香蕉", "price": 3.2},
    ]
    assert result.thought == "图片中有两个商品"


@patch("uiautoagent.detector.content_extractor.chat_completion")
def test_extract_content_with_example(mock_chat, tmp_path):
    """示例模式：传入 example，AI 按示例格式输出"""
    img = tmp_path / "test.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

    mock_chat.return_value = _make_chat_response(
        json.dumps(
            {
                "thought": "提取到商品信息",
                "content": {"name": "华为手机", "price": 4999.0},
            }
        )
    )

    example = {"name": "示例商品", "price": 0}
    result = extract_content(img, "提取商品信息", example=example)
    assert result.success is True
    assert result.content == {"name": "华为手机", "price": 4999.0}


@patch("uiautoagent.detector.content_extractor.chat_completion")
def test_extract_content_with_list_example(mock_chat, tmp_path):
    """示例模式：传入 list 类型 example"""
    img = tmp_path / "test.jpg"
    img.write_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 100)

    mock_chat.return_value = _make_chat_response(
        json.dumps(
            {
                "thought": "提取到列表",
                "content": [{"id": 1, "text": "标题一"}, {"id": 2, "text": "标题二"}],
            }
        )
    )

    example = [{"id": 0, "text": "示例文本"}]
    result = extract_content(img, "提取列表数据", example=example)
    assert result.success is True
    assert len(result.content) == 2


def test_extract_content_file_not_found():
    """图片不存在时抛出 FileNotFoundError"""
    with pytest.raises(FileNotFoundError):
        extract_content("/nonexistent/image.png", "测试查询")


@patch("uiautoagent.detector.content_extractor.safe_validate_json")
@patch("uiautoagent.detector.content_extractor.chat_completion")
def test_extract_content_invalid_json_response(mock_chat, mock_validate, tmp_path):
    """AI 返回无法解析的内容时，返回失败结果"""
    img = tmp_path / "test.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

    mock_chat.return_value = _make_chat_response("这不是有效的JSON")
    mock_validate.side_effect = ValueError("无法解析")

    result = extract_content(img, "提取内容")
    assert result.success is False
    assert result.content is None


@patch("uiautoagent.detector.content_extractor.chat_completion")
def test_extract_content_uses_vision_category(mock_chat, tmp_path):
    """验证使用 VISION category 调用"""
    img = tmp_path / "test.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

    mock_chat.return_value = _make_chat_response(
        json.dumps({"thought": "ok", "content": {"key": "value"}})
    )

    extract_content(img, "测试")
    call_kwargs = mock_chat.call_args
    assert call_kwargs.kwargs["category"] == "vision"
    assert call_kwargs.kwargs["response_format"] == {"type": "json_object"}
    assert call_kwargs.kwargs["temperature"] == 0.0


@patch("uiautoagent.detector.content_extractor.chat_completion")
def test_extract_content_with_string_example(mock_chat, tmp_path):
    """示例模式：传入非 JSON 字符串，AI 参考格式描述输出"""
    img = tmp_path / "test.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

    mock_chat.return_value = _make_chat_response(
        json.dumps(
            {
                "thought": "按格式提取",
                "content": [
                    {"商品": "苹果", "价格": "5.5元"},
                    {"商品": "香蕉", "价格": "3.2元"},
                ],
            }
        )
    )

    result = extract_content(img, "提取商品信息", example="商品, 价格")
    assert result.success is True
    assert result.content[0]["商品"] == "苹果"
