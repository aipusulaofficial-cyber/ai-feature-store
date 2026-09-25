# Failure matrix

| Failure | Detection | Action | Retry? | Impact |
|---|---|---|---|---|
| Invalid input | validation | reject | No | 4xx |
| Dependency timeout | timeout budget | normalize | Safe/idempotent only | bounded failure/degradation |
| Dependency error | adapter | exponential backoff | Safe/idempotent only | bounded latency |
| Repeated failure | circuit breaker | open circuit | No while open | fast failure |
| Overload | bounded executor/token bucket | fail fast/degrade | No | 429/degraded |
| Telemetry failure | exporter | preserve domain result | exporter-local | no corruption |

Provider timeout -> bounded retry for idempotent reads/writes; stale feature -> explicit freshness failure/degradation; repeated provider failure -> circuit open; unbounded reads are rejected.