""" Script for a figure similar to Figure 1. in Zagar et al. 2015.
Script is from valentino Neduhal with minor modifications
Normalized frequencies are saved for each zonal wavenumber.
They are saved in following order: First frequencies for EIG then for WIG with ROT at the end.
Kelvin waves are first EIG modes while MRG waves are first ROT modes.

WARNING:
One file should contain 200 frequencies for EIG, 200 for WIG, and 200 ROT (for each vertical mode)!
BUT for some unknown reason there are 200 frequencies for EIG, 200 for WIG, and 400 ROT (for each vertical mode)!
So in this scrip below I simply cut away last 200 ROT modes.
"""

import numpy as np
import matplotlib.pyplot as plt

#params = {'mathtext.default': 'regular' }  # Allows tex-style title & labels
#plt.rcParams.update(params)

freq_path = "../../input_data/hough/FILENAME_WITH_FREQUENCIE.data.wn00" # Path to the frequencies to p

K = 30  # Number of zonal modes that you wish to plot
M = 60  # Number of vertical modes
N = 200 # Number of meridional modes for each wave species (total number of modes is 3*N)


# Variables for storing read frequencies
freq_EIG = np.zeros([N,M,K])
freq_WIG = np.zeros([N,M,K])
freq_ROT = np.zeros([N,M,K])

# Reading freqencies for each k and separating them to corresponding wave species
for k in range(0,K):
    print("Reading frequency file for zonal wavenumber k=",k)
    freq_data = np.fromfile(freq_path + "%03d"%k)
    temp = np.reshape(freq_data[0:M*N*3], [3*N, M]) #HERE im cutting away last 200 ROT modes
    freq_EIG[:,:,k] = temp[:N,:]
    freq_WIG[:,:,k] = temp[N:2*N,:]
    freq_ROT[:,:,k] = temp[2*N:3*N,:]



#M_plot = [0,5,15] # which vertical modes to plot
M_plot = [0]
N_plot = [1,5,10,15,20,25] # which meridional modes to plot
tags = ['a)','b)','c)','d)','e)','f)']
i = 0
s = 10

# You will get some runtime warnings but you can ignore them
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(18, 10), gridspec_kw={'height_ratios': [5, 1]})
plt.subplots_adjust(hspace=0.05) 
fig.supylabel("Normalized Frequency", fontsize=30, fontweight='bold', x=0.07)
fig.supxlabel("Zonal Wavenumber", fontsize=30, fontweight='bold', y = 0.025)
for m in M_plot:

    ax[0].scatter(np.linspace(0, K - 1, K), np.log10(freq_EIG[0, m, :]),s=s, linestyle='-',  color = 'magenta')
    ax[0].scatter(-np.linspace(0, K - 1, K), np.log10(-freq_WIG[0, m, :]),s=s, linestyle='-',  color = 'red')
    ax[0].scatter(-np.linspace(0, K - 1, K), np.log10(-freq_ROT[0, m, :]),s=s, linestyle='-',  color = 'magenta')
    for n in N_plot:
        ax[0].scatter(-np.linspace(0, K - 1, K), np.log10(-freq_WIG[n, m, :]),s=s, linestyle='-',  color='red')
        ax[0].scatter(np.linspace(0,K-1,K), np.log10(freq_EIG[n,m,:]),s=s, linestyle='-',  color = 'blue')
        ax[0].scatter(-np.linspace(0,K-1,K), np.log10(-freq_ROT[n,m,:]),s=s, linestyle='-',  color = 'black')

    
    ax[0].text(10,0.15-i*0.45,'K',color ='magenta',fontsize = 25, fontweight = 'bold')
    ax[0].text(-20,-1,'MRG',color ='magenta',fontsize = 25, fontweight = 'bold')
    ax[0].text(-10,-2.5,'ROT',color ='black',fontsize = 25, fontweight = 'bold')
    ax[0].text(-14,1.35-i*0.45,'WIG',color ='red',fontsize = 25, fontweight = 'bold')
    ax[0].text(10,1.35-i*0.45,'EIG',color ='blue',fontsize = 25, fontweight = 'bold')

    ax[0].tick_params(axis='both', labelsize=12)
    ax[0].set_ylim([-2.75,1.75])
    ax[0].set_xlim([-K,K])
    ax[0].set_yticks([-2,-1,0,1])
    ax[0].set_yticklabels(['$10^{-2}$','$10^{-1}$','$10^{0}$','$10^{1}$'])



    #Making the lower plot before combining them
    ax[1].scatter( np.linspace(-K + 1, K - 1, 2*K - 1), np.zeros(2*K - 1), s=s, linestyle='-', color = 'seagreen' )
    ax[1].tick_params(axis='both', labelsize=12)
    ax[1].text(15,0.015,'Moist (M)',color ='seagreen',fontsize = 25, fontweight = 'bold')
    ax[1].set_ylim([-0.02,0.02])
    ax[1].set_xlim([-K,K])

    #"Stitching" the plots together
    ax[0].spines.bottom.set_visible(False)
    ax[0].set_xticks([])
    ax[1].spines.top.set_visible(False)
    ax[1].set_yticks([0])
    ax[1].set_yticklabels(['$0$'])


    d = .5  # proportion of vertical to horizontal extent of the slanted line
    kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
                  linestyle="none", color='k', mec='k', mew=1, clip_on=False)
    ax[0].plot([0, 1], [0, 0], transform=ax[0].transAxes, **kwargs)
    ax[1].plot([0, 1], [1, 1], transform=ax[1].transAxes, **kwargs)


fig.savefig("../../output_data/plots/DispersionRelationsByMode.png")
