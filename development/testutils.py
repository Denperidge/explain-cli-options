from subprocess import run
def eco(command: str):
    out = run("../eco.py " + command, shell=True, encoding="utf-8", capture_output=True)
    if out.returncode != 0:
        raise Exception(out.stderr)
    return out.stdout

# man --all passwd | cat