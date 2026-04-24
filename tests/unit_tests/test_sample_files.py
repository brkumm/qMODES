from qMODES import get_QMODES_VSF_DIR, get_QMODES_VSFINT_DIR, get_QMODES_COEF_DIR, get_QMODES_HOUGH_DIR, get_QMODES_FREQ_DIR, get_QMODES_ERA_DIR
from qMODES import template_vsf_fname, template_vsf_int_fname, template_coef_fname, template_hough_fname, template_freq_fname, sample_ERA_file
from qMODES import sample_ERA_file, sample_freq_file, sample_hough_file, sample_coef_file, sample_vsf_int_file, sample_vsf_int_file
import os
import pytest

def test_sample_vsf_file():
	assert os.path.isfile( sample_vsf_int_file() )

def test_sample_vsf_int_file():
	assert os.path.isfile( sample_vsf_int_file() )

def test_sample_coef_file():
	assert os.path.isfile( sample_coef_file() )

def test_sample_hough_file():
	assert os.path.isfile( sample_hough_file() )

def test_sample_freq_file():
	assert os.path.isfile( sample_freq_file() )

def test_sample_ERA_file():
	assert os.path.isfile( sample_ERA_file() )