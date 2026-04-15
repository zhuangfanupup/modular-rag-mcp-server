# Internal Review Checklist

## 1. Architecture

1. 分层边界是否清晰（core/ingestion/libs/mcp_server/observability）
2. 是否存在跨层耦合与隐藏依赖
3. 配置项是否具备可解释默认值

## 2. Critical Paths

1. Ingestion: load -> split -> transform -> encode -> upsert
2. Query: process -> retrieve -> fuse -> rerank -> response
3. MCP: tools/list, tools/call, error/timeout behavior

## 3. Quality

1. 是否有对应单元与集成测试
2. 失败路径是否可观测（trace/log）
3. 外部依赖不可用时是否优雅降级
