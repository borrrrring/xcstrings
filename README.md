# XCStrings Localization Tool

This document is also available in [Chinese (点击此处查看中文版本)](README.zh.md).

**Note: The free Gemini service provided by Google has been under heavy load recently, with a very high request failure rate. If you encounter frequent errors, we recommend switching to another translation service or waiting for Google to open the paid Gemini interface in the future.**

> Latest update in 20240322
> Support the use of [DeepLX](https://github.com/OwO-Network/DeepLX) translation
>  Configuration is required before using `xcstrings_DeepLX.py`
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

This tool helps automate the translation of iOS apps. It uses Google Translation for this purpose. There are two main scripts: `xcstrings.py` and `xcstrings_Gemini.py`. 

## Installation

To setup and run this project, you need to install some requirements. Use the following command:

`pip3 install -r requirements.txt`

The requirements.txt file should contain: 
> googletrans==4.0.0rc1
> opencc-python-reimplemented
> google-generativeai


1. Setup Google API Key: 

You can find the setup guide here [Google AI Studio](https://makersuite.google.com). 

For the error of "The caller does not have permission", maybe you can find help at [Gemini, MakerSuite, API Keys, and "The caller does not have permission"](https://freedium.cfd/https://medium.com/@afirstenberg/gemini-makersuite-api-keys-and-the-caller-does-not-have-permission-c75bedcbe886).（对于“The caller does not have permission”的错误，也许您可以在[Gemini, MakerSuite, API Keys, and "The caller does not have permission"](https://freedium.cfd/https://medium.com/@afirstenberg/gemini-makersuite-api-keys-and-the-caller-does-not-have-permission-c75bedcbe886)找到帮助）

Replace `GOOGLE_API_KEY` in `xcstrings_Gemini.py` with your API key.


## Running The Scripts

First, navigate to your preferred directory and clone the project using git: 

git clone <this repo URL>
cd <repo directory>


Run the scripts:

```bash
python3 xcstrings.py
```
or
```bash
python3 xcstrings_Gemini.py
```

## Usage

The programs will ask you to enter the path to your .xcstrings file.

> Enter the string Catalog (.xcstrings) file path:

Then, it will automatically load the keys of strings, detect the source language, translate the strings to the target language, and save the "localizations" in the JSON file.

## Contributing 

Contributions are welcome! Please create an issue or open a PR.