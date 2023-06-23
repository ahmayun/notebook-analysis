import sys
import os
import argparse
import random
import pandas as pd
import tqdm
from datetime import datetime
import nbformat
from nbconvert import PythonExporter
from pylint.lint import Run
from pylint.reporters import CollectingReporter
import concurrent.futures

random.seed("ahmad35")

def mkdirs(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    except:
        raise

DEFAULT_LOG_FOLDER=".log"
mkdirs(DEFAULT_LOG_FOLDER)
current_time = datetime.now().strftime("%y%m%d-%H%M%S")
DEFAULT_LOG_FILE=open(f"{DEFAULT_LOG_FOLDER}/{current_time}.log", 'w')

def logln(logstr, log_file=DEFAULT_LOG_FILE):
    log_file.write(f"{logstr}\n")

def log(logstr, log_file=DEFAULT_LOG_FILE):
    log_file.write(f"{logstr}")


def parse_args(args):
    parser = argparse.ArgumentParser(description='Argument Parser')
    parser.add_argument('--directory', type=str, help='Directory path')
    parser.add_argument('--limit', type=int, help='Limit value')
    parser.add_argument('--random', action='store_true', help='Random flag')
    parser.add_argument('--outdir', type=str, help='output directory')
    
    parsed_args = parser.parse_args(args)
    return parsed_args

def create_dataframe(file_paths, map_func):
    file_contents = map(map_func, file_paths)
    df = pd.DataFrame({'File Path': file_paths, 'File Contents': file_contents})
    return df

def list_full_paths(directory):
    file_paths = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_paths.append(file_path)
    return file_paths


def ipynb_to_py_str(ipynb_file):
    try:
        with open(ipynb_file, 'r', encoding='utf-8') as nb_file:
            notebook = nbformat.read(nb_file, as_version=4)

        exporter = PythonExporter()
        script, _ = exporter.from_notebook_node(notebook)

        return script
        
    except:
        return None

def has_magics(pycode):
    return False

def valid_pyfile(pycode):
    return (
        not has_magics(pycode) and
        True
    )

def ipynb_to_py_file(src, destdir):
    name = os.path.splitext(os.path.basename(src))[0]
    contents = ipynb_to_py_str(src)
    
    if not contents:
        return None
    
    dest = os.path.join(destdir, f"{name}.py")

    with open(dest, 'w') as f:
        f.write(contents)

    return str(dest)

def run_static_analysis(pyfile):
    reporter = CollectingReporter()
    result = Run(["--ignored-modules=*", "--additional-builtins=get_ipython", "--disable=R,C,W,import-error",  pyfile], reporter=reporter, exit=False)
    for m in reporter.messages:
        if m.category != 'error':
            print(m)
    return len(reporter.messages)
    """
    Message(
        msg_id='E0602', 
        symbol='undefined-variable', 
        msg="Undefined variable 'N_TRAIN_BATCHES'", 
        C='E', 
        ctegory='error', 
        confidence=Confidence(name='UNDEFINED', description='Warning without any associated confidence level.'), 
        abspath='/home/student/notebooks-ahmad/temp/0000a9bfb38582c1a3ce59d7bdb6cb2d1e19bfc1.py', 
        path='temp/0000a9bfb38582c1a3ce59d7bdb6cb2d1e19bfc1.py', 
        module='0000a9bfb38582c1a3ce59d7bdb6cb2d1e19bfc1', 
        obj='', 
        line=241, 
        column=18, 
        end_line=241, 
        end_column=33
        )
    """
    
def ipynb_to_py(src, limit, pick_random, outdir):
    mkdirs(os.path.join(outdir, "invalid"))
    files = list_full_paths(src)
    done = 0
    worklist = files if not limit else random.sample(files, limit) if pick_random else files[:limit]
    max_threads = 4
    for f in tqdm.tqdm(worklist):
        pyfile = ipynb_to_py_file(f, outdir)
        done += 1
        if done == 10000:

            done = 0
        # if pyfile:
        #     num_errors = run_static_analysis(pyfile)
        #     logln(f"{f} --> {pyfile},{num_errors}")



def main(args):
    parsed_args = parse_args(args[1:])
    directory = parsed_args.directory
    limit = parsed_args.limit
    pick_random = parsed_args.random
    outdir = parsed_args.outdir

    ipynb_to_py(directory, limit, pick_random, outdir)

    

if __name__ == "__main__":
    main(sys.argv)

DEFAULT_LOG_FILE.close()