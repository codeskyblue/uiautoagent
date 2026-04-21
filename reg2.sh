#!/bin/bash
#

set -e

NAME=${1:?}
uv run uiautoagent -m ai -t "帮我完成后续的注册流程，邮箱先跳过，姓名是$NAME, 头像从相册中选择一个能用的，权限弹出通通允许"
