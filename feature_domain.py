import time
from dataclasses import dataclass


@dataclass(frozen=True)
class Feature:
    name: str
    version: int
    value: float
    expires_at: float


class FeatureStore:
    def __init__(self):
        self._items = {}

    def put(self, f: Feature):
        if f.version < 1 or f.expires_at <= 0:
            raise ValueError("invalid feature")
        self._items[(f.name, f.version)] = f

    def get(self, name, version, now=None) -> float:
        f = self._items[(name, version)]
        now = time.time() if now is None else now
        if now >= f.expires_at:
            raise KeyError("feature expired")
        return f.value
