from __future__ import division

import numpy as np

__all__ = ['normalize_ct_scan', 'normalize_mr_scan']


def normalize_ct_scan(image, dtype='float32'):
    """
    Normalizes a CT scan from the range of Hounsfield Units [-1000, ~3000) to the range [0,1]

    :param image: numpy array
    :param dtype: output dtype, should be a floating point type
    :return: numpy array
    """
    image = np.asanyarray(image)
    image_pos = np.clip(image + 1000, 0, 4096)
    return image_pos.astype(dtype) / 4096


def normalize_mr_scan(image, dtype='float32'):
    """
    Normalizes an MR scan by scaling the values in the [5%,95%] percentiles to the range [0,1]

    :param image: numpy array
    :param dtype: output dtype, should be a floating point type
    :return: numpy array
    """
    image = np.asanyarray(image, dtype=dtype)
    p5, p95 = np.percentile(image, (5, 95))
    image = (image - p5) / (p95 - p5)
    return np.clip(image, 0, 1)
