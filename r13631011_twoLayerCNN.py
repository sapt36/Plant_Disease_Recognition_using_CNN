from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Dropout
import keras.backend.tensorflow_backend as KTF
import tensorflow as tf
from service.analyticService.core.analyticCore.classificationBase import classification
from service.analyticService.core.analyticCore.utils import XYdataGenerator, XdataGenerator
from math import ceil


class r13631011_twoLayerCNN(classification):
    def trainAlgo(self):

        # Parameters can be adjusted in the inanalysis system
        # self.param[]
        # Input & Output can be adjusted in the inanalysis system
        # self.inputData[] self.outputData[]

        # default hidden_kernel_size = (3, 3)
        hidden_kernel_size = (self.param['hidden_kernel_size'], self.param['hidden_kernel_size'])
        # default hidden_activation = 'relu'
        hidden_activation = self.param['hidden_activation']
        # default dropout_rate = 0.25
        dropout_rate = self.param['dropout_rate']

        # Create a Sequential model
        self.model = Sequential()

        # Add CNN with 8 filters, input images have a shape of 64x64 with 3 color channels (RGB).
        self.model.add(Conv2D(8, hidden_kernel_size, activation=hidden_activation,
                              input_shape=(64, 64, 3), data_format='channels_last'))
        # Add another CNN layer with 8 filters.
        self.model.add(Conv2D(16, hidden_kernel_size, activation=hidden_activation))

        # Add a pooling layer to reduce the spatial dimensions of the output volume.
        self.model.add(MaxPooling2D((2, 2)))

        self.model.add(Flatten())
        self.model.add(Dense(16, activation=hidden_activation))
        self.model.add(Dropout(dropout_rate))

        # Classification task: The number of neurons in the last layer is equal to the number of categories.
        # Output layer use softmax activation function, 3 categories : Rust, Healthy, Powdery.
        self.model.add(Dense(3, activation='softmax'))

        # Compile the model with categorical crossentropy loss function and the default optimizer is adam.
        self.model.compile(loss='categorical_crossentropy', optimizer=self.param['optimizer'])

        # Train the model using the data generator with chosen batch size and number of epochs.
        self.model.fit_generator(
            XYdataGenerator(self.inputData['X'], self.outputData['Y'], 64, 64,
                            self.param['batch_size']),
            steps_per_epoch=int(ceil((len(self.inputData['X']) / self.param['batch_size']))),
            epochs=self.param['epochs']
        )

    def predictAlgo(self):
        # Predict the output using the trained model.
        r = self.model.predict_generator(
            XdataGenerator(self.inputData['X'], 64, 64, self.param['batch_size']),
            steps=int(ceil((len(self.inputData['X']) / self.param['batch_size'])))
        )
        # Store the prediction result.
        self.result['Y'] = r
