#!/bin/bash
#

set -e

NUMBER=${1:?}
uv run uiautoagent -m ai -t "帮我打开whatsapp，注册账号，号码是${NUMBER}, 使用号码对应的国家语言, 遇到封禁界面或注册码界面退出"
