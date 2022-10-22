import os

os.system("python3 -m pip install --upgrade build")
os.system("python3 -m build -s")
os.system("python3 -m pip install --upgrade twine")
os.system("python3 -m twine upload dist/*")