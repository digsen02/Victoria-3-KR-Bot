import json
import os


def load_file(folder, file):
    try:
        with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_file(folder, file, plans):
    try:
        with open(os.path.join(folder, file), "w", encoding="utf-8") as f:
            json.dump(plans, f, ensure_ascii=False, indent=2)
    except FileNotFoundError :
        print("File not found")