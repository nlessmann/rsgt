[![Test status](https://github.com/nlessmann/rsgt/workflows/Tests/badge.svg)](https://github.com/nlessmann/rsgt/actions)
[![pypi](https://img.shields.io/pypi/v/rsgt)](https://pypi.org/project/rsgt/)

# Random Smooth Grayvalue Transformations

## Installation

To use data augmentation with random smooth grayvalue transformations in your own project, simply install the `rsgt` package:

```
pip install rsgt
```

* Supports Python 2.7 and newer (including 3.x)
* Numpy is the only dependency

## Data augmentation

The expected input is a numpy array with integer values, which is usually the case for medical grayvalue images, such as CT and MR scans.

```python
from rsgt.augmentation import random_smooth_grayvalue_transform

# Apply grayvalue transformation to a numpy array
new_image = random_smooth_grayvalue_transform(image, dtype='float32')
```

The returned numpy array will have a floating point dataype and values in the range [0,1].

### Examples

<img alt="Original CT scan" src="/examples/ct0.png" width="216">
<img alt="Transformed CT scan #1" src="/examples/ct1.png" width="216">
<img alt="Transformed CT scan #2" src="/examples/ct2.png" width="216">
<img alt="Transformed CT scan #3" src="/examples/ct3.png" width="216">

The left most image is the original CT slice. The other images show the same slice with random smooth grayvalue transformations applied. The transformation
function is shown below the transformed image. This CT scan is from the [kits19 challenge](https://kits-challenge.org)
([CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license).

## Normalization functions

Because the augmentation function returns values in the range [0,1], it is necessary to either also apply the grayvalue transformation at inference time, or to
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

## License

This package is released under the MIT license, as found in the LICENSE file.
