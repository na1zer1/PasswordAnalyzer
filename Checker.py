import math
import json
from pathlib import Path

config_path = Path("json_files/config.json")

def password_evaluation(info: dict) -> str:
    global MAX_LENTH_POINTS, MAX_TF_POINTS, points, config

    with open(config_path, "r") as file:
        config = json.load(file)

    MAX_LENTH_POINTS = config["max_lenth_points"] 
    MAX_TF_POINTS = config["max_tf_points"] 
    points = 0

    good_lenth = False # Подразумевается, что если False, то мало и наоборот

    if info["lenth"] > 8:
        good_lenth = True
    
    good_diversity = all(list(info.values())[2:])

    word = word_grade(good_lenth, good_diversity)

    num_grade(word, info)

    return [word, points]


def word_grade(good_lenth: bool, good_diversity: bool) -> str:
    if all([good_lenth, good_diversity]):
        return "GOOD"
    elif any([good_lenth, good_diversity]):
        return "MEDIUM"
    elif not(all([good_lenth, good_diversity])):
        return "WEAK"

def num_grade(word: str, info: dict):
    global points
    points += MAX_LENTH_POINTS * (1 - math.exp(-0.10 * info["lenth"]))

    if info["digits_in"]:
        points += MAX_TF_POINTS * 0.2
    if info["upper_cases_in"]:
        points += MAX_TF_POINTS * 0.3
    if info["spec_symbols_in"]:
        points += MAX_TF_POINTS * 0.5
    
    k = config["word_k"][word]
    
    points = round(points * k)

def recomendations():
    pass