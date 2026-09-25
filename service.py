import time
import uuid

from fastapi import FastAPI, HTTPException
from fastapi import Request as FastAPIRequest
from opentelemetry import trace
from pydantic import BaseModel

from feature_domain import Feature, FeatureStore

try:
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

    p = TracerProvider(resource=Resource.create({"service.name": "ai-feature-store"}))
    p.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(p)
except Exception:
    pass

app = FastAPI(title="ai-feature-store", version="1.0.0")
tracer = trace.get_tracer("ai-feature-store")


class Request(BaseModel):
    key: str
    payload: dict = {}


@app.middleware("http")
async def observability_headers(request: FastAPIRequest, call_next):
    started = time.perf_counter()
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    correlation_id = request.headers.get("x-correlation-id") or request_id
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    response.headers["x-correlation-id"] = correlation_id
    response.headers["x-latency-ms"] = f"{(time.perf_counter() - started) * 1000:.3f}"
    return response


@app.get("/health/live")
def live():
    return {"status": "ok"}


@app.get("/health/ready")
def ready():
    return {"status": "ready"}


@app.post("/v1/features")
def handle(r: Request):
    with tracer.start_as_current_span("ai-feature-store.domain"):
        try:
            s = FeatureStore()
            f = Feature(
                r.key,
                int(r.payload.get("version", 1)),
                float(r.payload.get("value", 0)),
                float(r.payload.get("expires_at", 1)),
            )
            s.put(f)
            return {
                "name": f.name,
                "version": f.version,
                "value": s.get(f.name, f.version, now=float(r.payload.get("now", 0))),
            }
        except (ValueError, KeyError, RuntimeError) as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
