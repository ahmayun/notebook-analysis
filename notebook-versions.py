import json
import os
import glob
import time
import sys

def get_notebook_version(notebook_path):
    with open(notebook_path, 'r') as file:
        try:
            notebook = json.load(file)
        except:
            print(f"[PARSING FAILED] {notebook_path}")
            return "PARSING_FAILED"

        if 'nbformat' in notebook:
            nbformat = notebook['nbformat']
            return nbformat

    print(f"[NO FIELD nbformat] {notebook_path}")
    return "NO_FIELD_NBFORMAT"


# notebooks_dir = sys.argv[1]
# notebooks = glob.glob(os.path.join(notebooks_dir,"*.ipynb"))

notebooks_file = sys.argv[1]
with open(notebooks_file, "r") as f:
    notebooks = list(map(lambda filename: f"/var/waris_backups/notebooks/{filename}", filter(lambda s: s, f.read().split("\n"))))



version_counts = {}
file_to_version = {}
TOTAL = len(notebooks)
for i, notebook_path in enumerate(notebooks):
    print(f"[Analyzing {i}/{TOTAL}] {notebook_path}")

    ver = get_notebook_version(notebook_path)
    print(f"[Version] {ver}")
    if ver in version_counts:
        version_counts[ver] += 1 
    else: 
        version_counts[ver] = 1

    file_to_version[os.path.basename(notebook_path)] = ver


with open("ipynb_to_version.json", "w") as json_file:
    json.dump(file_to_version, json_file)

with open("version_stats.json", "w") as json_file:
    json.dump(version_counts, json_file)