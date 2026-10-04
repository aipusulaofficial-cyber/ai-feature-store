from persistent_feature_store import PersistentFeatureStore


def test_expired_features_are_not_returned(tmp_path):
    store = PersistentFeatureStore(tmp_path / "features.db")
    store.put("old", 1, "secret", expires_at=99.0)
    store.put("fresh", 1, "value", expires_at=101.0)
    assert store.get("old", 1, now=100.0) is None
    assert store.get("fresh", 1, now=100.0)[2] == "value"
