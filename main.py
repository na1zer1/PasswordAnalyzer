import sys
import subprocess
import json
from rich import print
from pathlib import Path
from Checker import password_evaluation
import History as memory
from Decorators import new_screen

config_path = Path("json_files/config.json")

if not memory.h_path.exists():
        memory.h_path.write_text(json.dumps(memory.clear_json))

# Функции:
@new_screen
def main():
    global config
    with open(config_path, "r") as file:
        config = json.load(file)
        
    print("[b blue]MENU[/b blue]\n\n"
    "[1][i] Check password\n[/i]"
    "[2][i] Settings\n[/i]"
    "[3][i] History\n[/i]"
    "[4][i] Quit[/i]")
    answer = input()

    match answer:
        case "1":
            check_password()
        case "2":
            settings()
        case "3":
            history()
        case "4":
            sys.exit()
        case _:
            error()

@new_screen
def check_password():
    print("[i]Write here your password:[/i]\n")
    password = input()
    
    memory_res = memory.search_password(password)

    subprocess.run("cls", shell=True)

    if not memory_res:
        res = subprocess.run(
            "password_checker\\target\\debug\\password_checker.exe",
            shell=True, # shell - запуск cmd.exe
            input=password.strip(), # input - stdin
            capture_output=True, # capture_output - ловит потоки вывода (stdout и stderr)
            text=True, # Указание, чтобы обработать потоки stdin и stdout как обычный текст
            encoding="cp866") # расшифровка текста (для stderr)

        if res.stderr:
            print(f"[red][b]An error occurred :/[/b]\n\n[i]Error[/i] => [/red]{res.stderr.strip()}")
            input()
            return None
        else:
            result = (res.stdout).strip().split("\n")
            result = {x[0]: int(x[1]) if x[1].isdigit() else (x[1] == "true") for x in [i.split(":") for i in result]}
            
            word, points = password_evaluation(result)
            if config["enable_hostory"]:
                memory.add_password_in_history(password, word, points)     
    else:
        word = memory_res[0]
        points = memory_res[1]

    print(f"The strength of your password [b i]{password}[/b i] was rated as: [b]{word}[/b]\n\n"
          f"[green]Points[/green]: [b]{points}/100[/b]")

    print("[i]Press Enter to continue...[/i]")
    input()

@new_screen
def settings():

    print(f"[b blue]SETTINGS[/b blue]\n\n"
          "[1][i] Clear history\n[/i]"
          f"[2][i] History: {config["enable_hostory"]}\n[/i]"
          "[3][i] Back[/i]")
    
    set_answer = input()
    match set_answer:
        case "1":
            memory.clear_history()
            input()
        case "2":
            config["enable_hostory"] = not config["enable_hostory"]
            with open(config_path, "w") as file:
                json.dump(config, file, indent=4)
        case _:
            return None

@new_screen
def history():
    memory.show_history()
    input()

@new_screen
def error():
    print("[b red]ERROR[/b red]")
    input()



if __name__ == "__main__":
    while True:
        main()