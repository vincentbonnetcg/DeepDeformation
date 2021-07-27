"""
@author: Vincent Bonnet
@description : Python code to export bone and point data into a dataset folder
"""
from .. import common
from ..clip_data import ClipData
import hou_common
import numpy as np
import os
import hou

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

def get_bone_parents(sop_name, bone_names):
    parents = []
    for bone_name in bone_names:
        node = hou.node(sop_name+bone_name)
        parentName = node.inputs()[0].name()
        parents.append(parentName)

    return parents

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

    # extract skinning data
    data_type = {}
    data_type['names'] = ['numInfluences', 'boneIds', 'weights']
    data_type['formats'] = ['int8', ('int8', max_influences), ('float32', max_influences)]
    skinning_data = np.zeros(num_points, dtype=np.dtype(data_type, align=True))

    for i, point in enumerate(points):
        boneIds = point.intListAttribValue('boneCapture_index')
        weights = point.floatListAttribValue('boneCapture_data')
        num_influences = len(boneIds)
        skinning_data[i]['numInfluences'] = num_influences
        for j in range(num_influences):
            skinning_data[i]['boneIds'][j] = boneIds[j]
            skinning_data[i]['weights'][j] = weights[j]

    return skinning_data

def export_data_from_current_frame(sop_name):
    # Get the dataset directory (create directory if doesn't exist)
    common.get_dataset_dir()

    # Check the frame is in a valid range
    num_frames = hou.evalParm(sop_name+'/nFrames')
    frame_id = hou.intFrame()
    if frame_id > num_frames or frame_id <= 0:
        print('do not write frame_id({}) because > max_frames({})'.format(frame_id, num_frames))
        return

    # Get the current clip name
    clip_name = hou_common.get_current_clip_name(sop_name)

    # Export skeleton
    # The skeleton hierarchy is frame invariant => only write it once
    bone_names = get_bone_names(hou_common.SMOOTH_SKINNING_INPUT_ID)
    skeleton_path = common.get_skeleton_path()
    if not os.path.exists(skeleton_path):
        parent_names = get_bone_parents(sop_name, bone_names)
        with open(skeleton_path, 'w') as file_handler:
            for i, bone_name in enumerate(bone_names):
                file_handler.write(bone_name + ',' + parent_names[i])
                file_handler.write('\n')

    # Export skinning
    # The skinning data is frame invariant => only write it once
    skinning_data = get_skinning_data(hou_common.SMOOTH_SKINNING_INPUT_ID)
    skinning_path = common.get_skinning_path()
    if not os.path.exists(skinning_path):
        np.save(skinning_path, skinning_data)

    # Export bone and geometry dataset
    bone_data = get_bone_data(sop_name, bone_names)
    base_mesh = get_vertices(hou_common.BASE_SKINNING_INPUT_ID)
    smooth_mesh = get_vertices(hou_common.SMOOTH_SKINNING_INPUT_ID)

    # Create clip data
    clip_data = ClipData(clip_name)
    clip_path = common.get_clip_path(clip_name)
    if not os.path.exists(clip_path):
        num_bones = len(bone_names)
        num_vertices = base_mesh.shape[0]
        clip_data.allocate(num_bones, num_vertices, num_frames)
    else:
        clip_data.allocate_from_file()

    # Save data
    # Houdini animation clip are between [1-max_frames]
    index = frame_id-1;
    clip_data.bone_data[index] = bone_data
    clip_data.base_meshes[index] = base_mesh
    clip_data.smooth_meshes[index] = smooth_mesh

    clip_data.save()

    print('writing frame {}/{} from animation into the file : {}'.format(frame_id, num_frames, clip_path))
