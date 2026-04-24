"""
EdgeBrain 3.0 Pro - LangGraph State Definition
Defines the global state for the Agent's state machine.
"""
from typing import TypedDict, List, Optional, Annotated
from typing_extensions import NotRequired
import operator

class AgentState(TypedDict):
    """
    The global state of the EdgeBrain Agent.
    """
    # User input and conversation history
    messages: Annotated[List[dict], operator.add]
    
    # Intermediate reasoning steps (Chain of Thought)
    reasoning_steps: List[str]
    
    # Tool execution results
    tool_calls: List[dict]
    tool_results: List[dict]
    
    # RAG context
    retrieved_docs: List[dict]
    
    # Context Management (for pruning/summarization)
    context_summary: Optional[str]
    
    # Multimodal inputs (Image paths or base64)
    visual_input: Optional[List[str]]
    image_path: Optional[str]  # Single image path for quick VLM analysis
    
    # VLM Analysis results
    vlm_output: Optional[str]
    
    # Screen Awareness results
    screen_analysis: Optional[str]
    last_screenshot_path: Optional[str]
    
    # System status
    current_node: str
    error_message: Optional[str]
    
    # HITL (Human-in-the-Loop) flags
    requires_approval: bool
    approval_status: Optional[str]  # "approved", "rejected"
    
    # Planning & Routing fields
    next_action: Optional[str]  # "execute", "retrieve", "respond"
    target_skill: Optional[str]  # ID of the skill to execute
    
    # Self-healing fields
    retry_count: int
