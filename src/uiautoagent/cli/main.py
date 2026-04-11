"""设备Agent - AI自主执行手机任务（命令行入口）"""

from __future__ import annotations

import argparse

from uiautoagent.agent import Action, ActionType, AgentConfig, DeviceAgent
from uiautoagent.agent.executor import run_ai_task
from uiautoagent.controller import AndroidController


def demo_manual_control():
    """演示手动控制Agent执行任务（适用于已知步骤的任务）"""
    print("=" * 50)
    print("📱 设备Agent - 手动控制模式")
    print("=" * 50)

    # 检查设备
    devices = AndroidController.list_devices()
    if not devices:
        print("❌ 未检测到Android设备，请确保ADB已连接")
        return

    print(f"✅ 检测到设备: {devices[0]}")

    # 创建Agent
    controller = AndroidController(devices[0])
    agent = DeviceAgent(
        controller,
        config=AgentConfig(
            max_steps=20,
            save_screenshots=True,
        ),
    )

    info = controller.get_device_info()
    print(f"📋 设备信息: {info['model']} ({info['width']}x{info['height']})\n")

    # 示例：打开应用并执行操作（手动步骤）
    steps = [
        Action(
            type=ActionType.TAP,
            thought="打开应用",
            target="微信图标",
        ),
        Action(
            type=ActionType.WAIT,
            thought="等待应用启动",
            wait_ms=2000,
        ),
        Action(
            type=ActionType.TAP,
            thought="点击搜索框",
            target="搜索框",
        ),
        Action(
            type=ActionType.INPUT,
            thought="输入搜索关键词",
            text="test",
        ),
        Action(
            type=ActionType.DONE,
            thought="任务完成",
        ),
    ]

    # 执行步骤
    for action in steps:
        agent.step(action)

    # 保存历史
    agent.save_history()
    agent.print_summary()


def demo_ai_assisted_task(task: str = "修改昵称为kitty"):
    """
    演示AI辅助任务执行 - AI自主决策并完成任务

    Args:
        task: 要执行的任务描述
    """
    run_ai_task(task)


def demo_find_and_click():
    """演示简单的查找并点击"""
    print("=" * 50)
    print("📱 设备Agent - 查找并点击")
    print("=" * 50)

    devices = AndroidController.list_devices()
    if not devices:
        print("❌ 未检测到Android设备")
        return

    controller = AndroidController(devices[0])
    agent = DeviceAgent(controller)

    # 查找并点击元素
    agent.step(
        Action(
            type=ActionType.TAP,
            thought="查找并点击返回按钮",
            target="返回按钮",
        )
    )

    agent.save_history()


def main():
    """Main entry point for the uiautoagent CLI."""
    parser = argparse.ArgumentParser(
        description="设备Agent - AI自主执行手机任务",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-m",
        "--mode",
        choices=["manual", "ai", "find"],
        default="find",
        help="运行模式",
    )
    parser.add_argument(
        "-t",
        "--task",
        default="修改昵称为kitty",
        help="要执行的任务描述（ai模式使用）",
    )
    parser.add_argument(
        "-s",
        "--serial",
        default=None,
        help="指定设备序列号（默认使用第一个可用设备）",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=30,
        help="最大执行步数",
    )
    args = parser.parse_args()

    if args.mode == "manual":
        demo_manual_control()
    elif args.mode == "ai":
        demo_ai_assisted_task(args.task)
    else:
        demo_find_and_click()


if __name__ == "__main__":
    main()
