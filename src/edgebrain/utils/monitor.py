"""
EdgeBrain 3.0 Pro - System Monitor & Context Manager
Handles heartbeat signals and dynamic context pruning for resource-constrained environments.
"""
import time
from typing import List, Dict
from loguru import logger
from ..core.config import config

class SystemMonitor:
    def __init__(self):
        self.last_heartbeat = time.time()
        self.interval = config.heartbeat_interval

    def beat(self):
        """Update the heartbeat timestamp."""
        self.last_heartbeat = time.time()
        logger.debug("System heartbeat updated.")

    def check_health(self) -> bool:
        """Check if the system is responsive based on heartbeat interval."""
        now = time.time()
        if now - self.last_heartbeat > self.interval * 2:
            logger.error("Heartbeat timeout! System may be unresponsive.")
            return False
        return True

class ContextManager:
    def __init__(self, max_tokens: int = 4096):
        self.max_tokens = max_tokens

    def prune_context(self, messages: List[Dict]) -> List[Dict]:
        """
        Simple token-based pruning. 
        In a real implementation, this would use LlamaIndex summarization or vector filtering.
        """
        # Placeholder logic: keep only the last N messages if too long
        if len(messages) > 10:
            logger.info(f"Context pruned from {len(messages)} to last 10 messages.")
            return messages[-10:]
        return messages

# Global instances
monitor = SystemMonitor()
context_mgr = ContextManager()
