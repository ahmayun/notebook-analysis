import sys
import argparse
import random
import tqdm
from datetime import datetime
from utils import *
from pylint.lint import Run
from pylint.reporters import CollectingReporter
import ast

LOG_FOLDER=".log"
mkdirs(LOG_FOLDER)
current_time = datetime.now().strftime("asserts_%y%m%d-%H%M%S")
LOG_FILE = open(f"{LOG_FOLDER}/assert_testfuncs{current_time}.log", 'w', buffering=512)

def compute_asserts_single(file_path):
    # Read the Python file
    with open(file_path, 'r') as file:
        source_code = file.read()

    # Parse the source code into an AST
    try:
        ast_tree = ast.parse(source_code)
    except:
        return True, None, None, None

    # Initialize counters
    test_functions_count = 0
    assert_keyword_count = 0
    has_unittest = False

    # Traverse the AST nodes
    for node in ast.walk(ast_tree):
        if isinstance(node, ast.FunctionDef):
            # Check if function name contains "test"
            if 'test' in node.name:
                test_functions_count += 1
        if isinstance(node, ast.Assert):
            # Count occurrences of the "assert" keyword
            assert_keyword_count += 1
        if isinstance(node, ast.Import):
            if "unittest" in node.names:
                has_unittest = True
        if isinstance(node, ast.ImportFrom):
            if not node.module:
                has_unittest = False
            elif "unittest" in node.module:
                has_unittest = True

    # Return the counts
    return False, test_functions_count, assert_keyword_count, has_unittest

def compute_asserts(srcdir, limit, pick_random, outdir):
    files = list_full_paths(srcdir)
    worklist = files if not limit else random.sample(files, limit) if pick_random else files[:limit]
    pbar = tqdm.tqdm(worklist)
    for f in pbar:
        fail, num_tests, num_asserts, has_unittest = compute_asserts_single(f)
        if fail:
            logln(f"PARSE ERROR: {f}", LOG_FILE)
        else:
            logln(f"{f},{num_tests},{num_asserts},{has_unittest}", LOG_FILE)
        

def main(args):
    parsed_args = parse_args(args[1:])
    directory = parsed_args.directory
    limit = parsed_args.limit
    pick_random = parsed_args.random
    outdir = parsed_args.outdir

    compute_asserts(directory, limit, pick_random, outdir)

    

if __name__ == "__main__":
    main(sys.argv)

LOG_FILE.close()