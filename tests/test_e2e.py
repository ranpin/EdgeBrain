import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.edgebrain.core.engine import EdgeBrainEngine
from src.edgebrain.core.state import AgentState

class TestEdgeBrainE2E:
    @pytest.fixture
    def engine(self):
        """初始化 EdgeBrain 引擎实例"""
        return EdgeBrainEngine()

    def test_text_routing_chat(self, engine):
        """测试 1: 纯文本闲聊路由"""
        input_data = {
            "messages": [{"role": "user", "content": "你好，请介绍一下你自己"}],
            "reasoning_steps": [],
            "tool_calls": [],
            "tool_results": [],
            "retrieved_docs": [],
            "visual_input": None,
            "image_path": None,
            "vlm_output": None,
            "context_summary": None,
            "current_node": "",
            "error_message": None,
            "requires_approval": False,
            "approval_status": None,
            "next_action": None,
            "target_skill": None
        }
        result = engine.run(input_data)
        assert result['messages'][-1]['role'] == 'assistant'
        assert "EdgeBrain" in result['messages'][-1]['content'] or "processed" in result['messages'][-1]['content'].lower()

    def test_skill_execution_mock(self, engine):
        """测试 2: 技能执行链路（Mock 模式）"""
        input_data = {
            "messages": [{"role": "user", "content": "查询当前系统 CPU 状态"}],
            "reasoning_steps": [],
            "tool_calls": [],
            "tool_results": [],
            "retrieved_docs": [],
            "visual_input": None,
            "image_path": None,
            "vlm_output": None,
            "context_summary": None,
            "current_node": "",
            "error_message": None,
            "requires_approval": False,
            "approval_status": None,
            "next_action": None,
            "target_skill": None
        }
        
        # 模拟安全网关直接通过，避免 HITL 中断阻塞测试
        with patch.object(engine.security_gateway, 'check_permission', return_value={"allowed": True}):
            result = engine.run(input_data)
            
        assert result.get('tool_results') is not None
        assert len(result['tool_results']) > 0

    def test_vlm_node_trigger(self, engine):
        """测试 3: 多模态感知链路触发"""
        # 创建一个临时测试图片路径
        test_img_path = "/tmp/test_edgebrain_screen.png"
        
        input_data = {
            "messages": [{"role": "user", "content": "分析一下这张截图"}],
            "reasoning_steps": [],
            "tool_calls": [],
            "tool_results": [],
            "retrieved_docs": [],
            "visual_input": None,
            "image_path": test_img_path,
            "vlm_output": None,
            "context_summary": None,
            "current_node": "",
            "error_message": None,
            "requires_approval": False,
            "approval_status": None,
            "next_action": None,
            "target_skill": None
        }

        # 模拟 VLM 节点的分析结果
        with patch.object(engine.vlm_node, 'analyze', return_value={"vlm_output": "Detected: UI Dashboard with metrics."}):
            result = engine.run(input_data)
            
        assert result.get('vlm_output') == "Detected: UI Dashboard with metrics."

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
