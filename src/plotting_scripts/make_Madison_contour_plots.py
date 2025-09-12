#-------------------------------------------------------------------------
# Imports
from mpl_toolkits.basemap import Basemap, shiftgrid
from matplotlib.patches   import Polygon
from OmegaMODES_Functions import read_ERA_grid_data, get_single_plev_ERA_and_flippedMODES_q_data

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
outputfile = f"../../output_data/plots/qMODES_plev"
#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Reading in data

# Reading Grid Data
[plev, lat, lon] = read_ERA_grid_data(ERA_datafile,'plev','lat','lon')

nplev = plev.shape[0]
nlat  = lat.shape[0]
nlon  = lon.shape[0]

# Reading in ERA and qMODES data
[qERA, qEIG, qWIG, qROT, qM] = get_single_plev_ERA_and_flippedMODES_q_data(ERA_datafile, qMODES_datafile, iplev)

#Changing units to g/kg and adding IG modes
qERA = 1000.0 * qERA
qROT = 1000.0 * qROT
qEIG = 1000.0 * qEIG
qWIG = 1000.0 * qWIG
qM   = 1000.0 * qM

qIG  = qEIG + qWIG

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
#Setting Plot Parameters
cllw = 0.5
latmin = 20   # full globe values -90
latmax = 70   # full globe values 90
lonmin = -135 # full globe values -180 
lonmax = -60 # full globe values 180

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
#Plotting the data

#Instantiating the Basemap
map = Basemap( projection = 'mill', resolution = 'i',
               llcrnrlat  = latmin,  urcrnrlat = latmax,
               llcrnrlon  = lonmin,  urcrnrlon = lonmax  )

qERA, shifted_lon = shiftgrid(180., qERA, lon, start=False)  # shiftgrid
qROT, _           = shiftgrid(180., qROT, lon, start=False)  # shiftgrid
qIG,  _           = shiftgrid(180., qIG,  lon, start=False)  # shiftgrid
qM,   _           = shiftgrid(180., qM,   lon, start=False)  # shiftgrid

X , Y  = np.meshgrid(shifted_lon,lat)
xx, yy = map(X,Y)

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# MODES Contour Plots

Cfig = plt.figure(constrained_layout=True, figsize=(14,7))
gs   = Cfig.add_gridspec(2,2)

ax00 = Cfig.add_subplot(gs[0,0])
ax01 = Cfig.add_subplot(gs[0,1])
ax10 = Cfig.add_subplot(gs[1,0])
ax11 = Cfig.add_subplot(gs[1,1])

#qERA plot
ax00.set_title("a)      q_ERA (anomaly) [g/kg]")
map.ax = ax00
map.drawcoastlines(linewidth=cllw)
qERA_contour = map.contourf(xx,yy, qERA, qERA_contours, cmap=qERA_cmap)
qERA_cbar    = Cfig.colorbar(qERA_contour, ax=ax00)


#qROT plot
ax01.set_title("b)      q_ROT (anomaly) [g/kg]")
map.ax = ax01
map.drawcoastlines(linewidth=cllw)
qROT_contour = map.contourf(xx,yy, qROT, qROT_contours, cmap=qROT_cmap)
qROT_cbar    = Cfig.colorbar(qROT_contour, ax=ax01)


#qIG plot
ax10.set_title("c)      q_IG (anomaly) [g/kg]")
map.ax = ax10
map.drawcoastlines(linewidth=cllw)
qIG_contour = map.contourf(xx,yy, qIG, qIG_contours, cmap=qIG_cmap)
qIG_cbar    = Cfig.colorbar(qIG_contour, ax=ax10)


#qM plot
ax11.set_title("d)      q_M (anomaly) [g/kg]")
map.ax = ax11
map.drawcoastlines(linewidth=cllw)
qM_contour = map.contourf(xx,yy, qM, qM_contours, cmap=qM_cmap)
qM_cbar    = Cfig.colorbar(qM_contour, ax=ax11)

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Saving Plot

outputfile1   = f"../../output_data/plots/Madison_Contour_Plot_{date}_plev{iplev}.pdf"
outputfile2   = f"../../output_data/plots/Madison_Contour_Plot_{date}_plev{iplev}.jpeg"
save_bool_str = input(f"\n\nSave Plot in the following locations?(y,n):\n\t {outputfile1}\n\t{outputfile2}\n >>>")
print("\n")

if save_bool_str == 'y':
	plt.savefig(outputfile1)
	plt.savefig(outputfile2)
	print(f"Plot(s) saved to:\n\t{outputfile1}\n\t{outputfile2}\n")

plt.show()

#-------------------------------------------------------------------------
