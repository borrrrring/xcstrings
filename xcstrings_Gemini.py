import os
import json
import datetime
import time
import re
from argparse import ArgumentParser
import google.api_core.exceptions
import requests

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
LANGUAGE_IDENTIFIERS = ['en', 'zh-Hans', 'zh-Hant', 'es', 'ja', 'ko', 'pt-PT']#, 'ar', 'de', 'es', 'fr', 'ja', 'ko', 'pt-PT', 'ru', 'tr']

# Use automatic detection source language for translation
def translate_string(string, target_language):
    prompt = """
    You are a professional, authentic translation engine who can help me translate for iOS app, only returns translations.
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
    """.format(target_language, string)

    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'key': GOOGLE_API_KEY,
    }

    json_data = {
        'contents': [
            {
                'parts': [
                    {
                        'text': prompt,
                    },
                ],
            },
        ],
    }

    try:
#        response = model.generate_content(prompt)
#        result = response.text
        response = requests.post('https://gaga.now.cc/api/proxy/gemini-pro', params=params, headers=headers, json=json_data)
        response.raise_for_status()  # Raise an error for HTTP error responses
        data_parsed = response.json()
        result = get_text_from_json(data_parsed)
        match = re.search('<Start>(.*?)<End>', result, re.DOTALL)
        if match:
            translated_text = match.group(1).strip()
            print(f"{target_language}: {translated_text}")
            return translated_text
    except google.api_core.exceptions.PermissionDenied:
        raise ValueError("The GOOGLE_API_KEY is invalid. Please double check your GOOGLE_API_KEY and make sure the corresponding Google API is enabled.")
    except Exception as e:
        print(f'{type(e).__name__}: {e}')
        print("Translation timeout, retrying after 1 seconds...")
        time.sleep(1)
        return translate_string(string, target_language)

# Function to safely get the 'text' from parsed JSON data
def get_text_from_json(data):
    try:
        # Ensure 'candidates' is a list and not empty
        if (isinstance(data.get('candidates'), list) and
                len(data['candidates']) > 0):
            
            content = data['candidates'][0].get('content')
            # Ensure 'content' has a 'parts' list and it's not empty
            if content and isinstance(content.get('parts'), list) and len(content['parts']) > 0:
                
                text = content['parts'][0].get('text')
                # Return text if it's a string, otherwise, return a default string or raise an error
                return text if isinstance(text, str) else 'No text found'
        # If checks fail, return a default value or raise an error
        return 'No text found'
    except Exception as e:
        print(f'Error retrieving text: {e}')
        # Handle the exception as needed (e.g., return a default value, raise an error, log the issue, etc.)
        return 'No text found'

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
    filename, _ = os.path.splitext(os.path.basename(json_path))
    return filename == 'InfoPlist'

if __name__ == "__main__":
    # Input json_path from terminal
    json_path = input("Enter the string Catalog (.xcstrings) file path:\n").strip(' "\'')
    is_info_plist = is_infoplist(json_path)
    main()
