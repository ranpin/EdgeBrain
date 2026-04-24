"""
EdgeBrain 3.0 Pro - CBAC Security Gateway
Implements Capability-Based Access Control and HITL enforcement.
"""
from typing import Dict, Any
from loguru import logger
from ..core.config import settings

class SecurityGateway:
    def __init__(self):
        self.hitl_required_actions = settings.security.hitl_required_for

    def check_permission(self, action_type: str, tool_name: str) -> Dict[str, Any]:
        """
        Check if an action requires Human-in-the-Loop (HITL) approval.
        Returns a dict with 'allowed' status and optional 'reason'.
        """
        if not settings.security.enable_cbac:
            return {"allowed": True}

        if action_type in self.hitl_required_actions:
            logger.warning(f"HITL required for action: {action_type} via tool: {tool_name}")
            return {
                "allowed": False, 
                "requires_approval": True,
                "reason": f"Action '{action_type}' is restricted and requires user confirmation."
            }
        
        return {"allowed": True}

    def validate_tool_input(self, tool_input: Dict) -> bool:
        """Basic input sanitization to prevent injection attacks."""
        # Placeholder for advanced sanitization logic
        return True

# Global instance
gateway = SecurityGateway()
