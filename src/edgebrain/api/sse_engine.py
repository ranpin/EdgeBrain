"""
EdgeBrain 3.0 Pro - SSE Streaming Engine
提供基于 FastAPI 的 Server-Sent Events (SSE) 接口，用于实时推送 Agent 状态。
"""
import json
from typing import AsyncGenerator
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from src.edgebrain.core.engine import EdgeBrainEngine

app = FastAPI(title="EdgeBrain API")

# 初始化引擎实例
engine = EdgeBrainEngine()

async def event_generator(query: str) -> AsyncGenerator[str, None]:
    """
    通过 LangGraph 的 astream_events 获取真实状态流转并生成 SSE 事件。
    """
    input_data = {"messages": [{"role": "user", "content": query}]}
    
    async for event in engine.graph.astream_events(input_data, version="v2"):
        kind = event["event"]
        name = event.get("name", "unknown_node")
        
        # 过滤出我们关心的节点事件
        if kind == "on_chain_start" and name in ["plan", "retrieve", "execute", "vlm", "screen", "respond"]:
            yield f"data: {json.dumps({'step': name, 'status': 'started', 'message': f'Node {name} started...'})}\n\n"
        elif kind == "on_chain_end" and name in ["plan", "retrieve", "execute", "vlm", "screen", "respond"]:
            yield f"data: {json.dumps({'step': name, 'status': 'completed', 'message': f'Node {name} finished.'})}\n\n"

@app.get("/stream")
async def stream_status(q: str = Query(..., description="User query to process")):
    return StreamingResponse(event_generator(q), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
