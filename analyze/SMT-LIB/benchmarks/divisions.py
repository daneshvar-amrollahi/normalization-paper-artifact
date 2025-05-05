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

def gen_data(file):
    cnt = dict()
    with open(file, 'r') as benchmarks:
        for benchmark in benchmarks:
            t = benchmark.split('/')
            div = divisions[t[7]]
            if div not in cnt:
                cnt[div] = 0
            cnt[div] += 1

    # Sort results by division name
    for div, c in sorted(cnt.items(), key=lambda x: str(x[0])):
        print(f'{div}: {c}')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('benchmarks')
    args = ap.parse_args()
    gen_data(args.benchmarks)

if __name__ == '__main__':
    main()