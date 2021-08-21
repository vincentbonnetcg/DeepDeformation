"""
@author: Vincent Bonnet
@description : Python utilities to get data from Houdini
"""

from .. import common
from ..clip_data import ClipData
from ..skeleton_data import SkeletonData
from ..skinning_data import SkinningData
import numpy as np
import hou
import os

BASE_SKINNING_INPUT_ID = 0
SMOOTH_SKINNING_INPUT_ID = 1

'''
 Helper function to get the current animation clip
'''
def get_current_clip_name(sop_name):

    anim_type = hou.parm(sop_name+'/anim_types').evalAsString()
    clip_name = hou.parm(sop_name+'/'+anim_type).evalAsString()
    return clip_name.replace('.bclip','')

'''
 Helper functions to get geometry data
'''
def get_geo(input_id):
    node = hou.pwd()
    inputs = node.inputs()
    if input_id >= len(inputs):
        raise Exception('input_id >= len(inputs)')
    return inputs[input_id].geometry()

def get_vertices(input_id):
    points = get_geo(input_id).points()
    num_points = len(points)

    pos_array = np.zeros((num_points, 3), dtype=float)
    for i, point in enumerate(points):
        pt = point.position()
        pos_array[i] = [pt[0],pt[1],pt[2]]

    return pos_array

'''
 Helper functions to get the animation data
'''
def get_bone_data(sop_name, bone_names):
    # sop_name : name of the sop network containing the bones
    # bone_names : name of the node representing the bone
    num_bones = len(bone_names)
    num_attributes = len(common.BONE_ATTRIBUTES)
    result = np.empty((num_bones, num_attributes), dtype=float)
    for i, bone_name in enumerate(bone_names):
        for j, attr in enumerate(common.BONE_ATTRIBUTES):
            result[i,j] = hou.evalParm(sop_name+bone_name+'/'+attr)

    return result

def get_clip_data(sop_name, skeleton_data, frame_id, num_frames):
    # Get bone and geometry data
    bone_data = get_bone_data(sop_name, skeleton_data.bone_names)
    base_mesh = get_vertices(BASE_SKINNING_INPUT_ID)
    smooth_mesh = get_vertices(SMOOTH_SKINNING_INPUT_ID)

     # Get the current clip name
    clip_name = get_current_clip_name(sop_name)

    # Create clip data
    clip_data = ClipData(clip_name)
    clip_path = clip_data.get_clip_path(predicted=False)
    if not os.path.exists(clip_path):
        num_bones = len(skeleton_data.bone_names)
        num_vertices = base_mesh.shape[0]
        clip_data.allocate(num_bones, num_vertices, num_frames)
    else:
        clip_data.allocate_from_file()

    # Add data to the correct frame
    # Houdini animation clip are between [1-max_frames]
    index = frame_id-1;
    clip_data.bone_data[index] = bone_data
    clip_data.base_meshes[index] = base_mesh
    clip_data.smooth_meshes[index] = smooth_mesh

    return clip_data


'''
 Helper functions to get skeleton data
'''
def get_bone_names(input_id):
    geo = get_geo(input_id)
    regions = geo.stringListAttribValue('boneCapture_pCaptPath')
    bone_names = []
    for region in regions:
        if '/cregion 0' in region:
            bone_names.append(region.replace('/cregion 0', ''))
        else:
            raise Exception('region format not supported')
    return bone_names

def get_bone_parent_names(sop_name, bone_names):
    parents = []
    for bone_name in bone_names:
        node = hou.node(sop_name+bone_name)
        parentName = node.inputs()[0].name()
        parents.append(parentName)

    return parents

def get_skeleton_data(sop_name):
    # Export skeleton
    bone_names = get_bone_names(SMOOTH_SKINNING_INPUT_ID)
    parent_names = get_bone_parent_names(sop_name, bone_names)
    skeleton_data = SkeletonData()
    skeleton_data.allocate(bone_names, parent_names)
    return skeleton_data


'''
 Helper function to get skinning data
'''
def get_skinning_data(input_id):
    geo = get_geo(input_id)
    points = geo.points()
    num_points = len(points)

    # get max influence per attribute
    max_influences = 0
    for point in points:
        boneids = point.intListAttribValue('boneCapture_index')
        if len(boneids) > max_influences:
            max_influences = len(boneids)

    skinning_data = SkinningData()
    skinning_data.allocate(num_points, max_influences)
    # extract skinning data
    for i, point in enumerate(points):
        boneIds = point.intListAttribValue('boneCapture_index')
        weights = point.floatListAttribValue('boneCapture_data')
        num_influences = len(boneIds)
        skinning_data.data[i]['numInfluences'] = num_influences
        for j in range(num_influences):
            skinning_data.data[i]['boneIds'][j] = boneIds[j]
            skinning_data.data[i]['weights'][j] = weights[j]

    return skinning_data
