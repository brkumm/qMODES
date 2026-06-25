#-----------------------------------------------------------------------------
# File:          helpers.py
# Author:        Bradley Kumm (brkumm@gmail.com)
# Last Modified: 2026/06/16 (YYYY/MM/DD)
# Description:   Functions used to compute the qk (meridional Fourier
#                component) values. See Kumm et al. 2026 (currently in review)
#                paper for equations relavent to the computations.
#
# Notes:         
#               
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# IMPORTS

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# MISCELLANEOUS HELPER FUNCTIONS

def convert_pos_int_to_padded_str(val: int, max_len: int = 3) -> str:
    if len(str(val)) > max_len or val < 0:
        raise ValueError(f"Input val ({val}) must be positive and have fewer digits than max_length ({max_len}).")
    return f"{val:0{max_len}}"

#-----------------------------------------------------------------------------