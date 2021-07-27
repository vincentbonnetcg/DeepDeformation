"""
@author: Vincent Bonnet
@description : Manage read/write for the various files/folder
"""

from clip_data import ClipData
import numpy as np
import os

def normalize(data):
    min_v = np.min(data)
    max_v = np.max(data)
    data -= min_v
    data /= (max_v - min_v)

def load_dataset(clip_name, test_ratio = 0.1):
    # load a single dataset
    # TODO : should load from multiple datasets !
    clip_data = ClipData(clip_name)
    clip_data.allocate_from_file(predicted = False)

    bones = clip_data.bone_data
    bases = clip_data.base_meshes
    smooths = clip_data.smooth_meshes
    num_examples = clip_data.num_frames

    in_shape = np.prod(bones.shape[1:])
    out_shape = np.prod(smooths.shape[1:])

    # pre-allocate tests and training data
    # TODO : do not suffle
    example_ids = np.arange(num_examples)
    np.random.shuffle(example_ids)
    num_test = int(num_examples * test_ratio)
    num_train = num_examples - num_test
    test_ids = example_ids[num_train:]
    train_ids = example_ids[:num_train]

    x_train = np.empty((num_train, in_shape))
    y_train = np.empty((num_train, out_shape))
    x_test = np.empty((num_test, in_shape))
    y_test = np.empty((num_test, out_shape))

    # set data for training and test
    for i, example_id in enumerate(train_ids):
        x_train[i][:] = bones[example_id].flatten()[:]
        y_train[i][:] = smooths[example_id].flatten()[:] - bases[example_id].flatten()[:]

    for i, example_id in enumerate(test_ids):
        x_test[i][:] = bones[example_id].flatten()[:]
        y_test[i][:] = smooths[example_id].flatten()[:] - bases[example_id].flatten()[:]

    # normalize data
    # TODO - add container to store the re-scaling parameters
    #normalize(x_train)
    #normalize(y_train)
    #normalize(x_test)
    #normalize(y_test)

    return x_train, y_train, x_test, y_test, train_ids, test_ids


def write_predicted_clip(clip_name, predicted_offsets, example_ids):
    clip_data = ClipData(clip_name)
    predict_clip_path = clip_data.get_clip_path(predicted = True)

    if not os.path.exists(predict_clip_path):
        clip_data.allocate_from_file(predicted = False)
    else:
        clip_data.allocate_from_file(predicted = True)

    for i, example_id in enumerate(example_ids):
        offsets = predicted_offsets[i].reshape(clip_data.base_meshes.shape[1:])
        clip_data.smooth_meshes[example_id] = clip_data.base_meshes[example_id] + offsets

    clip_data.save(predicted = True)

