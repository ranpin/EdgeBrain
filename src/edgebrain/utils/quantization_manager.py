"""
EdgeBrain 3.0 Pro - Quantization Manager
管理端侧模型的量化版本切换与性能基准测试。
"""
import time
import requests
from loguru import logger
from edgebrain.config import OLLAMA_URL, MODEL_QUANTIZATION

class QuantizationManager:
    def __init__(self):
        self.api_url = f"{OLLAMA_URL}/api/generate"

    def get_quantized_model_name(self, base_name: str) -> str:
        """
        根据基础模型名和配置的量化等级生成完整的模型标签。
        例如: 'llava:7b' + 'q4_K_M' -> 'llava:7b-q4_K_M'
        """
        if MODEL_QUANTIZATION == "f16":
            return base_name
        # 处理可能已经包含标签的情况
        if ":" in base_name:
            return f"{base_name}-{MODEL_QUANTIZATION}"
        return f"{base_name}:{MODEL_QUANTIZATION}"

    def benchmark_latency(self, model_name: str, prompt: str = "Describe the color red in one word.") -> float:
        """
        测量模型生成首个 Token 的延迟 (Time to First Token)。
        """
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
        
        start_time = time.time()
        try:
            response = requests.post(self.api_url, json=payload, timeout=60)
            response.raise_for_status()
            latency = time.time() - start_time
            logger.info(f"[Perf] Model: {model_name} | Latency: {latency:.2f}s")
            return latency
        except Exception as e:
            logger.error(f"[Perf] Benchmark failed for {model_name}: {e}")
            return -1.0

    def get_recommended_model(self, platform: str) -> str:
        """
        根据目标硬件平台推荐最优的量化模型。
        """
        recommendations = {
            "orin": "llava:7b",      # Orin 算力较强，可跑 7B
            "8397": "moondream:latest", # 8397 资源受限，推荐轻量级
            "macos": "llava:7b"
        }
        return recommendations.get(platform, "moondream:latest")
