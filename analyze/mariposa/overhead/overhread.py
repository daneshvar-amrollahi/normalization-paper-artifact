#!/usr/bin/env python3
import argparse
import polars as pl

def calculate_overhead(csv_files):
    # Initialize counters for total times
    total_norm_time = 0
    total_solving_time = 0
    total_benchmarks = 0
    
    # Process each CSV file
    for csv_file in csv_files:
        print(f"\nProcessing file: {csv_file}")
        
        # Read the CSV file
        df = pl.read_csv(csv_file)
        
        # Filter out benchmarks with status "to" if that column exists
        # if 'status' in df.columns:
        #     df = df.filter(pl.col('status') != 'to')
        
        file_benchmarks = len(df)
        print(f'Number of benchmarks in file: {file_benchmarks}')
        total_benchmarks += file_benchmarks
        
        # Add to total times
        file_norm_time = df['norm_time'].sum()
        file_solving_time = df['total_time'].sum()
        
        total_norm_time += file_norm_time
        total_solving_time += file_solving_time
        
        print(f"File normalization time: {file_norm_time:.6f} seconds")
        print(f"File solving time: {file_solving_time:.6f} seconds")
        if file_norm_time + file_solving_time > 0:
            file_overhead = file_norm_time / (file_norm_time + file_solving_time)
            print(f"File overhead: {file_overhead:.6f}")
    
    # Calculate the overall overhead
    overall_overhead = total_norm_time / (total_norm_time + total_solving_time)
    
    # Print aggregate results
    print("\n=== AGGREGATE RESULTS ===")
    print(f"Total benchmarks processed: {total_benchmarks}")
    print(f"Total normalization time: {total_norm_time:.6f} seconds")
    print(f"Total solving time: {total_solving_time:.6f} seconds")
    print(f"Overall overhead: {overall_overhead:.6f}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('csv_files', nargs='+', help='Path to one or more CSV files with benchmark data')
    args = ap.parse_args()
    
    calculate_overhead(args.csv_files)

if __name__ == '__main__':
    main()