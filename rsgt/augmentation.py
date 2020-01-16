from __future__ import division

import numpy as np
import collections

__all__ = ['random_smooth_grayvalue_transform']


# Parameters of a single sinusoidal function
Sinusoid = collections.namedtuple('Sinusoid', ('frequency', 'amplitude', 'offset'))


def random_smooth_grayvalue_transform(image, n_sinusoids=4, min_frequency=0.2, max_freqency=1.6, dtype='float32', min_max_val=None):
    """
    Applies random smooth grayvalues transformations to a numpy array.

    The original array is not changed, a new array is returned.
    The input array is expected to have integer values, the returned array will have
    values in the range [0,1] and the specified dtype, which should therefore be a
    floating point type.

    The shape of the sin terms can be restricted through the two min/max frequency
    parameters. These define how "bouncy" the final transformation function will be
    (larger values = more ups and downs in the function).

    The range of input values can be optionally specified, otherwise the min and max
    values of the input image are used. In cases where the input value range
    is known, it makes sense to use this parameter, e.g., when using CT data.

    :param image: numpy array, or anything convertable into a numpy array
    :param n_sinusoids: int, the number of sinusoidal functions that will make up the transformation function
    :param min_frequency: float, minimal frequency of the randomly generated sin functions
    :param max_freqency: float, maximal frequency of the randomly generated sin functions
    :param dtype: Target dtype, should be a floating point type because output values are in [0,1]
    :param min_max_val: Tuple of two values (min/max), or None; range of input values
    :return: numpy array with specific dtype and values in the range [0, 1]
    """
    assert n_sinusoids > 0
    assert min_frequency > 0
    assert max_freqency > min_frequency

    # Make sure input data is an integer array, otherwise the LUT does not work
    image = np.asanyarray(image, dtype=int)

    # Randomly generate a number of sinusoids
    sinusoids = []
    for _ in range(n_sinusoids):
        frequency = np.random.uniform(min_frequency, max_freqency)
        sinusoids.append(Sinusoid(
            frequency=frequency,
            amplitude=np.random.uniform(-1 / frequency, 1 / frequency),
            offset=np.random.uniform(0, 2 * np.pi)
        ))

    # Sample and sum up the sinusoids
    if min_max_val is None:
        min_val = np.min(image)
        max_val = np.max(image)
    else:
        min_val, max_val = min_max_val
    x = np.linspace(0, 2 * np.pi, max_val - min_val + 1)

    y = np.zeros_like(x)
    for sin in sinusoids:
        y += sin.amplitude * np.sin(sin.frequency * (x + sin.offset))

    # Scale amplitude so that y has values from 0 to 1
    min_amp = np.min(y)
    max_amp = np.max(y)
    y = (y - min_amp) / (max_amp - min_amp)

    # Apply LUT to image
    return y[image - min_val].astype(dtype)
