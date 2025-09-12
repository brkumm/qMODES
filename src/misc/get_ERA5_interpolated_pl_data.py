#-------------------------------------------------------------------------
# File:          get_ERA5_interpolated_pl_data.py
# Author:        Bradley Kumm (bkumm@wisc.edu) 
# Last Modified: 2023/02/03 (YYYY/MM/DD)
# Description:   Script that downloads model level ERA5 data for a user 
#                specified list of parameters over a user specified time
#                frame (start_date, end_date, time_list) that then uses 
#                the ml2plx CDO function to interpolate the data to a
#                pressure level coordinate system (instead of a model level
#                system) then combines the pressure level data into a
#                single file.
# Notes:         Must have CDO functions installed. If running on a Mac
#                you can install the CDO functions by installing homebrew
#                and simply running 'brew install cdo'. Script is based on
#                a script recieved from Valentino Neduhal
#                (valentino.neduhal@uni-hamburg.de) with some small 
#                modifications.
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
#IMPORTS
import subprocess
import cdsapi
from datetime import *
import time
import os
#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
#INPUT FROM USER

#Location to Save Files To
save_dir = '../../input_data/ERA_Data/'

#Date and Grid Info
start_date = datetime(2018,8,11)
end_date   = datetime(2018,8,11)

time_list  = ['00:00:00']
grid_str   = 'F320'
ml_list    = [str(i+1) for i in range(137)]

#Parameter info
param_list      = ['133'] # 4 --> equivalent potential temperature(eqpt), 133 --> specific humidity (q), 130 --> temperature (t), 135 --> vertical velocity (Pa s^-1)
param_name_list = ['q']    #"short name" of the param_list_variables (this is used in naming the files) list of vars here!!! https://codes.ecmwf.int/grib/param-db/
surface_params  = ['129', '152']   # 129 - Geopotential (z), 152 - Logarithm of surface pressure (lnsp)


os.chdir(save_dir)

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
c = cdsapi.Client()
t = start_date

print(f"\nRETRIEVING DATA FOR:")

while t <= end_date:
    date      = t.strftime("%Y%m%d")
    printdate = "********** " +  t.strftime("%Y%m%d") + " **********"
    
    print("" + f"*"*len(printdate))
    print(f"{printdate}")
    print(f"*"*len(printdate) + "\n")



    param_outfile = 'ERA5_' + date + '_' + '-'.join(param_name_list) + '_ml_data.grib'
    surf_outfile  = 'ERA5_' + date + '_z-lnsp_surf-ml_data.grib'

    final_outfile = 'ERA5_' + date + '_' + '-'.join(param_name_list) + '_pl_data.nc'


    c.retrieve('reanalysis-era5-complete', {
        'class': "ea",
        'date': date,
        'levelist': '/'.join(ml_list),
        'levtype': 'ml', #specifying to use model level data
        'grid': grid_str,
        'param': '/'.join(param_list),  
        'stream': 'oper',
        'time': '/'.join(time_list),
        'type': 'an',
    }, param_outfile)

    c.retrieve('reanalysis-era5-complete', {
        'class': "ea",
        'date': date,
        'levelist': '1',
        'levtype': 'ml', #specifying to use model level data
        'grid': grid_str,
        'param': '/'.join(surface_params),  # 129 - Geopotential (z), 152 - Logarithm of surface pressure (lnsp)
        'stream': 'oper',
        'time': '/'.join(time_list),
        'type': 'an',
    }, surf_outfile)
    
    # Calling cdo commands for data manipulation and interpolation to the pressure levels
    subprocess.call("cdo merge " + param_outfile + " " +  surf_outfile +  " era5_lev_ml.grib", shell=True) # Mergeing the files
    subprocess.call("cdo ml2plx,1,3,4,6,8,12,16,22,29,38,49,62,78,97,119,145,175,210,249,293,343,398,460,529,604,687,777,875,982,1097,1221,1355,1498,1651,1813,1987,2171,2366,2572,2789,3018,3258,3511,3776,4053,4343,4645,4960,5286,5626,5977,6342,6719,7112,7520,7945,8388,8851,9335,9842,10371,10924,11502,12105,12735,13392,14077,14791,15534,16309,17116,17955,18829,19737,20681,21662,22681,23738,24836,25976,27157,28382,29652,30967,32329,33739,35199,36709,38271,39885,41554,43278,45059,46897,48795,50750,52757,54803,56877,58968,61066,63162,65244,67304,69330,71316,73253,75134,76953,78705,80386,81993,83524,84977,86352,87650,88871,90017,91090,92092,93026,93895,94702,95451,96143,96783,97374,97919,98420,98881,99305,99695,100052,100379,100679,100954,101205 era5_lev_ml.grib era5_lev_pl_1.grib",shell=True), # interpolation to the pressure levels
    subprocess.call("rm era5_lev_ml.grib", shell=True) # Removing the old file

    #subprocess.call("cdo delete,name=z Era5_pl.grib era5_lev_pl_1.grib",shell=True) # Removing redundant variable
    #subprocess.call("rm Era5_pl.grib",shell=True) # Removing the old file
    subprocess.call("cdo delete,name=lnsp era5_lev_pl_1.grib era5_lev_pl_2.grib", shell=True) # Removing redundant variable
    subprocess.call("rm era5_lev_pl_1.grib", shell=True) # Removing the old file
    subprocess.call("cdo -z zip1 -f nc copy era5_lev_pl_2.grib " + final_outfile , shell=True) # Changing the format from grib to nc
    subprocess.call("rm era5_lev_pl_2.grib", shell=True) # Removing the old grib file

    t += timedelta(days=1)
