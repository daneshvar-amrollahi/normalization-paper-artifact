#!/usr/bin/env python3

import argparse
import csv
from collections import defaultdict, Counter
import os
import sys

def read_csv(file_path):
    """Read a CSV file and return its contents as a list of dictionaries."""
    data = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def parse_float(value):
    """Safely parse a float value, returning None if it can't be parsed."""
    try:
        if value is None or value == '':
            return None
        return float(value)
    except ValueError:
        return None

def gen_data(csv_file, benchmarks_remaining_path):
    # Read the CSV file
    data = read_csv(csv_file)
    
    # Load benchmarks_remaining
    benchmarks_remaining = set()
    try:
        with open(benchmarks_remaining_path, 'r') as infile:
            for line in infile:
                benchmarks_remaining.add(line.strip())
        print(f"Loaded {len(benchmarks_remaining)} benchmarks from benchmarks_remaining file")
    except FileNotFoundError:
        print(f"Error: Could not find benchmarks file: {benchmarks_remaining_path}")
        sys.exit(1)
    
    # Filter data to only include benchmarks in benchmarks_remaining
    filtered_data = [row for row in data if row['benchmark'] in benchmarks_remaining]
    
    # Get unique benchmarks
    unique_benchmarks = set(row['benchmark'] for row in filtered_data)
    
    print(f'Number of benchmarks: {len(filtered_data)}')
    print(f'Number of unique benchmarks: {len(unique_benchmarks)}')
    
    # Group data by benchmark
    benchmark_groups = defaultdict(list)
    for row in filtered_data:
        benchmark_groups[row['benchmark']].append(row)
    
    # Calculate statistics for all benchmarks combined
    unique_counts = []
    norm_times = []
    histogram = Counter()
    
    for benchmark, rows in benchmark_groups.items():
        # Count unique SHA256 sums
        unique_shas = set(row['sha256sum'] for row in rows)
        num_unique = len(unique_shas)
        
        # Update histogram
        histogram[num_unique] += 1
        
        # Store count of unique SHA256 sums
        unique_counts.append(num_unique)
        
        # Store norm_time values
        for row in rows:
            norm_time = parse_float(row['norm_time'])
            if norm_time is not None:
                norm_times.append(norm_time)
    
    # Calculate overall statistics
    avg_unique = sum(unique_counts) / len(unique_counts) if unique_counts else 0
    avg_norm_time = sum(norm_times) / len(norm_times) if norm_times else 0
    max_norm_time = max(norm_times) if norm_times else 0
    
    print("\n--- Overall Statistics ---")
    print(f"Average Unique Outputs: {avg_unique:.2f}")
    print(f"Average Norm Time: {avg_norm_time:.4f}")
    print(f"Maximum Norm Time: {max_norm_time:.4f}")
    
    print("\n--- Histogram of Unique Outputs ---")
    print("Number of Unique Outputs | Number of Benchmarks")
    print("-------------------------|--------------------")
    for i in range(1, 11):
        print(f"{i:25} | {histogram[i]}")
    
    # Return total histogram
    return dict(histogram)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('csv', help='Path to the CSV file containing benchmark results')
    ap.add_argument('benchmarks_file', help='Path to the benchmarks_remaining file')
    args = ap.parse_args()
    
    histogram = gen_data(args.csv, args.benchmarks_file)
    print("\nHistogram dictionary:")
    print(histogram)

if __name__ == '__main__':
    main()