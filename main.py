# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 12:45:39 2021

@author: mhele
"""
import csv
import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd 
from scipy.io import savemat
from DataPreprocessing import plt_time
from DataPreprocessing import plt_freq
from DataPreprocessing import filtering
from DataPreprocessing import removeMVCs

# %%
#change directory for the different subjects
#data=open("C:/Users/mhele/OneDrive/Ambiente de Trabalho/DTU/2nd year/4rd semester/Special course/Code/Paragit's data/1625746417-jGRI5/Converted_csv/SUB1PARAGIT2.csv")
#data=open("C:/Users/mhele/OneDrive/Ambiente de Trabalho/DTU/2nd year/4rd semester/Special course/Code/Converted_csv/SUB01.csv")
data=open("C:/Users/mhele/OneDrive/Ambiente de Trabalho/DTU/2nd year/4rd semester/Special course/Code/Converted_csv/Healthy_data_MyRecordings/SUB04.csv")
csvreader=csv.reader(data)

rows = []
for row in csvreader:
    rows.append(row)

rows=np.array(rows)

time=[]
for elem in rows[:,0]:
    time.append(float(elem))

#emg=[]
#for elem in rows[:,7]: #column 8 is the EMG
#    emg.append(float(elem))
    

#For jiayi's files
emg=[]
for elem in rows[:,1]: #column 2 is the EMG
    emg.append(float(elem))

 # %% Check signals 
 
checkSignal_plot_time = plt_time(emg)
checkSignal_plot_freq = plt_freq(emg)

 # %% 
checkSignal_remove,  nSecCut_init, nSecCut_end = removeMVCs(emg)
#checkSignal, time_cut = filtering( nSecCut_init, nSecCut_end, emg, time) #no MVC is removed

checkSignal, emg_correctmean,emg_filtered,emg_normalized = filtering(checkSignal_remove)
#emg, emg_correctmean,emg_filtered,emg_normalized=filtering(emg)
plot_filtering(emg,checkSignal, emg_correctmean,emg_filtered,emg_normalized)
#checkSignal, time_cut=filtering( nSecCut_init,emg[0:(len(time)-nSecCut_init-1)],time) #for sub03, only remove the last MVC
Time_min=len(emg)/(2000*60) #2000 is fs, 60s/min


 # %% Save to mat file
data_dictionary= {"data": (emg, checkSignal_remove, emg_normalized)}
savemat("F02_cut_filtered.mat", data_dictionary)

    
# %% Test data Paragit's sub 2

paths = glob.glob(r"./*.csv")
EMGSignal_all=[]
for i in range(15): #for each subject
    data_X = pd.read_csv(paths[i])
    data_X.columns =['time','EMG','batt','gX','gY','gZ','aX','aY','aZ']
    time=data_X['time']
    EMGSignal = data_X['EMG'] 
    EMGSignal_all += [EMGSignal]
    #checkSignal_plot_time = plt_time(EMGSignal,time)
    EMGFilter = filtering(EMGSignal)
    data_dictionary= {"data": (EMGSignal, EMGFilter[3])}
    number=i
    name="SUB%d_PARAGIT_cut_filtered.mat" % (number)
    savemat(name,data_dictionary)

# %% Test data Paragit's sub 1

paths = glob.glob(r"./*.csv")
EMGSignal_all=[]
for i in range(33): #for each subject
    if i==29: #there is a problem with this file
        continue
    else:
        data_X = pd.read_csv(paths[i])
        data_X.columns =['time','EMG','batt','gX','gY','gZ','aX','aY','aZ']
        time=data_X['time']
        EMGSignal = data_X['EMG'] 
        EMGSignal_all += [EMGSignal]
        #checkSignal_plot_time = plt_time(EMGSignal,time)
        EMGFilter = filtering(EMGSignal)
        data_dictionary= {"data": (EMGSignal, EMGFilter[3])}
        number=i
        name="SUB%d_PARAGIT_cut_filtered.mat" % (number)
        savemat(name,data_dictionary)
    
# %% 

paths = glob.glob(r"./*.csv")
EMGSignal_all=[]
for i in range(13): #for each subject
    data_X = pd.read_csv(paths[i])
    data_X.columns =['time','EMG','batt','gX','gY','gZ','aX','aY','aZ']
    time=data_X['time']
    EMGSignal = data_X['EMG'] 
    EMGSignal_all += [EMGSignal]
    checkSignal_plot_time = plt_time(EMGSignal,time)
    EMGFilter = filtering(EMGSignal)
    data_dictionary= {"data": (EMGSignal, EMGFilter[3])}
    number=i
    name="SUB%d_FAKE_cut_filtered.mat" % (number)
    savemat(name,data_dictionary)  