import subprocess
from rich import print





title_text = """
=============================
      [green]Password analyzer[/green]    
=============================

    """





# Декораторы:
def new_screen(func):
    def wrapper(*args, **kwargs):
        subprocess.run("cls", shell=True)
        print(f"[b]{title_text}[/b]")
        res = func(*args, **kwargs)
        return res
    return wrapper



#Функции:
def made_options_list(title: str, title_color: str, options: tuple):
        print(f"[b {title_color}]{title}[/b {title_color}]\n")
        for num in range(len(options)):
            print(f"[{num+1}][i] {options[num]}[/i]")



@new_screen
def error(exception=""):
    print("[b red]ERROR[/b red]")
    if exception:
         print(f"\n[i red]{exception}[/i red]\n")
    print("[i grey35]Press Enter to continue...[/i grey35]")
    input()