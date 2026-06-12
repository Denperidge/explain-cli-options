from sys import path, argv
path.append("../")
from eco import run
from testutils import more_found

ENCODING = "utf-8"

if __name__ == "__main__":
    # Prep template
    with open("template.README.md", mode="r", encoding=ENCODING) as file:
        template = file.read()
    
    # Get minimum python version
    vermin_out = run("uv run vermin ../eco.py").split("\n")
    version = list(filter(lambda line: line.startswith("Minimum"), vermin_out))[0]
    version = version.replace("versions", "Python version")

    # Get example output from eco
    usage = ""
    usage_examples = ["rsync -rlptgoD --progress", "cargo add --dev"]
    for example in usage_examples:
        usage += "$ eco " + example + "\n"
        usage += run("../eco.py " + example).replace(more_found("", example, True), "")
        usage += "\n"

    # Replace vermin, example usage & help in template
    out = template\
        .replace("{vermin}", version)\
        .replace("{help}", run("../eco.py ++help"))\
        .replace("{usage}", usage.rstrip())
    
    # Write README.md
    with open("../README.md", mode="w", encoding=ENCODING) as file:
        file.write(out)
