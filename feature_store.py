"""Canonical versioned feature store with optional TTL semantics."""

from __future__ import annotations

import math
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
        if isinstance(self.version, bool) or not isinstance(self.version, int) or self.version < 1:
            raise ValueError("feature version must be positive")
        if isinstance(self.value, bool) or not isinstance(self.value, (int, float)) or not math.isfinite(self.value):
            raise ValueError("feature value must be finite")
        if self.expires_at is not None and (
            isinstance(self.expires_at, bool)
            or not isinstance(self.expires_at, (int, float))
            or not math.isfinite(self.expires_at)
            or self.expires_at <= 0
        ):
            raise ValueError("feature expiry must be finite and positive")


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
        if (
            isinstance(current_time, bool)
            or not isinstance(current_time, (int, float))
            or not math.isfinite(current_time)
        ):
            raise ValueError("now must be a finite timestamp")
        if feature.expires_at is not None and current_time >= feature.expires_at:
            raise KeyError("expired feature")
        return feature.value
