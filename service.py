from fastapi import FastAPI
from pydantic import BaseModel
from opentelemetry import trace
app=FastAPI(title="ai-feature-store",version="1.0.0");tracer=trace.get_tracer("ai-feature-store")
class Request(BaseModel):key:str;payload:dict={}
@app.get("/health/live")
def live():return {"status":"ok"}
@app.get("/health/ready")
def ready():return {"status":"ready"}
@app.post("/v1/features")
def handle(r:Request):
 with tracer.start_as_current_span("features"):return {"status":"accepted","key":r.key}
