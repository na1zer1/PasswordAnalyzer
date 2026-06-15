import math
import json
from pathlib import Path





config_path = Path("json_files/config.json")





def password_evaluation(info: dict) -> tuple:
    good_length = False # Подразумевается, что если False, то мало и наоборот

    if info["length"] > 8:
        good_length = True
    
    good_diversity = all(list(info.values())[2:])

    word = word_grade(good_length, good_diversity)
    points = num_grade(word, info)

    return (word, points)



def word_grade(good_length: bool, good_diversity: bool) -> str:
    if all((good_length, good_diversity)):
        return "GOOD"
    elif any((good_length, good_diversity)):
        return "MEDIUM"
    elif not(all((good_length, good_diversity))):
        return "WEAK"



def num_grade(word: str, info: dict) -> int:
    with open(config_path, "r") as file:
        config = json.load(file)

    points = min(config["max_length_points"], round(7*math.sqrt(info["length"])))

    if info["digits_in"]:
        points += config["max_tf_points"] * 0.2
    if info["upper_cases_in"]:
        points += config["max_tf_points"] * 0.3
    if info["spec_symbols_in"]:
        points += config["max_tf_points"] * 0.5
    
    k = config["word_k"][word]
    
    return round(points * k)