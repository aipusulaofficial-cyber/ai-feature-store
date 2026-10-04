import pytest

from feature_store import Feature, FeatureStore
from persistent_feature_store import PersistentFeatureStore


def test_expired_features_are_not_returned(tmp_path):
    store = PersistentFeatureStore(tmp_path / "features.db")
    store.put("old", 1, "secret", expires_at=99.0)
    store.put("fresh", 1, "value", expires_at=101.0)
    assert store.get("old", 1, now=100.0) is None
    assert store.get("fresh", 1, now=100.0)[2] == "value"


def test_canonical_feature_store_rejects_nonfinite_ttl():
    with pytest.raises(ValueError):
        Feature("bad", 1, 1.0, float("nan"))


def test_canonical_feature_store_rejects_nonfinite_clock():
    store = FeatureStore()
    store.put(Feature("ok", 1, 1.0, 100.0))
    with pytest.raises(ValueError):
        store.get("ok", 1, now=float("inf"))
