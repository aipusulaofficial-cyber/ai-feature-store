import math

import pytest

from persistent_feature_store import PersistentFeatureStore


def test_expired_feature_is_not_returned(tmp_path):
    store = PersistentFeatureStore(tmp_path / "features.db")
    store.put("user_score", 1, "42", expires_at=100)
    assert store.get("user_score", 1, now=99)[2] == "42"
    assert store.get("user_score", 1, now=100) is None
    assert store.get("user_score", 1, now=99) is None


def test_feature_without_expiry_is_readable(tmp_path):
    store = PersistentFeatureStore(tmp_path / "features.db")
    store.put("score", 1, "10")
    assert store.get("score", 1, now=100000)[2] == "10"


@pytest.mark.parametrize("timestamp", [math.nan, math.inf, -math.inf, "tomorrow"])
def test_invalid_expiry_rejected(tmp_path, timestamp):
    store = PersistentFeatureStore(tmp_path / "features.db")
    with pytest.raises(ValueError):
        store.put("score", 1, "10", expires_at=timestamp)
