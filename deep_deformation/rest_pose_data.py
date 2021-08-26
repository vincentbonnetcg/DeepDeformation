"""
@author: Vincent Bonnet
@description : Rest pose of a skeleton

File Format:
 numpy file (npy)

Content:
 1 numpy array
  - float_array(num_bones, size(BONE_ATTRIBUTES))
"""

import common
import os
import numpy as np

class RestPoseData:

    def __init__(self):
        self.bone_data = None

    def allocate(self, num_bones):
        bone_data_shape = (num_bones, len(common.BONE_ATTRIBUTES))
        self.bone_data = np.zeros(bone_data_shape, dtype=float)

    def save(self, overwrite = False):
        rest_path = common.get_rest_pose_path()
        if os.path.exists(rest_path) and overwrite == False:
            return
        np.save(rest_path, self.bone_data)

    def load(self):
        rest_path = common.get_rest_pose_path()
        self.bone_data = np.load(rest_path)
