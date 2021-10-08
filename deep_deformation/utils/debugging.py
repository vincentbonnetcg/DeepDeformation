"""
@author: Vincent Bonnet
@description : Debugging functions to check data
"""

import deep_deformation.utils.common as common
from deep_deformation.objects.skeleton import Skeleton
from deep_deformation.objects.skinning import Skinning
from deep_deformation.objects.rest_pose_data import RestPoseData
from deep_deformation.objects.skeleton_data import SkeletonData
from deep_deformation.objects.skinning_data import SkinningData
from deep_deformation.objects.clip_data import ClipData

import fnmatch, os

def config_summary():
    print('---------------')
    print('CONFIG SUMMARY')
    print('working_dir : {}'.format(common.WORKING_DIR))
    print('dataset_folder : {}'.format(common.DATASET_FOLDER))
    print('prediction_folder : {}'.format(common.PREDICTION_FOLDER))
    print('rest_pose_clip_name : {}'.format(common.REST_POSE_CLIP_NAME))
    print('bone_attributes : {}'.format(common.BONE_ATTRIBUTES))

def dataset_summary():
    dataset_dir = common.get_dataset_dir()
    skinning_path = common.get_skinning_path()
    skeleton_path = common.get_skeleton_path()

    print('---------------')
    print('DATASET SUMMARY')
    clips = fnmatch.filter(os.listdir(dataset_dir),'*.npz')
    print(clips)
    print('num clips : {}'.format(str(len(clips))))

    print('skinning file({}) | exists({})'.format(skinning_path,
                                                  os.path.exists(skinning_path)))

    print('skeleton file({}) | exists({})'.format(skeleton_path,
                                                  os.path.exists(skeleton_path)))

    skeleton_data = SkeletonData()
    skeleton_data.load()
    skeleton = Skeleton(skeleton_data)
    skeleton.print_root()

def skinning_summary():
    print('----------------')
    print('SKINNING SUMMARY')
    # Load time-invariant data (skeleton and skinning)
    skeleton_data = SkeletonData()
    skeleton_data.load()
    skeleton = Skeleton(skeleton_data)
    print('skeleton : num bones {}'.format(len(skeleton_data.bone_names)))

    skinning_data = SkinningData()
    skinning_data.load()
    print('skinning : weights {}'.format(skinning_data.num_weights.shape))
    print('skinning : bone_ids {}'.format(skinning_data.bones_ids.shape))
    print('skinning : weights {}'.format(skinning_data.weights.shape))

    rest_pose_data = RestPoseData()
    rest_pose_data.load()
    print('rest pose {}'.format(rest_pose_data.bone_data.shape))


def clipdata_summary(clip_name):
    print('----------------')
    print('CLIP SUMMARY')
    # Load time-variant data (animation clip)
    clip_data = ClipData(clip_name)
    clip_data.load()
    print('clip_name : {}'.format(clip_name))
    print('clip_data : pose {} '.format(clip_data.bone_data.shape))
    print('clip_data : base_meshes {} '.format(clip_data.base_meshes.shape))
    print('clip_data : smooth_meshes {} '.format(clip_data.smooth_meshes.shape))
