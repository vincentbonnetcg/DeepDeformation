"""
@author: Vincent Bonnet
@description : Script to train and test the model
"""

import sys
import os

# make deep_deformation package available
working_directory = os.getcwd()
if working_directory not in sys.path:
    sys.path.append(working_directory)

import yaml
import deep_deformation.utils.common as common
from deep_deformation.pipeline import Pipeline

if __name__ == '__main__':
    # Set the working directory
    common.WORKING_DIR = os.getcwd()

    # Create the pipeline
    pipeline = Pipeline()
    pipeline.set_dataset(clip_name = 'SideFX_Male_walk_L_001')
    pipeline.prepare_data()
    pipeline.train(epochs=200, batch_size=10)
    pipeline.predict()

