"""uiautoagent - AI-powered UI automation framework"""

import dotenv

# 加载 .env 文件环境变量
dotenv.load_dotenv()

from uiautoagent.ai import get_ai_client, get_ai_config, get_ai_model
from uiautoagent.agent import (
    DeviceAgent,
    Action,
    ActionType,
    AgentConfig,
    TaskStep,
)
from uiautoagent.agent.executor import execute_ai_task, run_ai_task
from uiautoagent.agent.memory import TaskMemory, get_task_memory
from uiautoagent.agent.ai_utils import clarify_task, compress_markdown, summarize_task
from uiautoagent.controller import (
    AndroidController,
    DeviceController,
    IOSController,
    SwipeDirection,
)
from uiautoagent.detector import BBox, DetectionResult, draw_bbox, detect_element

__all__ = [
    # AI client
    "get_ai_client",
    "get_ai_model",
    "get_ai_config",
    # Agent
    "DeviceAgent",
    "Action",
    "ActionType",
    "AgentConfig",
    "TaskStep",
    "run_ai_task",
    "execute_ai_task",
    # Memory
    "TaskMemory",
    "get_task_memory",
    "summarize_task",
    "clarify_task",
    "compress_markdown",
    # Controller
    "DeviceController",
    "AndroidController",
    "IOSController",
    "SwipeDirection",
    # Detector
    "BBox",
    "DetectionResult",
    "detect_element",
    "draw_bbox",
]

__version__ = "0.1.0"
