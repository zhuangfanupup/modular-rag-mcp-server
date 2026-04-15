# Project Technical Knowledge (Internal)

## Architecture

- Layered modules: core / ingestion / libs / mcp_server / observability
- Provider abstraction with factories
- Config-first behavior

## Critical Stability Points

- Ingestion idempotency
- Vector/BM25 consistency
- MCP tool timeout and error handling
- Trace completeness

## Regression Focus

- Stage A-E acceptance
- Full `pytest -q`
- External dependency skip logic validity
