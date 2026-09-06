#-------------------------------------------------------------------------
# Imports

from qMODES import template_ERA_fname, template_qmodes_fname
from qMODES import get_QMODES_ERA_DIR, get_QMODES_QMODESDATA_DIR, get_QMODES_PLOTS_DIR
from qMODES import read_ERA_grid_data, get_single_plev_ERA_and_flipped_qmodes_data, get_single_plev_ERA_and_flipped_qmodes_data_with_p_and_lat_dependent_background
import custom_colormap as cc



import matplotlib.pyplot  as plt
import cartopy.feature    as cfeature
import cartopy.crs        as ccrs

import xarray            as xa
import numpy             as np
import argparse
#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Getting Command Line inputs using Argparse

parser = argparse.ArgumentParser(description='This script is used to generate EIG, WIG, BAL/ROT, and M modal global atmospheric moisture plots at a given pressure level.)')
parser.add_argument('-d','--date', help='date to make the contours for',                    required=True)
parser.add_argument('-p','--plev', help='pressure level to generate the contour plots for', required=True)
parser.add_argument('-u','--updated_contours', help='Tag to allow use of updated contour profiles', action='store_true')

args   = parser.parse_args()
date   = args.date
iplev  = int(args.plev)
useUpdatedContours = args.updated_contours
#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Initial Calculations

# Input Parameters
ERA_datafile    = f"{get_QMODES_ERA_DIR()}/{template_ERA_fname(date)}"
qMODES_datafile = f"{get_QMODES_QMODESDATA_DIR()}/{template_qmodes_fname(date)}"

# Output Parameters
outputfile = f"{get_QMODES_PLOTS_DIR()}"
#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Reading in data

# Reading Grid Data
[plev, lat, lon] = read_ERA_grid_data(ERA_datafile,'plev','lat','lon')


nplev = plev.shape[0]
nlat  = lat.shape[0]
nlon  = lon.shape[0]

# Reading in ERA and qMODES data
#[qERA, qEIG, qWIG, qROT, qM] = get_single_plev_ERA_and_flipped_qmodes_data(ERA_datafile, qMODES_datafile, iplev)
[qERA, qEIG, qWIG, qROT, qM] = get_single_plev_ERA_and_flipped_qmodes_data_with_p_and_lat_dependent_background(ERA_datafile, qMODES_datafile, iplev)

## Replacing bad datapoints
#bad_lon_indicies = np.array([0]) # WARNING!! Possible indexing issues. List of points to replace	
#
#print(f"WARNING: REPLACING BAD DATA POINTS!!!")
#for blon in bad_lon_indicies:
#	#replacing bad lon values with average of two previous points at the same latitude
#	qERA[:, blon] = ( qERA[:, blon + 1] + qERA[:, blon - 1] ) / 2.0
#	qEIG[:, blon] = ( qEIG[:, blon + 1] + qEIG[:, blon - 1] ) / 2.0
#	qWIG[:, blon] = ( qWIG[:, blon + 1] + qWIG[:, blon - 1] ) / 2.0
#	qROT[:, blon] = ( qROT[:, blon + 1] + qROT[:, blon - 1] ) / 2.0
#	qM[:, blon]   = (   qM[:, blon + 1] +   qM[:, blon - 1] ) / 2.0
#print(f"BAD DATA POINTS REPLACED")

#-------------------------------------------------------------------------
#Adjusting the data 

#Changing units to g/kg and combining IG modes

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
qERA_contours = np.linspace(-10.0, 10.0,21)
qROT_contours = np.linspace(-4.0,  4.0, 21)
qIG_contours  = np.linspace(-2.0,  2.0, 21)
qM_contours   = np.linspace(-10.0, 10.0,21)

if useUpdatedContours:
	qERA_contours = np.linspace(-5.0,  5.0, 21)
	qROT_contours = np.linspace(-2.0,  2.0, 21)
	qIG_contours  = np.linspace(-1.0,  1.0, 21)
	qM_contours   = np.linspace(-5.0,  5.0, 21)

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

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Saving Plot
outputfile1 = f"{get_QMODES_PLOTS_DIR()}/{useUpdatedContours * "updated-contours_"}Global_qMODES_{date}_plev{plev[iplev]}.pdf"
outputfile2 = f"{get_QMODES_PLOTS_DIR()}/{useUpdatedContours * "updated-contours_"}Global_qMODES_{date}_plev{plev[iplev]}.jpeg"

plt.savefig(outputfile1)
plt.savefig(outputfile2)

print(f"\nPlot(s) saved to:\n\t{outputfile1}\n\t{outputfile2}\n")

#-------------------------------------------------------------------------



