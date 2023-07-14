import csv
import matplotlib.pyplot as plt
import numpy as np

def create_num_tests_histogram(csv_file, output_directory, bucket_size, title=""):
    # Read the CSV file
    data = []
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)

    # Extract the values of num_tests
    print("\n".join([str(row) for row in data if int(row['num_tests']) > 50]))

    num_tests = [int(row['num_tests']) for row in data]
    zeroes = len(list(filter(lambda x: x == 0, num_tests)))
    print(f"# Zero tests: {zeroes}")
    print(f"Total notbooks: {len(num_tests)}")
    print(f"% Zero tests: {zeroes/len(num_tests)*100:.2f}")

    # Create and save the histogram for num_tests
    bins = range(0, max(num_tests) + bucket_size, bucket_size)
    plt.hist(num_tests, bins=bins)
    plt.xticks(np.arange(min(bins), max(bins), bucket_size))  # Set x-axis ticks as integers
    plt.title(title)
    plt.xlabel('num_tests')
    plt.ylabel('Frequency')
    plt.yscale('log')  # Set y-axis to logarithmic scale
    plt.tight_layout()
    plt.savefig(output_directory + '/num_tests_histogram.png')
    plt.close()

def create_num_asserts_histogram(csv_file, output_directory, bucket_size, title=""):
    # Read the CSV file
    data = []
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)

    # Extract the values of num_asserts
    num_asserts = [int(row['num_asserts']) for row in data]
    print("\n".join([str(row) for row in data if int(row['num_asserts']) > 70]))
    
    # count the number of rows with num_asserts == 0
    zeroes = len(list(filter(lambda x: x == 0, num_asserts)))
    print(f"# Zero asserts: {zeroes}")
    print(f"Total notbooks: {len(num_asserts)}")
    print(f"% Zero asserts: {zeroes/len(num_asserts)*100:.2f}")

    # Create and save the histogram for num_asserts
    bins = range(0, max(num_asserts) + bucket_size, bucket_size)
    plt.hist(num_asserts, bins=bins)
    plt.xticks(np.arange(min(bins), max(bins), bucket_size))  # Set x-axis ticks as integers
    plt.title(title)
    plt.xlabel('num_asserts')
    plt.ylabel('Frequency')
    plt.yscale('log')  # Set y-axis to logarithmic scale
    plt.tight_layout()
    plt.savefig(output_directory + '/num_asserts_histogram.png')
    plt.close()


# Example usage
csv_file = './final_results/final_tests_asserts_units.csv'
output_directory = './graphs'
create_num_tests_histogram(csv_file, output_directory, 2, "# of function names containing 'test' per notebook")
create_num_asserts_histogram(csv_file, output_directory, 10, "# of uses of 'assert' per notebook")