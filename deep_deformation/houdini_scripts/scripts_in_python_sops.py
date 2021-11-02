## Those scripts are in the Python SOPs of tube_rig.hipnc

## -------------------------- ##
## Script to generate dataset ##
## -------------------------- ##
import hou
import os
import sys

# For now working_dir == package_dir, they could be different
working_dir = os.path.dirname(os.path.dirname(hou.hipFile.path()))
package_dir = working_dir
for a_dir in [working_dir, package_dir]:
    if not a_dir in sys.path:
        sys.path.append(a_dir)

import deep_deformation
import deep_deformation.utils.common
from deep_deformation.houdini_scripts import hou_gen
reload(hou_gen)

deep_deformation.utils.common.WORKING_DIR = working_dir
hou_gen.export_data_from_current_frame('/obj/mocapbiped3/')


## ---------------------- ##
## Script to read dataset ##
## ---------------------- ##
import hou
import os
import sys

# For now working_dir == package_dir, they could be different
working_dir = os.path.dirname(os.path.dirname(hou.hipFile.path()))
package_dir = os.path.dirname(working_dir)
for a_dir in [working_dir, package_dir]:
    if not a_dir in sys.path:
        sys.path.append(a_dir)

# For now working_dir == package_dir, they could be different
import deep_deformation
from deep_deformation.houdini_scripts import hou_eval
reload(hou_eval)

# mode(0) => bases
# mode(1) => smooth
# mode(2) => predicted
deep_deformation.utils.common.WORKING_DIR = working_dir
hou_eval.read_dataset_from_current_frame('/obj/mocapbiped3/', mode=0)

