from qMODES import nK, nM, nN, nplev, nlat, nlon, ps0, Omega
from qMODES import sample_coef_file, sample_ERA_file

import xarray as xa
import pytest

coef_ds = xa.open_dataset( sample_coef_file() )
ERA_ds  = xa.open_dataset( sample_ERA_file() ) 

def test_nK():
    assert nK == coef_ds.sizes["k"]

def test_nM():
    assert nM == coef_ds.sizes["m"]

def test_nN():
    assert nN == coef_ds.sizes["n"]

def test_nplev():
    assert nplev == ERA_ds.sizes["plev"]

def test_nlat():
    assert nlat == ERA_ds.sizes["lat"]

def test_nlon():
    assert nlon == ERA_ds.sizes["lon"]