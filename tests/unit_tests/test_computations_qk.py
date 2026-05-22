from qMODES import compute_qk
from qMODES import parameters as params

import xarray as xa
import pytest


compute_qk("EIG", "20180801", 0, params.test_nK, params.test_nK)
compute_qk("WIG", "20180801", 0, params.test_nK, params.test_nK)
compute_qk("BAL", "20180801", 0, params.test_nK, params.test_nK)

def test_compute_qk():f
    