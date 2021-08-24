"""
@author: Vincent Bonnet
@description : Debugging functions to check data
"""

import common
from skeleton import Skeleton
from skinning import Skinning
from skeleton_data import SkeletonData
from skinning_data import SkinningData
from clip_data import ClipData
import fnmatch, os

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
    skeleton_data = SkeletonData()
    skeleton_data.load()
    skeleton = Skeleton(skeleton_data)
    skeleton.print_root()

def skinning_test():
    print('-- SKINNING TEST --')
    # Load time-invariant data (skeleton and skinning)
    skeleton_data = SkeletonData()
    skeleton_data.load()

    skinning_data = SkinningData()
    skinning_data.load()
    print(skinning_data.num_weights.shape)
    print(skinning_data.bones_ids.shape)
    print(skinning_data.weights.shape)

    # Load time-variant data (animation clip)
    # TODO
