#-----------------------------------------------------------------------------
from qMODES import qMODES_deriv, qMODES_deriv_at_point

import pytest
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
def test_qMODES_deriv_at_point():
        
    # simple quadratic (x^2 + 3x) should give 
    # derivative of 2x+3 at various points
    assert qMODES_deriv_at_point([(0,0), (1,4), (2,10)], 0)   ==  3.0 # at min x-value
    assert qMODES_deriv_at_point([(0,0), (1,4), (2,10)], 2)   ==  7.0 # at max x-value
    assert qMODES_deriv_at_point([(0,0), (1,4), (2,10)], 1)   ==  5.0 # at middle x-value
    assert qMODES_deriv_at_point([(0,0), (1,4), (2,10)], 0.5) ==  4.0 # inside of input range not on point
    assert qMODES_deriv_at_point([(0,0), (1,4), (2,10)], 3)   ==  9.0 # outside of input range

    # order of data points shouldn't matter checking all permutations
    assert qMODES_deriv_at_point([(0,0), (1,4), (2,10)], 5) == qMODES_deriv_at_point([(0,0), (2,10), (1,4)], 5)
    assert qMODES_deriv_at_point([(0,0), (1,4), (2,10)], 5) == qMODES_deriv_at_point([(2,10), (0,0), (1,4)], 5)
    assert qMODES_deriv_at_point([(0,0), (1,4), (2,10)], 5) == qMODES_deriv_at_point([(2,10), (1,4), (0,0)], 5)
    assert qMODES_deriv_at_point([(0,0), (1,4), (2,10)], 5) == qMODES_deriv_at_point([(1,4), (0,0), (2,10)], 5)
    assert qMODES_deriv_at_point([(0,0), (1,4), (2,10)], 5) == qMODES_deriv_at_point([(1,4), (2,10), (0,0)], 5)

    # repeated x-values should throw ZeroDivisionError
    with pytest.raises(ZeroDivisionError, match="Repeated x-values causes ZeroDivisionError"):
        qMODES_deriv_at_point([(0,0), (2,4), (2,10)], 5)

def test_qMODES_deriv():
    
    # Interior points in list are covered by test_qMODES_deriv_at_point.
    # xvals = [0, 1, 2] and yvals = [0, 4, 10] defines parabola
    test_derivs = qMODES_deriv([0, 1, 2], [0, 4, 10])
    assert  test_derivs[0] == 4 # 0th entry should be linear slope of first 2 points
    assert  test_derivs[1] == 5 # 1st entry should be linear slope of first 2 points
    assert  test_derivs[2] == 6 # last entry should be linear slope of last 2 points

    # Repeated x-values for inner derivatives should be caught by 
    # test_qMODES_deriv_at_point so we only need to test if first and last
    # derivs throw a ZeroDivisionError

    with pytest.raises(ZeroDivisionError, match="Repeated x-values causes ZeroDivisionError"):
        qMODES_deriv([0, 0, 2], [0, 4, 10]) # repeat first two x-vals
    with pytest.raises(ZeroDivisionError, match="Repeated x-values causes ZeroDivisionError"):
        qMODES_deriv([0, 1, 1], [0, 4, 10]) # repeat last two x-vals
#-----------------------------------------------------------------------------