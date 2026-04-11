"""AI 客户端管理 - 统一 OpenAI 客户端初始化"""

from __future__ import annotations

import os
from functools import lru_cache

from openai import OpenAI


@lru_cache(maxsize=1)
def get_ai_client() -> OpenAI:
    """
    获取 AI 客户端实例（单例模式）

    Returns:
        OpenAI 客户端实例

    Example:
        >>> from uiautoagent.ai import get_ai_client, get_ai_model
        >>> client = get_ai_client()
        >>> model = get_ai_model()
    """
    return OpenAI(
        base_url=os.getenv("BASE_URL", "https://api.openai.com/v1"),
        api_key=os.getenv("API_KEY"),
    )


def get_ai_model() -> str:
    """
    获取 AI 模型名称

    Returns:
        模型名称，如 "gpt-4o"
    """
    return os.getenv("MODEL_NAME", "gpt-4o")


def get_ai_config() -> dict:
    """
    获取 AI 配置信息

    Returns:
        包含 base_url, model, timeout 等配置的字典
    """
    return {
        "base_url": os.getenv("BASE_URL", "https://api.openai.com/v1"),
        "model": os.getenv("MODEL_NAME", "gpt-4o"),
        "timeout": int(os.getenv("REQUEST_TIMEOUT", "30")),
    }
