import os
import json
import matplotlib.pyplot as plt
from utils import *
import sys
from datetime import datetime

LOG_FOLDER = sys.argv[4]
mkdirs(LOG_FOLDER)
current_time = datetime.now().strftime("%y%m%d-%H%M%S")
LOG_FILE = open(f"{LOG_FOLDER}/errortypes_{current_time}.log", 'w', buffering=512)

def generate_barplot(files, exclusion_list, output_dir):
    # Dictionary to store error symbol counts
    error_counts = {}
    TOTAL = len(files)
    i = 0

    # Iterate over JSON files in the directory
    for file_path in files:
        i+=1
        print(f'[ANALYZING {i}/{TOTAL}] {file_path}')
        
        file_id = os.path.basename(file_path).split('.')[0]
        if file_id in exclusion_list:
            print("EXCLUDED_AS_PYTHON2")
            logln(f"{file_path},EXCLUDED_AS_PYTHON2", LOG_FILE) 
            continue

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except:
            print("PARSE_ERROR")
            logln(f"{file_path},FAILED_TO_PARSE", LOG_FILE) 
            continue

        symbols_list = []
        try:
            symbols_found = set()
            for error in data:
                symbol = error['symbol']
                symbols_list.append(symbol)
                if symbol not in symbols_found:
                    error_counts[symbol] = error_counts.get(symbol, 0) + 1
                    symbols_found.add(symbol)
        except Exception as e:
            logln(f"{file_path},UNKNOWN_ERROR={e}", LOG_FILE)
            continue 


        logln(f"{file_path},SYMBOLS={'|'.join(symbols_list)}", LOG_FILE) 

    # Extract error symbols and their corresponding counts
    # symbols = list(error_counts.keys())
    # counts = list(error_counts.values())

    symbols = sorted(error_counts, key=error_counts.get, reverse=True)
    counts = [error_counts[symbol] for symbol in symbols]
    # Create a bar chart
    plt.figure(figsize=(12, 6)) 
    plt.bar(symbols, counts, width=1, edgecolor='black')
    plt.xlabel('Error Symbol')
    plt.ylabel('Count')
    plt.title('Error Symbol Counts in JSON Files')
    plt.xticks(rotation=90)
    plt.yscale('log')
    plt.tight_layout()

    # Save the plot to a file
    output_file = os.path.join(output_dir, 'error_symbol_counts.png')
    plt.savefig(output_file)

    # output_file = os.path.join(output_dir, 'error_symbol_counts.svg')
    # plt.savefig(output_file, format='svg')

# Directory containing the JSON files
json_file_list_file = sys.argv[1]
output_dir = sys.argv[2]
exclusion_list_file = sys.argv[3]

with open(json_file_list_file, "r") as f:
    files_list = list(map(lambda x: x, filter(lambda s: s, f.read().split("\n"))))

exclusion_list = dict()
with open(exclusion_list_file, "r") as f:
    for file_id in filter(lambda s: s, f.read().split("\n")):
        exclusion_list[file_id] = True


generate_barplot(files_list, exclusion_list, output_dir)

LOG_FILE.close()