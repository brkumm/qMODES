#-----------------------------------------------------------------------------
# IMPORTS

from qMODES import get_QMODES_ERA_DIR, get_QMODES_PLOTS_DIR

import matplotlib.pyplot as plt
import xarray            as xa
import numpy             as np
import argparse
import os
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# READING IN COMMAND LINE ARGUMENTS AND INITIALZING DIR VARIABLES

parser = argparse.ArgumentParser(description='This script is used to generate averaged background moisture plots.)')
parser.add_argument('--reduction_factor', help='factor to reduce (average) the number of lat values by', type=int, required=True)

args             = parser.parse_args()
reduction_factor = args.reduction_factor

ERA_dir  = get_QMODES_ERA_DIR()
plot_dir = get_QMODES_PLOTS_DIR()
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# CUSTOM FUNCTIONS

def reduce_by_factor_to_mean(arr, factor, axis=0):
    # Calculate the new shape
    # The dimension being reduced must be divisible by the factor
    if arr.shape[axis] % factor != 0:
        raise ValueError("Dimension size must be divisible by the reduction factor")

    new_shape = list(arr.shape)
    new_shape[axis] //= factor
    new_shape.insert(axis + 1, factor) # Insert the factor as a new dimension


    # Reshape the array to create chunks
    reshaped_arr = arr.reshape(new_shape)
    
    # Calculate the mean along the new dimension
    reduced_arr = np.mean(reshaped_arr, axis=axis + 1)
    
    return reduced_arr

def get_lat_color_key(lat_val):
    return f"{np.abs(lat_val):04.2f}"

def get_date_from_ERA_filename(ERA_filename):
    return ERA_filename[5:13]

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# CREATE LIST OF DATAFILES IN ERA_dir
datafiles = []
startdate = ""
enddate   = ""

for entry in os.listdir(ERA_dir):

    #checking if entry is a datafile 
    full_path = os.path.join(ERA_dir, entry)

    if os.path.isfile(full_path) and full_path[-14:] == "q-t_pl_data.nc":
        datafiles.append(full_path)
        date = get_date_from_ERA_filename(entry)
        date = get_date_from_ERA_filename(entry)
        if startdate == "":
            startdate = date
            enddate  = date

        if date < startdate: startdate = date
        if date > enddate: enddate = date

print(f"startdate is: {startdate}")
print(f"enddate is:   {enddate}"  )


#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# READING IN GRID DATA
ERA_q_ds = xa.open_dataset(datafiles[0])
plev = ERA_q_ds['plev'].values / 100.
lat  = ERA_q_ds['lat'].values
lon  = ERA_q_ds['lon'].values

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# MAIN LOOP 
# COMPUTE AVERAGE PROFILES AND PRESSURE DERIVATIVES
# REDUCE NUMBER OF LAT VALUES BY REDUCTION FACTOR

# initializing qbkg_avg to the q data in the first file
print(f"reading data from {datafiles[0]}")
q_vals   = ERA_q_ds['q'].values[0,:,:,:] # ilat ordering is: time, plev, lat, lon
qbkg_avg = np.mean(q_vals, axis=2)



# summing over remaining datafiles
for datafile in datafiles[1:]:
    print(f"reading data from {datafile}")
    ERA_q_ds = xa.open_dataset(datafile)
    q_vals   = ERA_q_ds['q'].values[0,:,:,:]
    qbkg_avg += np.mean(q_vals, axis=2)

# converting units to [g/kg] and dividing by number of datafiles to get an avrage
qbkg_avg = 1000 * qbkg_avg / float( len(datafiles) )


#reducing qbkg_avg and lat data to smaller number of lat values
qbkg_avg = reduce_by_factor_to_mean(qbkg_avg, reduction_factor, 1) # reduce over lat axis (0)
lat      = reduce_by_factor_to_mean(lat, reduction_factor, 0)

qbkg_avg_deriv = np.zeros(qbkg_avg.shape)
for ilat in range(len(lat)):
    qbkg_avg_deriv[:,ilat] = np.gradient(qbkg_avg[:,ilat], plev)

#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
# GENERATE AND SAVE PLOT(S)

fig, [[ax00, ax01], [ax10, ax11]] = plt.subplots(nrows=2, ncols=2, figsize=(12,8) )

nlat = len(lat)
ilat = 0

color_map = {} # used to make color maping same between hemispheres
color_key = ""

iplev_deriv = 10


#Make northern qbkg_avg plot (ax00 -> top left)
while ilat < nlat and lat[ilat] >= 0.0:
    color_key = get_lat_color_key(lat[ilat])
    NHplot = ax00.plot(qbkg_avg[:,ilat], plev, label=f"lat: {color_key}")
    color_map[color_key] = NHplot[0].get_color()
    ilat += 1


#Make southern qbkg_avg plot (ax10 -> bottom left)
while ilat < nlat:
    color_key = get_lat_color_key(lat[ilat])
    ax10.plot(qbkg_avg[:,ilat], plev, color=color_map[color_key], label=f"lat: -{color_key}")
    ilat += 1


#Make northern qbkg_avg_deriv plot (ax10 -> top right)
ilat = 0
while ilat < nlat and lat[ilat] >= 0.0:
    color_key = get_lat_color_key(lat[ilat])
    ax01.plot(qbkg_avg_deriv[iplev_deriv:,ilat], plev[iplev_deriv:], color=color_map[color_key], label=f"lat: {color_key}")
    ilat += 1

#Make southern qbkg_avg plot (ax11 -> bottom right)
while ilat < nlat:
    color_key = get_lat_color_key(lat[ilat])
    ax11.plot(qbkg_avg_deriv[iplev_deriv:,ilat], plev[iplev_deriv:], color=color_map[color_key], label=f"lat: -{color_key}")
    ilat += 1


ax00.set_title("a)", loc='left')
ax00.set_ylabel("Northern Hemisphere\nPressure Level [hPa]")
ax00.invert_yaxis()
ax00.legend()

ax00.set_title("b)", loc='left')
ax01.invert_yaxis()
ax01.legend()

ax10.set_title("c)", loc='left')
ax10.set_xlabel("Specific Humidity [g/kg]")
ax10.set_ylabel("Southern Hemisphere\nPressure Level [hPa]")
ax10.invert_yaxis()
ax10.legend(reverse=True)

ax00.set_title("d)", loc='left')
ax11.set_xlabel("Specific Humidity Derivative [g/kg hPa]")
ax11.invert_yaxis()
ax11.legend(reverse=True)
plt.show()


# Saving the plot to the plot_dir
outputfile1 = f"{plot_dir}/qbkg_averaged_profiles-{nlat}_{startdate}-{enddate}-{len(datafiles)}.pdf"
outputfile2 = f"{plot_dir}/qbkg_averaged_profiles-{nlat}_{startdate}-{enddate}-{len(datafiles)}.jpeg"

plt.savefig(outputfile1)
plt.savefig(outputfile2)

print("plots saved to:")
print(f"{outputfile1}")
print(f"{outputfile2}")

#-----------------------------------------------------------------------------
