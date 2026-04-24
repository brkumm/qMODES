from qMODES import get_QMODES_VSF_DIR, get_QMODES_VSFINT_DIR, get_QMODES_ERA_DIR, get_QMODES_MODES_DIR, get_QMODES_COEF_DIR, get_QMODES_HOUGH_DIR, get_QMODES_FREQ_DIR, get_QMODES_QKDATA_DIR, get_QMODES_QMODESDATA_DIR, get_QMODES_PLOTS_DIR

import os
import pytest

def test_get_QMODES_VSF_DIR():
    assert os.path.isdir(get_QMODES_VSF_DIR())

def test_get_QMODES_VSFINT_DIR():
    assert os.path.isdir(get_QMODES_VSFINT_DIR())

def test_get_QMODES_ERA_DIR():
	assert os.path.isdir(get_QMODES_ERA_DIR())

def test_get_QMODES_MODES_DIR():
	assert os.path.isdir(get_QMODES_MODES_DIR())

def test_get_QMODES_COEF_DIR():
	assert os.path.isdir(get_QMODES_COEF_DIR())

def test_get_QMODES_HOUGH_DIR():
	assert os.path.isdir(get_QMODES_HOUGH_DIR())

def test_get_QMODES_FREQ_DIR():
	assert os.path.isdir(get_QMODES_FREQ_DIR())

def test_get_QMODES_QKDATA_DIR():
	assert os.path.isdir(get_QMODES_QKDATA_DIR())

def test_get_QMODES_QMODESDATA_DIR():
	assert os.path.isdir(get_QMODES_QMODESDATA_DIR())

def test_get_QMODES_PLOTS_DIR():
	assert os.path.isdir(get_QMODES_PLOTS_DIR())