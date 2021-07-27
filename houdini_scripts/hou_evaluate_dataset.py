"""
@author: Vincent Bonnet
@description : Python code to test the training data
"""
from ..clip_data import ClipData
import hou_common
import hou

def read_dataset_from_current_frame(sop_name, mode):
    # mode(0) => bases
    # mode(1) => smooth
    # mode(2) => predicted
    clip_name = hou_common.get_current_clip_name(sop_name)

    clip_data = ClipData(clip_name)
    clip_data.allocate_from_file(predicted = (mode == 2))

    mesh_data = None
    if mode == 0:
        mesh_data = clip_data.base_meshes
    else:
        mesh_data = clip_data.smooth_meshes

    mesh = mesh_data[hou.intFrame() - 1]

    node = hou.pwd()
    geo = node.geometry()
    for i, point in enumerate(geo.points()):
        point.setPosition(mesh[i])
