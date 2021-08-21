"""
@author: Vincent Bonnet
@description : Skinning data
"""

import common
import numpy as np
import os

class SkinningData:

    def __init__(self):
        self.data = None

    def allocate(self, num_points, max_influences):
        data_type = {}
        data_type['names'] = ['numInfluences', 'boneIds', 'weights']
        data_type['formats'] = ['int8', ('int8', max_influences), ('float32', max_influences)]
        self.data = np.zeros(num_points, dtype=np.dtype(data_type, align=True))

    def save(self, overwrite = False):
        skinning_path = common.get_skinning_path()
        if os.path.exists(skinning_path) and overwrite==False:
            return

        np.save(skinning_path, self.data)
