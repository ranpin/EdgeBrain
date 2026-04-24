"""
EdgeBrain 3.0 Pro - Screen Awareness Node
负责截取屏幕并调用 VLM 进行 UI 元素识别与空间分析。
"""
import base64
import requests
from typing import Dict, Any
from edgebrain.config import OLLAMA_URL, VLM_MODEL_NAME

class ScreenAwarenessNode:
    def __init__(self):
        self.model_name = VLM_MODEL_NAME
        self.api_url = f"{OLLAMA_URL}/api/chat"

    def capture_screen(self) -> str:
        """
        模拟截图功能。在真实环境中，这里会调用系统的截图 API。
        目前返回一个预设的测试图片路径。
        """
        # 在实际部署到 Orin/8397 时，这里将替换为真实的 framebuffer 或 X11/Wayland 截图逻辑
        return "./tests/assets/test_image.png"

    def analyze_ui(self, image_path: str, prompt: str = "Describe the UI elements and their positions in this screenshot.") -> Dict[str, Any]:
        """
        调用 LLaVA 模型分析截图中的 UI 元素。
        """
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            payload = {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [base64_image]
                    }
                ],
                "stream": False
            }
            
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            result = response.json()
            return {"status": "success", "analysis": result["message"]["content"]}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        LangGraph 节点执行入口。
        """
        print(f"[ScreenAwarenessNode] Capturing screen...")
        img_path = self.capture_screen()
        
        print(f"[ScreenAwarenessNode] Analyzing UI with {self.model_name}...")
        analysis_result = self.analyze_ui(img_path)
        
        # 按照 LangGraph 规范，返回需要更新的状态字段
        return {
            "screen_analysis": analysis_result.get("analysis", "Analysis failed."),
            "last_screenshot_path": img_path
        }
