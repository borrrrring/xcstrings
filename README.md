# xcstrings
Use googletrans to automatically translate String Catalog (.xcstrings) files in Xcode 15.

### xcstrings.py
**Require:**
python3
`pip install --upgrade googletrans==4.0.0rc1`

1. Modify `languageIdentifiers = ['en', 'zh-Hans', 'zh-Hant', 'ja']` to specify the language type that needs to be translated.
2. `python3 xcstrings.py`
3. Input String Catalog (.xcstrings) file's path
4. Wait until it done.

**中文：**

使用谷歌翻译在Xcode 15中自动翻译String Catalog（.xcstrings）文件。
**要求：** 
python3 
`pip install --upgrade googletrans==4.0.0rc1 `
1. 修改`languageIdentifiers = ['en', 'zh-Hans', 'zh-Hant', 'ja']`以指定需要翻译的语言类型。
2. `python3 xcstrings.py` 
3. 输入String Catalog（.xcstrings）文件的路径
4. 等待完成。

### xcstringsForXcode.py
**Require:**
Xcode
HomeBrew
`pip install --upgrade googletrans==4.0.0rc1`
`brew install python3`

1. Drag xcstringsForXcode.py to project root folder in Xcode. Select Copy items if needed, Create groups and check Add to tagets. 
2. Open Project - Targets - Build Phases - add 'New Run Script Phase'.
3. Copy then Paste below code to Script Phase.

```
    if [[ "$(uname -m)" == arm64 ]]; then
        export PATH="/opt/homebrew/bin:$PATH"
    fi
    
    if which python3 > /dev/null; then
       python3 "${PROJECT_DIR}/${PROJECT}/xcstrings.py" "${PROJECT_DIR}/${PROJECT}/Localizable.xcstrings"
       python3 "${PROJECT_DIR}/${PROJECT}/xcstrings.py" "${PROJECT_DIR}/${PROJECT}/InfoPlist.xcstrings"
    else
      echo "warning: python3 not installed"
    fi
```
    
4. Build project.

**中文：**

**要求：**
Xcode
HomeBrew
`pip install --upgrade googletrans==4.0.0rc1`
`brew install python3`

1. 将 xcstringsForXcode.py 拖至 Xcode 中的项目根文件夹。 选择“根据需要复制项目”、“创建组”并选中“添加到目标”。
2. 打开项目-目标-构建阶段-添加“新运行脚本阶段”。
3. 将以下代码复制并粘贴到脚本阶段。

```
    if [[ "$(uname -m)" == arm64 ]]; then
        export PATH="/opt/homebrew/bin:$PATH"
    fi
    
    if which python3 > /dev/null; then
       python3 "${PROJECT_DIR}/${PROJECT}/xcstrings.py" "${PROJECT_DIR}/${PROJECT}/Localizable.xcstrings"
       python3 "${PROJECT_DIR}/${PROJECT}/xcstrings.py" "${PROJECT_DIR}/${PROJECT}/InfoPlist.xcstrings"
    else
      echo "warning: python3 not installed"
    fi
```
    
4. 构建项目。