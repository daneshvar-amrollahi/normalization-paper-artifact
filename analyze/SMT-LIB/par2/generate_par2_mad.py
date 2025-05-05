#!/usr/env/bin python3NI

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


def bf(res1, res2):
    r1 = int(res1)
    r2 = int(res2)
    if (r1 > r2):
        return f'\\textbf{{{r1:,}}}'
    return f'{r1:,}'

def mad_func(x: pl.Series):
    return (x - x.median()).abs().median()

def gen_data(csv):
    df = pl.read_csv(csv)

    # Only use remaining benchmarks
    benchmarks_remaining = set()
    with open('../benchmarks/benchmarks_remaining', 'r') as infile:
        for line in infile:
            benchmarks_remaining.add(line.strip())
        assert len(benchmarks_remaining) == 41075

    df = df.filter(pl.col('benchmark').is_in(benchmarks_remaining))

    print(f'Number of benchmarks: {len(df)}')

    assert len(df.unique(pl.col('benchmark'))) ==  41075

    # Compute PAR2 score, all unsolved get a score of 120
    df = df.with_columns(pl.when((pl.col('result') != 'sat') &
                                 (pl.col('result') != 'unsat'))
                           .then(120)
                           .otherwise(pl.col('total_time')).alias('par2'))


    # Extract logic
    df = df.with_columns(
            pl.col('benchmark').str.split(by='/').list.get(0).alias('logic'))

    # Determine division
    map_div = lambda x : str(divisions[x])
    df = df.with_columns(
            pl.col('logic').map_elements(map_div,
                                         return_dtype=str).alias('division'))

    # Compute MAD grouped by config
    dfcd = df.group_by(['config', 'division']).agg([pl.col('par2').sum()])
    dfc = dfcd.group_by(['division']).agg(
            [pl.col('par2').mean().alias('par2_avg'),
             pl.col('par2').min().alias('par2_min'),
             pl.col('par2').max().alias('par2_max'),
             pl.col('par2').map_elements(mad_func,
                                         return_dtype=pl.Float64).alias('par2_mad')])

    dfc = dfc.with_columns((pl.col('par2_max') - pl.col('par2_min')).alias('min_max_diff'))

    # Compute MAD grouped by benchmark
    dfg = df.group_by(['benchmark', 'division']).agg(
            [pl.col('par2').map_elements(mad_func, return_dtype=pl.Float64).alias('par2_mad')])
    dfgd = dfg.group_by(['division']).agg([pl.col('par2_mad').sum()])

    with pl.Config(tbl_formatting='NOTHING',
                   tbl_cols=-1,
                   tbl_rows=-1,
                   tbl_hide_column_data_types=True,
                   tbl_hide_dataframe_shape=True,
                   tbl_cell_numeric_alignment='RIGHT',
                   float_precision=1):
        print(dfc.with_columns(
               pl.col('par2_avg').round(0).cast(pl.Int64),
               pl.col('par2_min').round(0).cast(pl.Int64),
               pl.col('par2_max').round(0).cast(pl.Int64)
               ).sort(pl.col('division')).select(['division', 'par2_avg', 'par2_mad']))
        print()
        # print(dfgd.sort(pl.col('division')))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('csv')
    args = ap.parse_args()
    gen_data(args.csv)

if __name__ == '__main__':
    main()