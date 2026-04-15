# Developer Specification (DEV_SPEC)

Version: 1.0.0 (Personal Edition)

## 1. Project Positioning

This repository is a personally maintained engineering project for production-oriented RAG and MCP service delivery.

Primary goals:

- Build a robust, modular, and observable RAG system
- Expose standardized MCP tools for AI clients
- Keep architecture extensible for evolving business needs
- Maintain predictable quality via staged acceptance and full regression tests

## 2. Scope

In scope:

- Ingestion pipeline (load, split, transform, encode, upsert)
- Hybrid retrieval (dense + sparse + fusion + optional rerank)
- MCP server and core tools
- Dashboard and trace observability
- Evaluation and regression testing

Out of scope:

- Public teaching curriculum
- Interview-prep-focused narrative
- Public coaching workflow as project default

## 3. Architecture Principles

- Pluggable providers: LLM/Embedding/Reranker/VectorStore
- Strict layering: core / ingestion / libs / mcp_server / observability
- Config-first behavior with explicit defaults
- Graceful degradation when external dependencies are unavailable
- Idempotent operations where practical

## 4. Quality Gates

Stage acceptance must be completed in order:

1. Stage A: Baseline imports and config loading
2. Stage B: Provider/factory and adapter stability
3. Stage C: Ingestion/storage consistency
4. Stage D: Query/retrieval/trace integrity
5. Stage E: MCP protocol and tool-chain reliability

Final gate:

- Run full regression (`pytest -q`)
- Must pass with deterministic, explainable skips for external-service-only tests

## 5. Operational Rules

- No destructive git/file actions without explicit approval
- Keep behavior backward-compatible unless intentionally versioned
- Prefer small, test-backed changes
- Document any environment assumptions and skip logic

## 6. Delivery Standard

A release candidate is considered deliverable when:

- Stage A-E acceptance all pass
- Full regression passes
- Critical paths (ingest/query/MCP) verified
- Documentation matches current behavior

## 7. Repository

- GitHub: https://github.com/zhuangfanupup/modular-rag-mcp-server.git

## 8. Maintenance Notes

- This project is maintained as a personal engineering asset
- Priorities are driven by real usage and delivery needs
- Optional reference materials may exist but are not the project's primary orientation

