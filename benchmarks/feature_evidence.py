import json
from feature_store import Feature,FeatureStore
s=FeatureStore(); f=Feature("age",42); s.put(f); got=s.get("age"); report={"round_trip":got==f,"name":got.name,"value":got.value}
if not report["round_trip"]: raise SystemExit(report)
print(json.dumps(report,sort_keys=True))
