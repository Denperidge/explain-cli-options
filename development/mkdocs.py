from subprocess import run
from sys import path
path.append("../")
from eco import get_help

ENCODING = "utf-8"

if __name__ == "__main__":
    with open("template.README.md", mode="r", encoding=ENCODING) as file:
        template = file.read()
    
    vermin_proc = run("vermin ../eco.py", capture_output=True, shell=True, encoding=ENCODING)
    if vermin_proc.returncode != 0:
        raise Exception(vermin_proc.stderr)
    vermin_out = vermin_proc.stdout.split("\n")
    version = list(filter(lambda line: line.startswith("Minimum"), vermin_out))[0]
    version = version.replace("versions", "Python version")

    out = template\
        .replace("{vermin}", version)\
        .replace("{help}", "\n".join(get_help("../eco.py")))
    
    with open("../README.md", mode="w", encoding=ENCODING) as file:
        file.write(out)
