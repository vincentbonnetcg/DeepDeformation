"""
@author: Vincent Bonnet
@description : Skeleton data contains bones and respective
"""

import common
import os
import json

class SkeletonData:

    def __init__(self):
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

        details = {}
        details['bone_names'] = self.bone_names
        details['parent_names'] = self.parent_names

        with open(skeleton_path, 'w') as file_handler:
            file_handler.write(json.dumps(details))

    def load(self):
        skeleton_path = common.get_skeleton_path()

        with open(skeleton_path, 'r') as file_handler:
            details = json.load(file_handler)
            self.bone_names = details['bone_names']
            self.parent_names = details['parent_names']

        assert(len(self.bone_names) == len(self.parent_names))
