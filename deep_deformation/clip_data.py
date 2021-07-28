"""
@author: Vincent Bonnet
@description : Clip data is an animation clip
"""

import common
import numpy as np

class ClipData:

    def __init__(self, clip_name):
        self.clip_name = clip_name
        # infos
        self.num_bones = 0
        self.num_vertices = 0
        self.num_frames = 0
        # data
        self.bone_data = None
        self.base_meshes = None
        self.smooth_meshes = None

    def get_clip_path(self, predicted = False):
        if predicted:
            return common.get_predicted_clip_path(self.clip_name)
        return common.get_clip_path(self.clip_name)

    def allocate(self, num_bones, num_vertices, num_frames):
        # set infos
        self.num_bones = num_bones
        self.num_vertices = num_vertices
        self.num_frames = num_frames
        # data shape
        bone_data_shape = (num_frames, num_bones, len(common.BONE_ATTRIBUTES))
        base_mesh_shape = (num_frames, num_vertices, 3)
        smooth_mesh_shape = (num_frames, num_vertices, 3)
        # set data
        self.bone_data = np.empty(bone_data_shape, dtype=float)
        self.base_meshes = np.empty(base_mesh_shape, dtype=float)
        self.smooth_meshes = np.empty(smooth_mesh_shape, dtype=float)

    def allocate_from_file(self, predicted = False):
        clip_path = self.get_clip_path(predicted)
        npzfile = np.load(clip_path)
        # set data
        self.bone_data = npzfile['bones']
        self.base_meshes = npzfile['bases']
        self.smooth_meshes = npzfile['smooths']
        # set infos
        self.num_bones = self.bone_data.shape[1]
        self.num_vertices = self.base_meshes.shape[1]
        self.num_frames = len(self.bone_data)

    def save(self, predicted = False):
        clip_path = self.get_clip_path(predicted)
        out_attributes = {'bones' : self.bone_data,
                          'bases' : self.base_meshes,
                          'smooths' : self.smooth_meshes}
        np.savez(clip_path, **out_attributes)

