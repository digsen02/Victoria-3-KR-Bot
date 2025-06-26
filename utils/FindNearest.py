import datetime
import json
from utils.DateJudg import *
from utils.dataFileManager import *

def find_nearest(plans=None, number=0):
    if plans is None:
        plans = load_file("database", "multi.json")

    first_key, first_value = list(plans.items())[number]
    nearest_title = first_key
    nearest_date = datetime.datetime.strptime(first_value["start_date"], "%Y-%m-%d_%H:%M")
    comp_target = nearest_date

    for key, value in plans.items():
        current_date = datetime.datetime.strptime(value["start_date"], "%Y-%m-%d_%H:%M")

        if current_date < comp_target:
            comp_target = current_date
            nearest_date = current_date
            nearest_title = key

    return nearest_title, nearest_date