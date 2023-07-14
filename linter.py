import sys
import argparse
import random
import tqdm
from datetime import datetime
from utils import *
from pylint.lint import Run
from pylint.reporters import CollectingReporter
import subprocess
from functools import partial
from joblib import Parallel, delayed

LOG_FOLDER=".log"
mkdirs(LOG_FOLDER)
current_time = datetime.now().strftime("%y%m%d-%H%M%S")
LOG_FILE = open(f"{LOG_FOLDER}/linter_{current_time}.log", 'w', buffering=512)


# def run_linter_single(pyfile):
#     reporter = CollectingReporter()
#     result = Run(["--ignored-modules=*", "--additional-builtins=get_ipython", "--disable=R,C,W,import-error,function-redefined",  pyfile], reporter=reporter, exit=False)
#     num_errs = len(reporter.messages)
#     msg_strs = list(map(lambda m: str(m), reporter.messages))
#     return num_errs, "\n".join(msg_strs)

# def run_linter_single(filename):
#     command = f"pylint --ignored-modules=* --additional-builtins=get_ipython, --disable=R,C,W,import-error,function-redefined {filename}"
#     result = subprocess.run(command, shell=True, capture_output=True, text=True)
#     output = result.stdout.strip()
#     return result.returncode, output



# def run_linter(srcdir, limit, pick_random, outdir, skip_first):
#     files = list_full_paths(srcdir)
#     worklist = files if not limit else random.sample(files, limit) if pick_random else files[:limit]
#     worklist = worklist[skip_first:]
#     pbar = tqdm.tqdm(worklist)
#     for f in pbar:
#         pbar.set_description(f)
#         num_errs, stdout = run_linter_single(f)
#         logln(f"{f},{num_errs}", LOG_FILE)
#         filename = os.path.basename(f)
#         with open(f"{outdir}/{filename}.output", "w") as stdoutfile:
#             stdoutfile.write(stdout)

def run_linter_single(outdir, filename):
    basename = os.path.basename(filename)
    outpath = os.path.join(outdir,basename)
    command = f"pylint --ignored-modules=* --additional-builtins=get_ipython, --disable=R,C,W,import-error,function-redefined {filename} --output-format=json:{outpath}.json"
    subprocess.run(command, shell=True)
    # output = result.stdout.strip()
    # return result.returncode, output

def run_linter(srcdir, limit, pick_random, outdir, skip_first):
    files = list_full_paths(srcdir)
    worklist = files if not limit else random.sample(files, limit) if pick_random else files[:limit]
    worklist = worklist[skip_first:]
    
    def process_file(f):
        pass
        # pbar.set_description(f)
        # num_errs, stdout = run_linter_single(f)
        # print(f"{f},{num_errs}")
        # filename = os.path.basename(f)
        # with open(f"{outdir}/{filename}.output", "w") as stdoutfile:
        #     stdoutfile.write(stdout)
    
    partial_func = partial(run_linter_single, outdir)
    Parallel(n_jobs=14)(delayed(partial_func)(f) for f in worklist)
    

def main(args):
    parsed_args = parse_args(args[1:])
    directory = parsed_args.directory
    limit = parsed_args.limit
    pick_random = parsed_args.random
    outdir = parsed_args.outdir
    skip_first = parsed_args.skip
    mkdirs(outdir)

    run_linter(directory, limit, pick_random, outdir, skip_first)

    

if __name__ == "__main__":
    main(sys.argv)


LOG_FILE.close()
