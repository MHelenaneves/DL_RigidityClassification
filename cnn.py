# FCN model
# when tuning start with learning rate->mini_batch_size ->
# momentum-> #hidden_units -> # learning_rate_decay -> #layers
import tensorflow.keras as keras
import tensorflow as tf
import numpy as np
import time
from matplotlib import pyplot as plt

from utils import save_logs
from utils import calculate_metrics
from sklearn.metrics import confusion_matrix
import seaborn as sns

class Classifier_CNN:

    def __init__(self, output_directory, input_shape, nb_classes, verbose=False,build=True):
        self.output_directory = output_directory

        if build == True:
            self.model = self.built(input_shape, nb_classes)
            if (verbose == True):
                self.model.summary()
            self.verbose = verbose
            self.model.save_weights(self.output_directory + "model_init.hdf5")

        return

    def built(self, input_shape, nb_classes):
        padding = 'valid'
        input_layer = keras.layers.Input(input_shape)

        if input_shape[0] < 60: # for italypowerondemand dataset
            padding = 'same'
        
        ##
        conv1 = keras.layers.Conv1D(filters=6,kernel_size=7,padding=padding,activation='sigmoid')(input_layer)
        conv1 = keras.layers.AveragePooling1D(pool_size=3)(conv1)
        #conv1 = keras.layers.BatchNormalization()(conv1)
        
        conv2 = keras.layers.Conv1D(filters=12,kernel_size=7,padding=padding,activation='sigmoid')(conv1)
        conv2 = keras.layers.AveragePooling1D(pool_size=3)(conv2)
        #conv2 = keras.layers.Dropout(0.25)(conv2)

        flatten_layer = keras.layers.Flatten()(conv2)

        output_layer = keras.layers.Dense(units=nb_classes,activation='sigmoid')(flatten_layer)

        model = keras.models.Model(inputs=input_layer, outputs=output_layer)
        
        ##

        model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=False), optimizer=keras.optimizers.Adam(),
                      metrics=['accuracy'])
        model.summary()

        file_path = self.output_directory + 'best_model.hdf5'

        model_checkpoint = keras.callbacks.ModelCheckpoint(filepath=file_path, monitor='loss',
                                                           save_best_only=True)

        self.callbacks = [model_checkpoint]

        return model

    def fit(self, x_train, y_train, x_val, y_val, y_true, y_test, x_test):
        if not tf.test.is_gpu_available:
            print('error')
            exit()

        # x_val and y_val are only used to monitor the test loss and NOT for training
        mini_batch_size = 16
        nb_epochs = 2000

        start_time = time.time()

        hist = self.model.fit(x_train, y_train, batch_size=mini_batch_size, epochs=nb_epochs,
                              verbose=self.verbose, validation_data=(x_val, y_val), callbacks=self.callbacks)

        duration = time.time() - start_time

        self.model.save(self.output_directory+'last_model.hdf5')

        model = keras.models.load_model(self.output_directory + 'best_model.hdf5')

        y_pred = model.predict(x_val)
        #test_eval = model.evaluation(x_test, y_test, verbose=0)
        #test_loss=test_eval[0]
        #test_accuracy=test_eval[1]
        #model.plot_confusion(y_test,y_pred, self.output_directory + 'Confusion Matrix.png')

        # convert the predicted from binary to integer
        y_pred = np.argmax(y_pred, axis=1)

        save_logs(self.output_directory, hist, y_pred, y_true, y_test, duration,lr=False)

        #keras.backend.clear_session()
        #return y_pred
        #return test_loss, test_accuracy
        

    def predict(self, x_test,y_true,x_train,y_train,y_test,return_df_metrics = True):
        model_path = self.output_directory + 'best_model.hdf5'
        model = keras.models.load_model(model_path)
        y_pred = model.predict(x_test)
        if return_df_metrics:
            y_pred = np.argmax(y_pred, axis=1)
            df_metrics = calculate_metrics(y_true, y_pred, 0.0)
            return df_metrics
        else:
            return y_pred

    def evaluation(self, x_test,y_test):
        test_eval = self.model.evaluate(x_test, y_test, verbose=0)
        #print('Test loss:', test_eval[0])
        #print('Test accuracy:', test_eval[1])
        return test_eval
        
    def plot_confusion(self,y_test,y_pred,file_name):
        #Generate the confusion matrix
        cf_matrix = confusion_matrix(y_test, y_pred)
        ax = sns.heatmap(cf_matrix, annot=True, cmap='Blues')
        ax.set_title('Seaborn Confusion Matrix with labels\n\n');
        ax.set_xlabel('\nPredicted Values')
        ax.set_ylabel('Actual Values ');
        ## Ticket labels - List must be in alphabetical order
        ax.xaxis.set_ticklabels(['False','True'])
        ax.yaxis.set_ticklabels(['False','True'])
        plt.savefig(file_name, bbox_inches='tight')
        plt.close()