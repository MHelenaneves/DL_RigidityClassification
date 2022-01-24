# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 08:45:08 2021

@author: mhele
"""

import tensorflow as tf
from tensorflow import keras
from keras.utils.vis_utils import plot_model
import numpy as np
import os
import scipy as sp
import scipy.io
from matplotlib import pyplot as plt
import pandas as pd
import utils
from sklearn.metrics import confusion_matrix
import seaborn as sns


#%%  Load the dataset

trainPD = scipy.io.loadmat('trainPD')["emd_trainPD"]
trainhealthy = scipy.io.loadmat('trainhealthy')["emd_trainHealthy"]
testPD = scipy.io.loadmat('testPD')["emd_testPD"]
testhealthy = scipy.io.loadmat('testhealthy')["emd_testhealthy"]

X_train_healthy=trainhealthy[:,:,0:20]
X_train_PD=trainPD[:,:,0:20]
X_validate_healthy=trainhealthy[:,:,20:23]
X_validate_PD=trainPD[:,:,20:23]
X_test_healthy=testhealthy
X_test_PD=testPD
#%% Create labels

Y_train_healthy = np.zeros(20)
Y_train_PD = np.ones(20)

Y_validate_healthy = np.zeros(3)
Y_validate_PD = np.ones(3)

Y_test_healthy = np.zeros(5)
Y_test_PD = np.ones(5)

x_train=np.transpose(np.append(X_train_healthy , X_train_PD, axis=2 ))
y_train=np.column_stack((np.append(Y_train_healthy , Y_train_PD), np.append(Y_train_PD, Y_train_healthy)))

x_test=np.transpose((np.append(X_test_healthy , X_test_PD, axis=2 )) )
y_test=np.column_stack((np.append(Y_test_healthy , Y_test_PD), np.append(Y_test_PD, Y_test_healthy)))

x_validate=np.transpose((np.append(X_validate_healthy , X_validate_PD, axis=2 )) )
y_validate=np.column_stack((np.append(Y_validate_healthy , Y_validate_PD), np.append(Y_validate_PD, Y_validate_healthy)))

#%% Model

classifier_name="cnn"
def fit_classifier(y_test):
    
    nb_classes = 2

    # save orignal y because later we will use binary
    y_true = np.argmax(y_test, axis=1)

    input_shape = x_train.shape[1:]
    classifier = create_classifier(classifier_name, input_shape, nb_classes, output_directory)
    
    #y_pred=classifier.fit(x_train, y_train, x_test, y_test, y_true, y_test)
    #test_loss, test_accuracy=classifier.fit(x_train, y_train,  x_val,  y_val, y_true, x_test, y_test)
    classifier.fit(x_train, y_train, x_test, y_test, y_true, y_test, x_test)
    
    test_eval = classifier.evaluation(x_test, y_test)
    test_loss=test_eval[0]
    test_accuracy=test_eval[1]

    plot_model(classifier, to_file='model_plot.png', show_shapes=True)
    
    return test_loss, test_accuracy

def create_classifier(classifier_name, input_shape, nb_classes, output_directory, verbose=False):
    if classifier_name == 'fcn':
        
        import fcn
        return fcn.Classifier_FCN(output_directory, input_shape, nb_classes, verbose)
    
    if classifier_name == 'encoder':
        import encoder
        return encoder.Classifier_ENCODER(output_directory, input_shape, nb_classes, verbose)

    if classifier_name == 'cnn':  # Time-CNN
        import cnn
        return cnn.Classifier_CNN(output_directory, input_shape, nb_classes, verbose)



    
#%%
        
root_dir = "C://Users//mhele//OneDrive//Ambiente de Trabalho//DTU//2nd year//4rd semester//Special course//Code//Converted_csv"       
output_directory = root_dir + "//results//" + classifier_name + "//" 
#output_directory = utils.create_directory(output_directory)
utils.create_directory(output_directory)

#y_pred,y_true=fit_classifier(y_test)
test_loss, test_accuracy=fit_classifier(y_test)

print("DONE")

#%% 
#test_eval = model.evaluate(x_test, y_test, verbose=0)

#def plot_confusion(y_test,y_pred,file_name):
#    #Generate the confusion matrix
#    cf_matrix = confusion_matrix(y_test, y_pred)
#    ax = sns.heatmap(cf_matrix, annot=True, cmap='Blues')
#    ax.set_title('Seaborn Confusion Matrix with labels\n\n');
#    ax.set_xlabel('\nPredicted Values')
#    ax.set_ylabel('Actual Values ');
#    
#    ## Ticket labels - List must be in alphabetical order
#    ax.xaxis.set_ticklabels(['False','True'])
#    ax.yaxis.set_ticklabels(['False','True'])
#    plt.savefig(file_name, bbox_inches='tight')
#    plt.close()
#
#plot_confusion(y_test,y_pred,output_directory + 'Confusion Matrix.png')
#%% 

