import pytest
import numpy as np

import rsgt.normalization


# Fix random seed
np.random.seed(239085)


@pytest.fixture
def ct_scan():
    image = np.random.rand(64, 32, 24) * 4096 - 1024
    image = np.clip(np.round(image), -1024, 3072)
    return image.astype('int16')


@pytest.fixture
def mr_scan():
    image = np.random.rand(64, 32, 24) * np.random.randint(100, 400)
    return image.round().astype('int16')


def test_ct_normalization(ct_scan, eps=0.0001):
    normalized = rsgt.normalization.normalize_ct_scan(ct_scan)
    assert normalized.shape == ct_scan.shape  # shape should stay the same
    assert not np.array_equal(normalized, ct_scan)  # values should be different

    # Output value should be in [0,1], but does not have to include 0 and 1
    assert np.min(normalized) >= 0 - eps
    assert np.max(normalized) <= 1 + eps


def test_mr_normalization(mr_scan, eps=0.0001):
    normalized = rsgt.normalization.normalize_mr_scan(mr_scan)
    assert normalized.shape == mr_scan.shape  # shape should stay the same
    assert not np.array_equal(normalized, mr_scan)  # values should be different

    # Output value range should be from 0 to 1
    assert abs(np.min(normalized)) <= eps
    assert abs(np.max(normalized) - 1) <= eps
