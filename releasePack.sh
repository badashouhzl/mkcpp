#!/bin/bash

set -e  # 出错立即退出

# 1. 获取最近的 Git tag（离 HEAD 最近的）
# 如果没有 tag，就用 commit hash 或 "unknown"
if git describe --tags --exact-match >/dev/null 2>&1; then
    # 当前提交正好是一个 tag
    VERSION=$(git describe --tags --exact-match)
	echo "__version__ = '$VERSION' # 此号落后一个版本" > src/version.py
	VERSION="_${VERSION}"
elif git describe --tags --abbrev=0 >/dev/null 2>&1; then
    # 获取最近的 tag（即使当前不在 tag 上）
    VERSION=$(git describe --tags --abbrev=0)
	echo "__version__ = '$VERSION' # 此号落后一个版本" > src/version.py
	VERSION="_${VERSION}"
else
    # 没有任何 tag，回退到 short commit hash
    VERSION=$(git rev-parse --short HEAD)
	VERSION="_${VERSION}"
fi


if [[ "$OSTYPE" == "linux"* ]]; then
	. .venv/bin/activate
	platform="linux-"
else
	. .venv/Scripts/activate
	platform="win-"
fi

# 刷新模板 请手执行
# python src/genTemplate.py

pyinstaller -F --name mkcpp main.py src/res.py src/version.py

mkdir bin -p
cp "dist/mkcpp" "bin/${platform}mkcpp${VERSION}"

rm -fr build/ mkcpp.spec dist/


echo "📦 当前版本: $VERSION"