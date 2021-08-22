"""
@author: Vincent Bonnet
@description : Skinning data
"""

import common
import numpy as np
import os


class SkinningData:

    def __init__(self):
        self.num_weights = None
        self.bones_ids = None
        self.weights = None

    def allocate(self, num_points, max_influences):
        self.num_weights = np.empty(num_points, dtype=int)
        self.bones_ids = np.empty((num_points, max_influences), dtype=int)
        self.weights = np.empty((num_points, max_influences), dtype=float)

    def save(self, overwrite=False):
        skinning_path = common.get_skinning_path()
        if os.path.exists(skinning_path) and overwrite == False:
            return

        details = {'num_weights': self.num_weights,
                   'bones_ids': self.bones_ids,
                   'weights': self.weights}
        np.savez(skinning_path, **details)

    def load(self):
        skinning_path = common.get_skinning_path()
        details = np.load(skinning_path)

        self.num_weights = details['num_weights']
        self.bones_ids = details['bones_ids']
        self.weights = details['weights']
