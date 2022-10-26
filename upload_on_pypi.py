import os

# Remove old versions
if os.path.isdir("dist"):
    for file in os.listdir("dist"):
        os.remove("dist/" + file)

# Build and send package

script = [
    "python3 -m pip install --upgrade build",
    "python3 -m build",
    "python3 -m pip install --upgrade twine",
    "python3 -m twine upload dist/*"
]

accept = ["", "yes", "y", "ye", "yeah", "yep", "oui", "ouai", "ouaip"]

for command in script:
    select = input(f"Do you want to execute the following command? [Y/n]\n{command}\n")
    if select.lower() in accept:
        os.system(command)
    else:
        exit(0)