import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import json

# 模拟 SSE 数据流
MOCK_SSE_DATA = [
    "event: state_update\ndata: {\"status\": \"thinking\", \"node\": \"planner\"}\n\n",
    "event: state_update\ndata: {\"status\": \"executing\", \"node\": \"skill_executor\"}\n\n",
    "event: state_update\ndata: {\"status\": \"completed\", \"result\": \"Task finished.\"}\n\n"
]

class AsyncIterator:
    """辅助类：将普通列表转换为异步迭代器"""
    def __init__(self, seq):
        self.iter = iter(seq)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration

@pytest.mark.asyncio
async def test_sse_stream_logic():
    """
    单元测试：验证 SSE 客户端解析逻辑
    通过 Mock 模拟 httpx.AsyncClient 的响应，不发起真实网络请求
    """
    from src.edgebrain.sse_client import SSEClient

    # 1. 创建 Mock 响应对象
    mock_response = MagicMock()
    # 关键修复：将 aiter_lines 的返回值设置为一个 AsyncIterator
    mock_response.aiter_lines = MagicMock(return_value=AsyncIterator(MOCK_SSE_DATA))
    
    # 2. 实例化客户端并注入 Mock 响应
    client = SSEClient(base_url="http://mock-server")
    
    collected_events = []
    
    # 3. 模拟 stream 上下文管理器
    # 我们需要 Mock 掉 client.client.stream 方法
    with patch.object(client.client, 'stream') as mock_stream:
        # 设置 stream 返回的上下文管理器行为
        mock_stream.return_value.__aenter__.return_value = mock_response
        
        # 4. 执行流式读取逻辑
        async for event in client.stream_events("test_query"):
            collected_events.append(event)

    # 5. 验证结果
    assert len(collected_events) == 3
    assert collected_events[0]["node"] == "planner"
    assert collected_events[1]["node"] == "skill_executor"
    assert collected_events[2]["result"] == "Task finished."
