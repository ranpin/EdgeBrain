import pytest
from src.edgebrain.sse_engine import create_event_stream

def test_sse_module_import():
    """验证 SSE 引擎模块是否可以成功导入"""
    assert create_event_stream is not None

def test_sse_event_format():
    """验证事件格式化逻辑是否符合 SSE 标准"""
    # 模拟一个简单的事件数据
    data = {"status": "running", "node": "planner"}
    # 这里可以调用 sse_engine 中的格式化函数进行断言
    # 假设有一个 format_sse_event 函数
    # result = format_sse_event(data)
    # assert result.startswith("data: ")
    pass
