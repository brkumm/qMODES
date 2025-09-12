#-------------------------------------------------------------------------
# Imports
from mpl_toolkits.basemap import Basemap, shiftgrid
from matplotlib.patches   import Polygon
from OmegaMODES_Functions import read_ERA_grid_data, get_single_plev_ERA_and_flippedMODES_q_data_with_p_and_lat_dependent_background

import cartopy.feature    as cfeature
import cartopy.crs        as ccrs
import cartopy.mpl.ticker as cticker
from   cartopy.util       import add_cyclic_point

import matplotlib.pyplot as plt
import xarray            as xa
import numpy             as np
import custom_colormap   as cc

import argparse

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Getting Command Line inputs using Argparse

parser = argparse.ArgumentParser(description='This script is used to generate pressure level contour plots for an event over a specific region (originally Madison WI )')
parser.add_argument('-d','--date', help='date to make the contours for',                    required=True)
parser.add_argument('-p','--plev', help='pressure level to generate the contour plots for', required=True)

args   = parser.parse_args()
date   = args.date
iplev  = int( args.plev )

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Initial Calculations

# Input Parameters
ERA_datafile    = f"../../ERA_Data/ERA_{date}_q_pl_data.nc"           # (ntime:1, nplev:137, nlat:640, nlon:1280)
qMODES_datafile = f"../../output_data/qMODES_Data/qMODES_{date}0000000.nc" # (nplev:137, nlat:640, nlon:1280)

# Output Parameters
outputfile1 = f"../../output_data/plots/Global_qMODES_{date}_plev{plev[iplev]}.pdf"
outputfile2 = f"../../output_data/plots/Global_qMODES_{date}_plev{plev[iplev]}.jpeg"

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Reading in data

# Reading Grid Data
[plev, lat, lon] = read_ERA_grid_data(ERA_datafile,'plev','lat','lon')

nplev = plev.shape[0]
nlat  = lat.shape[0]
nlon  = lon.shape[0]

# Reading in ERA and qMODES data
[qERA, qEIG, qWIG, qROT, qM] = get_single_plev_ERA_and_flippedMODES_q_data_with_p_and_lat_dependent_background(ERA_datafile, qMODES_datafile, iplev)

#changing units to g/kg and creating combined IG mode
qERA = 1000.0 * qERA
qROT = 1000.0 * qROT
qIG  = 1000.0 * (qEIG + qWIG)
qM   = 1000.0 * qM

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
#Setting Plot Parameters
cllw = 0.5
latmin = -90   # full globe values -90
latmax = 90   # full globe values 90
lonmin = -180 # full globe values -180
lonmax = 180 # full globe values 180

qERA_line_color = "blue"
qROT_line_color = "green"
qIG_line_color  = "orange"
qM_line_color   = "red"

band_alpha       = 0.20 # setting alpha value (transparancy) of the band region
line_alpha       = 0.75

# Plot Contours and Colormap info

qERA_contours = np.linspace(-10.0,  10.0, 21)
qROT_contours = np.linspace(-4.0,  4.0, 21)
qIG_contours  = np.linspace(-2.0,  2.0, 21)
qM_contours   = np.linspace(-10.0,  10.0, 21)

qERA_cmap     = cc.get_my_colormap( qERA_contours )
qROT_cmap     = cc.get_my_colormap( qROT_contours )
qIG_cmap      = cc.get_my_colormap( qIG_contours  )
qM_cmap       = cc.get_my_colormap( qM_contours   )

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# MODES Contour Plots

proj = ccrs.Robinson() #projection

Cfig, [[ax00, ax01], [ax10, ax11]] = plt.subplots(nrows=2, ncols=2, figsize=(10,5), subplot_kw={'projection': proj})

# #qERA plot
ax00.set_title("a)      q_ERA (anomaly) [g/kg]")
qERA_contour = ax00.contourf(lon, lat, qERA, qERA_contours, transform=ccrs.PlateCarree(), cmap=qERA_cmap, extend='both')
ax00.coastlines()
qROT_cbar    = Cfig.colorbar(qERA_contour, ax=ax00)


#qROT plot
ax01.set_title("b)      q_ROT (anomaly) [g/kg]")
qROT_contour = ax01.contourf(lon, lat, qROT, qROT_contours, transform=ccrs.PlateCarree(), cmap=qROT_cmap, extend='both')
ax01.coastlines()
qROT_cbar    = Cfig.colorbar(qROT_contour, ax=ax01)


# #qIG plot
ax10.set_title("c)      q_IG (anomaly) [g/kg]")
qIG_contour = ax10.contourf(lon, lat, qIG, qIG_contours, transform=ccrs.PlateCarree(), cmap=qIG_cmap, extend='both')
ax10.coastlines()
qIG_cbar    = Cfig.colorbar(qIG_contour, ax=ax10)


# #qM plot
ax11.set_title("d)      q_M (anomaly) [g/kg]")
qM_contour = ax11.contourf(lon, lat, qM, qM_contours, transform=ccrs.PlateCarree(), cmap=qM_cmap, extend='both')
ax11.coastlines()
qM_cbar    = Cfig.colorbar(qM_contour, ax=ax11)

#plt.show() # if you want to save the plots must "show" after saving

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Saving Plot

plt.savefig(outputfile1)
plt.savefig(outputfile2)

plt.show()

print(f"Plot(s) saved to:\n\t{outputfile1}\n\t{outputfile2}\n")

#-------------------------------------------------------------------------
