"""
@author: Vincent Bonnet
@description : Implementation of the deep deformation paper
"""

import os
import common
import debugging
from pipeline import Pipeline

def main():
    # Set the working directory
    common.WORKING_DIR = os.path.dirname(os.path.dirname(__file__))

    # Summarize the dataset
    debugging.dataset_summary()
    debugging.skinning_test()

    # Create the pipeline
    pipeline = Pipeline()
    pipeline.set_dataset(clip_name = 'SideFX_Male_walk_L_001')
    pipeline.prepare_data()
    pipeline.train(epochs=200, batch_size=10)
    pipeline.predict()

if __name__ == '__main__':
    main()
