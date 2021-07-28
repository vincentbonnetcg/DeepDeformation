"""
@author: Vincent Bonnet
@description : Python common code to generate or evaluate dataset
"""

import hou

BASE_SKINNING_INPUT_ID = 0
SMOOTH_SKINNING_INPUT_ID = 1


def get_current_clip_name(sop_name):
    '''
    Returns the current name of the animation clip from Houdini
    '''
    anim_type = hou.parm(sop_name+'/anim_types').evalAsString()
    clip_name = hou.parm(sop_name+'/'+anim_type).evalAsString()
    return clip_name.replace('.bclip','')


