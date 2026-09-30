# AI Feature Store

[![CI](https://github.com/aipusulaofficial-cyber/ai-feature-store/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/aipusulaofficial-cyber/ai-feature-store/actions/workflows/ci.yml)
[![Production Tests](https://github.com/aipusulaofficial-cyber/ai-feature-store/actions/workflows/production-tests.yml/badge.svg?branch=main)](https://github.com/aipusulaofficial-cyber/ai-feature-store/actions/workflows/production-tests.yml)
[![Security / SBOM](https://github.com/aipusulaofficial-cyber/ai-feature-store/actions/workflows/security-sbom.yml/badge.svg?branch=main)](https://github.com/aipusulaofficial-cyber/ai-feature-store/actions/workflows/security-sbom.yml)


A feature-serving platform built around explicit feature contracts, freshness validation, lifecycle versioning and online/offline consistency boundaries.

## What this project does
Features are registered with a defined shape and provenance, validated against contract expectations, and served through controlled boundaries. Freshness and consistency are treated as correctness properties rather than dashboard-only metrics.

## Architecture
```text
Feature definition
   -> contract + schema validation
   -> version / provenance
   -> offline or online boundary
   -> serving result
```

The online serving path is kept distinct from offline materialization so latency-sensitive access does not inherit batch concerns.

## Correctness contract
- Shape and type validation occurs at the boundary.
- Feature versions are explicit.
- Freshness is validated where required.
- Provenance is retained for operational diagnosis.
- Offline/online consistency failures are testable failure modes.

## Reliability & security
External stores are replaceable adapters. Failure paths are explicit and CI includes security validation.

## Evidence
[docs/PRINCIPAL-ENGINEERING.md](docs/PRINCIPAL-ENGINEERING.md) · [ARCHITECTURE.md](ARCHITECTURE.md) · [ADRs](ADRs/)

**Engineering chain:** Code → Contract → Test → Security → Runtime → Observability → Deployment → Evidence.

## Portfolio evidence
[Portfolio evidence map](docs/PORTFOLIO_EVIDENCE.md) — executable proof, architecture mapping and reviewable CI evidence.
