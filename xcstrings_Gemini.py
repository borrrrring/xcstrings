import os
import json
import datetime
import time
import threading
import re
from collections import defaultdict
import requests
import random

# pip install opencc-python-reimplemented
from opencc import OpenCC 

GOOGLE_API_KEY=''

if not GOOGLE_API_KEY:
    GOOGLE_API_KEY = input("Enter your Google API Key for Gemini translations:\n").strip()
    if not GOOGLE_API_KEY:
        raise ValueError("Don't forget to set your GOOGLE_API_KEY in Google AI Studio (https://makersuite.google.com) for Gemini translations!")

openCC = OpenCC('s2t')

# Global variables
is_info_plist = False
LANGUAGE_IDENTIFIERS = ['en', 'zh-Hans', 'zh-Hant']#, 'ja', 'ko', 'ar', 'de', 'es', 'fr', 'ja', 'ko', 'pt-PT', 'ru', 'tr']
BATCH_SIZE = 4000
SEPARATOR = "||"
APPCATEGORY = ""

def exponential_backoff(retry_count, base_delay=1, max_delay=60):
    exponential_delay = min(base_delay * (2 ** retry_count), max_delay)
    actual_delay = exponential_delay + random.uniform(0, 1)  # Add jitter
    return actual_delay

def print_elapsed_time(start_time, stop_event):
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")
        time.sleep(1)

# Use automatic detection source language for translation
def translate_batch(strings, target_language):
    time.sleep(1)
    prompt = f"""You are a professional localization service provider specializing in translating content for specific languages, cultures, and categories.
    For example:
    <Start>
    Hello{SEPARATOR}World{SEPARATOR}谷歌
    <End>
    The translation is:
    <Start>
    你好{SEPARATOR}世界{SEPARATOR}谷歌
    <End>
    
    Translate the following content to {target_language} Language"""
    
    if APPCATEGORY:
        prompt += f" for the app categorized as a {APPCATEGORY}."
        
    prompt += f"""
    Each item is separated by {SEPARATOR}. Please keep the same structure in your response.

    <Start>{SEPARATOR.join(strings)}<End>"""

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

    retry_count = 0
    while True:
        try:
            start_time = time.time()
            stop_event = threading.Event()
            timer_thread = threading.Thread(target=print_elapsed_time, args=(start_time, stop_event))
            timer_thread.start()
            print("Starting translation request...")
            response = requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent', 
                                     params=params, headers=headers, json=json_data)
            stop_event.set()
            timer_thread.join()
            response.raise_for_status()
            print("Request successful!")
            data_parsed = response.json()
            print("Response data:", data_parsed)
            result = get_text_from_json(data_parsed)
            match = re.search('<Start>(.*?)<End>', result, re.DOTALL)
            if match:
                translated_text = match.group(1).strip()
                return translated_text.split(SEPARATOR)
            else:
                continue
        except Exception as e:
            stop_event.set()
            timer_thread.join()
            print(f'{type(e).__name__}: {e}')
            retry_count += 1
            delay = exponential_backoff(retry_count)
            print(f"Translation timeout, retrying after {delay:.2f} seconds...")
            time.sleep(delay)

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

def process_others_translations(json_data, language, keys, strings_to_translate_list):
    translated_strings = translate_batch(strings_to_translate_list, language)
    for key, translated in zip(keys, translated_strings):
        print(f"{language}: {key} ==> {translated}")
        json_data["strings"][key]["localizations"][language] = {
            "stringUnit": {
                "state": "translated",
                "value": translated,
            }
        }

def process_english_translations(json_data, english_strings, strings_needing_english, strings_to_translate):
    english_translations = translate_batch(english_strings, "en")
    for (key, original), translated in zip(strings_needing_english, english_translations):
        print(f"en: {key} ==> {translated}")
        json_data["strings"][key]["localizations"]["en"] = {
            "stringUnit": {
                "state": "translated",
                "value": translated,
            }
        }
        # Add the English translation to other language queues
        for language in LANGUAGE_IDENTIFIERS:
            if language not in ["en", "zh-Hans", "zh-Hant"]:
                strings_to_translate[(language, key)] = translated

def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

def is_info_plist(file_path):
    return os.path.basename(file_path).lower() == 'infoplist.xcstrings'

def main():
    try:
    # Get all the keys of strings
        with open(json_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
    except Exception as e:
        print(f"Error decoding JSON data: {e}")
        return

    # Clearing the Screen
    clear()
    
    if not APPCATEGORY:
        print(f"Begin the localization process at path: \n{json_path}")
    else:
        print(f"Begin the localization process for the app categorized as a {APPCATEGORY} at path: \n{json_path}")

    global LANGUAGE_IDENTIFIERS
    # Get language identifiers from the user
    language_input = input("Enter the language codes to translate into (comma-separated), e.g., 'en, zh-Hans, zh-Hant' (default is ['en', 'zh-Hans', 'zh-Hant']):\n").strip()
    if language_input:
        LANGUAGE_IDENTIFIERS = [lang.strip() for lang in language_input.split(',')]
    else:
        print("No languages entered. Using default languages ['en', 'zh-Hans', 'zh-Hant'].")
        LANGUAGE_IDENTIFIERS = ['en', 'zh-Hans', 'zh-Hant']

    global is_info_plist
    is_info_plist_file = is_info_plist(json_path)
    strings_to_translate = {}
    strings_needing_english = []
    source_language = json_data["sourceLanguage"]

    mark_untranslated_manual = input("Do you want to mark untranslated parts as 'extractionState': 'manual'? (y/n, default is 'n'):\n").strip().lower()
    if mark_untranslated_manual == 'y':
        add_extraction_state = True
    else:
        add_extraction_state = False

    for key, strings in json_data["strings"].items():
        if "comment" in strings and "ignore xcstrings" in strings["comment"] or \
            ("shouldTranslate" in strings and strings["shouldTranslate"] == False):
            continue
        if not strings:
            if add_extraction_state:
                strings = {"extractionState": "manual", "localizations": {}}
            else:
                strings = {"localizations": {}}

        if "localizations" not in strings:
            strings["localizations"] = {}

        json_data["strings"][key] = strings

        localizations = strings["localizations"]
        
        if is_info_plist_file:
            # if key == "CFBundleName":
            #     continue
            # else:
                if source_language not in localizations:
                    print(f"Error: Source language '{source_language}' not found in InfoPlist.xcstrings")
                    return
                else:
                    if source_language == "zh-Hans":
                        source_string = localizations[source_language]["stringUnit"]["value"]
                    else:
                        source_string = (
                            localizations["en"]["stringUnit"]["value"]
                            if "en" in localizations
                            else key
                        )
                    
                strings_needing_english.append((key, source_string))
        else:
            if "en" in localizations:
                source_string = localizations["en"]["stringUnit"]["value"]
            elif source_language == "zh-Hans":
                source_string = key
                strings_needing_english.append((key, source_string))
            else:
                source_string = localizations[source_language]["stringUnit"]["value"] if source_language in localizations else key
                strings_needing_english.append((key, source_string))
        
        for language in LANGUAGE_IDENTIFIERS:
            if language not in localizations:
                if language == source_language:
                    translated_string = source_string
                elif source_language == "zh-Hans" and language == "zh-Hant":
                    translated_string = OpenCC('s2t').convert(source_string)
                elif language == "en" and source_language != "en":
                    continue  # We'll handle English translations separately
                else:
                    strings_to_translate[(language, key)] = source_string
                    continue

                localizations[language] = {
                    "stringUnit": {
                        "state": "translated",
                        "value": translated_string,
                    }
                }
            else:
                print(f"{language}: {{{key}: {source_string}}} has been translated")

    # Handle English translations first
    if strings_needing_english:
        english_strings = [s[1] for s in strings_needing_english]
        
        # Loop through the strings in chunks
        start_index = 0
        while start_index < len(english_strings):
        # Determine the end index for the current chunk
            combined_string = ""
            end_index = start_index
            while end_index < len(english_strings) and len(combined_string + english_strings[end_index] + SEPARATOR) <= BATCH_SIZE:
                combined_string += english_strings[end_index] + SEPARATOR
                end_index += 1
            
            # Remove the trailing separator
            combined_string = combined_string.rstrip(SEPARATOR)
            # Process the current chunk of translations
            process_english_translations(json_data, english_strings[start_index:end_index], strings_needing_english[start_index:end_index], strings_to_translate)
            # Update the start index for the next chunk
            start_index = end_index
        

    # Process any remaining strings for each language
    if strings_to_translate:
        languages = set(lang for lang, _ in strings_to_translate.keys())
        for language in languages:
            lang_strings = {key: value for (lang, key), value in strings_to_translate.items() if lang == language}
            if not lang_strings:
                continue
            
            keys = list(lang_strings.keys())
            strings_to_translate_list = list(lang_strings.values())
            # Loop through the strings in chunks
            start_index = 0
            while start_index < len(strings_to_translate_list):
            # Determine the end index for the current chunk
                combined_string = ""
                end_index = start_index
                while end_index < len(strings_to_translate_list) and len(combined_string + strings_to_translate_list[end_index] + SEPARATOR) <= BATCH_SIZE:
                    combined_string += strings_to_translate_list[end_index] + SEPARATOR
                    end_index += 1
                
                # Remove the trailing separator
                combined_string = combined_string.rstrip(SEPARATOR)
                # Process the current chunk of translations
                process_others_translations(json_data, language, keys[start_index:end_index], strings_to_translate_list[start_index:end_index])
                # Update the start index for the next chunk
                start_index = end_index

    # Save the modified JSON file
    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(json_data, ensure_ascii=False, fp=f, indent=4)

if __name__ == "__main__":
    # Input json_path from terminal
    json_path = input("Enter the string Catalog (.xcstrings) file path:\n").strip(' "\'')
    json_path = json_path.replace('\\ ', ' ')
    # 检查文件是否存在
    if os.path.exists(json_path):
        print(f"File found at: {json_path}")
        # 继续处理文件
        APPCATEGORY = input("Enter the app category or name for precise Gemini translations:\n").strip(' "\'')
        main()
    else:
        print(f"Error: No such file or directory: '{json_path}'")
