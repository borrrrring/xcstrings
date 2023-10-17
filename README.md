# xcstrings
Use Google to automatically translate String Catalog (.xcstrings) files in Xcode 15.

**Require:**
python3
pip install --upgrade googletrans==4.0.0rc1

1. Modify `languageIdentifiers = ['en', 'zh-Hans', 'zh-Hant', 'ja']` to specify the language type that needs to be translated.
2. Modify `languageIdentifiersForGoogle = { 'en': 'en',  'zh-Hans': 'zh-CN', 'zh-Hant': 'zh-TW', 'ja': 'ja' }` to specify the language type of Google Translate.
3. `python3 xcstrings.py`
4. Input String Catalog (.xcstrings) file's path
5. Wait until it done.

**中文：**

使用谷歌在Xcode 15中自动翻译String Catalog（.xcstrings）文件。
**要求：** 
python3 
pip install --upgrade googletrans==4.0.0rc1 
1. 修改`languageIdentifiers = ['en', 'zh-Hans', 'zh-Hant', 'ja']`以指定需要翻译的语言类型。
2. 修改 `languageIdentifiersForGoogle = { 'en': 'en', 'zh-Hans': 'zh-CN', 'zh-Hant': 'zh-TW', 'ja': 'ja' }` 以指定谷歌翻译的语言类型。
3. `python3 xcstrings.py` 
4. 输入String Catalog（.xcstrings）文件的路径
5. 等待完成。
