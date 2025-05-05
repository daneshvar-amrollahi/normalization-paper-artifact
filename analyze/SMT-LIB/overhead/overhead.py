#!/usr/env/bin python3

import argparse
import polars as pl

def calculate_overhead(csv_file, benchmarks_file):
    # Read the CSV file
    df = pl.read_csv(csv_file)
    
    # Filter out benchmarks with status "to"
    # df = df.filter(pl.col('status') != 'to')
    
    # Read the remaining benchmarks from file
    benchmarks_remaining = set()
    with open(benchmarks_file, 'r') as infile:
        for line in infile:
            benchmarks_remaining.add(line.strip())
    
    print(f'Number of remaining benchmarks: {len(benchmarks_remaining)}')
    
    # Filter only benchmarks in the remaining set
    df = df.filter(pl.col('benchmark').is_in(benchmarks_remaining))
    
    print(f'Number of benchmarks after filtering: {len(df)}')
    
    # Calculate total normalization time and total solving time
    total_norm_time = df['norm_time'].sum()
    total_solving_time = df['total_time'].sum()
    
    # Calculate the overall overhead
    overall_overhead = total_norm_time / (total_norm_time + total_solving_time)
    
    # Print results
    print("\nOverall Normalization Time Overhead:")
    print(f"Total normalization time: {total_norm_time:.6f} seconds")
    print(f"Total solving time: {total_solving_time:.6f} seconds")
    print(f"Overall overhead: {overall_overhead:.6f}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('csv', help='Path to the CSV file with benchmark data')
    ap.add_argument('benchmarks', help='Path to the file with remaining benchmarks')
    args = ap.parse_args()
    
    calculate_overhead(args.csv, args.benchmarks)

if __name__ == '__main__':
    main()