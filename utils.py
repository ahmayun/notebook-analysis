
import argparse
import os

def logln(logstr, log_file):
    log_file.write(f"{logstr}\n")

def log(logstr, log_file):
    log_file.write(f"{logstr}")


def list_full_paths(directory):
    file_paths = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_paths.append(file_path)
    return file_paths


def parse_args(args):
    parser = argparse.ArgumentParser(description='Argument Parser')
    parser.add_argument('--directory', type=str, help='Directory path')
    parser.add_argument('--limit', type=int, help='Limit value')
    parser.add_argument('--random', action='store_true', help='Random flag')
    parser.add_argument('--outdir', type=str, help='output directory')
    
    parsed_args = parser.parse_args(args)
    return parsed_args

def mkdirs(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    except:
        raise