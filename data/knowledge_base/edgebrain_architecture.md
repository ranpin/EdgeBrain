# EdgeBrain 3.0 Pro 架构说明

## 核心组件
1. **LangGraph**: 负责状态机编排，支持循环、分支和条件路由。
2. **LlamaIndex**: 提供数据连接器（Connectors）和索引器（Indices），用于处理非结构化数据。
3. **ChromaDB**: 轻量级向量数据库，用于存储 Embedding 向量并执行相似度检索。
4. **CBAC Gateway**: 基于能力的访问控制网关，确保端侧操作的安全性。

## 部署目标
- **Qualcomm 8397**: 利用 QNN 运行时进行低延迟推理。
- **NVIDIA Orin**: 适配车机环境，支持高并发任务处理。

## 技能系统
采用声明式 JSON 配置，支持热插拔。每个技能包含 `trigger_keywords` 和 `handler_module`。
