import json
import datetime

# pip install --upgrade googletrans==4.0.0rc1
from googletrans import Translator

# Global variables
languageIdentifiers = ['en', 'zh-Hans', 'zh-Hant']
languageIdentifiersForGoogle = {
    'zh-Hans': 'zh', 
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

    translation = translator.translate(string, dest=dest)

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
                # If not included, use Googletrans to fill in "localizations" after translation.
                localizations[language] = {
                    "stringUnit": {
                        "state": "translated",
                        "value": translate_string(key, language),
                    }
                }

        strings["localizations"] = localizations
        json_data["strings"][key] = strings

        # Save the modified JSON file every time to prevent flashback.
        with open(json_path, "w") as f:
            json.dump(json_data, f, indent=4)


if __name__ == "__main__":
    # Input json_path from terminal
    json_path = input("Enter the string Catalog (.xcstrings) file path:\n")
    main()
