import sys
import argparse
import random
import tqdm
from datetime import datetime
from utils import *
from pylint.lint import Run
from pylint.reporters import CollectingReporter


LOG_FOLDER=".log"
mkdirs(LOG_FOLDER)
current_time = datetime.now().strftime("linter_%y%m%d-%H%M%S")
LOG_FILE = open(f"{LOG_FOLDER}/{current_time}.log", 'w')

def run_linter_single(pyfile):
    reporter = CollectingReporter()
    result = Run(["--ignored-modules=*", "--additional-builtins=get_ipython", "--disable=R,C,W,import-error",  pyfile], reporter=reporter, exit=False)
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

def run_linter(srcdir, limit, pick_random, outdir):
    files = list_full_paths(srcdir)
    worklist = files if not limit else random.sample(files, limit) if pick_random else files[:limit]
    for f in tqdm.tqdm(worklist):
        num_errs = run_linter_single(f)
        logln(f"{f},{num_errs}", LOG_FILE)
    

def main(args):
    parsed_args = parse_args(args[1:])
    directory = parsed_args.directory
    limit = parsed_args.limit
    pick_random = parsed_args.random
    outdir = parsed_args.outdir

    run_linter(directory, limit, pick_random, outdir)

    

if __name__ == "__main__":
    main(sys.argv)

LOG_FILE.close()