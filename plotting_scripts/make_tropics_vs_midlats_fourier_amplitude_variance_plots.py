#-------------------------------------------------------------------------
# Imports
from qMODES import read_ERA_grid_data, get_single_plev_ERA_and_flipped_qmodes_data, get_single_plev_ERA_and_flipped_qmodes_data_with_p_and_lat_dependent_background
from qMODES import get_QMODES_PLOTS_DIR, get_QMODES_ERA_DIR, get_QMODES_QMODESDATA_DIR
from qMODES import template_ERA_fname, template_qmodes_fname

import cartopy.feature    as cfeature
import cartopy.crs        as ccrs
import cartopy.mpl.ticker as cticker
from   cartopy.util       import add_cyclic_point

import matplotlib.pyplot  as plt
import matplotlib.patches as mpatches
import xarray             as xa
import numpy              as np
import custom_colormap    as cc
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
# Input, Script, and Output Parameters

# Input Parameters
ERA_datafile    = f"{get_QMODES_ERA_DIR()}/{template_ERA_fname(date)}"           # (time:1, plev:137, lat:640, lon:1280)
qMODES_datafile = f"{get_QMODES_QMODESDATA_DIR()}/{template_qmodes_fname(date)}" # (plev:137, lat:640, lon:1280)

# Script Parameters
ilat       = 150 #latitude index to perform the FFT along
ilat_delta = 20 # number of lat indicies above and below that are included in the "average FFT"
MidlatN_indicies =  [105, 213] # 45 N +- 15 deg      ########[123, 195] # 45 N +- 10 deg
Tropics_indicies =  [266, 373] # 0    +- 15 deg      ########[283, 356] # 0    +- 10 deg
MidlatS_indicies =  [426, 534] # 45 S +- 15 deg      ########[444, 516] # 45 S +- 10 deg

nMidlatN = len(MidlatN_indicies)
nTropics = len(Tropics_indicies)
nMidlatS = len(MidlatS_indicies)


# # Output Parameters
# outfile = "/Users/bkumm/Desktop/qmodes/plots/Preliminary_Fourier_Band_Plot"

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Reading in data

# Reading Grid Data
[plev, lat, lon] = read_ERA_grid_data(ERA_datafile,'plev','lat','lon')

nplev = plev.shape[0]
nlat  = lat.shape[0]
nlon  = lon.shape[0]
nFFT  = int(nlon/2) 

#printing lat ranges for each band
print("\nThe latitude ranges for each region are:")
print(f"\tMidlatN: {lat[MidlatN_indicies[0]]} -- {lat[MidlatN_indicies[1]]}")
print(f"\tTropics: {lat[Tropics_indicies[0]]} -- {lat[Tropics_indicies[1]]}")
print(f"\tMidlatS: {lat[MidlatS_indicies[0]]} -- {lat[MidlatS_indicies[1]]}")

# Reading in ERA and qMODES data

[qERA, qEIG, qWIG, qROT, qM] = get_single_plev_ERA_and_flipped_qmodes_data_with_p_and_lat_dependent_background(ERA_datafile, qMODES_datafile, iplev)

# Replacing bad datapoints
bad_lon_indicies = np.array([0]) # WARNING!! Possible indexing issues. List of points to replace	

for blon in bad_lon_indicies:

	print(f"WARNING: REPLACING BAD DATA POINTS!!!")

	#replacing bad lon values with average of two previous points at the same latitude
	qERA[:, blon] = ( qERA[:, blon + 1] + qERA[:, blon - 1] ) / 2.0
	qEIG[:, blon] = ( qEIG[:, blon + 1] + qEIG[:, blon - 1] ) / 2.0
	qWIG[:, blon] = ( qWIG[:, blon + 1] + qWIG[:, blon - 1] ) / 2.0
	qROT[:, blon] = ( qROT[:, blon + 1] + qROT[:, blon - 1] ) / 2.0
	qM[:, blon]   = (   qM[:, blon + 1] +   qM[:, blon - 1] ) / 2.0

#Changing units to g/kg and adding IG modes
qERA = 1000.0 * qERA
qROT = 1000.0 * qROT
qEIG = 1000.0 * qEIG
qWIG = 1000.0 * qWIG
qM   = 1000.0 * qM

qIG  = qEIG + qWIG
#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# CALCULATING FFTS AND VARIANCE OF FFT AMPLITUDES

# Initializing vars
qERA_FFT = np.zeros([int(nFFT)])
qROT_FFT = np.zeros([int(nFFT)])
qIG_FFT  = np.zeros([int(nFFT)])
qM_FFT   = np.zeros([int(nFFT)])
MidlatN_qERA_FFT_var = np.zeros([nFFT])
MidlatN_qROT_FFT_var = np.zeros([nFFT])
MidlatN_qIG_FFT_var  = np.zeros([nFFT])
MidlatN_qM_FFT_var   = np.zeros([nFFT])

# Looping to add up FFT variances
for i in range(nMidlatN):

	ilat = MidlatN_indicies[i]

	qERA_FFT = np.fft.fft( qERA[ilat, :] )
	qROT_FFT = np.fft.fft( qROT[ilat, :] )
	qIG_FFT  = np.fft.fft( qIG[ilat, :]  )
	qM_FFT   = np.fft.fft( qM[ilat, :]   )

	for iFFT in range(nFFT):

		MidlatN_qERA_FFT_var[iFFT] += np.abs(qERA_FFT[iFFT]) * np.abs(qERA_FFT[iFFT])
		MidlatN_qROT_FFT_var[iFFT] += np.abs(qROT_FFT[iFFT]) * np.abs(qROT_FFT[iFFT])
		MidlatN_qIG_FFT_var[iFFT]  += np.abs(qIG_FFT[iFFT])  * np.abs(qIG_FFT[iFFT])
		MidlatN_qM_FFT_var[iFFT]   += np.abs(qM_FFT[iFFT])   * np.abs(qM_FFT[iFFT])

MidlatN_qERA_FFT_var /= nMidlatN 
MidlatN_qROT_FFT_var /= nMidlatN 
MidlatN_qIG_FFT_var  /= nMidlatN 
MidlatN_qM_FFT_var   /= nMidlatN   

# Tropics FFT Variance Calcs

# initializing FFT_var with zeros
Tropics_qERA_FFT_var = np.zeros([nFFT])
Tropics_qROT_FFT_var = np.zeros([nFFT])
Tropics_qIG_FFT_var  = np.zeros([nFFT])
Tropics_qM_FFT_var   = np.zeros([nFFT])
# Looping to add up FFT variances
for i in range(nTropics):

	ilat = Tropics_indicies[i]

	qERA_FFT = np.fft.fft( qERA[ilat, :] )
	qROT_FFT = np.fft.fft( qROT[ilat, :] )
	qIG_FFT  = np.fft.fft( qIG[ilat, :]  )
	qM_FFT   = np.fft.fft( qM[ilat, :]   )

	for iFFT in range(nFFT):
		
		Tropics_qERA_FFT_var[iFFT] += np.abs(qERA_FFT[iFFT]) * np.abs(qERA_FFT[iFFT])
		Tropics_qROT_FFT_var[iFFT] += np.abs(qROT_FFT[iFFT]) * np.abs(qROT_FFT[iFFT])
		Tropics_qIG_FFT_var[iFFT]  += np.abs(qIG_FFT[iFFT])  * np.abs(qIG_FFT[iFFT])
		Tropics_qM_FFT_var[iFFT]   += np.abs(qM_FFT[iFFT])   * np.abs(qM_FFT[iFFT])

Tropics_qERA_FFT_var /= nTropics 
Tropics_qROT_FFT_var /= nTropics 
Tropics_qIG_FFT_var  /= nTropics 
Tropics_qM_FFT_var   /= nTropics 

# MidlatS FFT Variance Calcs

# initializing FFT_var with zeros
MidlatS_qERA_FFT_var = np.zeros([nFFT])
MidlatS_qROT_FFT_var = np.zeros([nFFT])
MidlatS_qIG_FFT_var  = np.zeros([nFFT])
MidlatS_qM_FFT_var   = np.zeros([nFFT])
# Looping to add up FFT variances
for i in range(nMidlatS):

	ilat = MidlatS_indicies[i]

	qERA_FFT = np.fft.fft( qERA[ilat, :] )
	qROT_FFT = np.fft.fft( qROT[ilat, :] )
	qIG_FFT  = np.fft.fft( qIG[ilat, :]  )
	qM_FFT   = np.fft.fft( qM[ilat, :]   )

	for iFFT in range(nFFT):
		
		MidlatS_qERA_FFT_var[iFFT] += np.abs(qERA_FFT[iFFT]) * np.abs(qERA_FFT[iFFT])
		MidlatS_qROT_FFT_var[iFFT] += np.abs(qROT_FFT[iFFT]) * np.abs(qROT_FFT[iFFT])
		MidlatS_qIG_FFT_var[iFFT]  += np.abs(qIG_FFT[iFFT])  * np.abs(qIG_FFT[iFFT])
		MidlatS_qM_FFT_var[iFFT]   += np.abs(qM_FFT[iFFT])   * np.abs(qM_FFT[iFFT])

MidlatS_qERA_FFT_var /= nMidlatS 
MidlatS_qROT_FFT_var /= nMidlatS 
MidlatS_qIG_FFT_var  /= nMidlatS 
MidlatS_qM_FFT_var   /= nMidlatS


# Average profiles

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
# PLOTTING THE DATA

# Setting plot parameters

qERA_line_color = "blue"
qROT_line_color = "green"
qIG_line_color  = "orange"
qM_line_color   = "red"

line_alpha       = 0.75 # Setting line transparancy

qERA_contours = np.linspace(-10.0, 10.0,21) #New Contours
qROT_contours = np.linspace(-4.0,  4.0, 21) #New Contours
qEIG_contours = np.linspace(-1.0,  1.0, 21) #New Contours
qWIG_contours = np.linspace(-1.0,  1.0, 21) #New Contours
qIG_contours  = np.linspace(-2.0,  2.0, 21) #New Contours
qM_contours   = np.linspace(-10.0, 10.0,21) #New Contours

qERA_cmap     = cc.get_my_colormap( qERA_contours )
qROT_cmap     = cc.get_my_colormap( qROT_contours )
qIG_cmap      = cc.get_my_colormap( qIG_contours  )
qM_cmap       = cc.get_my_colormap( qM_contours   )

# Setting up figure
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
ax00.legend(loc='upper right')

ax10.set_title(f"d)     Northern Midlatitude FFTs")
ax10.set_xlabel("Wavenumber k")
ax10.set_ylabel("FFT Amplitude Variance")
ax10.plot( MidlatN_qERA_FFT_var, color=qERA_line_color, label='qERA_FFT', alpha=line_alpha)
ax10.plot( MidlatN_qROT_FFT_var, color=qROT_line_color, label='qROT_FFT', alpha=line_alpha)
ax10.plot( MidlatN_qIG_FFT_var , color=qIG_line_color,  label='qIG_FFT' , alpha=line_alpha)
ax10.plot( MidlatN_qM_FFT_var  , color=qM_line_color ,  label='qM_FFT'  , alpha=line_alpha)
ax10.set_xlim([0,351])
ax10.set_yscale('log')
ax10.legend(loc='lower left')

# Tropics Plots
ax01.set_title(f"b)     Tropics Profiles")
ax01.set_xlabel(f"Longitude [deg]")
ax01.set_ylabel(f"Averaged q Anomalies [g/kg]")
ax01.plot( lon, Tropics_qERA_avg, color=qERA_line_color, label='qERA', alpha=line_alpha)
ax01.plot( lon, Tropics_qROT_avg, color=qROT_line_color, label='qROT', alpha=line_alpha)
ax01.plot( lon, Tropics_qIG_avg , color=qIG_line_color,  label='qIG' , alpha=line_alpha)
ax01.plot( lon, Tropics_qM_avg  , color=qM_line_color  , label='qM ' , alpha=line_alpha)
ax01.legend(loc='upper right')

ax11.set_title(f"e)     Tropics FFTs")
ax11.set_xlabel("Wavenumber k")
ax11.set_ylabel("FFT Amplitude Variance")
ax11.plot( Tropics_qERA_FFT_var, color=qERA_line_color, label='qERA_FFT', alpha=line_alpha)
ax11.plot( Tropics_qROT_FFT_var, color=qROT_line_color, label='qROT_FFT', alpha=line_alpha)
ax11.plot( Tropics_qIG_FFT_var , color=qIG_line_color,  label='qIG_FFT' , alpha=line_alpha)
ax11.plot( Tropics_qM_FFT_var  , color=qM_line_color ,  label='qM_FFT'  , alpha=line_alpha)
ax11.set_xlim([0,351])
ax11.set_yscale('log')
ax11.legend(loc='lower left')

# Southern Midlat Plots
ax02.set_title(f"c)     Southern Midlatitude Profiles")
ax02.set_xlabel(f"Longitude [deg]")
ax02.set_ylabel(f"Averaged q Anomalies [g/kg]")
ax02.plot( lon, MidlatS_qERA_avg, color=qERA_line_color, label='qERA', alpha=line_alpha)
ax02.plot( lon, MidlatS_qROT_avg, color=qROT_line_color, label='qROT', alpha=line_alpha)
ax02.plot( lon, MidlatS_qIG_avg , color=qIG_line_color,  label='qIG' , alpha=line_alpha)
ax02.plot( lon, MidlatS_qM_avg  , color=qM_line_color  , label='qM ' , alpha=line_alpha)
ax02.legend(loc='upper right')

ax12.set_title(f"f)     Southern Midlatitude FFTs")
ax12.set_xlabel("Wavenumber k")
ax12.set_ylabel("FFT Amplitude Variance")
ax12.plot( MidlatS_qERA_FFT_var, color=qERA_line_color, label='qERA_FFT', alpha=line_alpha)
ax12.plot( MidlatS_qROT_FFT_var, color=qROT_line_color, label='qROT_FFT', alpha=line_alpha)
ax12.plot( MidlatS_qIG_FFT_var , color=qIG_line_color,  label='qIG_FFT' , alpha=line_alpha)
ax12.plot( MidlatS_qM_FFT_var  , color=qM_line_color ,  label='qM_FFT'  , alpha=line_alpha)
ax12.set_xlim([0,351])
ax12.set_yscale('log')
ax12.legend(loc='lower left')

plt.show()

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# SAVING THE PLOTS

FFT_outfile1 = f"{get_QMODES_PLOTS_DIR()}/qMODES_Fourier_Regional_FFT_var_{date}_plev{iplev}.pdf"
FFT_outfile2 = f"{get_QMODES_PLOTS_DIR()}/qMODES_Fourier_Regional_FFT_var_{date}_plev{iplev}.jpeg"
FFT_save_bool_str = input(f"\nSave FFT Plots in the following locations?:\n\t {FFT_outfile1}\n\t{FFT_outfile2}\n >>>(y/n):")

if FFT_save_bool_str == 'y':
	FFTfig.savefig(FFT_outfile1)
	FFTfig.savefig(FFT_outfile2)
	print(f"FFT Plot(s) saved.\n")

else: print("FFT Plots NOT saved.\n")
#-------------------------------------------------------------------------