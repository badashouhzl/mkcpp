[toc]
# mkcpp 项目创建器
此项目为 c++ 项目创建，完美用于 vscode 写 c++

## 运用以下技术
用 cmake 为项目管理
以 ninja 为构建生成器
用 vscode 为代码编辑器
使用 clangd 为 vscode 的语言服务器
使用插件 CodeLLDB + lldb 为项目调试器
使用 clang-format 为代码格式器


## 打包命令
```bash
uv venv .venv
uv sync
# 如果需要更新模板，请在 ../cpp 下, 克隆 cppAppTemplate 项目，并执行下面脚本
# python src/genTemplate.py
sh releasePack.sh # windows 用 ./releasePack.bat
```

## 安装
发行包，加权直接执行