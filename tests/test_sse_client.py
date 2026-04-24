import httpx
import asyncio

async def test_sse_stream():
    url = "http://127.0.0.1:8000/stream"
    params = {"q": "帮我分析一下当前系统状态"}
    
    print(f"Connecting to SSE stream at {url}...")
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("GET", url, params=params) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data_str = line[6:]
                    print(f"Received Event: {data_str}")

if __name__ == "__main__":
    asyncio.run(test_sse_stream())
