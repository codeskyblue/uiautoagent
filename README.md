# UIAutoAgent

AI 驱动的 UI 自动化框架，支持视觉定位和自主任务执行。

## 特性

- 🎯 AI 视觉定位元素，无需 DOM
- 🤖 自主决策执行任务
- 🧠 任务记忆学习
- 📱 Android 设备支持

## 安装

```bash
uv sync
cp .env.example .env
# 编辑 .env 配置 API_KEY
```

## 快速开始

```bash
# AI 自主执行任务
uv run uiautoagent -m ai -t "修改昵称为 kitty"

# 其他模式
uv run uiautoagent -m find    # 查找并点击
uv run uiautoagent -m manual  # 手动控制
```

## Python API

```python
from uiautoagent.detector import detect_element
from uiautoagent.controller import AndroidController
from uiautoagent.agent import DeviceAgent, Action, ActionType

# 元素检测
result = detect_element("screenshot.png", "登录按钮")
print(result.bbox)

# 设备自动化
controller = AndroidController()
agent = DeviceAgent(controller)
agent.step(Action(type=ActionType.TAP, thought="点击", target="按钮"))
```

## 要求

- Python 3.10+
- 支持 Vision 的模型（已测试：doubao-seed-2.0-pro）
- 兼容 OpenAI API 格式
- Android 需要 ADB

## License

[LICENSE](LICENSE)
