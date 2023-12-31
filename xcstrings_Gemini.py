import os
import json
import datetime
import time
import re

# pip install -q -U google-generativeai
import google.generativeai as genai

# pip install opencc-python-reimplemented
from opencc import OpenCC 

GOOGLE_API_KEY=''

if not GOOGLE_API_KEY:
    raise ValueError("The GOOGLE_API_KEY needs to be set in [Google AI Studio](https://makersuite.google.com)!")

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

openCC = OpenCC('s2t')

# Global variables
is_info_plist = False
LANGUAGE_IDENTIFIERS = ['en', 'zh-Hans', 'zh-Hant']#, 'es', 'pt-PT', 'ja', 'ko']
LANGUAGE_IDENTIFIERS_FOR_GOOGLE = {
    'zh-Hans': 'zh-CN', 
    'zh-Hant': 'zh-TW',
    'zh-HK': 'zh-TW',
    'pt-PT': 'pt'
}

# Use automatic detection source language for translation
def translate_string(string, target_language):
    if target_language not in LANGUAGE_IDENTIFIERS_FOR_GOOGLE:
        dest = target_language
    else:
        dest = LANGUAGE_IDENTIFIERS_FOR_GOOGLE[target_language]

    prompt = """
    You are a professional, authentic translation engine, only returns translations.
    For example:
    <Start>
    Hello <Keep This Symbol>
    World <Keep This Symbol>
    <End>
    The translation is:
    <Start>
    你好<Keep This Symbol>
    世界<Keep This Symbol>
    <End>

    Translate the content to {} Language:

    <Start>{}<End>
    """.format(dest, string)

    try:
        response = model.generate_content(prompt)
        result = response.text
        match = re.search('<Start>(.*?)<End>', result, re.DOTALL)
        if match: 
            translated_text = match.group(1).strip()
            print(f"{dest}: {translated_text}")
            return translated_text
    except Exception as e:
        print(f'{type(e).__name__}: {e}')
        print("Translation timeout, retrying after 1 seconds...")
        time.sleep(1)
        return translate_string(string, target_language)

def main():
    # Get all the keys of strings
    with open(json_path, "r", encoding="utf-8") as f:
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
            strings = {"extractionState": "manual", "localizations": {}}
        
        # The localizations field is empty
        if "localizations" not in strings:
            strings["localizations"] = {}
    
        localizations = strings["localizations"]

        for language in LANGUAGE_IDENTIFIERS:
            # Determine whether localizations contains the corresponding language key
            if language not in localizations:
                if not is_info_plist:
                    source_language = json_data["sourceLanguage"]
                    # If not included, use Google Gemini to fill in "localizations" after translation.
                    if source_language == "zh-Hans":
                        source_string = key
                    else:
                       source_string = (
                            localizations["en"]["stringUnit"]["value"]
                            if "en" in localizations
                            else key
                        ) 
                    if language == source_language:
                        translated_string = source_string
                    else:
                        if source_language == "zh-Hans" and language == "zh-Hant":
                            translated_string = openCC.convert(source_string)
                        else:
                            translated_string = translate_string(source_string, language)

                    localizations[language] = {
                        "stringUnit": {
                            "state": "translated",
                            "value": translated_string,
                        }
                    }
                else:
                    source_language = json_data["sourceLanguage"]
                    if source_language not in localizations:
                        print("String is empty in source language")
                        continue
                    else:
                        if source_language == "zh-Hans":
                            source_string = localizations[source_language]["stringUnit"]["value"]
                        else:
                            source_string = (
                                localizations["en"]["stringUnit"]["value"]
                                if "en" in localizations
                                else key
                            ) 
                        if source_language == "zh-Hans" and language == "zh-Hant":
                            translated_string = openCC.convert(source_string)
                        else:
                            translated_string = translate_string(source_string, language)
                        localizations[language] = {
                            "stringUnit": {
                                "state": "translated",
                                "value": translated_string,
                            }
                        }
            else:
                print(f"{language} has been translated")

        # strings["localizations"] = {}
        strings["localizations"] = localizations
        json_data["strings"][key] = strings

        # Save the modified JSON file every time to prevent flashback.
        with open(json_path, "w", encoding='utf-8') as f:
            json.dump(json_data, ensure_ascii=False, fp=f, indent=4)

def is_infoplist(json_path):
    """
    Determine whether the file name is "InfoPlist.xcstrings" 
    
    Args: 
        json_path: File path 
    Returns: 
        True: Yes "InfoPlist.xcstrings" 
        False: Not "InfoPlist.xcstrings" 
    """

    filename = os.path.basename(json_path)
    return filename == 'InfoPlist.xcstrings'

if __name__ == "__main__":
    # Input json_path from terminal
    json_path = input("Enter the string Catalog (.xcstrings) file path:\n")
    is_info_plist = is_infoplist(json_path)
    main()
