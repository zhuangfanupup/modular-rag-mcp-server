# 阶段文件整理与验收清单

更新时间：2026-04-15

## 阶段A（基础与配置）
- 验收：通过
- 相关文件：
  - src/libs/embedding/openai_embedding.py
  - src/libs/embedding/azure_embedding.py
  - tests/unit/test_azure_vision_llm.py

## 阶段B（Provider/Factory 稳定化）
- 验收：通过
- 相关文件：
  - src/libs/embedding/openai_embedding.py
  - src/libs/embedding/azure_embedding.py
  - tests/unit/test_azure_vision_llm.py

## 阶段C（摄取链路与存储一致性）
- 验收：通过
- 相关文件：
  - src/libs/loader/pdf_loader.py
  - src/ingestion/embedding/sparse_encoder.py
  - src/ingestion/embedding/batch_processor.py
  - src/libs/vector_store/chroma_store.py
  - src/ingestion/pipeline.py
  - scripts/ingest.py
  - tests/integration/test_chroma_store_roundtrip.py
  - tests/e2e/test_data_ingestion.py

## 阶段D（查询链路与观测）
- 验收：通过
- 相关文件：
  - src/core/trace/trace_context.py
  - src/observability/dashboard/services/trace_service.py
  - src/observability/evaluation/eval_runner.py

## 阶段E（MCP 工具与会话稳定性）
- 验收：通过
- 相关文件：
  - src/mcp_server/protocol_handler.py
  - src/mcp_server/tools/list_collections.py
  - src/mcp_server/tools/query_knowledge_hub.py
  - tests/unit/test_protocol_handler.py
  - tests/unit/test_list_collections.py
  - tests/e2e/test_mcp_client.py

## 外部依赖型集成测试整理（按环境跳过）
- 验收：通过（在无可用 Azure/OpenAI/Ollama 环境时正确 skip）
- 相关文件：
  - tests/integration/test_dense_encoder_azure.py
  - tests/integration/test_ingestion_pipeline.py
  - tests/integration/test_reranker_llm.py
  - tests/integration/test_chunk_refiner_llm.py

## 全量验收
- 命令：pytest -q
- 结果：1321 passed, 42 skipped, 5 warnings
- 结论：通过

## 目录清理
- 已清理：仓库根目录大部分 `.pytest_tmp*` 临时目录
- 残留（系统占用）：
  - .pytest_tmp
  - .pytest_tmp_stageA2
