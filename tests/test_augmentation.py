import pytest
import numpy as np

import rsgt.augmentation


# Fix random seed
np.random.seed(239085)


@pytest.fixture
def numpy_array():
    image = np.random.rand(16, 32, 24, 8) * 4096 - 1024
    image = np.clip(np.round(image), -1024, 3072)
    return image.astype('int16')


@pytest.mark.parametrize('ndim', (1, 2, 3, 4))
def test_rsgt(numpy_array, ndim, eps=0.0001):
    """Test whether random smooth grayvalue transform function produces the desired output"""
    if ndim < numpy_array.ndim:
        numpy_array = numpy_array.reshape(numpy_array.shape[:(ndim - 1)] + (-1,))
    transformed = rsgt.augmentation.random_smooth_grayvalue_transform(numpy_array)

    # Array shape should be the same, but value should be different
    assert transformed is not numpy_array
    assert transformed.shape == numpy_array.shape
    assert not np.array_equal(transformed, numpy_array)

    # No input value range specified, so output value range should be exactly from 0 to 1
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


def test_rsgt_tolerate_incorrect_min_max_values(numpy_array, eps=0.0001):
    """Test whether incorrect min/max values are tolerated"""
    min_val = np.min(numpy_array) + 1
    max_val = np.max(numpy_array) - 1
    transformed = rsgt.augmentation.random_smooth_grayvalue_transform(numpy_array, min_max_val=(min_val, max_val))

    # Output values should still be in [0,1], even though min/max were incorrectly specified
    assert np.min(transformed) >= 0 - eps
    assert np.max(transformed) <= 1 + eps
