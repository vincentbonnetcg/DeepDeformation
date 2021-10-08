"""
@author: Vincent Bonnet
@description : Skinning algorithms. Implement the Linear Blend Skinning (LBS)
"""

from deep_deformation.objects.skeleton_data import SkeletonData
from deep_deformation.objects.skinning_data import SkinningData
from deep_deformation.objects.clip_data import ClipData


class Skinning:

    def __init__(self, skeleton_data : SkeletonData, skinning_data : SkinningData):
        self.skeleton_data = skeleton_data
        self.skinning_data = skinning_data

    def get_vertices_from_clip(self, clip_data : ClipData):
        # TODO
        pass

