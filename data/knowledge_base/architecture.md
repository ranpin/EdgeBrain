# EdgeBrain 3.0 Pro 架构说明

## 1. 核心理念
EdgeBrain 3.0 Pro 是一个工业级的端侧 Agent 框架，深度融合了 OpenClaw（本地优先）、Harness（工程化可观测性）及 Claude Code（声明式配置）的设计理念。

## 2. 关键组件
- **LangGraph 编排引擎**：负责状态机流转、HITL 中断与自愈逻辑。
- **声明式技能系统 (Skills-as-Plugins)**：通过 `skill.json` Manifest 动态加载工具，支持热插拔。
- **CBAC 安全网关**：基于能力的访问控制，对敏感操作强制人机协同（HITL）。
- **智能上下文引擎**：结合 LlamaIndex 与 ChromaDB，实现动态上下文修剪与长期记忆。
- **多模态感知 (VLM)**：集成 Qwen2.5-VL，支持屏幕内容分析与具身智能交互。

## 3. 技术栈
- **基础框架**: Python 3.9+, LangGraph, LangChain
- **RAG**: LlamaIndex, ChromaDB
- **可观测性**: LangFuse, Ragas
- **模型适配**: Ollama, QNN, vLLM