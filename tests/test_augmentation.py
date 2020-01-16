import pytest
import numpy as np

import rsgt.augmentation


# Fix random seed
np.random.seed(239085)


@pytest.fixture
def numpy_array():
    image = np.random.rand(64, 32, 24) * 4096 - 1024
    image = np.clip(np.round(image), -1024, 3072)
    return image.astype('int16')


def test_rsgt_numpy(numpy_array, eps=0.0001):
    transformed = rsgt.augmentation.random_smooth_grayvalue_transform(numpy_array)
    assert transformed.shape == numpy_array.shape  # shape should stay the same
    assert not np.array_equal(transformed, numpy_array)  # values should be different

    # No input value range specified, so output value range should be from 0 to 1
    assert abs(np.min(transformed)) <= eps
    assert abs(np.max(transformed) - 1) <= eps
