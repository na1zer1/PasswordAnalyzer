import json
import subprocess
from pathlib import Path
from rich import print
from Decorators import new_screen

clear_json = {
    "passwords": []
}

h_path = Path("json_files/history.json") # h_path = history_path
    
def add_password_in_history(password: str, word: str, poitns: int):

    new_password = {
        "password": f"{password}",
        "word": f"{word}",
        "points": f"{poitns}"
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
            return [i["word"], i["points"]]
    return []

@new_screen
def clear_history():

    print("[b red]Are you sure to clear history?\n[/b red]"
    "[1][i] YES[/i]\n"
    "[2][i] NO[/i]")

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
        print("[i]History is empty...\n[/i]")
    else:
        print("[b blue]HISTORY[/b blue]")
        for i in history["passwords"]:
            print("[b]-[/b]"*25)
            print(f"[b green]\nPassword[/b green]: [i]{i["password"]}\n[/i]"
                  f"[b green]Difficulty[/b green]: [i]{i["word"]}\n[/i]"
                  f"[b green]Points[/b green]: [i]{i["points"]}\n[/i]")
            
    print("[i]Press Enter to continue...[/i]")