"""
@author: Vincent Bonnet
@description : Skinning algorithms. Implement the Linear Blend Skinning (LBS)
"""

from skeleton_data import SkeletonData
from skinning_data import SkinningData
from clip_data import ClipData


class Skinning:

    def __init__(self, skeleton_data : SkeletonData, skinning_data : SkinningData):
        self.skeleton_data = skeleton_data
        self.skinning_data = skinning_data

    def get_vertices_from_clip(self, clip_data : ClipData):
        # TODO
        pass

