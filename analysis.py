import sys
import os
import argparse
import random
from utils import *
import pandas as pd
import tqdm
from datetime import datetime
import nbformat
from nbconvert import PythonExporter
import concurrent.futures

random.seed("ahmad35")

LOG_FOLDER=".log"
mkdirs(LOG_FOLDER)
current_time = datetime.now().strftime("analysis_%y%m%d-%H%M%S")
LOG_FILE = open(f"{LOG_FOLDER}/{current_time}.log", 'w')


def ipynb_to_py_str(ipynb_file):
    try:
        with open(ipynb_file, 'r', encoding='utf-8') as nb_file:
            notebook = nbformat.read(nb_file, as_version=4)

        exporter = PythonExporter()
        script, _ = exporter.from_notebook_node(notebook)

        return script
        
    except:
        return None


def ipynb_to_py_file(src, destdir):
    name = os.path.splitext(os.path.basename(src))[0]
    contents = ipynb_to_py_str(src)
    
    if not contents:
        return None
    
    dest = os.path.join(destdir, f"{name}.py")

    with open(dest, 'w') as f:
        f.write(contents)

    return str(dest)
    
def ipynb_to_py(src, limit, pick_random, outdir):
    mkdirs(outdir)
    files = list_full_paths(src)
    worklist = files if not limit else random.sample(files, limit) if pick_random else files[:limit]
    for f in tqdm.tqdm(worklist):
        dest = ipynb_to_py_file(f, outdir)
        logln(f"{src} --> {dest}", LOG_FILE)
        
    # max_threads = 16
    # with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
    #     futures = [executor.submit(ipynb_to_py_file, f, outdir) for f in worklist]
    #     with tqdm.tqdm(total=len(futures)) as pbar:
    #         for future in concurrent.futures.as_completed(futures):
    #             pbar.update(1)
    #             dest = future.result()
    #             logln(f"{src} --> {dest}", LOG_FILE)


def main(args):
    parsed_args = parse_args(args[1:])
    directory = parsed_args.directory
    limit = parsed_args.limit
    pick_random = parsed_args.random
    outdir = parsed_args.outdir

    ipynb_to_py(directory, limit, pick_random, outdir)

    

if __name__ == "__main__":
    main(sys.argv)

LOG_FILE.close()