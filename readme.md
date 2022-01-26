# 工具箱

## Windows 配置方法

加入环境变量即可。Windows 配合 Chocolatey 食用更佳。

## Linux/WSL 配置方法

加入环境变量即可。以 zsh 为例，将以下内容写入 `.zshrc`：

```sh
if [ -d "/home/liu/git/dev-tools" ] ; then
  PATH="$PATH:/home/liu/git/dev-tools"
fi
```