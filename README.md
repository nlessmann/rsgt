![Test status](https://github.com/nlessmann/rsgt/workflows/Tests/badge.svg)
![Python](https://img.shields.io/pypi/pyversions/rsgt)
![pypi](https://img.shields.io/pypi/v/rsgt)

# Random Smooth Grayvalue Transformations

Usage:

```python
import numpy as np
from rsgt.augmentation import random_smooth_grayvalue_transform

image = np.zeros(shape=(64, 64, 64))
new_image = random_smooth_grayvalue_transform(image)
```

## License

This package is released under the MIT license, as found in the LICENSE file.
