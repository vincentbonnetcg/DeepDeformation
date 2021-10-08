"""
@author: Vincent Bonnet
@description : Clip data is an animation clip

File Format:
 numpy file (npz)

Content:
 3 numpy arrays
  - 'bones' : float_array(num_frames, num_bones, size(BONE_ATTRIBUTES))
  - 'bases' : float_array(num_frames, num_vertices, 3)
  - 'smooths' : float_array(num_frames, num_vertices, 3)
"""

import deep_deformation.utils.common as common
import numpy as np

class ClipData:

    def __init__(self, clip_name):
        self.clip_name = clip_name
        self.bone_data = None
        self.base_meshes = None
        self.smooth_meshes = None

    def get_clip_path(self, predicted = False):
        if predicted:
            return common.get_predicted_clip_path(self.clip_name)
        return common.get_clip_path(self.clip_name)

    def num_bones(self):
        return self.bone_data.shape[1]

    def num_frames(self):
        return len(self.bone_data)

    def num_vertices(self):
        return self.base_meshes.shape[1]

    def allocate(self, num_bones, num_vertices, num_frames):
        # data shape
        bone_data_shape = (num_frames, num_bones, len(common.BONE_ATTRIBUTES))
        base_mesh_shape = (num_frames, num_vertices, 3)
        smooth_mesh_shape = (num_frames, num_vertices, 3)
        # set data
        self.bone_data = np.zeros(bone_data_shape, dtype=float)
        self.base_meshes = np.zeros(base_mesh_shape, dtype=float)
        self.smooth_meshes = np.zeros(smooth_mesh_shape, dtype=float)

    def load(self, predicted = False):
        clip_path = self.get_clip_path(predicted)
        npzfile = np.load(clip_path)
        self.bone_data = npzfile['bones']
        self.base_meshes = npzfile['bases']
        self.smooth_meshes = npzfile['smooths']

    def save(self, predicted = False):
        clip_path = self.get_clip_path(predicted)
        out_attributes = {'bones' : self.bone_data,
                          'bases' : self.base_meshes,
                          'smooths' : self.smooth_meshes}
        np.savez(clip_path, **out_attributes)

