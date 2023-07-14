import json
import os
import glob
import time
import sys
from utils import *
from datetime import datetime



notebooks_file = sys.argv[1]
output_dir = sys.argv[2]

LOG_FOLDER = sys.argv[3]
mkdirs(LOG_FOLDER)
current_time = datetime.now().strftime("%y%m%d-%H%M%S")
LOG_FILE = open(f"{LOG_FOLDER}/execorder_{current_time}.log", 'w', buffering=512)

def load_notebook(notebook_path):
    try:
        with open(notebook_path, 'r') as file:
            notebook = json.load(file)
            return notebook
    except e:
        raise e

def get_execution_order(notebook):
        execution_order = {}
        i = 0
        MAXINT = sys.maxsize
        cells = notebook['cells']
        total_unordered = len([1 for cell in cells if cell["cell_type"] == "code" and cell['execution_count'] is None])
        for cell in cells:
            if cell["cell_type"] == "code" and 'execution_count' in cell:
                
                if all([not line or line.isspace() for line in cell['source']]):
                    continue

                execution_count = cell['execution_count']
                if execution_count is not None:
                    execution_order[execution_count] = cell
                else:
                    execution_order[f'unordered_{MAXINT-total_unordered+i}'] = cell
                    i+=1
                

        return execution_order

def create_ordered_notebook(original_notebook, ordered_notebook_path, execution_order):

    ordered_notebook = {
        'metadata': original_notebook['metadata'],
        'nbformat': original_notebook['nbformat'],
        'nbformat_minor': original_notebook['nbformat_minor'],
        'cells': []
    }

    execution_order_integer = {k if 'unordered' not in str(k) else int(k[10:]):v for k,v in execution_order.items()}
    for execution_count in sorted(execution_order_integer.keys()):
        source = execution_order_integer[execution_count]['source']
        # Find the original cell with the matching execution count
        original_cell = execution_order_integer[execution_count]
        # print(f"original cell = {original_cell}")
        if original_cell:
            # Create a new cell with the original metadata and updated source code
            cell = original_cell.copy()
            cell['source'] = source
            cell['outputs'] = []
            cell['execution_count'] = execution_count
            ordered_notebook['cells'].append(cell)

    with open(ordered_notebook_path, 'w') as file:
        json.dump(ordered_notebook, file)
    
    return True

def no_execution_order(ls):
    return all('unordered' in str(v) for v in ls)

def some_execution_order(ls):
    return any('unordered' in str(v) for v in ls) 

def is_sorted(lst):
    return all(lst[i] <= lst[i+1] for i in range(len(lst)-1))

# Specify the path to your IPython Notebook file
# notebooks_dir = sys.argv[1]
# notebooks = glob.glob(os.path.join(notebooks_dir,"*.ipynb"))


with open(notebooks_file, "r") as f:
    notebooks = list(map(lambda filename: f"/var/waris_backups/notebooks/{filename}", filter(lambda s: s, f.read().split("\n"))))

TOTAL = len(notebooks)
for i, notebook_path in enumerate(notebooks):
    print(f"[Analyzing {i}/{TOTAL}] {notebook_path}")
    basename = os.path.basename(notebook_path)

    try:
        notebook = load_notebook(notebook_path)
    except: 
        logln(f"{notebook_path},FAILED_TO_PARSE", LOG_FILE) 
        continue

    try:
        execution_order = get_execution_order(notebook)
        print(f'Execution Order: {execution_order.keys()}')

        out_file = os.path.join(output_dir, basename)

        if no_execution_order(execution_order.keys()):
            create_ordered_notebook(notebook, out_file, execution_order)
            logln(f"{notebook_path},NO_ORDER", LOG_FILE) 
        elif some_execution_order(execution_order.keys()):
            create_ordered_notebook(notebook, out_file, execution_order)
            logln(f"{notebook_path},PARTIAL_ORDER", LOG_FILE) 
        else:
            logln(f"{notebook_path},TOTAL_ORDER", LOG_FILE)
            create_ordered_notebook(notebook, out_file, execution_order)
    except Exception as e:
        print(e)
        logln(f"{notebook_path},UNKOWN_ERROR={e}", LOG_FILE)


LOG_FILE.close()