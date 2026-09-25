from feature_store import *
import pytest


def test_versioned_read():
    s = FeatureStore()
    s.put(Feature("risk", 1, 0.7))
    s.put(Feature("risk", 2, 0.8))
    assert s.get("risk", 2) == 0.8


def test_ttl():
    s = FeatureStore()
    s.put(Feature("x", 1, 1, 10))
    with pytest.raises(KeyError):
        s.get("x", 1, 10)


def test_missing():
    with pytest.raises(KeyError):
        FeatureStore().get("x", 1)
