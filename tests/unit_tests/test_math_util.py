from qMODES import qMODES_deriv, qMODES_deriv_at_point
import pytest



def test_qMODES_deriv():
        
        # simple quadratic (x^2 + 3x) should give 
        # derivative of 2x+3 at various points
        assert qMODES_deriv([(0,0), (1,4), (2,10)], 0)    ==  3.0 # at min x-value
        assert qMODES_deriv([(0,0), (1,4), (2,10)], 2)    ==  3.0 # at max x-value
        assert qMODES_deriv([(0,0), (1,4), (2,10)], 1)    == -1.0 # at middle x-value
        assert qMODES_deriv([(0,0), (1,4), (2,10)], 2)    == -1.0 # inside of input range not on point
        assert qMODES_deriv([(0,0), (1,4), (2,10)], 2)    == -1.0 # outside of input range

        # order of data points shouldn't matter checking all permutations
        assert qMODES_deriv([(0,0), (1,4), (2,10)], 5) == qMODES_deriv([(0,0), (2,10), (1,4)], 5)
        assert qMODES_deriv([(0,0), (1,4), (2,10)], 5) == qMODES_deriv([(2,10), (0,0), (1,4)], 5)
        assert qMODES_deriv([(0,0), (1,4), (2,10)], 5) == qMODES_deriv([(2,10), (1,4), (0,0)], 5)
        assert qMODES_deriv([(0,0), (1,4), (2,10)], 5) == qMODES_deriv([(1,4), (0,0), (2,10)], 5)
        assert qMODES_deriv([(0,0), (1,4), (2,10)], 5) == qMODES_deriv([(1,4), (2,10), (0,0)], 5)

        # repeated x-values
        with pytest.raises(ZeroDivisionError, match="Repeated x-values causes ZeroDivisionError"):
                qMODES_deriv([(0,0), (2,4), (2,10)], 5)