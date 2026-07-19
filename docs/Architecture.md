# Architecture

## System Overview

VoidLens is built as a modular, plugin-based OSINT framework with three execution modes: CLI, API, and Library.

```
┌─────────────────────────────────────────────────┐
│                   CLI / API / Library            │
├─────────────────────────────────────────────────┤
│                    Runner (Orchestrator)          │
├──────────┬──────────┬──────────┬────────────────┤
│  Engine  │  Cache   │  Proxy   │  Rate Limiter  │
├──────────┴──────────┴──────────┴────────────────┤
│              Module Registry                     │
├──────────────────┬──────────────────────────────┤
│  Email Modules   │     Username Modules          │
└──────────────────┴──────────────────────────────┘
```

## Data Flow

1. Input → CLI/API/Library entry point
2. Runner resolves target modules (filters by category/name)
3. Engine dispatches concurrent async requests
4. Rate limiter enforces per-host concurrency
5. Cache intercepts duplicate lookups
6. Results aggregated into typed `ScanResult` models
7. Output → Console table / Export file / JSON response

## Key Design Decisions

- **Plugin architecture**: Modules auto-register via importlib discovery
- **Typed models**: All data flows through `ScanResult`/`SiteResult` dataclasses
- **Async-first**: aiohttp with connection pooling for maximum throughput
- **Adaptive rate limiting**: Per-host semaphores with HTTP 429 backoff
