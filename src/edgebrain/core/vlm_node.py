"""
EdgeBrain 3.0 Pro - Visual Language Model (VLM) Node
负责处理图像输入，提供屏幕内容分析、UI 元素识别等能力。
"""

import base64
import requests
from typing import Optional, Dict, Any
from src.edgebrain.core.state import AgentState
from src.edgebrain.config import VLM_MODEL_NAME, OLLAMA_URL

class VLMNode:
    def __init__(self, model_name: str = VLM_MODEL_NAME, ollama_url: str = OLLAMA_URL):
        self.model_name = model_name
        self.ollama_url = ollama_url
        print(f"[VLMNode] Initialized with model: {model_name} at {ollama_url}")

    def encode_image(self, image_path: str) -> str:
        """将本地图片转换为 Base64 编码"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze(self, state: AgentState) -> Dict[str, Any]:
        """
        分析当前状态中的图像信息
        :param state: 当前的 Agent 状态
        :return: 更新后的状态字典
        """
        image_path = state.get("image_path")
        query = state.get("messages", [{"content": "请描述这张图片的内容"}])[-1].get("content", "请描述这张图片的内容")
        
        if not image_path:
            return {"messages": [{"role": "assistant", "content": "[VLMNode] No image provided for analysis."}]}

        try:
            # 1. 预处理图像
            base64_image = self.encode_image(image_path)
            
            # 2. 调用 Ollama API
            payload = {
                "model": self.model_name,
                "prompt": query,
                "images": [base64_image],
                "stream": False
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload)
            response.raise_for_status()
            
            result = response.json()
            analysis_result = result.get("response", "No response from VLM.")
            
            return {
                "messages": [{"role": "assistant", "content": analysis_result}],
                "vlm_output": analysis_result
            }
        except Exception as e:
            error_msg = f"[VLMNode] Error during analysis: {str(e)}"
            return {"messages": [{"role": "assistant", "content": error_msg}]}
