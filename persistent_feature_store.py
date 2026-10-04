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
        if not name or version < 1:
            raise ValueError("invalid feature")
        with sqlite3.connect(self.path) as db:
            db.execute(
                "INSERT OR REPLACE INTO features VALUES(?,?,?,?)",
                (name, version, value, expires_at),
            )

    def get(self, name, version, now=None):
        current = time.time() if now is None else now
        with sqlite3.connect(self.path) as db:
            return db.execute(
                "SELECT name,version,value,expires_at FROM features "
                "WHERE name=? AND version=? AND (expires_at IS NULL OR expires_at > ?)",
                (name, version, current),
            ).fetchone()
