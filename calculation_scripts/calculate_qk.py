#-----------------------------------------------------------------------------
# IMPORTS
from qMODES import compute_qk #compute_qk(mode, date, k_lb, k_ub, author_name=None, author_email=None)
from qMODES import nK
import argparse
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# READING COMMAND LINE ARGUMENTS WITH argparse
parser = argparse.ArgumentParser(description='This script is used to generate pressure level contour plots for an event over a specific region (originally Madison WI )')
parser.add_argument('-m','--mode', help='Mode to compute qk values for: [EIG, WIG, BAL] or ALL', required=True)
parser.add_argument('-d','--date', help='Date to comput the qk values for', required=True)
parser.add_argument('--klb',  help='Lower bound of k values', type=int, required=True)
parser.add_argument('--kub',  help='Upper bound of k values', type=int, required=True)
parser.add_argument('--ktot', help='Total number of k values', type=int, default=nK  )

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
    compute_qk("EIG", str(date), int(klb), int(kub))
    compute_qk("WIG", str(date), int(klb), int(kub))
    compute_qk("BAL", str(date), int(klb), int(kub))

elif mode in ["EIG", "WIG", "BAL"]:
    compute_qk(str(mode), str(date), int(klb), int(kub))

else:
    print(f"ERROR: for the mode command line argument you input: {mode}")
    print("\tHowever, this value must be EIG, WIG, BAL, or ALL.")
    print("\tPlease use one of these values and try again.")
#-----------------------------------------------------------------------------


