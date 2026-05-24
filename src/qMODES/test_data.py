#-----------------------------------------------------------------------------
# IMPORTS

from qMODES import get_QMODES_TEST_INPUT_DATA_DIR, get_QMODES_TEST_PARAMETERS_FILE
from qMODES import template_ERA_q_fname, template_ERA_uv_fname
from qMODES import template_coef_fname, template_hough_fname, template_vsf_fname

import os
import yaml
import pandas as pd
import xarray as xa
import numpy as np
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# FUNCTIONS

def generate_test_inputdata() -> None:
    # RETRIEVING TEST PARAMETERS AND GENERATING MODE AND GRID COORDINATE DATA
    # Test parameters
    with open(get_QMODES_TEST_PARAMETERS_FILE(), 'r') as param_file:
        params = yaml.safe_load(param_file)

    test_nK = params['mode_parameters']['nK']
    test_nM = params['mode_parameters']['nM']
    test_nN = params['mode_parameters']['nN']

    test_nlat = params['grid_parameters']['nlat']
    test_nlon = params['grid_parameters']['nlon']

    test_date      = params['grid_parameters']['test_date']
    test_date_dt64 = pd.to_datetime(test_date).to_datetime64()

    # Test data: mode values
    k_vals = [i for i in range(test_nK)]
    n_vals = [i for i in range(test_nN)]
    m_vals = [i for i in range(test_nM)]

    # Test data: grid values
    test_lat = [-90  + 180/(test_nlat)*(i+0.5) for i in range(test_nlat)]
    test_lon = [-180 + 360/(test_nlon)*(i+0.5) for i in range(test_nlon)]
    test_plev = params['grid_parameters']['test_plev'] #plevs specified in params file
    test_nplev = len(test_plev)

    # Initial print statement:
    print(f"\nTHE FOLLOWING TEST FILES HAVE BEEN CREATED:\n")

    #-------------------------------------------------------------------------
    # GENERATE ERA q and u,v TEST DATA FILES

    # Dataset from regular ERA q datafile
    # Dimensions:  (time: 1, lon: 1280, lat: 640, plev: 137)
    # Coordinates:
    #   * time     (time) datetime64[ns] 8B 2018-08-11
    #   * lon      (lon) float64 10kB 0.0 0.2812 0.5625 0.8438 ... 359.2 359.4 359.7
    #   * lat      (lat) float64 5kB 89.78 89.51 89.23 88.95 ... -89.23 -89.51 -89.78
    #   * plev     (plev) float64 1kB 1.0 3.0 4.0 6.0 ... 1.007e+05 1.01e+05 1.012e+05
    # Data variables:
    #     q        (time, plev, lat, lon) float32 449MB ...
    #
    #     ... same for u,v file ...
    #
    #     u        (time, plev, lat, lon) float32 449MB ...
    #     v        (time, plev, lat, lon) float32 449MB ...

    print(f"ERA TEST DATA")

    test_ntime = 1
    ERA_q_data = 0.002 * np.ones([test_ntime, test_nplev, test_nlat, test_nlon]) # kg / kg
    ERA_u_data = np.ones([test_ntime, test_nplev, test_nlat, test_nlon]) # m / s
    ERA_v_data = np.ones([test_ntime, test_nplev, test_nlat, test_nlon]) # m / s

    ERA_coords = {'time': (['time'], [test_date_dt64] ),
                  'lon' : (['lon' ], test_lon), 
                  'lat' : (['lat' ], test_lat), 
                  'plev': (['plev'], test_plev)}

    ERA_q_data_vars = {'q': (['time', 'plev', 'lat', 'lon'], ERA_q_data) }

    ERA_q_ds = xa.Dataset( data_vars = ERA_q_data_vars,
                           coords    = ERA_coords )

    ERA_q_outfile = template_ERA_q_fname(get_QMODES_TEST_INPUT_DATA_DIR(), test_date)
    ERA_q_ds.to_netcdf(ERA_q_outfile)
    ERA_q_ds.close()
    print(f"\t{ERA_q_outfile}")

    ERA_uv_data_vars = {'u': (['time', 'plev', 'lat', 'lon'], ERA_u_data),
                        'v': (['time', 'plev', 'lat', 'lon'], ERA_v_data) }
    
    ERA_uv_ds = xa.Dataset( data_vars = ERA_uv_data_vars,
                            coords    = ERA_coords )
    
    ERA_uv_outfile = template_ERA_uv_fname(get_QMODES_TEST_INPUT_DATA_DIR(), test_date)
    ERA_uv_ds.to_netcdf(ERA_uv_outfile)
    ERA_uv_ds.close()
    print(f"\t{ERA_uv_outfile}")

    #-------------------------------------------------------------------------
    # GENERATE VSF TEST DATA

    # Dataset from regular VSF file:
    # 
    # Dimensions:       (mp: 137, num_vmode: 120)
    # Coordinates:
    #   * mp            (mp) int32 548B 1 2 3 4 5 6 7 ... 131 132 133 134 135 136 137
    #   * num_vmode     (num_vmode) int32 480B 1 2 3 4 5 6 ... 115 116 117 118 119 120
    # Data variables:
    #     vsf           (num_vmode, mp) float64 132kB ...
    #     evht          (num_vmode) float64 960B ...
    #     vgrid         (mp) float64 1kB ...
    #     vgrid_weight  (mp) float64 1kB ...
    #     vsigma        (mp) float64 1kB ...
    #     vpres         (mp) float64 1kB ...
    #     stab          (mp) float64 1kB ...

    # Method for generating VSF test data:
    #    vsf(m=0, p) = 0 -> vsf_int(m=0, p) = 0
    #    vsf(m=1, p) = 1 -> vsf_int(m=1, p) = p
    #    vsf(m=2, p) = p -> vsf_int(m=2, p) = p^2 / 2

    print(f"VSF TEST DATA")

    poly = lambda p,m: p ** m

    vsf_vals = np.zeros([test_nM, test_nplev])

    for iM in range(1, test_nM):
        for iplev in range(test_nplev):
            vsf_vals[iM, iplev] = poly(test_plev[iplev], iM-1) 

    # Saving Values to test_data dir

    vsf_coords = {'mp'    : (['mp'], np.array([i for i in range(test_nplev)]) ), 
                 'vmodes' : (['num_vmode'], m_vals)}

    vsf_data_vars = {'vsf'  : (['num_vmode', 'mp'], vsf_vals),
                     'vgrid': (['mp'], test_plev)}

    vsf_ds = xa.Dataset( data_vars = vsf_data_vars,
                         coords    = vsf_coords )

    vsf_outfile = template_vsf_fname(get_QMODES_TEST_INPUT_DATA_DIR())
    vsf_ds.to_netcdf(vsf_outfile)
    print(f"\t{vsf_outfile}")

    #-------------------------------------------------------------------------
    # GENERATE HOUGH TEST DATA

    # Dataset from regular MODES Hough file:
    #
    # Dimensions:    (num_vmode: 60, uvz: 3, my: 640, maxl: 200)
    #                      m         uvz      lat         n
    # Coordinates:
    #   * num_vmode  (num_vmode) int32 240B 1 2 3 4 5 6 7 8 ... 54 55 56 57 58 59 60
    #   * uvz        (uvz) int32 12B 1 2 3
    #   * my         (my) int32 3kB 1 2 3 4 5 6 7 8 ... 634 635 636 637 638 639 640
    #   * maxl       (maxl) int32 800B 0 1 2 3 4 5 6 7 ... 193 194 195 196 197 198 199
    # Data variables:
    #     EIG        (num_vmode, uvz, my, maxl) float64 184MB ...
    #     WIG        (num_vmode, uvz, my, maxl) float64 184MB ...
    #     BAL        (num_vmode, uvz, my, maxl) float64 184MB ...
    #     lat        (my) float64 5kB ...

    # Method for generating Hough test data:
    # hough(m, uvz, lat, n) = 1 for all values.
    # Will turn terms in sum on and off with coef values.

    print(f"HOUGH TEST DATA")

    nHoughvec = 3
    hough_vals = np.ones([test_nM, nHoughvec, test_nlat, test_nN])

    # Saving Hough test data
    for kk in range(test_nK):
        hough_coords = {'num_vmode' : (['num_vmode'], m_vals),
                        'uvz'       : (['uvz'],  np.array([0,1,2])),
                        'my'        : (['my'],   np.array([i for i in range(test_nlat)])),
                        'maxl'      : (['maxl'], np.array([i for i in range(test_nN)])) }

        hough_data_vars = {'EIG': (['num_vmode', 'uvz', 'my', 'maxl'], hough_vals),
                           'WIG': (['num_vmode', 'uvz', 'my', 'maxl'], hough_vals),
                           'BAL': (['num_vmode', 'uvz', 'my', 'maxl'], hough_vals),
                           'lat': (['my'], test_lat) }

        hough_ds = xa.Dataset( data_vars = hough_data_vars,
                               coords    = hough_coords )

        k_str = "0"*(3-len(str(kk))) + str(kk)

        hough_outfile = template_hough_fname(get_QMODES_TEST_INPUT_DATA_DIR(), k_str)
        hough_ds.to_netcdf(hough_outfile)
        print(f"\t{hough_outfile}")

    #-------------------------------------------------------------------------
    # GENERATE COEF TEST DATA

    # Dataset from regular MODES Coef file:
    #
    # Dimensions:  (n: 200, m: 60, k: 351, time: 1, Re+Im: 2)
    # Coordinates:
    #   * n        (n) float64 2kB 0.0 1.0 2.0 3.0 4.0 ... 196.0 197.0 198.0 199.0
    #   * m        (m) float64 480B 1.0 2.0 3.0 4.0 5.0 ... 56.0 57.0 58.0 59.0 60.0
    #   * k        (k) float64 3kB 0.0 1.0 2.0 3.0 4.0 ... 347.0 348.0 349.0 350.0
    #   * time     (time) datetime64[ns] 8B 2018-08-01
    # Dimensions without coordinates: Re+Im
    # Data variables:
    #     EIG      (time, Re+Im, k, m, n) float64 67MB ...
    #     WIG      (time, Re+Im, k, m, n) float64 67MB ...
    #     BAL      (time, Re+Im, k, m, n) float64 67MB ...

    # Method for generating values
    # Going to turn on 2 qk coefs choosing a coef with m=1 (unitary vsf)
    # n=2 (all are 1 so it doesn't matter which), and various k values depending
    # on which ones ones we want to turn on for each mode.
    # NOTE: chooising unitary vsf means each qk value will effectively be multipled 
    # by a factor of p as we are using the INTEGRATED unitary vsf in the computation.
    #
    # coefs that will be turned on for each mode (q_{k,MODE}) are:
    #    q_{k,EIG} -> k=5,9 turned on
    #    q_{k,WIG} -> k=4,8 turned on
    #    q_{k,BAL} -> k=1,2 turned on

    print(f"COEF TEST DATA")


    EIG_coef_vals = np.zeros([1, 2, test_nK, test_nM, test_nN]) # coords are [time, Re+Im, k, m, n]
    WIG_coef_vals = np.zeros([1, 2, test_nK, test_nM, test_nN]) # coords are [time, Re+Im, k, m, n]
    BAL_coef_vals = np.zeros([1, 2, test_nK, test_nM, test_nN]) # coords are [time, Re+Im, k, m, n]

    # manually setting which coef values are non zero.
    # unitary amplitude for first non-zero coef
    EIG_coef_vals[0,0,5,1,2] = 1
    WIG_coef_vals[0,0,4,1,2] = 1
    BAL_coef_vals[0,0,1,1,2] = 1

    # 0.1 amplitude for second non-zero coef
    EIG_coef_vals[0,0,9,1,2] = 0.1
    WIG_coef_vals[0,0,8,1,2] = 0.1
    BAL_coef_vals[0,0,2,1,2] = 0.1

    # Saving Coef test data
    coef_coords = {'time'  : (['time'], np.array([0])),
                   'Re+Im' : (['Re+Im'], np.array([0,1])),
                   'k'     : (['k'], k_vals ),
                   'm'     : (['m'], m_vals ),
                   'n'     : (['n'], n_vals ) }

    coef_data_vars = {'EIG': (['time', 'Re+Im', 'k', 'm', 'n'], EIG_coef_vals),
                      'WIG': (['time', 'Re+Im', 'k', 'm', 'n'], WIG_coef_vals),
                      'BAL': (['time', 'Re+Im', 'k', 'm', 'n'], BAL_coef_vals),
                      'lat': (['my'], test_lat) }

    coef_ds = xa.Dataset( data_vars = coef_data_vars,
                          coords   = coef_coords )
    
    coef_outfile = template_coef_fname(get_QMODES_TEST_INPUT_DATA_DIR(), test_date)
    coef_ds.to_netcdf(coef_outfile)
    print(f"\t{coef_outfile}\n")

    return


def remove_test_inputdata() -> None:

    print("THE FOLLOWING TEST DATA FILES HAVE BEEN REMOVED:")
    # Traverse through the directory tree
    for root, _, files in os.walk( get_QMODES_TEST_INPUT_DATA_DIR()):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"\t{file_path}")
            except OSError as e:
                print(f"Error: {file_path} : {e.strerror}")

    return