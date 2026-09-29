import math
import sqlite3
import time
from pathlib import Path


class PersistentFeatureStore:
    def __init__(self, path="features.db"):
        self.path = str(Path(path))
        with sqlite3.connect(self.path) as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS features "
                "(name TEXT NOT NULL, version INTEGER NOT NULL, value TEXT NOT NULL, "
                "expires_at REAL, PRIMARY KEY(name,version))"
            )

    def put(self, name, version, value, expires_at=None):
        if not name or not isinstance(version, int) or version < 1:
            raise ValueError("invalid feature")
        if expires_at is not None and (
            not isinstance(expires_at, (int, float)) or not math.isfinite(expires_at)
        ):
            raise ValueError("expires_at must be a finite timestamp")
        with sqlite3.connect(self.path) as db:
            db.execute(
                "INSERT OR REPLACE INTO features VALUES(?,?,?,?)",
                (name, version, value, expires_at),
            )

    def get(self, name, version, *, now=None):
        current = time.time() if now is None else now
        if not isinstance(current, (int, float)) or not math.isfinite(current):
            raise ValueError("now must be a finite timestamp")
        with sqlite3.connect(self.path) as db:
            row = db.execute(
                "SELECT name,version,value,expires_at FROM features WHERE name=? AND version=?",
                (name, version),
            ).fetchone()
            if row is not None and row[3] is not None and row[3] <= current:
                db.execute(
                    "DELETE FROM features WHERE name=? AND version=? AND expires_at<=?",
                    (name, version, current),
                )
                return None
            return row
