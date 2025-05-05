#!/usr/bin/env python3

import argparse
import csv
from enum import Enum
from collections import defaultdict, Counter
import math
import os

class Division(Enum):
    def __str__(self):
        return str(self.value)

    Arith = 'Arith'
    BitVec = 'BitVec'
    Equality_LinearArith = 'Equality+LinearArith'
    Equality_MachineArith = 'Equality+MachineArith'
    Equality_NonLinearArith = 'Equality+NonLinearArith'
    Equality = 'Equality'
    FPArith = 'FPArith'
    QF_Bitvec = 'QF_Bitvec'
    QF_Datatypes = 'QF_Datatypes'
    QF_Equality_Bitvec = 'QF_Equality+Bitvec'
    Equality_Bitvec = 'Equality+Bitvec'
    QF_Equality_LinearArith = 'QF_Equality+LinearArith'
    QF_Equality_NonLinearArith = 'QF_Equality+NonLinearArith'
    QF_Equality = 'QF_Equality'
    QF_FPArith = 'QF_FPArith'
    QF_LinearIntArith = 'QF_LinearIntArith'
    QF_LinearRealArith = 'QF_LinearRealArith'
    QF_NonLinearIntArith = 'QF_NonLinearIntArith'
    QF_NonLinearRealArith = 'QF_NonLinearRealArith'
    QF_Strings = 'QF_Strings'


divisions = {
    'ABV': Division.Equality_MachineArith,
    'ABVFP': Division.Equality_MachineArith,
    'ABVFPLRA': Division.Equality_MachineArith,
    'ALIA': Division.Equality_LinearArith,
    'AUFBV': Division.Equality_MachineArith,
    'AUFBVDTLIA': Division.Equality_MachineArith,
    'AUFBVDTNIA': Division.Equality_MachineArith,
    'AUFBVDTNIRA': Division.Equality_MachineArith,
    'QF_UFBVDT': Division.QF_Equality_Bitvec,
    'UFBVDT': Division.Equality_Bitvec,
    'AUFBVFP': Division.Equality_MachineArith,
    'AUFDTLIA': Division.Equality_LinearArith,
    'AUFDTLIRA': Division.Equality_LinearArith,
    'AUFDTNIRA': Division.Equality_NonLinearArith,
    'AUFFPDTNIRA': Division.Equality_NonLinearArith,
    'AUFLIA': Division.Equality_LinearArith,
    'AUFLIRA': Division.Equality_LinearArith,
    'AUFNIA': Division.Equality_NonLinearArith,
    'AUFNIRA': Division.Equality_NonLinearArith,
    'UFNIRA': Division.Equality_NonLinearArith,
    'BV': Division.BitVec,
    'BVFP': Division.FPArith,
    'BVFPLRA': Division.FPArith,
    'FP': Division.FPArith,
    'FPLRA': Division.FPArith,
    'LIA': Division.Arith,
    'LRA': Division.Arith,
    'NIA': Division.Arith,
    'NRA': Division.Arith,
    'QF_ABV': Division.QF_Equality_Bitvec,
    'QF_ABVFP': Division.QF_FPArith,
    'QF_ABVFPLRA': Division.QF_FPArith,
    'QF_ALIA': Division.QF_Equality_LinearArith,
    'QF_ANIA': Division.QF_Equality_NonLinearArith,
    'QF_AUFBV': Division.QF_Equality_Bitvec,
    'QF_AUFBVFP': Division.QF_FPArith,
    'QF_AUFLIA': Division.QF_Equality_LinearArith,
    'QF_AUFNIA': Division.QF_Equality_NonLinearArith,
    'QF_AX': Division.QF_Equality,
    'QF_BV': Division.QF_Bitvec,
    'QF_BVFP': Division.QF_FPArith,
    'QF_BVFPLRA': Division.QF_FPArith,
    'QF_DT': Division.QF_Datatypes,
    'QF_FP': Division.QF_FPArith,
    'QF_FPLRA': Division.QF_FPArith,
    'QF_IDL': Division.QF_LinearIntArith,
    'QF_LIA': Division.QF_LinearIntArith,
    'QF_LIRA': Division.QF_LinearIntArith,
    'QF_LRA': Division.QF_LinearRealArith,
    'QF_NIA': Division.QF_NonLinearIntArith,
    'QF_NIRA': Division.QF_NonLinearIntArith,
    'QF_NRA': Division.QF_NonLinearRealArith,
    'QF_RDL': Division.QF_LinearRealArith,
    'QF_S': Division.QF_Strings,
    'QF_SLIA': Division.QF_Strings,
    'QF_SNIA': Division.QF_Strings,
    'QF_UF': Division.QF_Equality,
    'QF_UFBV': Division.QF_Equality_Bitvec,
    'QF_UFDT': Division.QF_Datatypes,
    'QF_UFDTLIRA': Division.QF_Equality_LinearArith,
    'QF_UFFP': Division.QF_FPArith,
    'QF_UFFPDTNIRA': Division.QF_FPArith,
    'QF_UFIDL': Division.QF_LinearIntArith,
    'QF_UFLIA': Division.QF_Equality_LinearArith,
    'QF_UFLRA': Division.QF_Equality_LinearArith,
    'QF_UFNIA': Division.QF_Equality_NonLinearArith,
    'QF_UFNRA': Division.QF_Equality_NonLinearArith,
    'UF': Division.Equality,
    'UFBV': Division.Equality_MachineArith,
    'UFBVFP': Division.Equality_MachineArith,
    'UFBVLIA': Division.Equality_MachineArith,
    'UFDT': Division.Equality,
    'UFDTLIA': Division.Equality_LinearArith,
    'QF_UFDTLIA': Division.QF_Equality_LinearArith,
    'QF_UFDTNIA': Division.QF_Equality_NonLinearArith,
    'UFDTLIRA': Division.Equality_LinearArith,
    'ANIA': Division.Equality_NonLinearArith,
    'UFDTNIA': Division.Equality_NonLinearArith,
    'UFDTNIRA': Division.Equality_NonLinearArith,
    'UFFPDTNIRA': Division.FPArith,
    'UFIDL': Division.Equality_LinearArith,
    'UFLIA': Division.Equality_LinearArith,
    'UFLRA': Division.Equality_LinearArith,
    'UFNIA': Division.Equality_NonLinearArith,
}


def read_csv(file_path):
    """Read a CSV file and return its contents as a list of dictionaries."""
    data = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


def get_logic_from_benchmark(benchmark):
    """Extract logic from benchmark path."""
    return benchmark.split('/')[0]


def get_division(logic):
    """Get division from logic."""
    return str(divisions.get(logic, "Unknown"))


def parse_float(value):
    """Safely parse a float value, returning None if it can't be parsed."""
    try:
        if value is None or value == '':
            return None
        return float(value)
    except ValueError:
        return None


def gen_data(csv_file, include_norm_time=False):
    # Read the CSV file
    data = read_csv(csv_file)
    
    # Hard-coded path to benchmarks_remaining
    benchmarks_remaining_path = '/barrett/scratch/daneshva/fmcad25/analyze/SMT-LIB/benchmarks/benchmarks_remaining'
    
    # Load benchmarks_remaining
    benchmarks_remaining = set()
    try:
        with open(benchmarks_remaining_path, 'r') as infile:
            for line in infile:
                benchmarks_remaining.add(line.strip())
        print(f"Loaded {len(benchmarks_remaining)} benchmarks from benchmarks_remaining file")
    except FileNotFoundError:
        print(f"Warning: Could not find {benchmarks_remaining_path}")
        print("Using all benchmarks from the CSV file instead")
        benchmarks_remaining = set(row['benchmark'] for row in data)
    
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
    
    # Calculate statistics
    unique_sha_by_division = defaultdict(list)
    norm_time_by_division = defaultdict(list)
    histogram = Counter()
    
    for benchmark, rows in benchmark_groups.items():
        # Get logic and division
        logic = get_logic_from_benchmark(benchmark)
        division = get_division(logic)
        
        # Count unique SHA256 sums
        unique_shas = set(row['sha256sum'] for row in rows)
        num_unique = len(unique_shas)
        
        # Update histogram
        histogram[num_unique] += 1
        
        # Store count of unique SHA256 sums by division
        unique_sha_by_division[division].append(num_unique)
        
        # Store norm_time values by division (only if needed)
        if include_norm_time:
            for row in rows:
                norm_time = parse_float(row['norm_time'])
                if norm_time is not None:
                    norm_time_by_division[division].append(norm_time)
    
    # Only update column headers if norm_time analysis is included
    print("\n--- Average Number of Unique Outputs by Division ---")
    if include_norm_time:
        print("Division                        | Avg Unique | Avg Norm Time | Max Norm Time")
        print("-------------------------------|------------|--------------|-------------")
    else:
        print("Division                        | Avg Unique")
        print("-------------------------------|------------")
    
    for division in sorted(unique_sha_by_division.keys()):
        unique_counts = unique_sha_by_division[division]
        avg_unique = sum(unique_counts) / len(unique_counts) if unique_counts else 0
        
        if include_norm_time:
            norm_times = norm_time_by_division[division]
            avg_norm_time = sum(norm_times) / len(norm_times) if norm_times else 0
            max_norm_time = max(norm_times) if norm_times else 0
            print(f"{division:30} | {avg_unique:10.2f} | {avg_norm_time:12.4f} | {max_norm_time:11.4f}")
        else:
            print(f"{division:30} | {avg_unique:10.2f}")
    
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
    ap.add_argument('--norm-time', action='store_true', help='Include norm_time analysis in the output')
    args = ap.parse_args()
    
    histogram = gen_data(args.csv, include_norm_time=args.norm_time)
    print("\nHistogram dictionary:")
    print(histogram)


if __name__ == '__main__':
    main()