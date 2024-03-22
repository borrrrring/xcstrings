import os
import json
import datetime
import time
import re
from argparse import ArgumentParser
import requests

# pip install opencc-python-reimplemented
from opencc import OpenCC

LANGUAGE_IDENTIFIERS = [
    "en",
    "zh-Hans",
    "zh-Hant",
]  # , 'ar', 'de', 'es', 'fr', 'ja', 'ko', 'pt-PT', 'ru', 'tr']


openCC = OpenCC("s2t")

deeplx_api = "http://127.0.0.1:1188/translate"

# Global variables
is_info_plist = False

LANGUAGE_IDENTIFIERS_FOR_DEEPL = {
    "zh-Hans": "ZH",
    "pt-PT": "PT",
    "en": "EN",
    "ar": "AR",
    "de": "DE",
    "bg": "BG",
    "cs": "CS",
    "da": "DA",
    "el": "EL",
    "en-GB": "EN-GB",
    "en-US": "EN-US",
    "es": "ES",
    "et": "ET",
    "fi": "FI",
    "fr": "FR",
    "hu": "HU",
    "id": "ID",
    "it": "IT",
    "ja": "JA",
    "ko": "KO",
    "lt": "LT",
    "lv": "LV",
    "nb": "NB",
    "nl": "NL",
    "pl": "PL",
    "pt-BR": "PT-BR",
    "ro": "RO",
    "ru": "RU",
    "sk": "SK",
    "sl": "SL",
    "sv": "SV",
    "tr": "TR",
    "uk": "UK",
}


# Use automatic detection source language for translation
def translate_string(string, target_language):
    if target_language not in LANGUAGE_IDENTIFIERS_FOR_DEEPL:
        dest = target_language
    else:
        dest = LANGUAGE_IDENTIFIERS_FOR_DEEPL[target_language]

    json_data = {"text": string, "target_lang": dest}

    try:
        response = requests.post(
            url=deeplx_api,
            json=json_data
        )
        response.raise_for_status()  # Raise an error for HTTP error responses
        data_parsed = response.json()
        translated_text = data_parsed.get("data")
        if not translated_text:  # Check if translated_text is empty or None
            raise ValueError("No translation data found in the response.")
        print(f"{target_language}: {translated_text}")
        return translated_text
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
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
                            translated_string = translate_string(
                                source_string, language
                            )

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
                            source_string = localizations[source_language][
                                "stringUnit"
                            ]["value"]
                        else:
                            source_string = (
                                localizations["en"]["stringUnit"]["value"]
                                if "en" in localizations
                                else key
                            )
                        if source_language == "zh-Hans" and language == "zh-Hant":
                            translated_string = openCC.convert(source_string)
                        else:
                            translated_string = translate_string(
                                source_string, language
                            )
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
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, ensure_ascii=False, fp=f, indent=4)


def is_infoplist(json_path):
    filename, _ = os.path.splitext(os.path.basename(json_path))
    return filename == "InfoPlist"


if __name__ == "__main__":
    # Input json_path from terminal
    json_path = input("Enter the string Catalog (.xcstrings) file path:\n").strip(
        " \"'"
    )
    is_info_plist = is_infoplist(json_path)
    main()
