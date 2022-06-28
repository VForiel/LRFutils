import datetime
import os
import git

number = None

def next_number(path):
    global number
    max_num = 0
    for file in os.listdir(path):
        if "_" in file: file = file.split("_")[0]
        try:
            if int(file) > max_num: max_num = int(file)
        except: pass
    number = max_num + 1
    return number

def new(name = None):
    global number

    timestamp = str(datetime.datetime.now()).split(" ")

    try:
        repo = git.Repo(search_parent_directories=True)
        sha  = "_" + repo.head.object.hexsha[:7]
    except: sha = ""

    path = "./archives/" + timestamp[0] + sha

    if not os.path.isdir(path): os.makedirs(path)

    if path is not None: next_number(path)
    else: number = 1

    if name is not None: name = "_" + name

    if not os.path.isdir(f"{path}/{number}{name}"): os.makedirs(f"{path}/{number}{name}")


    return f"{path}/{number}{name}"

def description(**kwargs):
    desc = ""
    for key,value in kwargs.items():
        if type(value) in [int, str, float, bool] : desc += f",{key}={value}"
        else: print(f"⚠️ Your archive description contain a non-supported type: {type(value)}")
    return desc[1:]
