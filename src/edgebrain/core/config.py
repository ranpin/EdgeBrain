"""
EdgeBrain 3.0 Pro - Global Configuration Module
Manages model parameters, hardware adaptation, and system paths.
"""
import os
from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class ModelConfig:
    """LLM/VLM Model Configuration"""
    provider: str = "ollama"  # ollama, qnn, vllm
    model_name: str = "qwen2.5:7b"
    temperature: float = 0.7
    max_tokens: int = 2048
    context_window: int = 8192
    # Hardware specific
    use_qnn: bool = False
    qnn_backend: Optional[str] = None  # e.g., "htp" for Qualcomm

@dataclass
class RAGConfig:
    """Retrieval-Augmented Generation Configuration"""
    vector_store_path: str = "./data/chroma_db"
    embedding_model: str = "nomic-embed-text"
    chunk_size: int = 512
    chunk_overlap: int = 50
    top_k: int = 5

@dataclass
class SecurityConfig:
    """CBAC & Sandbox Configuration"""
    enable_cbac: bool = True
    hitl_required_for: List[str] = field(default_factory=lambda: ["EXECUTE", "WRITE"])
    sandbox_mode: str = "wasm"  # wasm, docker, native

@dataclass
class SystemConfig:
    """Global System Configuration"""
    project_root: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    data_dir: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
    log_level: str = "INFO"
    heartbeat_interval: int = 30  # seconds
    max_retries: int = 3
    
    model: ModelConfig = field(default_factory=ModelConfig)
    rag: RAGConfig = field(default_factory=RAGConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)

    def load_from_env(self):
        """Load configuration from environment variables"""
        if os.getenv("EB_MODEL_NAME"):
            self.model.model_name = os.getenv("EB_MODEL_NAME")
        if os.getenv("EB_USE_QNN") == "true":
            self.model.use_qnn = True

# Global instance
settings = SystemConfig()
settings.load_from_env()
