import subprocess
from rich import print

title_text = """
=============================
      [green]Password analyzer[/green]    
=============================

    """

# Декораторы:
def new_screen(func: function) -> function:
    def wrapper(*args, **kwargs):
        subprocess.run("cls", shell=True)
        print(f"[b]{title_text}[/b]")
        res = func(*args, **kwargs)
        return res
    return wrapper