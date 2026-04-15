# Modular RAG MCP Server

个人维护的模块化 RAG MCP Server，面向实际业务落地。

## Repository

- GitHub: https://github.com/zhuangfanupup/modular-rag-mcp-server.git

## 项目定位

本项目用于构建可扩展的知识检索与问答服务，核心目标是：

- 支持本地/云端多后端切换（LLM、Embedding、Reranker、Vector Store）
- 提供可观测的 Ingestion 与 Query 全链路
- 通过 MCP 协议对外提供标准工具能力
- 面向业务场景的长期维护与迭代

## 核心能力

- Ingestion Pipeline: 文档加载、切分、增强、向量化、入库
- Hybrid Search: Dense + Sparse + RRF + Rerank
- MCP Tools: `query_knowledge_hub` / `list_collections` / `get_document_summary`
- Dashboard: 数据管理、链路追踪、评估面板
- Evaluation: Golden set 回归 + 指标评估

## 快速开始

```bash
git clone https://github.com/zhuangfanupup/modular-rag-mcp-server.git
cd modular-rag-mcp-server
```

安装依赖并配置 `config/settings.yaml` 后，可运行：

```bash
pytest -q
python -m src.mcp_server.server
```

## 目录说明

- `src/`: 核心源码
- `tests/`: 单元/集成/E2E 测试
- `config/`: 配置文件
- `scripts/`: 辅助脚本
- `docs/`: 项目文档

## 维护说明

- 本仓库按个人项目标准维护，优先服务当前业务目标
- 变更策略以稳定性、可维护性、可扩展性为主

## License

MIT

