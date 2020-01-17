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


def test_rsgt(numpy_array, eps=0.0001):
    """Test whether random smooth grayvalue transform function produces the desired output"""
    transformed = rsgt.augmentation.random_smooth_grayvalue_transform(numpy_array)

    # Array shape should be the same, but value should be different
    assert transformed is not numpy_array
    assert transformed.shape == numpy_array.shape
    assert not np.array_equal(transformed, numpy_array)

    # No input value range specified, so output value range should be from 0 to 1
    assert abs(np.min(transformed)) <= eps
    assert abs(np.max(transformed) - 1) <= eps


@pytest.mark.parametrize('dtype', ('float16', 'float32', 'float64'))
def test_rsgt_dtype(numpy_array, dtype):
    """Test whether the returned numpy array has the correct dtype"""
    transformed = rsgt.augmentation.random_smooth_grayvalue_transform(numpy_array, dtype=dtype)
    assert transformed.dtype == np.dtype(dtype)


def test_rsgt_randomness(numpy_array):
    """Test whether multiple calls of the augmentation function give different results"""
    t1 = rsgt.augmentation.random_smooth_grayvalue_transform(numpy_array)
    t2 = rsgt.augmentation.random_smooth_grayvalue_transform(numpy_array)

    # The two transformed images should not be the same
    assert not np.array_equal(t1, t2)
