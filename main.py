import sys
import subprocess
import json
from random import choices, randint, sample
from rich import print
from pathlib import Path
from Checker import password_evaluation
import History as memory
from Global_func import new_screen, made_options_list, error





config_path = Path("json_files/config.json")

if not memory.h_path.exists():
    memory.h_path.write_text(json.dumps(memory.clear_json))





# Функции:
@new_screen
def main():
    global config
    with open(config_path, "r") as file:
        config = json.load(file)

    made_options_list("MENU", "blue", ("Check password", "Generate password", "Settings", "History", "Quit"))
    answer = input()

    match answer:
        case "1":
            check_password()
        case "2":
            password_generator()
        case "3":
            settings()
        case "4":
            history()
        case "5":
            sys.exit()
        case _:
            error()



@new_screen
def check_password():
    print("[i]Write here your password:[/i]\n")
    password = input()
    
    subprocess.run("cls", shell=True)

    memory_res = memory.search_password(password)
    if not memory_res:
        res = subprocess.run(
            "password_checker\\target\\debug\\password_checker.exe",
            shell=True, # shell - запуск cmd.exe
            input=password.strip(), # input - stdin
            capture_output=True, # capture_output - ловит потоки вывода (stdout и stderr)
            text=True, # Указание, чтобы обработать потоки stdin и stdout как обычный текст
            encoding="utf-8") # расшифровка текста (для stderr)

        if res.stderr:
            #print(f"[red][b]An error occurred :/[/b]\n\n[i]Error[/i] => [/red]{res.stderr.strip()}")
            error(res.stderr.strip())
            return
        else:
            result = (res.stdout).strip().split("\n")
            result = {x[0]: int(x[1]) if x[1].isdigit() else (x[1] == "true") for x in [i.split(":") for i in result]}
            result["password"] = password

            password_problems = [config["recomendations"][x.upper()] for x, y in result.items() if isinstance(y, bool) and y == False]
            
            word, points = password_evaluation(result)
            if config["enable_history"]:
                memory.add_password_in_history(password, word, points, password_problems)
    else:
        word = memory_res[0]
        points = memory_res[1]
        password_problems = memory_res[2]

    word_clr = config["word_color"][word]

    print(f"The strength of your password [b i cyan]{password}[/b i cyan] was rated as: [b {word_clr}]{word}[/b {word_clr}]\n\n"
          f"[b bright_blue]Points[/b bright_blue]: [i]{points}/100[/i]\n")
    if password_problems:
        print(f"[b orange_red1]Password recommendations:[/b orange_red1]\n[i grey35] - {"\n - ".join(password_problems)}[/i grey35]\n")

    print("[i grey35]Press Enter to continue...[/i grey35]")
    input()



@new_screen
def password_generator():
    generated_passwords = []
    
    print("[i]How many passwords do you need?[/i]")
    try:
        how_many = int(input())
    except Exception as e:
        error(e)
        return
    if how_many > 25:
        how_many = 25
    for i in range(how_many):
        password = "".join(["".join(choices(x, k=randint(10,20))) for x in config["symbols"].values()])
        password = "".join(sample(password, len(password)))
        generated_passwords.append(password)
    made_options_list("\nGenerated passwords:", "blue", tuple(generated_passwords))
    print("[i grey35]Press Enter to continue...[/i grey35]")
    input()



@new_screen
def settings():
    made_options_list("SETTINGS", "blue", ("Clear history", f"History: {config["enable_history"]}", "Back"))
    set_answer = input()

    match set_answer:
        case "1":
            memory.clear_history()
            input()
        case "2":
            config["enable_history"] = not config["enable_history"]
            with open(config_path, "w") as file:
                json.dump(config, file, indent=4)
        case _:
            error()



@new_screen
def history():
    memory.show_history()
    input()






if __name__ == "__main__":
    while True:
        main()