#
# picasso.py
# MIT License
#
# a script to automagically edit .picasso files
# made by circular
#
# https://github.com/circularsprojects
# https://circulars.dev
#

import argparse
import zipfile
import platform
import os

if platform.system() != "Linux" and platform.system() != "Darwin":
    print("Error: this script is only compatible with Linux and MacOS")
    exit(-1)

parser = argparse.ArgumentParser(description='A script to automagically edit .picasso files')
parser.add_argument('file', metavar='file', type=str, nargs='+',
                    help='the file to edit')
args = parser.parse_args()

file = args.file[0]
if file[-8:] != ".picasso":
    print("Error: file must be a .picasso file")
    exit(-1)

files = []
with zipfile.ZipFile(file, 'r') as zip_ref:
    files = zip_ref.namelist()
    prefs = False
    settings = False
    info = False
    for i in range(len(zip_ref.namelist())):
        name = zip_ref.namelist()[i].split("/")
        if (name[1] == "prefs.json"):
            prefs = True
        if (name[1] == "tweak.json"):
            settings = True
        if (name[1] == "info.json"):
            info = True
    if (not prefs or not settings or not info):
        print("Error: malformed .picasso file")
        print(f"prefs.json: {'exists' if prefs else 'does not exist!'}")
        print(f"tweak.json: {'exists' if settings else 'does not exist!'}")
        print(f"info.json: {'exists' if info else 'does not exist!'}")
        exit(-1)
    zip_ref.extractall("/tmp/cpicasso")

# list all files
# for i in range(len(zip_ref.namelist())):
#     print(str(i) + ": " + zip_ref.namelist()[i])
print("Available actions:")
print("1: Edit prefs.json")
print("2: Edit tweak.json")
print("3: Edit info.json")
print("4: List files")
print("5: Extract here")
choice = input("Enter your choice: ")

# rezip
with zipfile.ZipFile(file, 'w') as zip_ref:
    for i in range(len(files)):
        name = files[i].split("/")
        zip_ref.write(f"/tmp/cpicasso/{files[i]}", '/'.join(name[1:]))
    