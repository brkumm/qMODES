#-------------------------------------------------------------------------
# Script: data_readers.py
# Author: Bradley Kumm (bkumm@wisc.edu)
# Creation Date: 2026/04/17/2026
# Description: This script contains commnly used functions for reading in
#               qMODES and ERA data.
# Notes: 
#
#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# IMPORTS

from .math_util import qMODES_deriv

import xarray as xa
import numpy as np
#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
# DATA READING FUNCTIONS

def get_full_field_ERA_and_flipped_qmodes_data(ERA_datafile, MODES_datafile):
	"""
	This functions reads in and computes relavent q and qmodes data. 
	Output data includes the following perturbation data for a single pressure level:
		qERA (perturbations)
		qEIG
		qWIG
		qBAL
		qM   (residual)
	NOTE: ERA and modes latitude indicies are flipped relative to each 
	other, so the qmodes values are flipped so that they agree.
	"""
	ERA_ds   = xa.open_dataset(ERA_datafile) 
	MODES_ds = xa.open_dataset(MODES_datafile)

	#Reading in qERA data (full q not perturbation quantity ... yet)
	qERA = ERA_ds['q'].values[0,:,:,:]
	
	#Initial qERA calcs
	qbkg = np.mean(qERA, axis=(1,2)) #average over lat and lon indicies (indicies 1 and 2 respectively)
	
	plev = ERA_ds['plev'].values
	qbkg_deriv = qMODES_deriv(plev, qbkg)

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


def get_full_field_ERA_and_flipped_qmodes_data_with_p_and_lat_dependent_background(ERA_datafile, MODES_datafile):
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

	NOTE: ERA and modes latitude indicies are flipped relative to each 
	other, so the qmodes values are flipped so that they agree.
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
		qbkg_deriv[:,ilat] = qMODES_deriv(plev,qbkg[:,ilat])


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


def get_single_plev_ERA_and_flipped_qmodes_data(ERA_datafile, MODES_datafile, iplev):
	"""
	This functions reads in and computes relavent q and qmodes data. 
	Output data includes the following perturbation data for a single pressure level:
		qERA (perturbations)
		qEIG
		qWIG
		qBAL
		qM   (qERA - all qMODES)

	NOTE: ERA and modes latitude indicies are flipped relative to each 
	other, so the qmodes values are flipped so that they agree.
	"""
	ERA_ds   = xa.open_dataset(ERA_datafile) 
	MODES_ds = xa.open_dataset(MODES_datafile)

	#Reading in qERA data (full q not perturbation quantity ... yet)
	qERA = ERA_ds['q'].values[0,:,:,:]
	plev = ERA_ds['plev'].values
	
	#Initial qERA calcs
	qbkg = np.mean(qERA, axis=(1,2)) #average over lat and lon indicies (indicies 1 and 2 respectively)
	
	plev = ERA_ds['plev'].values
	qbkg_deriv = qMODES_deriv(plev, qbkg)

	#Reading MODES Data
	qERA = qERA[iplev,:,:]   - qbkg[iplev]
	qEIG = qbkg_deriv[iplev] * np.flip( MODES_ds['q_EIG'].values[iplev,:,:], axis=0 ) # indexing for full q_EIG is [plev,lat,lon] flipping 
	qWIG = qbkg_deriv[iplev] * np.flip( MODES_ds['q_WIG'].values[iplev,:,:], axis=0 ) # indexing for full q_WIG is [plev,lat,lon] flipping 
	qBAL = qbkg_deriv[iplev] * np.flip( MODES_ds['q_BAL'].values[iplev,:,:], axis=0 ) # indexing for full q_BAL is [plev,lat,lon] flipping 

	#Calculating qM
	qM = qERA - qEIG - qWIG - qBAL

	return np.array([qERA, qEIG, qWIG, qBAL, qM])


def get_single_plev_ERA_and_flipped_qmodes_data_with_p_and_lat_dependent_background(ERA_datafile, MODES_datafile, iplev):
	"""
	This functions reads in and computes relavent q and qmodes data. 
	Output data includes the following perturbation data for a single pressure level:
		qERA (perturbations)
		qEIG
		qWIG
		qBAL
		qM   (qERA - all other qMODES)

	NOTE: ERA and modes latitude indicies are flipped relative to each 
	other, so the qmodes values are flipped so that they agree.
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
		qbkg_deriv[:,ilat] = qMODES_deriv(plev,qbkg[:,ilat])

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
#-------------------------------------------------------------------------