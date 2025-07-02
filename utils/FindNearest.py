import datetime
from utils.dataFileManager import *

def find_nearest(plans=None, number=0):
    if plans is None:
        plans = load_file("database", "multi.json")

    nearest_title = None
    nearest_date = None

    for title, plan in plans.items():
        try:
            date = datetime.datetime.strptime(plan["start_date"], "%Y-%m-%d_%H:%M")
        except (KeyError, ValueError) as e:
            print(f"[find_nearest] {title} 날짜 파싱 실패: {e}")
            continue

        if nearest_date is None or date < nearest_date:
            nearest_title = title
            nearest_date = date

    return nearest_title, nearest_date