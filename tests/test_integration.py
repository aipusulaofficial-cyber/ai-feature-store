from fastapi.testclient import TestClient
from service import app


def test_http_contract_and_domain():
    c = TestClient(app)
    assert c.get("/health/live").status_code == 200
    r = c.post(
        "/v1/features",
        json={
            "key": "integration",
            "payload": {"version": 1, "value": 2, "expires_at": 100, "now": 1},
        },
    )
    assert r.status_code == 200, r.text
