import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.edgebrain.core.engine import EdgeBrainEngine

def test_screen_analysis():
    print("Initializing EdgeBrain Engine...")
    engine = EdgeBrainEngine()
    
    # 模拟用户指令：分析屏幕
    user_input = {
        "messages": [{"role": "user", "content": "帮我分析一下当前的屏幕内容"}]
    }
    
    print("Running screen analysis task...")
    result = engine.run(user_input)
    
    print("\n--- Screen Analysis Result ---")
    # 打印完整的状态以便调试
    print("Full State Keys:", result.keys())
    if 'screen_analysis' in result:
        print(result['screen_analysis'])
    else:
        # 尝试从 messages 或其他可能的字段中查找
        print("State content:", result)
    print("------------------------------")

if __name__ == "__main__":
    test_screen_analysis()
