"""
@author: Vincent Bonnet
@description : Deep deformation common functions/variables
"""
import os

# Working directory should be set before using the Houdini bridge or API
WORKING_DIR = None

# Constants
DATASET_FOLDER = 'dataset'
RAW_FOLDER = 'raw'
PROCESSED_FLDER = 'processed'
PREDICTION_FOLDER = 'prediction'
BONE_ATTRIBUTES = ['rx', 'ry', 'rz', 'length']
REST_POSE_CLIP_NAME = 'SideFX_Male_t_pose_001'

def get_dataset_dir():
    '''
    Returns the directory of the dataset
    The function creates the folder if it doesn't exist
    '''
    dataset_dir = os.path.join(WORKING_DIR, DATASET_FOLDER)
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
    return dataset_dir

def get_prediction_dir():
    '''
    Returns the directory of the prediction (from neural network)
    The function creates the folder if it doesn't exist
    '''
    prediction_dir = os.path.join(WORKING_DIR, PREDICTION_FOLDER)
    if not os.path.exists(prediction_dir):
        os.makedirs(prediction_dir)
    return prediction_dir

def get_rest_pose_path():
    return os.path.join(get_dataset_dir(), 'rest_pose.npy')

def get_skeleton_path():
    return os.path.join(get_dataset_dir(), 'skeleton.txt')

def get_skinning_path():
    return os.path.join(get_dataset_dir(), 'skinning.npz')

def get_clip_path(clip_name):
    return os.path.join(get_dataset_dir(), clip_name+'.npz')

def get_predicted_clip_path(clip_name):
    return os.path.join(get_prediction_dir(), clip_name+'.npz')

