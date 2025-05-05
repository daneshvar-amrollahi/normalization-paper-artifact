#!/usr/env/bin python3

import argparse
import pandas as pd
import numpy as np

def mad_func(x):
    """Calculate the median absolute deviation"""
    return np.median(np.abs(x - np.median(x)))

def gen_data(csv):
    # Read the CSV file
    df = pd.read_csv(csv)

    # Only use remaining benchmarks
    benchmarks_remaining = set()
    with open('benchmark_set_lvbkv', 'r') as infile:
        for line in infile:
            benchmarks_remaining.add(line.strip())
        assert len(benchmarks_remaining) == 5334

    # Filter benchmarks
    df = df[df['benchmark'].isin(benchmarks_remaining)]

    print(f'Number of benchmarks: {len(df)}')

    assert len(df['benchmark'].unique()) == 5334

    # Compute PAR2 score, all unsolved get a score of 120
    df['par2'] = np.where(
        (df['result'] != 'sat') & (df['result'] != 'unsat'),
        120,
        df['total_time']
    )

    # Compute metrics for the entire dataset (no divisions)
    # Group by config to get sum of par2 scores for each config
    config_scores = df.groupby('config')['par2'].sum().reset_index()
    
    # Calculate overall metrics across configs
    par2_avg = config_scores['par2'].mean()
    par2_mad = mad_func(config_scores['par2'])

    # Calculate MAD grouped by benchmark (no divisions)
    benchmark_mad = df.groupby('benchmark')['par2'].apply(mad_func).reset_index()
    benchmark_mad_sum = benchmark_mad['par2'].sum()

    # Format and print results
    print("Overall Stats (no divisions):")
    print(f"par2_avg: {par2_avg:.1f}")
    print(f"par2_mad: {par2_mad:.1f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('csv')
    args = ap.parse_args()
    gen_data(args.csv)

if __name__ == '__main__':
    main()