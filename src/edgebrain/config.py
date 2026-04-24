"""
EdgeBrain 3.0 Pro - Global Configuration
集中管理模型路径、API 端点及硬件适配参数。
"""

# --- Model Configuration ---
OLLAMA_URL = "http://localhost:11434"
VLM_MODEL_NAME = "llava:7b"  # 可选: qwen2.5-vl, moondream, llava:7b
LLM_MODEL_NAME = "qwen2.5:0.5b"
EMBEDDING_MODEL_NAME = "nomic-embed-text"

# --- Quantization & Performance ---
# 量化等级: 'q4_K_M' (推荐平衡点), 'q8_0' (高精度), 'f16' (无量化)
MODEL_QUANTIZATION = "q4_K_M" 
ENABLE_PERF_MONITORING = True

# --- RAG Configuration ---
CHROMA_PERSIST_DIR = "./storage"
KNOWLEDGE_BASE_DIR = "./data/knowledge_base"

# --- Hardware Adaptation (Placeholder) ---
# Target Platform: 'orin', '8397', 'macos'
TARGET_PLATFORM = "macos"
