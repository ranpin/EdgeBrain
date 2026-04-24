"""
EdgeBrain 3.0 Pro - Quantization Benchmark Test
对比不同量化等级下的模型推理延迟。
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.edgebrain.utils.quantization_manager import QuantizationManager

def run_benchmark():
    qm = QuantizationManager()
    
    # 定义要对比的模型列表
    models_to_test = [
        ("llava:7b", "High Precision (7B)"),
        ("moondream:latest", "Edge Optimized (1.6GB)")
    ]
    
    print(f"\n--- EdgeBrain Model Performance Benchmark ---")
    print("-" * 50)
    
    for model_name, description in models_to_test:
        latency = qm.benchmark_latency(model_name)
        print(f"Model: {model_name:<20} | Desc: {description:<25} | Latency: {latency:.2f}s")

if __name__ == "__main__":
    run_benchmark()
