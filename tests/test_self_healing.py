"""
EdgeBrain 3.0 Pro - Self-Healing Verification Test
Simulates a skill execution failure to verify the self-healing logic.
"""
import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.edgebrain.core.engine import EdgeBrainEngine
from src.edgebrain.core.state import AgentState

async def main():
    print("🚀 Starting Self-Healing Verification Test...")
    
    # Initialize the engine
    engine = EdgeBrainEngine()
    
    # Initial state simulating a crash in a previous node
    initial_state: AgentState = {
        "messages": [{"role": "user", "content": "Analyze the screen"}],
        "reasoning_steps": [],
        "tool_calls": [],
        "tool_results": [],
        "retrieved_docs": [],
        "context_summary": None,
        "visual_input": None,
        "image_path": None,
        "vlm_output": None,
        "screen_analysis": None,
        "last_screenshot_path": None,
        "current_node": "screen_awareness",
        "error_message": "Ollama Connection Timeout: Failed to reach llava:7b after 30s",  # Simulated error
        "requires_approval": False,
        "approval_status": None,
        "next_action": "execute",
        "target_skill": None,
        "retry_count": 0
    }
    
    try:
        # Run the graph and observe the stream
        async for event in engine.graph.astream_events(initial_state, version="v2"):
            kind = event["event"]
            node_name = event.get("name", "unknown")
            
            if kind == "on_chain_start" or kind == "on_chain_end":
                print(f"🔄 Node Event: {kind} -> {node_name}")
                
            # Check if the self-healing node was triggered
            if node_name == "self_heal" and kind == "on_chain_end":
                print("✅ Self-Healing Node Triggered Successfully!")
                output_data = event["data"].get("output", {})
                if output_data:
                    print(f"   Healing Suggestion: {output_data.get('error_message', 'N/A')}")
                    
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
