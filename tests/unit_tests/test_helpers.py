#-----------------------------------------------------------------------------
# IMPORTS
from qMODES import convert_pos_int_to_padded_str

import pytest

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# TESTING FUNCTIONS IN helpers.py

def test_convert_pos_int_to_padded_str() -> None:
    # Test to run:
    #     1) check valid inputs give correct values
    #     2) check positive ints with more than 3 digits throw a ValueError
    #     3) check all negatives throw a ValueError 

    # Checking Valid inputs give correct values
    assert convert_pos_int_to_padded_str(  0) == "000"
    assert convert_pos_int_to_padded_str(  1) == "001"
    assert convert_pos_int_to_padded_str( 10) == "010"
    assert convert_pos_int_to_padded_str( 11) == "011"
    assert convert_pos_int_to_padded_str( 42) == "042"
    assert convert_pos_int_to_padded_str(100) == "100"
    assert convert_pos_int_to_padded_str(101) == "101"
    assert convert_pos_int_to_padded_str(110) == "110"
    assert convert_pos_int_to_padded_str(111) == "111"

    # Checking that invalide inputs raise a ValueError
    with pytest.raises(ValueError):
        convert_pos_int_to_padded_str(1111)
        convert_pos_int_to_padded_str(-1.0)
    

#-----------------------------------------------------------------------------