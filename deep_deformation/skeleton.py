"""
@author: Vincent Bonnet
@description : Skeleton object to deal with hierarchy and skeleton text file
skeleton = Skeleton();
skeleton.load(filename)
skeleton.print_root()
"""

from skeleton_data import SkeletonData

class Bone:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None

class Skeleton:
    def __init__(self):
        self.root = None # Bone root
        self.bones = {} # Map associating name with Bone
        self.clear()

    def clear(self):
        self.root = None
        self.bones = {}

    def set(self, skeleton_data : SkeletonData):
        self.clear()

        # Add bone
        for bone_name in skeleton_data.bone_names:
            self.add_bone(bone_name)

        # Add parent
        for i, parent_name in enumerate(skeleton_data.parent_names):
            self.parent(skeleton_data.bone_names[i], parent_name)


    def add_bone(self, bone_name):
        if bone_name in self.bones:
            # already inserted
            return
        self.bones[bone_name] = Bone(bone_name)

    def parent(self, bone_name, parent_name):
        bone = self.bones.get(bone_name, None)
        parent = self.bones.get(parent_name, None)

        assert(bone)

        # parent None is considered the root
        if not parent:
            if not self.root:
                parent = Bone(parent_name)
                self.root = parent
            elif self.root.name != parent_name:
                raise Exception('multiple roots found')
            parent = self.root

        # set hierarchy
        parent.children.append(bone)
        bone.parent = parent

    def print_root(self):
        self._print_hierarchy(self.root)

    def _print_hierarchy(self, node=None, space=0):
        if not node:
            return

        print('|'+'-' * space + node.name)
        for child in node.children:
            self._print_hierarchy(child, space+2)


