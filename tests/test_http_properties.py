from hypothesis import given, strategies as st
from fastapi.testclient import TestClient
from service import app

c = TestClient(app)


def test_contract():
    assert c.get("/health/live").status_code == 200


@given(st.text(min_size=1, max_size=32))
def test_property(v):
    assert (
        c.post(
            "/v1/features",
            json={
                "key": v,
                "payload": {"version": 1, "value": 1, "expires_at": 100, "now": 1},
            },
        ).status_code
        == 200
    )
