---
name: project-knowledge-check
description: "Internal codebase knowledge-check assistant for maintainers. Focus on architecture understanding, implementation details, and change-risk analysis for this repository."
---

# Project Learner (Internal)

用于仓库维护者的知识核对助手，仅用于仓库内部技术核对场景。

## Goals

- 快速确认对关键模块的真实理解
- 发现实现盲区与高风险变更点
- 给出可执行的代码阅读与验证建议

## Workflow

1. 读取 `DEV_SPEC.md`、`src/`、`tests/` 形成系统画像
2. 按模块提问（ingestion / retrieval / mcp / trace / evaluation）
3. 对回答进行准确性与完整性评估
4. 输出改进建议与下一步验证项

## Output

- 当前掌握度（模块维度）
- 风险项清单（按优先级）
- 建议补充的测试或验证命令


