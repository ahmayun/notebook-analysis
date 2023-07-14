import glob
import sys
import os
from functools import partial
from joblib import Parallel, delayed

def convert_ipynb_to_py(out_dir, filepath):
    # command = f"time prospector -W pep8 -W pep257 --with-tool vulture -8  -o json  >> result_{cmd_dir.split('/')[-1]}.json"
    # command = f"jupyter nbconvert --to python {filepath}"
    command = f'jupyter nbconvert --to script --output-dir={out_dir} {filepath}'

    print(f"{filepath}")
    os.system(command)
  


if __name__ == """__main__""":

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    
    ipynbs = glob.glob(input_dir+"*.ipynb")
    
    assert len(ipynbs) > 0, "No ipynb files found in input directory"
     
    partial_func = partial(convert_ipynb_to_py, output_dir)
    Parallel(n_jobs=14)(delayed(partial_func)(ipynb) for ipynb in ipynbs)
    # print(">> Conversion complete")