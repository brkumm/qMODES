#-----------------------------------------------------------------------------
# IMPORTS
from qMODES import compute_qmodes #compute_qk(mode, date, k_lb, k_ub, author_name=None, author_email=None)
from qMODES import nK
from qMODES import get_QMODES_SUPPRESS_NEW_USER_WARNINGS as suppress_warnings

import argparse
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
# PRINT WARNING(S)

if suppress_warnings == False:
    print("\nWARNING: When computing qmodes values in parallel they should be")
    print("batched in fairly large k-ranges. Each file will contain as much data")
    print("as the final file so computing too many will use a lot of memory.") 
    print("They should also be aggregated immediately after all parallel") 
    print("computations are completed.\n")
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# READING COMMAND LINE ARGUMENTS WITH argparse
parser = argparse.ArgumentParser(description='Script used to calculate the qmodes value (physical space) from the modal qk Fourier amplitudes over a specified range of k values.')
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
    compute_qmodes("EIG", str(date), int(klb), int(kub))
    compute_qmodes("WIG", str(date), int(klb), int(kub))
    compute_qmodes("BAL", str(date), int(klb), int(kub))

elif mode in ["EIG", "WIG", "BAL"]:
    compute_qmodes(str(mode), str(date), int(klb), int(kub))

else:
    print(f"ERROR: for the mode command line argument you input: {mode}")
    print("\tHowever, this value must be EIG, WIG, BAL, or ALL.")
    print("\tPlease use one of these values and try again.")
#-----------------------------------------------------------------------------
