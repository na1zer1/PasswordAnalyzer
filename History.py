import json
import subprocess
from pathlib import Path
from rich import print
from Global_func import new_screen, made_options_list






clear_json = {
    "passwords": []
}

h_path = Path("json_files/history.json") # h_path = history_path





def add_password_in_history(password: str, word: str, points: int, password_problems: list):

    new_password = {
        "password": f"{password}",
        "word": f"{word}",
        "points": points,
        "password_problems": password_problems
    }
    with open(h_path, "r") as file:
        history = json.load(file)
    
    history["passwords"].append(new_password)

    with open(h_path, "w") as file:
        json.dump(history, file, indent=4)



def search_password(password: str) -> list:
    with open(h_path, "r") as file:
        history = json.load(file)
    
    for i in history["passwords"]:
        if i["password"] == password:
            return [i["word"], i["points"], i["password_problems"]]
    return []



@new_screen
def clear_history():

    made_options_list("Are you sure to clear history?", "red", ("YES", "NO"))
    cls_answer = input()
    
    subprocess.run("cls", shell=True)
    if cls_answer == "1":
        with open(h_path, "w") as file:
            json.dump(clear_json, file, indent=4)
        print("[i green]History was successfully clear![/i green]")
    else:
        print("[i]Canceled[/i]")



def show_history():
    with open(h_path) as file:
        history = json.load(file)
    if not history["passwords"]:
        print("[i red]History is empty...\n[/i red]")
    else:
        print("[b blue]HISTORY[/b blue]")
        for i in history["passwords"]:
            print("[b]-[/b]"*25)
            print(f"[b cyan]\nPassword[/b cyan]: [i]{i["password"]}\n[/i]"
                  f"[b bright_yellow]Difficulty[/b bright_yellow]: [i]{i["word"]}\n[/i]"
                  f"[b bright_blue]Points[/b bright_blue]: [i]{i["points"]}\n[/i]"
                  f"[b orange_red1]Passwords recomendations[/b orange_red1]:\n[i grey35] - {"\n - ".join(i["password_problems"])}\n[/i grey35]")
            
    print("[i grey35]Press Enter to continue...[/i grey35]")