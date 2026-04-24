import sys
import os
from PIL import Image, ImageDraw, ImageFont
import requests
import base64

# 添加项目根目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.edgebrain.config import VLM_MODEL_NAME, OLLAMA_URL

def create_test_image(path: str):
    """创建一张包含简单文字的测试图片"""
    img = Image.new('RGB', (400, 200), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    # 尝试使用系统字体，如果失败则使用默认字体
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        font = ImageFont.load_default()
    
    d.text((50, 80), "EdgeBrain Test", fill=(255, 255, 0), font=font)
    img.save(path)
    print(f"Test image created at: {path}")

def test_llava_vlm():
    image_path = "./tests/assets/test_image.png"
    os.makedirs("./tests/assets", exist_ok=True)
    
    if not os.path.exists(image_path):
        create_test_image(image_path)

    # 1. 编码图片
    with open(image_path, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode('utf-8')

    # 2. 构造请求
    payload = {
        "model": VLM_MODEL_NAME,
        "prompt": "请描述这张图片里的文字内容。",
        "images": [base64_image],
        "stream": False
    }

    print(f"Sending request to Ollama ({OLLAMA_URL}) using model: {VLM_MODEL_NAME}...")
    
    try:
        response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        print("\n--- VLM Analysis Result ---")
        print(result.get("response", "No response received."))
        print("---------------------------\n")
    except Exception as e:
        print(f"Error calling Ollama: {e}")

if __name__ == "__main__":
    test_llava_vlm()
