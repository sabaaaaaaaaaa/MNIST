""" 
Use Convolutional instead of Fully connected
And
Use Functional API
Saba Heidari Gheshlaghi
"""
from keras.datasets import mnist
import numpy as np
from keras.utils import np_utils  # for labels transformation (one hot)

#Load Data
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
#test_images.shape

## ==================== Data Prepration============================
     # Data Prepration 
# 1. because it's  Convolutional Layers, our input is image( not vector as in FC model)

X_train = train_images.reshape(60000, 28, 28, 1) # 1 means channels and its B&W
X_test  = test_images.reshape(10000, 28, 28, 1)

X_train = X_train.astype("float32") 
X_test  = X_test.astype("float32") #change integer to float 

# 2. normalization
X_train /= 255  # equal to X_train = X_train/255
X_test  /= 255

    # Labeles Prepration
# we only do it on images, and lables doesn't require these changes
# but in labels, we have numbers between 0 to 9 and in output we have neurons!!!
# in output, we have a vector with 10 elements
# so we should change numbers to output types ( means vector)= onehot
# for example if we have no 5, the output vector is 0000010000
# for this change, the utils library from keras is used

Y_train = np_utils.to_categorical(train_labels)
Y_test  = np_utils.to_categorical(test_labels)
## ====================Creating our Model===========================
## ==================== Functional API Model ======================


from keras.models import Model   
from keras.layers import  Conv2D, MaxPool2D, Input, Flatten, Dense 
# 2D convolution , flatten for changing the output image to a vector 
# Dense for output layer
 
import keras

#==========create model structure===========

# first build input layer, not  model!
myInput = Input(shape =( 28, 28, 1))   # only apply shape of input data
# in this model, you shoul say that what is the layer input
conv1 = Conv2D(16, 3, activation= 'relu', padding= 'same'  )(myInput)   
# Conv2D(how many output filters, window size, act. Func., padding type) (layer input)
# in window size when you write 3, it mens a 3*3 window
# padding 'same' => output has the same size as input
# padding 'valid' => output has the smaller size than input

pool1 = MaxPool2D(pool_size=2)(conv1)
# pool1 = MaxPool2D(pool size) => 2*2 => data size will be 1/2

conv2 = Conv2D(32, 3, activation= 'relu', padding= 'same')(pool1)    # data size reduce=> you can have bigger filter
pool2 = MaxPool2D(pool_size=2)(conv2)

#our output layer is 10 neurons, but here output is an image, and we have to change it into a vector
flat = Flatten()(pool2)
out_layer = Dense(10,activation = 'softmax')(flat) 

#========== Making Model==========

myModel = Model(myInput, out_layer)
#Model(input_layer, output layer)

myModel.summary()  

# fewer parameters in comparision with Fully Connected Models
  
## ==================== Compiling Model ======================
myModel.compile(optimizer=keras.optimizers.Adam(), loss=keras.losses.categorical_crossentropy , metrics= ['accuracy'])
# adam is a func. so it needs ()
# our optimizer func needs () because it gets input and variables.


## ====================Training Model I ===========================
# we train model with "fit"
import matplotlib.pyplot as plt

# for future check, we write our fit model on a variable such as network_history

network_history= myModel.fit(X_train, Y_train, batch_size=128, epochs=20)
# batch size= no. data import to model each time
# no. epoc means no. of training reptation
# we increase epoc until the time that loss doesnt decrease and acc. dosnt increase
# it concludes mostly based on experiments.

    ## we use network_history to draw loss and accuracy chart 
history = network_history.history

# type(history) is dict => can access to keys! which is loss and acc.
# history.keys() show you the keys!
# now we want to show them in a chart and need mathlotlib 

losses = history['loss']
accuracies = history['acc']

plt.xlabel('epoches')
plt.ylabel('loss')
plt.plot(losses)

plt.figure()      # showing both figure seprately!
plt.xlabel('epoches')
plt.ylabel('Accuracy')
plt.plot(accuracies)