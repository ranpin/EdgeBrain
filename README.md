# EdgeBrain 3.0 Pro

**工业级端侧智能体编排平台 (Industrial-grade On-device Agent Orchestration Platform)**

## 1. 项目简介
EdgeBrain 3.0 Pro 是一个面向异构硬件（NVIDIA Orin, Qualcomm 8397）的高可用端侧 Agent 框架。它深度融合了 **OpenClaw**（本地优先/隐私沙箱）、**Harness**（工程化标准/可观测性）以及 **Claude Code**（声明式配置/HITL）的先进理念，旨在解决端侧大模型落地中的稳定性、安全性与成本效益痛点。

## 2. 核心特性
- **多模态原生 (VLM Native)**：支持 Qwen2.5-VL 等轻量级视觉模型，实现屏幕感知与环境分析。
- **分布式 A2A 协同**：基于 Google A2A 协议，实现跨设备（车机-手机-云端）的任务分片与联邦记忆同步。
- **声明式技能系统 (Skills-as-Plugins)**：兼容 MCP 标准，支持工具的热插拔与动态发现。
- **极致成本优化**：集成动态量化切换 (INT4/INT8) 与 KV Cache 压缩策略，提升 TCO 效益。
- **自愈式编排引擎**：基于 LangGraph 的状态机具备异常根因诊断与自动重试能力。

## 3. 技术栈
- **Core**: Python 3.9+, LangGraph, LlamaIndex
- **Vector DB**: ChromaDB
- **Observability**: LangFuse, Ragas
- **Hardware**: NVIDIA Orin (Ollama/vLLM), Qualcomm 8397 (QNN)

## 4. 快速开始
```bash
# 克隆仓库
git clone https://github.com/your-username/EdgeBrain-3.0-Pro.git
cd EdgeBrain-3.0-Pro

# 安装依赖
pip install -e .

# 运行基准测试
python benchmarks/run_benchmark.py
```

## 5. 路线图 (Roadmap)
- [x] 项目初始化与 PRD 定稿
- [ ] Phase 1: 声明式技能加载器 (SkillLoader) 实现
- [ ] Phase 2: 智能上下文引擎与安全网关 (HITL)
- [ ] Phase 3: 异构硬件抽象层 (HAL) 适配
- [ ] Phase 4: 全链路可观测性与自愈机制集成

---
*Author: Chen Runbin | License: MIT*
