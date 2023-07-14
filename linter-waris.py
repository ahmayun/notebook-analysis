import glob
import sys
import os
from functools import partial
from joblib import Parallel, delayed
import subprocess
from datetime import datetime
from utils import *

LOG_FOLDER=".log"
mkdirs(LOG_FOLDER)
current_time = datetime.now().strftime("%y%m%d-%H%M%S")
LOG_FILE = open(f"{LOG_FOLDER}/wlinter_{current_time}.log", 'w', buffering=512)

def run_pylint(output_dir, filename):
    command = f"pylint --ignored-modules=* --additional-builtins=get_ipython, --disable=R,C,W,import-error,function-redefined {filename}"
    output_file = os.path.join(output_dir, os.path.basename(filename))
    
    with open(output_file, 'w') as file:
        result = subprocess.run(command, shell=True, stdout=file)
    
    logln(f"{filename},{result.returncode}", LOG_FILE) 
  


if __name__ == """__main__""":

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    
    ipynbs = glob.glob(input_dir+"*.py")
    
    assert len(ipynbs) > 0, "No ipynb files found in input directory"
     
    partial_func = partial(run_pylint, output_dir)
    Parallel(n_jobs=14)(delayed(partial_func)(ipynb) for ipynb in ipynbs)
    # print(">> Conversion complete")


LOG_FILE.close()