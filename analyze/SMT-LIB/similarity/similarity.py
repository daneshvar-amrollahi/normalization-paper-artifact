#!/usr/bin/env python3

import argparse
from enum import Enum
import polars as pl

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


def analyze_similarity_by_division(csv_file, benchmarks_file):
    # Read the similarity CSV
    df = pl.read_csv(csv_file)
    
    # Load the benchmark_remaining file
    benchmarks_remaining = set()
    with open(benchmarks_file, 'r') as infile:
        for line in infile:
            benchmarks_remaining.add(line.strip())
    
    print(f'Total benchmarks in remaining file: {len(benchmarks_remaining)}')
    
    # Filter dataframe to only include benchmarks in the remaining set
    df = df.filter(pl.col('benchmark').is_in(benchmarks_remaining))
    print(f'Number of benchmarks after filtering: {len(df)}')
    
    # Extract logic from benchmark path
    df = df.with_columns(
        pl.col('benchmark').str.split(by='/').list.get(0).alias('logic')
    )
    
    # Map logic to division
    map_div = lambda x: str(divisions.get(x, "Unknown"))
    df = df.with_columns(
        pl.col('logic').map_elements(map_div, return_dtype=str).alias('division')
    )
    
    # Group by division and calculate statistics
    division_stats = df.group_by(['division']).agg([
        pl.col('avg_sim').mean().alias('avg_sim_mean'),
        pl.col('avg_sim').min().alias('avg_sim_min'),
        pl.col('avg_sim').max().alias('avg_sim_max')
    ])
    
    # Format and display results
    with pl.Config(tbl_formatting='NOTHING',
                  tbl_cols=-1,
                  tbl_rows=-1,
                  tbl_hide_column_data_types=True,
                  tbl_hide_dataframe_shape=True,
                  tbl_cell_numeric_alignment='RIGHT',
                  float_precision=2):
        print(division_stats.sort('division'))
    


def main():
    parser = argparse.ArgumentParser(description='Analyze similarity by SMT division')
    parser.add_argument('csv_file', help='Path to CSV file with similarity data')
    parser.add_argument('benchmarks_file', help='Path to benchmarks_remaining file')
    
    args = parser.parse_args()
    analyze_similarity_by_division(args.csv_file, args.benchmarks_file)


if __name__ == '__main__':
    main()