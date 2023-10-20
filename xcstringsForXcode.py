import os
import sys
import json
import datetime
import time

# pip install --upgrade googletrans==4.0.0rc1
from googletrans import Translator

# Global variables
isInfoPlist = False
languageIdentifiers = ['en', 'zh-Hans', 'zh-Hant']
languageIdentifiersForGoogle = {
    'zh-Hans': 'zh-CN', 
    'zh-Hant': 'zh-TW',
    'zh-HK': 'zh-TW',
    'pt-PT': 'pt'
}

# Use automatic detection source language for translation
def translate_string(string, target_language):
    translator = Translator()
    
    if target_language not in languageIdentifiersForGoogle:
        dest = target_language
    else:
        dest = languageIdentifiersForGoogle[target_language]

    try:
        source_language = translator.detect(string).lang
        if source_language == dest:
            return string
        
        translation = translator.translate(string, dest=dest)
    except Exception as e:
        print(e)
        print("翻译超时，等待3秒后重新执行翻译...")
        time.sleep(2)
        return translate_string(string, target_language)
        

    print(f"{target_language}: {translation.text}")
    return translation.text

def main():
    # Get all the keys of strings
    with open(json_path, "r") as f:
        json_data = json.load(f)
    strings_keys = list(json_data["strings"].keys())

    print(f"\nFound {len(strings_keys)} keys\n")

    # Traverse all keys
    for key_index, key in enumerate(strings_keys):
        if not key:
            continue
        # Get the current time
        now = datetime.datetime.now()
        # Format the current time
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now_str}]\n", f"🔥{key_index + 1}/{len(strings_keys)}: {key}")

        strings = json_data["strings"][key]
        # The strings field is empty.
        if not strings:
            strings = {
                "extractionState": "manual",
                "localizations": {},
            }
        # The localizations field is empty
        if "localizations" not in strings:
            strings["localizations"] = {}
    
        localizations = strings["localizations"]

        for language in languageIdentifiers:
            # Determine whether localizations contains the corresponding language key
            if language not in localizations:
                if not isInfoPlist:
                    # If not included, use Googletrans to fill in "localizations" after translation.
                    localizations[language] = {
                        "stringUnit": {
                            "state": "translated",
                            "value": translate_string(key, language),
                        }
                    }
                else:
                   sourceLanguage = json_data["sourceLanguage"]
                   if sourceLanguage not in localizations:
                       continue
                   else:
                    sourceString = localizations[sourceLanguage]["stringUnit"]["value"]
                    localizations[language] = {
                        "stringUnit": {
                            "state": "translated",
                            "value": translate_string(sourceString, language),
                        }
                    }

        strings["localizations"] = localizations
        json_data["strings"][key] = strings

        # Save the modified JSON file every time to prevent flashback.
        with open(json_path, "w", encoding="ascii") as f:
            json.dump(json_data, f, indent=4)

def is_infoplist(json_path):
    """
    判断文件名是否为“InfoPlist”

    Args:
        json_path: 文件路径

    Returns:
        True：是“InfoPlist”
        False：不是“InfoPlist”
    """

    filename = os.path.basename(json_path)
    return filename == 'InfoPlist.xcstrings'

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("请输入项目路径")
        sys.exit(1)

    json_path = sys.argv[1]
    isInfoPlist = is_infoplist(json_path)
    main()
