# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 14:05:36 2021

@author: mhele
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy as sp

from scipy import signal
from scipy.signal import butter, lfilter, hilbert, chirp
from statsmodels.tsa.stattools import adfuller


 #%% 
#data=open("C:/Users/mhele/OneDrive/Ambiente de Trabalho/DTU/2nd year/4rd semester/Special course/Code/Jiayi's code/OrderedFiles/F01.csv")
#csvreader=csv.reader(data)
#
#rows = []
#for row in csvreader:
#    rows.append(row)
#
#rows=np.array(rows)
#
#time=[]
#for elem in rows[:,0]:
#    time.append(float(elem))
#
##emg=[]
##for elem in rows[:,7]: #column 8 is the EMG
##    emg.append(float(elem))
#    
#
##For jiayi's files
#emg=[]
#for elem in rows[:,1]: #column 2 is the EMG
#    emg.append(float(elem))


 
 #%%   
def plt_time(emg):   
    #Time domain plot
    plt.figure()
    plt.plot(emg, 'r-')
    plt.show()
    plt.xlabel('Time (sec)')
    plt.ylabel('EMG (mV)')
    
def plt_freq(emg):
    fs=2000 
    #Frequency domain plot
#    fourier_transform = np.fft.rfft(emg)
#    abs_fourier_transform = np.abs(fourier_transform)
#    power_spectrum = np.square(abs_fourier_transform)
#    #frequency = np.linspace(0, fs/2, len(power_spectrum))
#    time_step=1/fs
#    freqs = np.fft.fftfreq(len(emg), time_step)
#    idx=np.argsort(freqs)
    
    plt.figure()
    f, Pxx_den = signal.periodogram(emg, fs)
    plt.semilogy(f, Pxx_den)
    plt.xlabel('frequency [Hz]')
    plt.ylabel('PSD [V**2/Hz]')
    plt.show()
   

 #%%  
#emg_cut=0

def removeMVCs(emg):
    fs=2000
    
    #remove the first MVC, cut recording around  2min50s 
    point=60*2+50 #change it according to each subject's threshold
    nSecCut_init=fs*point
    emg_cut_init=emg[(nSecCut_init-1):-1]
    
    
    #remove the last MVC, cut last 2min50
    nSecCut_end=nSecCut_init
    
    #for sub2 remove the first 5s
    #point1=5 
    #nSecCut_init=fs*point1
    #emg_cut_init=emg[(nSecCut_init-1):-1]
    #nSecCut_end=fs*point
    
    
    #for sub3 only remove last MVC // comment line 65
    #emg_cut_init=emg
   

    #for sub5 remove the last 5min50s (60*4+50=290)
    #point2=60*5+50
    #nSecCut_end=fs*point2
    
    #for sub6 only remove last 10s
    #point3=10
    #nSecCut_end=fs*point3
    #emg_cut_init=emg
    
    #Jiayi's files
    #F06 and F08 remove last 30s 
    #point4=30
#    time=len(emg)/(fs*60)
#    point4= (math.floor(time)/2)*60
#    nSecCut_end=fs*point4
#    nSecCut_end=int(nSecCut_end)
#    emg_cut_init=emg
    
    
    emg_cut_end=emg_cut_init[0:(len(emg_cut_init)-nSecCut_end-1)]
    
    emg_cut=emg_cut_end
    
    return  emg_cut ,  nSecCut_init, nSecCut_end

# emg_cut ,  nSecCut_init, nSecCut_end=removeMVCs(emg)

 #%%
#def filtering(nSecCut_init, nSecCut_end, emg_cut, time):
def filtering(emg_cut):    
    #emg_cut=emg
    #time_cut=time
    # process EMG signal: remove mean
    emg_correctmean = emg_cut - np.mean(emg_cut)
    
    #time_cut_init=time[(nSecCut_init-1):-1] 
    #time_cut=time_cut_init[0:(len(time_cut_init)- nSecCut_end -1)]
    #time_cut=time[0:(len(time)-nSecCut_end-1)] #only remove the last MVC on sub3
    
    #time_cut=time[0:(len(time)-nSecCut_end-1)] #remove last 30s from F06 and F08 Jiayi
    
   
    
    
    # create bandpass filter for EMG
    low = 5/(2000/2)
    high = 500/(2000/2)
    b, a = sp.signal.butter(4, [low,high], btype='bandpass')
    
    lim_low=49/(2000/2)
    lim_high= 51/(2000/2)
    
    d, c=sp.signal.butter(4, [lim_low, lim_high], btype="bandstop") #notch at 50 Hz, influence from surrounding electronics
    
    # process EMG signal: filter EMG
    emg_filtered1 = sp.signal.filtfilt(b, a, emg_correctmean) #bandpass
    emg_filtered = sp.signal.filtfilt(d,c, emg_filtered1) #notch
    
    #Z-score normalization
    emg_normalized= (emg_filtered- np.mean(emg_filtered))/np.std(emg_filtered)
   
    return emg_cut, emg_correctmean,emg_filtered,emg_normalized
    #return emg_cut, emg_correctmean,emg_filtered,emg_normalized, time_cut
    
#emg_cut, emg_correctmean,emg_filtered,emg_normalized=filtering(emg_cut)
    
def plot_filtering(emg,emg_cut, emg_correctmean,emg_filtered,emg_normalized):
    
#     # plot comparison of EMG with offset vs mean-corrected values
#    plt.figure()
#    plt.subplot(1, 2, 1)
#    plt.subplot(1, 2, 1).set_title('Mean offset present')
#    #plt.plot(time_cut, emg_cut)
#    plt.plot(emg_cut)
#    plt.locator_params(axis='x', nbins=4)
#    plt.locator_params(axis='y', nbins=4)
#    plt.ylim(np.amin(emg_cut), np.amax(emg_cut))
#    plt.xlabel('Time (sec)')
#    plt.ylabel('EMG (a.u.)')
#    
#    plt.subplot(1, 2, 2)
#    plt.subplot(1, 2, 2).set_title('Mean-corrected values')
#    #plt.plot(time_cut, emg_correctmean)
#    plt.plot( emg_correctmean)
#    plt.locator_params(axis='x', nbins=4)
#    plt.locator_params(axis='y', nbins=4)
#    plt.ylim(np.amin(emg_correctmean), np.amax(emg_correctmean))
#    plt.xlabel('Time (sec)')
#    plt.ylabel('EMG (a.u.)')
#    
#    # plot comparison of unfiltered vs filtered mean-corrected EMG
#    plt.figure()
#    plt.subplot(1, 2, 1)
#    plt.subplot(1, 2, 1).set_title('Unfiltered EMG')
#    #plt.plot(time_cut, emg_correctmean)
#    plt.plot(emg_correctmean)
#    plt.locator_params(axis='x', nbins=4)
#    plt.locator_params(axis='y', nbins=4)
#    plt.ylim(np.amin(emg_correctmean), np.amax(emg_correctmean))
#    plt.xlabel('Time (sec)')
#    plt.ylabel('EMG (a.u.)')
#    
#    plt.subplot(1, 2, 2)
#    plt.subplot(1, 2, 2).set_title('Filtered EMG')
#    #plt.plot(time_cut, emg_filtered)
#    plt.plot(emg_filtered)
#    plt.locator_params(axis='x', nbins=4)
#    plt.locator_params(axis='y', nbins=4)
#    plt.ylim(np.amin(emg_filtered), np.amax(emg_filtered))
#    plt.xlabel('Time (sec)')
#    plt.ylabel('EMG (a.u.)')
#
## plot comparison of Unnormalized(after filtering) vs Normalized EMG
#    plt.figure()
#    plt.subplot(1, 2, 1)
#    plt.subplot(1, 2, 1).set_title('Unnormalized EMG')
#    #plt.plot(time_cut, emg_filtered)
#    plt.plot(emg_filtered)
#    plt.locator_params(axis='x', nbins=4)
#    plt.locator_params(axis='y', nbins=4)
#    plt.ylim(np.amin(emg_filtered), np.amax(emg_filtered))
#    plt.xlabel('Time (sec)')
#    plt.ylabel('EMG (a.u.)')
#    
#    plt.subplot(1, 2, 2)
#    plt.subplot(1, 2, 2).set_title('Normalized EMG')
#    #plt.plot(time_cut, emg_normalized)
#    plt.plot(emg_normalized)
#    plt.locator_params(axis='x', nbins=4)
#    plt.locator_params(axis='y', nbins=4)
#    plt.ylim(np.amin(emg_normalized), np.amax(emg_normalized))
#    plt.xlabel('Time (sec)')
#    plt.ylabel('EMG (a.u.)')


#    plt.figure()
#    plt.subplot(4,1,1)
#    plt.subplot(4,1,1).set_title('Mean offset present')
#    plt.plot(emg_cut)
#    plt.locator_params(axis='x', nbins=4)
#    plt.locator_params(axis='y', nbins=4)
#    plt.ylim(np.amin(emg_cut), np.amax(emg_cut))
#    plt.xlabel('Time (sec)')
#    plt.ylabel('EMG (a.u.)')
#    plt.subplot(4,1,2)
#    plt.subplot(4,1,2).set_title('Mean-corrected values')
#    plt.plot( emg_correctmean)
#    plt.locator_params(axis='x', nbins=4)
#    plt.locator_params(axis='y', nbins=4)
#    plt.ylim(np.amin(emg_correctmean), np.amax(emg_correctmean))
#    plt.xlabel('Time (sec)')
#    plt.ylabel('EMG (a.u.)')
#    plt.subplot(4,1,3)
#    plt.subplot(4,1,3).set_title('Filtered EMG')
#    plt.plot(emg_filtered)
#    plt.locator_params(axis='x', nbins=4)
#    plt.locator_params(axis='y', nbins=4)
#    plt.ylim(np.amin(emg_filtered), np.amax(emg_filtered))
#    plt.xlabel('Time (sec)')
#    plt.ylabel('EMG (a.u.)')
#    plt.subplot(4,1,4)
#    plt.subplot(4,1,4).set_title('Normalized EMG')
#    plt.plot(emg_normalized)
#    plt.locator_params(axis='x', nbins=4)
#    plt.locator_params(axis='y', nbins=4)
#    plt.ylim(np.amin(emg_normalized), np.amax(emg_normalized))
#    plt.xlabel('Time (sec)')
#    plt.ylabel('EMG (a.u.)')
    
    plt.figure()
    plt.subplot(1,4,1)
    plt.subplot(1,4,1).set_title('Raw EMG')
    plt.plot(emg)
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=4)
    plt.ylim(np.amin(emg), np.amax(emg))
    plt.xlabel('Time (sec)')
    plt.ylabel('EMG (mV)')
    plt.subplot(1,4,2)
    plt.subplot(1,4,2).set_title('Mean-corrected values')
    plt.plot( emg_correctmean)
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=4)
    plt.ylim(np.amin(emg_correctmean), np.amax(emg_correctmean))
    plt.xlabel('Time (sec)')
    #plt.ylabel('EMG (a.u.)')
    plt.subplot(1,4,3)
    plt.subplot(1,4,3).set_title('Filtered EMG')
    plt.plot(emg_filtered)
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=4)
    plt.ylim(np.amin(emg_filtered), np.amax(emg_filtered))
    plt.xlabel('Time (sec)')
    #plt.ylabel('EMG (a.u.)')
    plt.subplot(1,4,4)
    plt.subplot(1,4,4).set_title('Normalized EMG')
    plt.plot(emg_normalized)
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=4)
    plt.ylim(np.amin(emg_normalized), np.amax(emg_normalized))
    plt.xlabel('Time (sec)')
    #plt.ylabel('EMG (a.u.)')
    
#plot_filtering(emg, emg_correctmean,emg_filtered,emg_normalized)