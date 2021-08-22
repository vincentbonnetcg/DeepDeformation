"""
@author: Vincent Bonnet
@description : Skinning algorithms. Implement the Linear Blend Skinning (LBS)
"""

from skeleton_data import SkeletonData
from skinning_data import SkinningData
from clip_data import ClipData


class Skinning:

    def __init__(self, skeleton : SkeletonData, skinning : SkinningData):
        self.skeleton = skeleton
        self.skinning = skinning

    def get_vertices_from_clip(self, clip : ClipData):
        # TODO
        pass

