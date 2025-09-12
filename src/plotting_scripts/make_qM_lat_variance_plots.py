#--------------------------------------------------------------------------
# IMPORTS

from mpl_toolkits.basemap    import Basemap, shiftgrid
from matplotlib.patches      import Polygon
from OmegaMODES_Functions    import read_ERA_grid_data, get_single_plev_ERA_and_flippedMODES_q_data

import matplotlib.pyplot as plt
import xarray            as xa
import numpy             as np
import argparse

#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# Reading in command line arguments using argparse
parser = argparse.ArgumentParser(description='Script that make variance plots of q, qIG, qROT, and qM over each latitude band.')
parser.add_argument('-d', '--date', help='date to generate plot for in YYYYMMDD format', required=True)

args  = parser.parse_args()
date  = args.date

plev_list = [95, 82] #list of plev indices to generate curves for
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# PARAMETERS, INITIAL CALCS, AND CHECKS

# Input Files

ERA_datafile    = ERA_dir    + f"ERA5_{date}_q-t_pl_data.nc"
qMODES_datafile = qMODES_dir + f"qmodes_{date}0000000.nc"

#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# IMPORTING MODES AND ERA DATA AND PERFORMING CALCULATIONS

#Reading Grid Data
[plev, lat, lon] = read_ERA_grid_data(ERA_datafile,'plev','lat','lon')

nplev = plev.shape[0]
nlat  = lat.shape[0] 
nlon  = lon.shape[0] 
    
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
#Main Plotting Loop

#Setting up the plots

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12,8))

color_list = ['r','g','b','goldenrod','c','mediumpurple','m','k','gray','darkorange']

#Initalizing values for loop

qERA = np.zeros((nlat,nlon))
qROT = np.zeros((nlat,nlon))
qIG  = np.zeros((nlat,nlon))
qM   = np.zeros((nlat,nlon))

qERA_variance = np.zeros(nlat)
qROT_variance = np.zeros(nlat)
qIG_variance  = np.zeros(nlat)
qM_variance   = np.zeros(nlat)

for iplev in range(len(plev_list)):

	[qERA,qEIG,qWIG,qROT,qM] = get_single_plev_ERA_and_flippedMODES_q_data(ERA_datafile, qMODES_datafile, plev_list[iplev]) #indexing for q vars is [lat,lon]

	qERA = 1000.0 * qERA          #converting to g/kg
	qROT = 1000.0 * qROT          #converting to g/kg
	qIG  = 1000.0 * (qEIG + qWIG) #converting to g/kg and switch to IG only
	qM   = 1000.0 * qM            #converting to g/kg

	for ilat in range(nlat):

		qERA_variance[ilat] = np.var(qERA[ilat,:],ddof=1)
		qROT_variance[ilat] = np.var(qROT[ilat,:],ddof=1)
		qIG_variance[ilat]  = np.var(qIG[ilat,:], ddof=1)
		qM_variance[ilat]   = np.var(qM[ilat,:],  ddof=1)

    #Generating The Plots

    #qERA plot -- axes[0,0]
	axes[0,0].plot(lat, qERA_variance, color=color_list[iplev], label=f'plev -- {plev[plev_list[iplev]] / 100.0} hPa')
	if plev_list[iplev] == plev_list[0]:  axes[0,0].set_title("a)     qERA Variance")
	if plev_list[iplev] == plev_list[0]:  axes[0,0].set_ylabel("Variance [g^2 / kg^2]")

    #qROT plot -- axes[0,1]
	axes[0,1].plot(lat, qROT_variance, color=color_list[iplev], label=f'plev -- {plev[plev_list[iplev]] / 100.0} hPa')
	if plev_list[iplev] == plev_list[0]:  axes[0,1].set_title("b)     qROT Variance")
	if plev_list[iplev] == plev_list[0]:  axes[0,1].set_ylabel("Variance [g^2 / kg^2]")
	if plev_list[iplev] == plev_list[-1]: axes[0,1].legend()

    #qIG plot  -- axes[1,0]
	axes[1,0].plot(lat, qIG_variance, color=color_list[iplev], label=f'plev -- {plev[plev_list[iplev]] / 100.0} hPa')
	if plev_list[iplev] == plev_list[0]:  axes[1,0].set_title("c)     qIG Variance")
	if plev_list[iplev] == plev_list[0]:  axes[1,0].set_xlabel("Latitude")
	if plev_list[iplev] == plev_list[0]:  axes[1,0].set_ylabel("Variance [g^2 / kg^2]")

    #qM plot   -- axes[1,1]
	axes[1,1].plot(lat, qM_variance, color=color_list[iplev], label=f'plev -- {plev[plev_list[iplev]] / 100.0} hPa')
	if plev_list[iplev] == plev_list[0]:  axes[1,1].set_title("d)     qM Variance")
	if plev_list[iplev] == plev_list[0]:  axes[1,1].set_xlabel("Latitude")
	if plev_list[iplev] == plev_list[0]:  axes[1,1].set_ylabel("Variance [g^2 / kg^2]")


plt.show()

#--------------------------------------------------------------------------
