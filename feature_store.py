"""Feature store contract: typed definitions, versions and TTL-aware online reads."""

from dataclasses import dataclass
import time


@dataclass(frozen=True)
class Feature:
    name: str
    version: int
    value: float
    expires_at: float | None = None


class FeatureStore:
    def __init__(self):
        self.data = {}

    def put(self, f):
        self.data[(f.name, f.version)] = f

    def get(self, name, version, now=None):
        f = self.data.get((name, version))
        if f is None:
            raise KeyError(name)
        now = time.time() if now is None else now
        if f.expires_at is not None and now >= f.expires_at:
            raise KeyError("expired feature")
        return f.value
