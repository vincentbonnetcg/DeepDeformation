"""
@author: Vincent Bonnet
@description : Prepare input data for the model
"""


from clip_data import ClipData
import numpy as np

'''
def normalize(data):
    min_v = np.min(data)
    max_v = np.max(data)
    data -= min_v
    data /= (max_v - min_v)
'''

def prepare_data(clip_data, example_ids):
    bones = clip_data.bone_data
    bases = clip_data.base_meshes
    smooths = clip_data.smooth_meshes
    num_examples = clip_data.num_frames
    num_examples_ids = len(example_ids)

    # TODO : replace the bases with a skinning algorithm

    assert(num_examples_ids <= num_examples)

    in_shape = np.prod(bones.shape[1:])
    out_shape = np.prod(smooths.shape[1:])

    x = np.empty((num_examples_ids, in_shape))
    y = np.empty((num_examples_ids, out_shape))

    for i, example_id in enumerate(example_ids):
        x[i][:] = bones[example_id].flatten()[:]
        y[i][:] = smooths[example_id].flatten()[:] - bases[example_id].flatten()[:]

    # normalize data
    # TODO - add container to store the re-scaling parameters
    #normalize(x)
    #normalize(y)
    return x, y

def load_dataset(clip_name, validation_ratio = 0.1):
    # load a single dataset and split between train and validation data
    clip_data = ClipData(clip_name)
    clip_data.allocate_from_file(predicted = False)
    num_examples = clip_data.num_frames

    if (validation_ratio == 0.0):
        return prepare_data(clip_data, range(num_examples))

    # pre-allocate tests and training data
    # TODO : do not suffle
    example_ids = np.arange(num_examples)
    np.random.shuffle(example_ids)

    num_valid = max(int(num_examples * validation_ratio), 1)
    num_train = num_examples - num_valid

    train_ids = example_ids[:num_train]
    valid_ids = example_ids[num_train:]

    x_train, y_train = prepare_data(clip_data, train_ids)
    x_valid, y_valid = prepare_data(clip_data, valid_ids)

    return x_train, y_train, x_valid, y_valid
