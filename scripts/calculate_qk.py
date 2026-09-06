#-----------------------------------------------------------------------------
# IMPORTS
from qMODES import compute_qk

import argparse
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# READING COMMAND LINE ARGUMENTS WITH argparse
parser = argparse.ArgumentParser(description='This script is used to calculate the qk (zonal Fourier coefficients) values for a given date mode for a specided range of k values.')
parser.add_argument('-m','--mode', help='Mode to compute qk values for: [EIG, WIG, BAL] or ALL', type=str, required=True)
parser.add_argument('-d','--date', help='Date to comput the qk values for', type=str, required=True)
parser.add_argument('--klb',  help='Lower bound of k values',  type=int, required=True)
parser.add_argument('--kub',  help='Upper bound of k values',  type=int, required=True)
parser.add_argument('--ktot', help='Total number of k values', type=int, required=True)

args   = parser.parse_args()
mode   = args.mode
date   = args.date
klb    = args.klb
kub    = args.kub
ktot   = args.ktot
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# MAIN COMPUTATIONS

if mode == 'ALL':
    compute_qk("EIG", date, klb, kub, ktot)
    compute_qk("WIG", date, klb, kub, ktot)
    compute_qk("BAL", date, klb, kub, ktot)

elif mode in ["EIG", "WIG", "BAL"]:
    compute_qk(mode, date, klb, kub, ktot)

else:
    print(f"ERROR: for the mode command line argument you input: {mode}")
    print("\tHowever, this value must be EIG, WIG, BAL, or ALL.")
    print("\tPlease use one of these values and try again.")
#-----------------------------------------------------------------------------