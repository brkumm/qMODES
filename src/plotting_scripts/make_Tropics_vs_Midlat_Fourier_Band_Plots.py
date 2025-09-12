#-------------------------------------------------------------------------
# Imports
from mpl_toolkits.basemap import Basemap, shiftgrid
from matplotlib.patches   import Polygon
from OmegaMODES_Functions import read_ERA_grid_data, get_single_plev_ERA_and_flippedMODES_q_data, get_single_plev_ERA_and_flippedMODES_q_data_with_p_and_lat_dependent_background

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
# Custom Functions used in script

#Function to draw the banded regions
def draw_screen_poly( lats, lons, bmap, clr, alp):
    x, y = bmap( lons, lats)
    xy   = zip(x,y)
    poly = Polygon( list(xy), facecolor=clr, alpha=alp, edgecolor='k' )
    bmap.ax.add_patch(poly)

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
# Input, Script, and Output Parameters

# Input Parameters
ERA_datafile    = f"../../ERA_Data/ERA_{date}_q_pl_data.nc"           # (ntime:1, nplev:137, nlat:640, nlon:1280)
qMODES_datafile = f"../../output_data/qMODES_Data/qMODES_{date}0000000.nc" # (nplev:137, nlat:640, nlon:1280)

# Script/Plotting Parameters
ilat       = 150 #latitude index to perform the FFT along
ilat_delta = 20 # number of lat indicies above and below that are included in the "average FFT"
MidlatN_indicies =  [105, 213] # 45 N +- 15 deg      ########[123, 195] # 45 N +- 10 deg
Tropics_indicies =  [266, 373] # 0    +- 15 deg      ########[283, 356] # 0    +- 10 deg
MidlatS_indicies =  [426, 534] # 45 S +- 15 deg      ########[444, 516] # 45 S +- 10 deg


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

#Changing units to g/kg and adding IG modes
qERA = 1000.0 * qERA
qROT = 1000.0 * qROT
qEIG = 1000.0 * qEIG
qWIG = 1000.0 * qWIG
qM   = 1000.0 * qM

qIG  = qEIG + qWIG

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
#Calculations

#Calculating the averages for the 3 regions

MidlatN_qERA_avg = np.mean( qERA[MidlatN_indicies[0]:MidlatN_indicies[1]+1, :], 0)
MidlatN_qROT_avg = np.mean( qROT[MidlatN_indicies[0]:MidlatN_indicies[1]+1, :], 0)
MidlatN_qIG_avg  = np.mean(  qIG[MidlatN_indicies[0]:MidlatN_indicies[1]+1, :], 0)
MidlatN_qM_avg   = np.mean(   qM[MidlatN_indicies[0]:MidlatN_indicies[1]+1, :], 0)


Tropics_qERA_avg = np.mean( qERA[Tropics_indicies[0]:Tropics_indicies[1]+1, :], 0)
Tropics_qROT_avg = np.mean( qROT[Tropics_indicies[0]:Tropics_indicies[1]+1, :], 0)
Tropics_qIG_avg  = np.mean(  qIG[Tropics_indicies[0]:Tropics_indicies[1]+1, :], 0)
Tropics_qM_avg   = np.mean(   qM[Tropics_indicies[0]:Tropics_indicies[1]+1, :], 0)


MidlatS_qERA_avg = np.mean( qERA[MidlatS_indicies[0]:MidlatS_indicies[1]+1, :], 0)
MidlatS_qROT_avg = np.mean( qROT[MidlatS_indicies[0]:MidlatS_indicies[1]+1, :], 0)
MidlatS_qIG_avg  = np.mean(  qIG[MidlatS_indicies[0]:MidlatS_indicies[1]+1, :], 0)
MidlatS_qM_avg   = np.mean(   qM[MidlatS_indicies[0]:MidlatS_indicies[1]+1, :], 0)

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Calculating the FFTs

qERA_FFT = np.fft.fft( qERA[ilat,:] ) / nlon 
qROT_FFT = np.fft.fft( qROT[ilat,:] ) / nlon 
qIG_FFT  = np.fft.fft( qIG[ilat, :] ) / nlon 
qM_FFT   = np.fft.fft( qM[ilat,  :] ) / nlon 


MidlatN_qERA_FFT = np.fft.fft( MidlatN_qERA_avg ) / nlon
MidlatN_qROT_FFT = np.fft.fft( MidlatN_qROT_avg ) / nlon
MidlatN_qIG_FFT  = np.fft.fft( MidlatN_qIG_avg  ) / nlon
MidlatN_qM_FFT   = np.fft.fft( MidlatN_qM_avg   ) / nlon

Tropics_qERA_FFT = np.fft.fft( Tropics_qERA_avg ) / nlon
Tropics_qROT_FFT = np.fft.fft( Tropics_qROT_avg ) / nlon
Tropics_qIG_FFT  = np.fft.fft( Tropics_qIG_avg  ) / nlon
Tropics_qM_FFT   = np.fft.fft( Tropics_qM_avg   ) / nlon

MidlatS_qERA_FFT = np.fft.fft( MidlatS_qERA_avg ) / nlon
MidlatS_qROT_FFT = np.fft.fft( MidlatS_qROT_avg ) / nlon
MidlatS_qIG_FFT  = np.fft.fft( MidlatS_qIG_avg  ) / nlon
MidlatS_qM_FFT   = np.fft.fft( MidlatS_qM_avg   ) / nlon

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
#Setting Plot Parameters
cllw = 0.5
latmin = -90
latmax = 90
lonmin = -180
lonmax = 180

qERA_line_color = "blue"
qROT_line_color = "green"
qIG_line_color  = "orange"
qM_line_color   = "red"

band_alpha       = 0.20 # setting alpha value (transparancy) of the band region
line_alpha       = 0.75

# Coreners of regions for drawing rectangle over region
MidlatN_lats = [lat[MidlatN_indicies[0]], lat[MidlatN_indicies[1]], lat[MidlatN_indicies[1]], lat[MidlatN_indicies[0]] ]
MidlatN_lons = [lonmin,                   lonmin,                   lonmax,                   lonmax                   ]

Tropics_lats = [lat[Tropics_indicies[0]], lat[Tropics_indicies[1]], lat[Tropics_indicies[1]], lat[Tropics_indicies[0]] ]
Tropics_lons = [lonmin,                   lonmin,                   lonmax,                   lonmax                   ]

MidlatS_lats = [lat[MidlatS_indicies[0]], lat[MidlatS_indicies[1]], lat[MidlatS_indicies[1]], lat[MidlatS_indicies[0]] ]
MidlatS_lons = [lonmin,                   lonmin,                   lonmax,                   lonmax                   ]

# Plot Contours and Colormap info
qERA_contours = np.linspace(-10.0, 10.0,21)
qROT_contours = np.linspace(-4.0,  4.0, 21)
qEIG_contours = np.linspace(-1.0,  1.0, 21)
qWIG_contours = np.linspace(-1.0,  1.0, 21)
qIG_contours  = np.linspace(-2.0,  2.0, 21)
qM_contours   = np.linspace(-10.0, 10.0,21)

qERA_cmap     = cc.get_my_colormap( qERA_contours )
qROT_cmap     = cc.get_my_colormap( qROT_contours )
qIG_cmap      = cc.get_my_colormap( qIG_contours  )
qM_cmap       = cc.get_my_colormap( qM_contours   )

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
#Plotting the data

map = Basemap( projection = 'robin', lon_0=0, resolution = 'i',
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

Cfig = plt.figure(constrained_layout=True, figsize=(12,6))
gs   = Cfig.add_gridspec(2,2)

ax00 = Cfig.add_subplot(gs[0,0])
ax01 = Cfig.add_subplot(gs[0,1])
ax10 = Cfig.add_subplot(gs[1,0])
ax11 = Cfig.add_subplot(gs[1,1])

#qERA plot
ax00.set_title("q_ERA (anomaly) [g/kg]")
map.ax = ax00
map.drawcoastlines(linewidth=cllw)
qERA_contour = map.contourf(xx,yy, qERA, qERA_contours, cmap=qERA_cmap)
qERA_cbar    = Cfig.colorbar(qERA_contour, ax=ax00)
draw_screen_poly( MidlatN_lats, MidlatN_lons, map, qERA_line_color, band_alpha)
draw_screen_poly( Tropics_lats, Tropics_lons, map, qERA_line_color, band_alpha)
draw_screen_poly( MidlatS_lats, MidlatS_lons, map, qERA_line_color, band_alpha)


#qROT plot
ax01.set_title("q_ROT (anomaly) [g/kg]")
map.ax = ax01
map.drawcoastlines(linewidth=cllw)
qROT_contour = map.contourf(xx,yy, qROT, qROT_contours, cmap=qROT_cmap)
qROT_cbar    = Cfig.colorbar(qROT_contour, ax=ax01)
draw_screen_poly( MidlatN_lats, MidlatN_lons, map, qROT_line_color, band_alpha)
draw_screen_poly( Tropics_lats, Tropics_lons, map, qROT_line_color, band_alpha)
draw_screen_poly( MidlatS_lats, MidlatS_lons, map, qROT_line_color, band_alpha)


#qIG plot
ax10.set_title("q_IG (anomaly) [g/kg]")
map.ax = ax10
map.drawcoastlines(linewidth=cllw)
qIG_contour = map.contourf(xx,yy, qIG, qIG_contours, cmap=qIG_cmap)
qIG_cbar    = Cfig.colorbar(qIG_contour, ax=ax10)
draw_screen_poly( MidlatN_lats, MidlatN_lons, map, qIG_line_color, band_alpha)
draw_screen_poly( Tropics_lats, Tropics_lons, map, qIG_line_color, band_alpha)
draw_screen_poly( MidlatS_lats, MidlatS_lons, map, qIG_line_color, band_alpha)


#qM plot
ax11.set_title("q_M (anomaly) [g/kg]")
map.ax = ax11
map.drawcoastlines(linewidth=cllw)
qM_contour = map.contourf(xx,yy, qM, qM_contours, cmap=qM_cmap)
qM_cbar    = Cfig.colorbar(qM_contour, ax=ax11)
draw_screen_poly( MidlatN_lats, MidlatN_lons, map, qM_line_color, band_alpha)
draw_screen_poly( Tropics_lats, Tropics_lons, map, qM_line_color, band_alpha)
draw_screen_poly( MidlatS_lats, MidlatS_lons, map, qM_line_color, band_alpha)

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Profile and FFT Plots

FFTfig = plt.figure(constrained_layout=True, figsize=(14,8))
gs   = FFTfig.add_gridspec(2,3)

ax00 = FFTfig.add_subplot(gs[0,0])
ax10 = FFTfig.add_subplot(gs[1,0])
ax01 = FFTfig.add_subplot(gs[0,1])
ax11 = FFTfig.add_subplot(gs[1,1])
ax02 = FFTfig.add_subplot(gs[0,2])
ax12 = FFTfig.add_subplot(gs[1,2])

# Northern Midlat Plots
ax00.set_title(f"a)     Northern Midlatitude Profiles")
ax00.set_xlabel(f"Longitude [deg]")
ax00.set_ylabel(f"Averaged q Anomalies [g/kg]")
ax00.plot( lon, MidlatN_qERA_avg, color=qERA_line_color, label='qERA', alpha=line_alpha)
ax00.plot( lon, MidlatN_qROT_avg, color=qROT_line_color, label='qROT', alpha=line_alpha)
ax00.plot( lon, MidlatN_qIG_avg , color=qIG_line_color,  label='qIG' , alpha=line_alpha)
ax00.plot( lon, MidlatN_qM_avg  , color=qM_line_color  , label='qM ' , alpha=line_alpha)
ax00.legend()

ax10.set_title(f"d)     Northern Midlatitude FFTs")
ax10.set_xlabel("Wavenumber k")
ax10.set_ylabel("FFT Amplitude")
ax10.plot( np.abs( MidlatN_qERA_FFT[:int(nlon/2)] ), color=qERA_line_color, label='qERA_FFT', alpha=line_alpha)
ax10.plot( np.abs( MidlatN_qROT_FFT[:int(nlon/2)] ), color=qROT_line_color, label='qROT_FFT', alpha=line_alpha)
ax10.plot( np.abs( MidlatN_qIG_FFT[:int(nlon/2) ] ), color=qIG_line_color,  label='qIG_FFT' , alpha=line_alpha)
ax10.plot( np.abs( MidlatN_qM_FFT[:int(nlon/2)  ] ), color=qM_line_color ,  label='qM_FFT'  , alpha=line_alpha)
ax10.set_xlim([0,351])
#ax10.set_ylim()
ax10.set_yscale('log')
ax10.legend()

# Tropics Midlat Plots
ax01.set_title(f"b)     Tropics Profiles")
ax01.set_xlabel(f"Longitude [deg]")
ax01.set_ylabel(f"q Anomalies [g/kg]")
ax01.plot( lon, Tropics_qERA_avg, color=qERA_line_color, label='qERA', alpha=line_alpha)
ax01.plot( lon, Tropics_qROT_avg, color=qROT_line_color, label='qROT', alpha=line_alpha)
ax01.plot( lon, Tropics_qIG_avg , color=qIG_line_color,  label='qIG' , alpha=line_alpha)
ax01.plot( lon, Tropics_qM_avg  , color=qM_line_color  , label='qM ' , alpha=line_alpha)
ax01.legend()

ax11.set_title(f"e)     Tropics FFTs")
ax11.set_xlabel("Wavenumber k")
ax11.set_ylabel("FFT Amplitude")
ax11.plot( np.abs( Tropics_qERA_FFT[:int(nlon/2)] ), color=qERA_line_color, label='qERA_FFT', alpha=line_alpha)
ax11.plot( np.abs( Tropics_qROT_FFT[:int(nlon/2)] ), color=qROT_line_color, label='qROT_FFT', alpha=line_alpha)
ax11.plot( np.abs( Tropics_qIG_FFT[:int(nlon/2) ] ), color=qIG_line_color,  label='qIG_FFT' , alpha=line_alpha)
ax11.plot( np.abs( Tropics_qM_FFT[:int(nlon/2)  ] ), color=qM_line_color ,  label='qM_FFT'  , alpha=line_alpha)
ax11.set_xlim([0,351])
#ax11.set_ylim()
ax11.set_yscale('log')
ax11.legend()

# Southern Midlat Plots
ax02.set_title(f"c)     Southern Midlatitude Profiles")
ax02.set_xlabel(f"Longitude [deg]")
ax02.set_ylabel(f"q Anomalies [g/kg]")
ax02.plot( lon, MidlatS_qERA_avg, color=qERA_line_color, label='qERA', alpha=line_alpha)
ax02.plot( lon, MidlatS_qROT_avg, color=qROT_line_color, label='qROT', alpha=line_alpha)
ax02.plot( lon, MidlatS_qIG_avg , color=qIG_line_color,  label='qIG' , alpha=line_alpha)
ax02.plot( lon, MidlatS_qM_avg  , color=qM_line_color  , label='qM ' , alpha=line_alpha)
ax02.legend()

ax12.set_title(f"f)     Southern Midlatitude FFTs")
ax12.set_xlabel("Wavenumber k")
ax12.set_ylabel("FFT Amplitude")
ax12.plot( np.abs( MidlatS_qERA_FFT[:int(nlon/2)] ), color=qERA_line_color, label='qERA_FFT', alpha=line_alpha)
ax12.plot( np.abs( MidlatS_qROT_FFT[:int(nlon/2)] ), color=qROT_line_color, label='qROT_FFT', alpha=line_alpha)
ax12.plot( np.abs( MidlatS_qIG_FFT[:int(nlon/2) ] ), color=qIG_line_color,  label='qIG_FFT' , alpha=line_alpha)
ax12.plot( np.abs( MidlatS_qM_FFT[:int(nlon/2)  ] ), color=qM_line_color ,  label='qM_FFT'  , alpha=line_alpha)
ax12.set_xlim([0,351])
ax12.set_yscale('log')
ax12.legend()

plt.show()

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
#Saving Figures


Contour_save_bool_str = input(f"\n\nSave Regional Contour Plot(s) in the following locations?:\n\t {Contour_outfile1}\n\t{Contour_outfile2}\n >>>(y/n):")
print("\n")

if Contour_save_bool_str == 'y':
	Contour_outfile1 = f"../../output_data/plots/qMODES_Fourier_Regional_Contours_{date}_plev{iplev}.pdf"
	Contour_outfile2 = f"../../output_data/plots/qMODES_Fourier_Regional_Contours_{date}_plev{iplev}.jpeg"

	Cfig.savefig(Contour_outfile1)
	Cfig.savefig(Contour_outfile2)
	print(f"Profile Plot(s) saved to:\n\t{Contour_outfile1}\n\t{Contour_outfile2}\n")


FFT_save_bool_str = input(f"\n\nSave FFT Regional Plot(s) in the following locations?:\n\t {FFT_outfile1}\n\t{FFT_outfile2}\n >>>(y/n):")
print("\n")

if FFT_save_bool_str == 'y':
	FFT_outfile1 = f"../../output_data/plots/qMODES_Fourier_Regional_FFT_{date}_plev{iplev}.pdf"
	FFT_outfile2 = f"../../output_data/plots/qMODES_Fourier_Regional_FFT_{date}_plev{iplev}.jpeg"

	FFTfig.savefig(FFT_outfile1)
	FFTfig.savefig(FFT_outfile2)
	print(f"FFT Plot(s) saved to:\n\t{FFT_outfile1}\n\t{FFT_outfile2}\n")

#-------------------------------------------------------------------------
