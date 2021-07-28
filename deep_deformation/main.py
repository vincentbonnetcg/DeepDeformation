"""
@author: Vincent Bonnet
@description : Implementation of the deep deformation paper
"""

import common
import fnmatch,os
from skeleton import Skeleton
from pipeline import Pipeline

def dataset_summary():
    dataset_dir = common.get_dataset_dir()
    skinning_path = common.get_skinning_path()
    skeleton_path = common.get_skeleton_path()

    print('-- CLIPS --')
    clips = fnmatch.filter(os.listdir(dataset_dir),'*.npz')
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
    common.WORKING_DIR = os.path.dirname(os.path.dirname(__file__))

    # Summarize the dataset
    #dataset_summary()

    # Create the pipeline
    pipeline = Pipeline()
    pipeline.set_dataset(clip_name = 'SideFX_Male_walk_L_001')
    pipeline.prepare_data()
    pipeline.train(epochs=10, batch_size=10)
    pipeline.predict()

