# XCStrings本地化工具

**注意：谷歌提供的 Gemini 的免费服务近期负载巨大，请求失败率非常高。如频繁遇到错误，建议切换到其他翻译服务，或者等待谷歌未来开放 Gemini 付费接口后再使用。**

> 20240322 最新更新
> 支持使用[DeepLX](https://github.com/OwO-Network/DeepLX)翻译
> 使用`xcstrings_DeepLX.py`前需要配置
> ```
> brew tap owo-network/brew
> brew install deeplx
> brew services start owo-network/brew/deeplx
>
> # Update to the latest version
> brew update
> brew upgrade deeplx
> brew services restart owo-network/brew/deeplx
> 
> # View the currently installed version
> brew list --versions deeplx
> ```

此工具帮助自动编译iOS应用的语言。它使用了Google的翻译服务。主要有两种脚本:`xcstrings.py`和`xcstrings_Gemini.py`.

## 安装

要设置和运行此项目，您需要安装一些要求。使用以下命令：

`pip3 install -r requirements.txt`

其中requirements.txt文件应包含以下内容：
> googletrans==4.0.0rc1
> opencc-python-reimplemented
> google-generativeai


1. 设置Google API 密钥：

您可以在这里 [Google AI Studio](https://makersuite.google.com) 找到相关的设置引导。

对于“The caller does not have permission”的错误，也许您可以在[Gemini, MakerSuite, API Keys, and "The caller does not have permission"](https://freedium.cfd/https://medium.com/@afirstenberg/gemini-makersuite-api-keys-and-the-caller-does-not-have-permission-c75bedcbe886)找到帮助

替代 `xcstrings_Gemini.py` 中的 `GOOGLE_API_KEY` 为你的API密钥。


## 运行脚本

首先，导航至您所选择的文件夹，然后使用git克隆项目：

git clone <this repo URL>
cd <repo directory>


运行脚本：

```bash
python3 xcstrings.py
```
或
```bash
python3 xcstrings_Gemini.py
```

## 使用

当程序要求您输入 .xcstrings 文件的路径时，按提示操作：

> Enter the string Catalog (.xcstrings) file path:

然后，它将会自动的加载字符串的键值，检测源语言，将字符串编译为目标语言，然后保存在JSON文件中的“本地化”项目中。

## 参与贡献

欢迎参与贡献! 请创建问题或打开PR。