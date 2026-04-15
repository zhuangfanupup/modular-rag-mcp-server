# Technical Readiness Questions

## Module A: Ingestion

1. 分块策略如何保证召回与上下文连续性平衡？
2. 外部 embedding 不可用时链路如何降级？
3. 写入向量与 BM25 的一致性如何保证？

## Module B: Retrieval

1. Dense/Sparse 融合权重如何验证？
2. rerank 失败时是否有可预期回退？
3. 无结果与低置信结果如何返回？

## Module C: MCP

1. tools/call 的超时与错误语义是否统一？
2. 并发请求下是否存在阻塞或饥饿？
3. 响应顺序与会话稳定性如何验证？
