# ADR-0002: Production hardening
FastAPI defines the feature service contract and OpenTelemetry traces reads. Kubernetes/Helm package bounded runtime resources; Terraform owns infrastructure inputs. Trivy/CycloneDX gate security and SBOM; contract/property tests protect feature APIs; Locust validates load.
Online/offline consistency and durable storage remain domain responsibilities and are externalized in production.
