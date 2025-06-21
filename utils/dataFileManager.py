import json
import os


def load_file(folder, file):
    try:
        with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_file(folder, file, plans):
    print("뭐가 문제여")
    try:
        print("뭐가 문제여2")

        with open(os.path.join(folder, file), "w", encoding="utf-8") as f:
            print("뭐가 문제여3")
            json.dump(plans, f, ensure_ascii=False, indent=2)
    except FileNotFoundError :
        print("에러가 났네")