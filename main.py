"""
@author: Vincent Bonnet
@description : Implementation of the deep deformation paper
"""

# TODO
#Data preprocessing
  # normalize inputs
  # do not train with bones not involved in the skinning
#Training
  # in load_dataset() should use multiple datasets

import common
import fnmatch,os
import numpy as np
import io_utils
from optimizer import ModelOpt
from skeleton import Skeleton

def training(epochs=100, batch_size=10):
    # Get Data
    clip_name = 'SideFX_Male_walk_L_001'
    x_train, y_train, x_test, y_test, train_ids, test_ids = io_utils.load_dataset(clip_name)
    in_shape = x_train.shape[1]
    out_shape = y_train.shape[1]

    # Get model
    model = ModelOpt()
    model.create_model(in_shape, out_shape)
    # TODO : below should not use test for validation data
    model.set_data(x_train, y_train, x_test, y_test)
    model.fit(epochs=epochs, batch_size=batch_size)

    # Predict from test
    predicted = model.predict(x_test)
    error = np.sqrt((y_test-predicted)**2)
    io_utils.write_predicted_clip(clip_name, predicted, test_ids)
    print(test_ids)

    # Predicted from train
    io_utils.write_predicted_clip(clip_name, model.predict(x_train), train_ids)

    # Display the errors
    print('---- errors ---- ')
    print(np.min(error), np.max(error), np.average(error))
    print(y_train.shape)

def dataset_summary():
    dataset_folder = common.get_dataset_dir()
    skinning_path = os.path.join(dataset_folder, 'skinning.npy')
    skeleton_path = os.path.join(dataset_folder, 'skeleton.txt')

    print('-- ANIMATION CLIPS --')
    clips = fnmatch.filter(os.listdir(dataset_folder),'*.npz')
    print(clips)
    print('num clips : ' + str(len(clips)))

    print('-- SKINNING --')
    print('skinning file : ' + str(os.path.exists(skinning_path)))

    print('-- SKELETON --')
    print('skeleton file : ' + str(os.path.exists(skeleton_path)))
    skeleton = Skeleton()
    skeleton.load(skeleton_path)
    skeleton.print_root()


if __name__ == '__main__':
    # Set the working directory
    common.WORKING_DIR = os.path.dirname(__file__)
    training(epochs=100, batch_size=10)
    #dataset_summary()

