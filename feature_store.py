"""Canonical versioned feature store with optional TTL semantics."""

from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass(frozen=True)
class Feature:
    name: str
    version: int
    value: float
    expires_at: float | None = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("feature name is required")
        if self.version < 1:
            raise ValueError("feature version must be positive")
        if self.expires_at is not None and self.expires_at <= 0:
            raise ValueError("feature expiry must be positive")


class FeatureStore:
    def __init__(self) -> None:
        self._items: dict[tuple[str, int], Feature] = {}

    def put(self, feature: Feature) -> None:
        self._items[(feature.name, feature.version)] = feature

    def get(self, name: str, version: int, now: float | None = None) -> float:
        feature = self._items.get((name, version))
        if feature is None:
            raise KeyError(name)
        current_time = time.time() if now is None else now
        if feature.expires_at is not None and current_time >= feature.expires_at:
            raise KeyError("expired feature")
        return feature.value
