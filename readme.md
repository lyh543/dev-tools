# 工具箱

为了更好的跨平台，脚本都使用 Python 重写了。请在 Windows 设置 Python 为 `.py` 文件的默认打开方式。

## Windows 配置方法

1. 将文件夹加入环境变量。
2. 并设置 Python 为 `.py` 文件的默认打开方式即可。 
3. 部分命令可能需要安装 PowerShell 7 并加入环境变量（能正常运行 `pwsh`）才能正确执行。
4. Windows 配合 Chocolatey 食用更佳。

## Linux/WSL 配置方法

加入环境变量即可。以 zsh 为例，将以下内容写入 `.zshrc`：

```sh
if [ -d "/home/liu/git/dev-tools" ] ; then
  PATH="$PATH:/home/liu/git/dev-tools"
fi
```