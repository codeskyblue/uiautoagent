"""AI agent module for autonomous device automation."""

from uiautoagent.agent.ai_utils import clarify_task, compress_markdown, summarize_task
from uiautoagent.agent.device_agent import (
    Action,
    ActionType,
    AgentConfig,
    DeviceAgent,
    TaskStep,
)
from uiautoagent.agent.executor import TaskResult, execute_ai_task, run_ai_task
from uiautoagent.agent.memory import TaskMemory, get_task_memory

__all__ = [
    # Core agent
    "DeviceAgent",
    "Action",
    "ActionType",
    "AgentConfig",
    "TaskStep",
    # Memory
    "TaskMemory",
    "get_task_memory",
    # AI utils
    "summarize_task",
    "clarify_task",
    "compress_markdown",
    # Executor
    "TaskResult",
    "execute_ai_task",
    "run_ai_task",
]
