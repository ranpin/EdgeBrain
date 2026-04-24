import pytest

def test_sse_module_import():
    """验证 SSE 引擎模块是否可以成功导入"""
    try:
        from src.edgebrain.api.sse_engine import create_event_stream
        assert create_event_stream is not None
    except ImportError as e:
        pytest.fail(f"无法导入 SSE 引擎模块: {e}")

def test_sse_function_signature():
    """验证 create_event_stream 函数是否存在且可调用"""
    from src.edgebrain.api.sse_engine import create_event_stream
    assert callable(create_event_stream)
