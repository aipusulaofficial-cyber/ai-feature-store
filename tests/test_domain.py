from feature_domain import Feature, FeatureStore


def test_ttl():
    s = FeatureStore()
    s.put(Feature("x", 1, 3, 10))
    assert s.get("x", 1, now=9) == 3
