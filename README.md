# XCStrings Localization Tool (XCStrings本地化工具)

This tool helps automate the translation of iOS apps. It uses Google Translation for this purpose. There are two main scripts: `xcstrings.py` and `xcstrings_Gemini.py`. 
（此工具帮助自动编译iOS应用的语言。它使用了Google的翻译服务。主要有两种脚本:`xcstrings.py`和`xcstrings_Gemini.py`.）

## Installation (安装)

To setup and run this project, you need to install some requirements. Use the following command: (要设置和运行此项目，您需要安装一些要求。使用以下命令：)

`pip3 install -r requirements.txt`

The requirements.txt file should contain: (其中requirements.txt文件应包含以下内容：)
> googletrans==4.0.0rc1
> opencc-python-reimplemented
> google-generativeai


1. Setup Google API Key: (设置Google API 密钥：)

You can find the setup guide here [Google AI Studio](https://makersuite.google.com). (您可以在这里 [Google AI Studio](https://makersuite.google.com) 找到相关的设置引导。)

Replace `GOOGLE_API_KEY` in `xcstrings_Gemini.py` with your API key. (替代 `xcstrings_Gemini.py` 中的 `GOOGLE_API_KEY` 为你的API密钥。)


## Running The Scripts (运行脚本)

First, navigate to your preferred directory and clone the project using git: (首先，导航至您所选择的文件夹，然后使用git克隆项目：)

git clone <this repo URL>
cd <repo directory>


Run the scripts: (运行脚本：)

```bash
python3 xcstrings.py
```
or (或)
```bash
python3 xcstrings_Gemini.py
```

## Usage (使用)

The programs will ask you to enter the path to your .xcstrings file. (当程序要求您输入 .xcstrings 文件的路径时，按提示操作：)

> Enter the string Catalog (.xcstrings) file path:

Then, it will automatically load the keys of strings, detect the source language, translate the strings to the target language, and save the "localizations" in the JSON file. (然后，它将会自动的加载字符串的键值，检测源语言，将字符串编译为目标语言，然后保存在JSON文件中的“本地化”项目中。)

## Contributing (参与贡献)

Contributions are welcome! Please create an issue or open a PR. (欢迎参与贡献! 请创建问题或打开PR。)