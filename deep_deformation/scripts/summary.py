"""
@author: Vincent Bonnet
@description : Script to print the summarized dataset
"""

import sys
import os

# make deep_deformation package available
working_directory = os.getcwd()
if working_directory not in sys.path:
    sys.path.append(working_directory)

import yaml
import deep_deformation.utils.debugging as dgb
import deep_deformation.utils.common as common

if __name__ == '__main__':
    # Set the working directory
    common.WORKING_DIR = os.getcwd()

    # Summarize the dataset
    dgb.config_summary()
    dgb.dataset_summary
    dgb.skinning_summary()
    dgb.clipdata_summary(clip_name = 'SideFX_Male_walk_L_001')


