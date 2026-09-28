from feature_store import Feature, FeatureStore


def test_feature_store_round_trip_and_expiry():
    store = FeatureStore()
    store.put(Feature("ctr", 1, 0.42, expires_at=100.0))
    assert store.get("ctr", 1, now=99.0) == 0.42
    try:
        store.get("ctr", 1, now=100.0)
    except KeyError as exc:
        assert str(exc).strip("'") == "expired feature"
    else:
        raise AssertionError("expired feature must not be returned")
