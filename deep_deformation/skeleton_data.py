"""
@author: Vincent Bonnet
@description : Skeleton data contains bones and respective
"""

import common
import os

class SkeletonData:

    def __init__(self):
        # infos
        self.bone_names = []
        self.parent_names = []

    def allocate(self, bone_names, parent_names):
        assert(len(bone_names) == len(parent_names))
        self.bone_names = bone_names
        self.parent_names = parent_names

    def save(self, overwrite = False):
        skeleton_path = common.get_skeleton_path()
        if os.path.exists(skeleton_path) and overwrite==False:
            return

        with open(skeleton_path, 'w') as file_handler:
            # TODO : write with a dictionnary
            for i, bone_name in enumerate(self.bone_names):
                file_handler.write(bone_name + ',' + self.parent_names[i])
                file_handler.write('\n')

