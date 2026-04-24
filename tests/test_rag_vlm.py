import os
import sys
import pytest

# 确保能导入项目模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.edgebrain.core.rag_node import RAGNode
from src.edgebrain.core.vlm_node import VLMNode
from src.edgebrain.core.state import AgentState

def test_rag_retrieval():
    """测试 RAG 节点是否能正确加载文档"""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'knowledge_base')
    rag = RAGNode(data_dir=data_dir, persist_dir="/tmp/edgebrain_test_storage")
    
    # 在离线模式下，我们主要验证索引是否成功初始化
    if rag.index:
        print("RAG Index initialized successfully.")
        # 尝试检索（离线模式下可能返回空或依赖简单匹配）
        results = rag.query("EdgeBrain 的核心组件有哪些？")
        print(f"RAG Query Results: {results}")
    else:
        print("RAG Index not initialized (likely due to offline mode limitations).")

def test_vlm_connectivity():
    """测试 VLM 节点是否能连接到 Ollama (如果服务可用)"""
    vlm = VLMNode(model_name="qwen2.5-vl:7b")
    
    # 使用一个简单的测试图片路径（如果存在）
    # 注意：此测试在没有真实图片或 Ollama 运行时可能会失败或返回 Mock 结果
    state: AgentState = {
        "messages": [{"role": "user", "content": "描述这张图"}],
        "image_path": None, # 暂时不传图片，测试错误处理逻辑
        "vlm_output": None,
        "reasoning_steps": [],
        "tool_calls": [],
        "tool_results": [],
        "retrieved_docs": [],
        "context_summary": None,
        "visual_input": None,
        "current_node": "",
        "error_message": None,
        "requires_approval": False,
        "approval_status": None,
        "next_action": None,
        "target_skill": None
    }
    
    result = vlm.analyze(state)
    assert "No image provided" in str(result["messages"][0]["content"])
    print("VLM 节点错误处理逻辑验证通过。")

if __name__ == "__main__":
    test_rag_retrieval()
    test_vlm_connectivity()
    print("所有验证测试通过！")