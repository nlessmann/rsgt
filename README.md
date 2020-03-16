[![Test status](https://github.com/nlessmann/rsgt/workflows/Tests/badge.svg)](https://github.com/nlessmann/rsgt/actions)
[![Code coverage](https://codecov.io/gh/nlessmann/rsgt/branch/master/graph/badge.svg)](https://codecov.io/gh/nlessmann/rsgt)
[![Documentation status](https://readthedocs.org/projects/rsgt/badge/?version=latest)](https://rsgt.readthedocs.io/en/latest/?badge=latest)
[![pypi](https://img.shields.io/pypi/v/rsgt)](https://pypi.org/project/rsgt/)

# Random Smooth Grayvalue Transformations

Convolutional neural networks trained for a detection or segmentation task in a specific type of medical gray value images, such as CT or MR images, typically
fail in other medical gray value images, even if the target structure *looks* similar in both types of images. Random smooth gray value transformations are a
data augmentation technique aimed at forcing the network to become gray value invariant. During training, the gray value of the training images or patches are
randomly changed, but using a smooth and continous transfer function so that shape and texture information is largely retained.

API documentation: http://rsgt.readthedocs.io/

## Installation

To use data augmentation with random smooth gray value transformations in your own project, simply install the `rsgt` package:

```
pip install rsgt
```

* Requires Python 2.7+ or 3.5+
* Numpy is the only other dependency

## Data augmentation

The expected input is a numpy array with integer values, which is usually the case for medical gray value images, such as CT and MR scans.

```python
from rsgt.augmentation import random_smooth_grayvalue_transform

# Apply gray value transformation to a numpy array
new_image = random_smooth_grayvalue_transform(image, dtype='float32')
```

The returned numpy array will have a floating point dataype and values in the range [0,1].

### Mini-batches

While the function supports input data with any number of dimensions, it does currently not support mini-batches. A mini-batch of 3D images can be treated as a
4D input array, but all images in the mini-batch will then be subject to the same transformation. This means that a single random look up table will be computed
and applied to all images in the mini-batch. There is currently no vectorized implementation of the transformation function, so a for loop is at this point the
only way to transform images in a mini-batch with different transformation functions:

```python
for i in range(minibatch.shape[0]):
    minibatch[i] = random_smooth_grayvalue_transform(minibatch[i], dtype='float32')
```

### Examples

<img alt="Original CT scan" src="/examples/ct0.png" width="216"><img alt="Transformed CT scan #1" src="/examples/ct1.png" width="216"><img alt="Transformed CT scan #2" src="/examples/ct2.png" width="216"><img alt="Transformed CT scan #3" src="/examples/ct3.png" width="216">

The left most image is the original CT slice. The other images show the same slice with random smooth gray value transformations applied. The transformation
function is shown below the transformed image.

This CT scan is from the [kits19 challenge](https://kits-challenge.org) ([CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license).

## Normalization functions

Because the augmentation function returns values in the range [0,1], it is necessary to either also apply the gray value transformation at inference time, or to
normalize input images at inference time to [0,1]. The `rsgt` package comes with helper functions for CT and MR scans:

### CT scans

Expected values of the original image are Hounsfield units ranging from -1000 for air (and below for background outside the image area) to around 3000 for very
dense structures like metal implants.

```python
from rsgt.normalization import normalize_ct_scan
normalized_image = normalize_ct_scan(image, dtype='float32')
```

### MR scans

Because values of MR scans are not standardized like those of CT scans, the normalization is based on the 5% and the 95% percentiles of the input values. Values
below and above are clipped.

```python
from rsgt.normalization import normalize_mr_scan
normalized_image = normalize_mr_scan(image, dtype='float32')
```

This normalization can also be used in combination with the augmentation technique:

```python
from rsgt.augmentation import random_smooth_grayvalue_transform
from rsgt.normalization import normalize_mr_scan

N = 4096  # number of bins
normalized_integer_image = (normalize_mr_scan(image, dtype='float32') * N).round().astype(int)
new_image = random_smooth_grayvalue_transform(normalized_integer_image, min_max_val=(0, N), dtype='float32')
```

## Citation

Please cite our short paper describing random smooth gray value transformations for data augmentation when using this technique in your work:

> N. Lessmann and B. van Ginneken, "Random smooth gray value transformations for cross modality learning with gray value invariant networks",
> [arXiv:2003.06158](https://arxiv.org/abs/2003.06158)

## License

This package is released under the [MIT license](LICENSE), as found in the LICENSE file, with the exception of the images in the `/examples` directory, which
are released under a Creative Commons license ([CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)).
