import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from feature_store import Feature,FeatureStore
s=FeatureStore(); f=Feature("age",1,42.0); s.put(f); got=s.get("age",1); report={"round_trip":got==f.value,"name":f.name,"version":f.version,"value":got}
if not report["round_trip"] or report["version"] != 1: raise SystemExit(report)
print(json.dumps(report,sort_keys=True))
