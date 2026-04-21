#-------------------------------------------------------------------------
# Imports
from qMODES import get_QMODES_PLOTS_DIR, get_QMODES_ERA_DIR, get_QMODES_QMODESDATA_DIR
from qMODES import template_ERA_fname, template_qmodes_fname, template_ERA_uv_fname
from qMODES import read_ERA_grid_data, get_single_plev_ERA_and_flippedMODES_q_data, get_single_plev_ERA_and_flippedMODES_q_data_with_p_and_lat_dependent_background

import cartopy.feature        as cfeature
import cartopy.crs            as ccrs
import cartopy.mpl.ticker     as cticker
import cartopy.io.shapereader as shpreader


from shapely.geometry import Point

import matplotlib.pyplot as plt
import xarray            as xa
import numpy             as np
import custom_colormap   as cc

import argparse
#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Custom Functions used in script
def get_state_geometry(state_name):
    # Fetch the Natural Earth states and provinces shapefile
    shpfilename = shpreader.natural_earth(
        resolution='10m',  # Use '10m' for highest detail
        category='cultural',
        name='admin_1_states_provinces_lakes'
    )
    reader = shpreader.Reader(shpfilename)

    # Iterate through records to find the specific state
    for state in reader.records():
        # Check the 'name' attribute for the desired state
        if state.attributes['name'] == state_name:
            return state.geometry
    return None


#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Getting Command Line inputs using Argparse

parser = argparse.ArgumentParser(description='This script is used to generate pressure level contour plots for an event over a specific region (originally Madison WI)')
parser.add_argument('-d','--date', help='date to make the contours for', required=True)
parser.add_argument('-p','--plev', help='pressure level to generate the contour plots for', required=True)
parser.add_argument('-u','--updated_contours', help='Tag to allow use of updated contour profiles', action='store_true')
parser.add_argument('-w','--wind', help='add horizontal wind vectors to the plot', action='store_true')

args   = parser.parse_args()
date   = args.date
iplev  = int( args.plev )
include_wind = args.wind
useUpdatedContours = args.updated_contours
#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Initial Calculations

# Input Parameters
ERA_q_datafile  = f"{get_QMODES_ERA_DIR()}/{template_ERA_fname(date)}"
qMODES_datafile = f"{get_QMODES_QMODESDATA_DIR()}/{template_qmodes_fname(date)}"

if include_wind: ERA_uv_datafile = f"{get_QMODES_ERA_DIR()}/{template_ERA_uv_fname(date)}"

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Reading in data

# Reading Grid Data
[plev, lat, lon] = read_ERA_grid_data(ERA_q_datafile,'plev','lat','lon')

nplev = plev.shape[0]
nlat  = lat.shape[0]
nlon  = lon.shape[0]

# Reading in ERA and qMODES data
#[qERA, qEIG, qWIG, qROT, qM] = get_single_plev_ERA_and_flippedMODES_q_data(ERA_q_datafile, qMODES_datafile, iplev)
[qERA, qEIG, qWIG, qROT, qM] = get_single_plev_ERA_and_flippedMODES_q_data_with_p_and_lat_dependent_background(ERA_q_datafile, qMODES_datafile, iplev)

# Replacing bad datapoints
bad_lon_indicies = np.array([0]) # WARNING!! Possible indexing issues. List of points to replace	

print(f"WARNING: REPLACING BAD DATA POINTS!!!")
for blon in bad_lon_indicies:

	#replacing bad lon values with average of two previous points at the same latitude
	qERA[:, blon] = ( qERA[:, blon + 1] + qERA[:, blon - 1] ) / 2.0
	qEIG[:, blon] = ( qEIG[:, blon + 1] + qEIG[:, blon - 1] ) / 2.0
	qWIG[:, blon] = ( qWIG[:, blon + 1] + qWIG[:, blon - 1] ) / 2.0
	qROT[:, blon] = ( qROT[:, blon + 1] + qROT[:, blon - 1] ) / 2.0
	qM[:, blon]   = (   qM[:, blon + 1] +   qM[:, blon - 1] ) / 2.0
print(f"BAD DATA POINTS REPLACED")

# reading in horizontal wind (u & v) data
if include_wind:
	uv_ds = xa.open_dataset(ERA_uv_datafile)
	u = uv_ds['u'].values
	v = uv_ds['v'].values
	u = u[0,iplev,:,:]
	v = v[0,iplev,:,:]
#-------------------------------------------------------------------------
#Adjusting the data 

#Changing units to g/kg and adding IG modes

qERA = 1000.0 * qERA
qROT = 1000.0 * qROT
qIG  = 1000.0 * (qEIG + qWIG)
qM   = 1000.0 * qM
#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
#Setting Plot Parameters

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

# Setting Plot Grid Parameters
lonmin = -135 # full globe values -180 
lonmax = -60 # full globe values 180
latmin = 20   # full globe values -90
latmax = 70   # full globe values 90

proj = ccrs.Miller() #projection
regional_extent = [lonmin, lonmax, latmin, latmax]

lon, lat = np.meshgrid(lon, lat)

# skip function used determine number of wind vectors to draw
skip = (slice(None, None, 10), slice(None, None, 10))

arrow_scale = 400
arrow_color = "black"
arrow_width = 0.0025

# Getting WI geometry
wisconsin_geom = get_state_geometry('Wisconsin')


# Generating Figure and Subplots
Cfig, [[ax00, ax01], [ax10, ax11]] = plt.subplots(nrows=2, ncols=2, figsize=(12,8), subplot_kw={'projection': proj})

# qERA plot
ax00.set_title("a)      q_ERA (anomaly) [g/kg]")
ax00.set_extent(regional_extent, crs=ccrs.PlateCarree())
qERA_contour = ax00.contourf(lon, lat, qERA, qERA_contours, transform=ccrs.PlateCarree(), cmap=qERA_cmap, extend='both')
ax00.add_feature(cfeature.COASTLINE)
ax00.add_feature(cfeature.LAKES, facecolor='none', edgecolor='black')
ax00.add_geometries(
        [wisconsin_geom],  # Must be a collection (list) of geometries
        crs=ccrs.PlateCarree(),
        edgecolor='seagreen',   # Outline color
        facecolor='none',  # No fill
        linewidth=1.75
    )
if include_wind:
	qERA_wind = ax00.quiver(lon[skip], lat[skip], u[skip], v[skip],
		                    transform=ccrs.PlateCarree(), scale=arrow_scale, color=arrow_color, width=arrow_width)
qROT_cbar    = Cfig.colorbar(qERA_contour, ax=ax00)

# qROT plot
ax01.set_title("b)      q_ROT (anomaly) [g/kg]")
ax01.set_extent(regional_extent, crs=ccrs.PlateCarree())
qROT_contour = ax01.contourf(lon, lat, qROT, qROT_contours, transform=ccrs.PlateCarree(), cmap=qROT_cmap, extend='both')
ax01.add_feature(cfeature.COASTLINE)
ax01.add_feature(cfeature.LAKES, facecolor='none', edgecolor='black')
ax01.add_geometries(
        [wisconsin_geom],  # Must be a collection (list) of geometries
        crs=ccrs.PlateCarree(),
        edgecolor='seagreen',   # Outline color
        facecolor='none',  # No fill
        linewidth=1.75
    )
if include_wind:
	qROT_wind = ax01.quiver(lon[skip], lat[skip], u[skip], v[skip],
		                    transform=ccrs.PlateCarree(), scale=arrow_scale, color=arrow_color, width=arrow_width)
qROT_cbar    = Cfig.colorbar(qROT_contour, ax=ax01)

# qIG plot
ax10.set_title("c)      q_IG (anomaly) [g/kg]")
ax10.set_extent(regional_extent, crs=ccrs.PlateCarree())
qIG_contour = ax10.contourf(lon, lat, qIG, qIG_contours, transform=ccrs.PlateCarree(), cmap=qIG_cmap, extend='both')
ax10.add_feature(cfeature.COASTLINE)
ax10.add_feature(cfeature.LAKES, facecolor='none', edgecolor='black')
ax10.add_geometries(
        [wisconsin_geom],  # Must be a collection (list) of geometries
        crs=ccrs.PlateCarree(),
        edgecolor='seagreen',   # Outline color
        facecolor='none',  # No fill
        linewidth=1.75
    )
if include_wind:
	qIG_wind = ax10.quiver(lon[skip], lat[skip], u[skip], v[skip],
		                   transform=ccrs.PlateCarree(), scale=arrow_scale, color=arrow_color, width=arrow_width)
qIG_cbar    = Cfig.colorbar(qIG_contour, ax=ax10)

# qM plot
ax11.set_title("d)      q_M (anomaly) [g/kg]")
ax11.set_extent(regional_extent, crs=ccrs.PlateCarree())
qM_contour = ax11.contourf(lon, lat, qM, qM_contours, transform=ccrs.PlateCarree(), cmap=qM_cmap, extend='both')
ax11.add_feature(cfeature.COASTLINE)
ax11.add_feature(cfeature.LAKES, facecolor='none', edgecolor='black')
ax11.add_geometries(
        [wisconsin_geom],  # Must be a collection (list) of geometries
        crs=ccrs.PlateCarree(),
        edgecolor='seagreen',   # Outline color
        facecolor='none',  # No fill
        linewidth=1.75
    )
if include_wind:
	qM_wind = ax11.quiver(lon[skip], lat[skip], u[skip], v[skip],
		                  transform=ccrs.PlateCarree(), scale=arrow_scale, color=arrow_color, width=arrow_width)
qM_cbar    = Cfig.colorbar(qM_contour, ax=ax11)
#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Saving Plot
outputfile1 = f"{get_QMODES_PLOTS_DIR()}/{useUpdatedContours * "updated-contours_"}Madison_qmodes_contour_plot_{include_wind * 'with_windvectors_'}{date}_plev{plev[iplev]}_with_WI_outline.pdf"
outputfile2 = f"{get_QMODES_PLOTS_DIR()}/{useUpdatedContours * "updated-contours_"}Madison_qmodes_contour_plot_{include_wind * 'with_windvectors_'}{date}_plev{plev[iplev]}_with_WI_outline.jpeg"
 
plt.savefig(outputfile1)
plt.savefig(outputfile2)

print(f"Plot(s) saved to:\n\t{outputfile1}\n\t{outputfile2}\n")
#-------------------------------------------------------------------------



