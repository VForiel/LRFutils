import os

# Remove old versions
if os.path.isdir("dist"):
    for file in os.listdir("dist"):
        os.remove("dist/" + file)

# Build and send package
os.system("python3 -m pip install --upgrade build")
os.system("python3 -m build -s")
os.system("python3 -m pip install --upgrade twine")
os.system("python3 -m twine upload dist/*")