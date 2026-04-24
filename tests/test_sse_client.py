import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio

# 模拟 SSE 数据行
MOCK_SSE_DATA = [
    "data: {\"status\": \"planning\", \"message\": \"正在规划任务...\"}",
    "data: {\"status\": \"executing\", \"message\": \"正在执行技能...\"}",
    "data: {\"status\": \"completed\", \"message\": \"任务完成\"}"
]

@pytest.mark.asyncio
async def test_sse_stream_logic():
    """
    测试 SSE 客户端的数据解析逻辑，不发起真实网络请求。
    """
    # 模拟 httpx.AsyncClient 及其响应流
    mock_response = MagicMock()
    mock_response.aiter_lines = AsyncMock()
    mock_response.aiter_lines.return_value.__aiter__.return_value = iter(MOCK_SSE_DATA)
    
    mock_client = MagicMock()
    mock_client.stream = MagicMock()
    mock_client.stream.return_value.__aenter__.return_value = mock_response
    
    received_events = []
    
    # 模拟业务逻辑：解析 SSE 数据
    async with mock_client.stream("GET", "http://mock-url/stream") as response:
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                data_str = line[6:]
                received_events.append(data_str)

    # 验证解析结果
    assert len(received_events) == 3
    assert "\"status\": \"planning\"" in received_events[0]
    assert "\"status\": \"completed\"" in received_events[2]
    print(f"Successfully parsed {len(received_events)} SSE events.")

if __name__ == "__main__":
    asyncio.run(test_sse_stream_logic())
