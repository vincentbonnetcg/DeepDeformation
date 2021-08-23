"""
@author: Vincent Bonnet
@description : The all pipleine to load+prepare data, create, train and evaluate model
"""

import data_wrangler
from clip_data import ClipData
from models import DeformerModel

class Pipeline:

    def __init__(self):
        # neural network model
        self.model = None
        # dataset
        self.clip_name = None
        # data prepared for neural network
        self.x_train = None
        self.y_train = None
        self.x_valid = None
        self.y_valid = None

    def set_dataset(self, clip_name):
        # TODO : for now only testing on a single animation clip
        self.clip_name = clip_name

    def prepare_data(self):
        result = data_wrangler.load_dataset(self.clip_name)
        self.x_train = result[0]
        self.y_train = result[1]
        self.x_valid = result[2]
        self.y_valid = result[3]

    def train(self, epochs=100, batch_size=10):
        # Get Data
        in_shape = self.x_train.shape[1]
        out_shape = self.y_train.shape[1]

        # Create and train model
        self.model = DeformerModel()
        self.model.create_model(in_shape, out_shape)
        self.model.set_data(self.x_train, self.y_train, self.x_valid, self.y_valid)
        self.model.fit(epochs=epochs, batch_size=batch_size)

    def predict(self):
        # Predict the shapes
        x_test, y_test = data_wrangler.load_dataset(self.clip_name, validation_ratio=0.0)
        y_predicted = self.model.predict(x_test)
        new_shape = (y_predicted.shape[0], int(y_predicted.shape[1] / 3), 3)
        y_predicted = y_predicted.reshape(new_shape)
        y_test = y_test.reshape(new_shape)

        # Load a clip from databset and update the smooth attribute
        clip = ClipData(self.clip_name)
        clip.load(predicted=False)
        clip.smooth_meshes = clip.base_meshes + y_predicted
        clip.save(predicted=True)

        # Display the errors
        # TODO - add a diagram
        #error = np.sqrt((y_test-y_predicted)**2)
        #print('-- ERROR --', error)

