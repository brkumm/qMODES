#-------------------------------------------------------------------------
# Script: OmegaMODES_Functions.py
# Author: Bradley Kumm (bkumm@wisc.edu)
# Creation Date: July 25, 2024
# Description: This script contains commnly used functions for analyzing 
#              data using the MODES Framework
# Notes: 
#
#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# Imports

import math
import xarray as xa
import numpy  as np

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# MY DERIVATIVE FUNCTIONS TO ENSURE I KNOW EXACTLY WHAT THEY ARE DOING

def Deriv(xvals, yvals):
    ny = len(yvals)
    deriv = np.zeros(ny)

    # deriv at first point
    deriv[0] = (yvals[1] - yvals[0]) / (xvals[1]-xvals[0])

    for i in range(1,ny-1):
        plist    = [(xvals[i-1],yvals[i-1]), (xvals[i],yvals[i]), (xvals[i+1],yvals[i+1])]
        deriv[i] = Deriv_At_Point(plist,xvals[i])

    deriv[ny-1] = (yvals[ny-1] - yvals[ny-2]) / (xvals[ny-1] - xvals[ny-2])

    return deriv

def Deriv_At_Point(points_list,xval):
    """
    This function calculates the derivative at the given point xval, from
    the three points given in points list. Calculated by finding the 
    coefficients a,b, and c that solve for the 2nd order polynomial that 
    passes through the points in the points_list (f(x) = ax^2 + bx + c)
    then the derivative of this polynomial should give an good approximation
    of the derivative in the range [min(x1,x2,x3), max(x1,x2,x3)]
    """
    x1 = float( points_list[0][0] ) 
    x2 = float( points_list[1][0] ) 
    x3 = float( points_list[2][0] )

    y1 = float( points_list[0][1] ) 
    y2 = float( points_list[1][1] ) 
    y3 = float( points_list[2][1] ) 

    a = ( x1 * ( y3 - y2) + x2 * (y1 - y3) + x3 * (y2 - y1) ) / ((x1 - x2)*(x1 - x3)*(x2 - x3))
    b = (y2 - y1) / (x2 - x1)  - a * (x1 + x2)
    #c coefficient doesn't matter after taking deriv 

    return 2.0 * a * float(xval) + b

#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# DATA READING FUNCTIONS

# Combined ERA-MODES Data
def get_full_field_ERA_and_flippedMODES_q_data(ERA_datafile, MODES_datafile):
	"""
	This functions reads in and computes relavent q and qmodes data. 
	Output data includes the following perturbation data for a single pressure level:
		qERA (perturbations)
		qEIG
		qWIG
		qBAL
		qM   (residual)
	"""
	ERA_ds   = xa.open_dataset(ERA_datafile) 
	MODES_ds = xa.open_dataset(MODES_datafile)

	#Reading in qERA data (full q not perturbation quantity ... yet)
	qERA = ERA_ds['q'].values[0,:,:,:]
	
	#Initial qERA calcs
	qbkg = np.mean(qERA, axis=(1,2)) #average over lat and lon indicies (indicies 1 and 2 respectively)
	
	plev = ERA_ds['plev'].values
	qbkg_deriv = Deriv(plev, qbkg)

	#Reading MODES Data
	qEIG = np.flip(MODES_ds['q_EIG'].values, axis=1)
	qWIG = np.flip(MODES_ds['q_WIG'].values, axis=1)
	qBAL = np.flip(MODES_ds['q_BAL'].values, axis=1)

	#turning qERA into a perturbation quantity and reading in and computing MODES values
	for i in range(len(plev)):
		qERA[i,:,:] = qERA[i,:,:]   - qbkg[i]
		qEIG[i,:,:] = qbkg_deriv[i] * qEIG[i,:,:] # indexing is [plev,lat,lon] flipping MODES data along lat ERA and MODES data grids correspond
		qWIG[i,:,:] = qbkg_deriv[i] * qWIG[i,:,:] # indexing is [plev,lat,lon] flipping MODES data along lat ERA and MODES data grids correspond
		qBAL[i,:,:] = qbkg_deriv[i] * qBAL[i,:,:] # indexing is [plev,lat,lon] flipping MODES data along lat ERA and MODES data grids correspond

	#Calculating qM
	qM = qERA - qEIG - qWIG - qBAL

	return np.array([qERA, qEIG, qWIG, qBAL, qM])

# Combined ERA-MODES Data
def get_full_field_ERA_and_flippedMODES_q_data_with_p_and_lat_dependent_background(ERA_datafile, MODES_datafile):
	"""
	This functions reads in and computes relavent q and qmodes data. 
	Output data includes the following perturbation data for a single pressure level:
		qERA (perturbations)
		qEIG
		qWIG
		qBAL
		qM   (residual)

	These values are calculated with latitude and p dependent background functions, 
	by simply replacing the pressure dependant one in the original function above.
	"""
	ERA_ds   = xa.open_dataset(ERA_datafile) 
	MODES_ds = xa.open_dataset(MODES_datafile)

	#Reading in qERA data (full q not perturbation quantity ... yet)
	qERA  = ERA_ds['q'].values[0,:,:,:]
	plev  = ERA_ds['plev'].values
	nplev = np.shape(qERA)[0]
	nlat  = np.shape(qERA)[1]
	

	#Background Calculations
	qbkg = np.mean(qERA, axis=2) #average over lat and lon indicies (indicies 1 and 2 respectively)

	qbkg_deriv = np.zeros((nplev,nlat))
	for ilat in range(nlat):
			qbkg_deriv[:,ilat] = Deriv(plev,qbkg[:,ilat])


	#Reading MODES Data
	qEIG = np.flip(MODES_ds['q_EIG'].values, axis=1)
	qWIG = np.flip(MODES_ds['q_WIG'].values, axis=1)
	qBAL = np.flip(MODES_ds['q_BAL'].values, axis=1)

	#turning qERA into a perturbation quantity and reading in and computing MODES values
	for i in range(nplev):
		for j in range(nlat):
			qERA[i,j,:] = qERA[i,j,:]     - qbkg[i,j]
			qEIG[i,j,:] = qbkg_deriv[i,j] * qEIG[i,j,:] # indexing is [plev,lat,lon] flipping MODES data along lat ERA and MODES data grids correspond
			qWIG[i,j,:] = qbkg_deriv[i,j] * qWIG[i,j,:] # indexing is [plev,lat,lon] flipping MODES data along lat ERA and MODES data grids correspond
			qBAL[i,j,:] = qbkg_deriv[i,j] * qBAL[i,j,:] # indexing is [plev,lat,lon] flipping MODES data along lat ERA and MODES data grids correspond

	#Calculating qM
	qM = qERA - qEIG - qWIG - qBAL

	return np.array([qERA, qEIG, qWIG, qBAL, qM])


def get_single_plev_ERA_and_flippedMODES_q_data(ERA_datafile, MODES_datafile, iplev):
	"""
	This functions reads in and computes relavent q and qmodes data. 
	Output data includes the following perturbation data for a single pressure level:
		qERA (perturbations)
		qEIG
		qWIG
		qBAL
		qM   (qERA - all qMODES)
	"""
	ERA_ds   = xa.open_dataset(ERA_datafile) 
	MODES_ds = xa.open_dataset(MODES_datafile)

	#Reading in qERA data (full q not perturbation quantity ... yet)
	qERA = ERA_ds['q'].values[0,:,:,:]
	plev = ERA_ds['plev'].values
	
	#Initial qERA calcs
	qbkg = np.mean(qERA, axis=(1,2)) #average over lat and lon indicies (indicies 1 and 2 respectively)
	
	plev = ERA_ds['plev'].values
	qbkg_deriv = Deriv(plev, qbkg)
	

	

	#Reading MODES Data
	qERA = qERA[iplev,:,:]   - qbkg[iplev]
	qEIG = qbkg_deriv[iplev] * np.flip( MODES_ds['q_EIG'].values[iplev,:,:], axis=0 ) # indexing for full q_EIG is [plev,lat,lon] flipping 
	qWIG = qbkg_deriv[iplev] * np.flip( MODES_ds['q_WIG'].values[iplev,:,:], axis=0 ) # indexing for full q_WIG is [plev,lat,lon] flipping 
	qBAL = qbkg_deriv[iplev] * np.flip( MODES_ds['q_BAL'].values[iplev,:,:], axis=0 ) # indexing for full q_BAL is [plev,lat,lon] flipping 

	#Calculating qM
	qM = qERA - qEIG - qWIG - qBAL

	return np.array([qERA, qEIG, qWIG, qBAL, qM])

def get_single_plev_ERA_and_flippedMODES_q_data_with_p_and_lat_dependent_background(ERA_datafile, MODES_datafile, iplev):
	"""
	This functions reads in and computes relavent q and qmodes data. 
	Output data includes the following perturbation data for a single pressure level:
		qERA (perturbations)
		qEIG
		qWIG
		qBAL
		qM   (qERA - all qMODES)
	"""
	ERA_ds   = xa.open_dataset(ERA_datafile) 
	MODES_ds = xa.open_dataset(MODES_datafile)

	#Reading in qERA data (full q not perturbation quantity ... yet)
	qERA  = ERA_ds['q'].values[0,:,:,:]
	plev  = ERA_ds['plev'].values
	nplev = np.shape(qERA)[0]
	nlat  = np.shape(qERA)[1]
	nlon  = np.shape(qERA)[2]
	
	#Background Calculations
	qbkg = np.mean(qERA, axis=2) #average over lon indicies (index 2)

	qbkg_deriv = np.zeros((nplev,nlat))
	for ilat in range(nlat):
			qbkg_deriv[:,ilat] = Deriv(plev,qbkg[:,ilat])

	#Reading MODES Data
	qERA = qERA[iplev,:,:] #Reducing qERA to desired plev data only
	qEIG = np.zeros((nlat,nlon))
	qWIG = np.zeros((nlat,nlon))
	qBAL = np.zeros((nlat,nlon))
	for ilat in range(nlat):
		qERA[ilat,:] = qERA[ilat,:]   - qbkg[iplev,ilat]
		qEIG[ilat,:] = qbkg_deriv[iplev,ilat] * np.flip( MODES_ds['q_EIG'].values[iplev,:,:], axis=0 )[ilat,:] # indexing for full q_EIG is [plev,lat,lon] flipping 
		qWIG[ilat,:] = qbkg_deriv[iplev,ilat] * np.flip( MODES_ds['q_WIG'].values[iplev,:,:], axis=0 )[ilat,:] # indexing for full q_WIG is [plev,lat,lon] flipping 
		qBAL[ilat,:] = qbkg_deriv[iplev,ilat] * np.flip( MODES_ds['q_BAL'].values[iplev,:,:], axis=0 )[ilat,:] # indexing for full q_BAL is [plev,lat,lon] flipping 

	#Calculating qM
	qM = qERA - qEIG - qWIG - qBAL

	return np.array([qERA, qEIG, qWIG, qBAL, qM])




#ERA Data Readers
def read_ERA_grid_data(datafile,var1,var2,var3):
	'''reads in ERA grid data and outputs the data as a list with the grid parameters in specified order'''
	ERA_ds = xa.open_dataset(datafile)
	return [ ERA_ds[var1].values, ERA_ds[var2].values, ERA_ds[var3].values ]

def read_ERA_entire_Field_data_from_file(datafile,var):
	''' This function reads in the variable var, from the datafile'''
	ERA_ds = xa.open_dataset(datafile)
	return ERA_ds[var].values

def read_ERA_t0_field_plev_contour_from_file(datafile,var,iplev):
	''' This function reads in the variable var, from the datafile'''
	ERA_ds = xa.open_dataset(datafile)
	return ERA_ds[var].values[0,iplev,:,:] #index ordering time,plev,lat,lon





#MODES Data Readers
def read_MODES_notflipped_grid_data(datafile,var1,var2,var3):
	'''reads in ERA grid data and outputs the data as a list with the grid parameters in specified order'''
	MODES_ds = xa.open_dataset(datafile)
	return [ MODES_ds[var1].values, MODES_ds[var2].values, MODES_ds[var3].values ]

def read_flippedMODES_entire_Field_data_from_file(datafile,var):
	''' This function reads in the variable var, from the datafile'''
	ERA_ds = xa.open_dataset(datafile) #standard indexing order [plev,lat,lon]
	iflip=1
	return np.flip(ERA_ds[var].values,iflip)

def read_flippedMODES_t0_field_plev_contour_from_file(datafile,var,iplev):
	''' This function reads in the variable var, from the datafile'''
	ERA_ds = xa.open_dataset(datafile)
	indata = ERA_ds[var].values[iplev,:,:] #index ordering [plev,lat,lon]
	iflip  = 0 # index 0 is now latitude, index 1 is now longitude
	return np.flip(indata,iflip)


#-------------------------------------------------------------------------
