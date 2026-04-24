from loguru import logger
from .state import AgentState

class SelfHealingNode:
    def __init__(self):
        self.max_retries = 2

    def analyze_and_repair(self, state: AgentState) -> dict:
        """分析错误并尝试修复状态"""
        error_msg = state.get("error_message", "Unknown error")
        retry_count = state.get("retry_count", 0)
        
        logger.warning(f"Self-healing triggered. Error: {error_msg} | Retry: {retry_count}")

        if retry_count >= self.max_retries:
            logger.error("Max retries reached. Giving up.")
            return {"messages": [{"role": "assistant", "content": f"任务执行失败，已重试 {self.max_retries} 次仍无法解决：{error_msg}"}], "requires_approval": False}

        # 简单的自愈逻辑：如果是技能执行失败，尝试重置目标技能或提供建议
        repair_suggestion = ""
        if "No target skill" in error_msg:
            repair_suggestion = "检测到未指定技能，已自动切换至通用响应模式。"
            return {"next_action": "respond", "error_message": None, "retry_count": retry_count + 1, "messages": [{"role": "system", "content": repair_suggestion}]}
        
        # 默认重试策略：保持原状再次尝试（适用于网络波动等临时错误）
        logger.info("Attempting automatic retry...")
        return {"retry_count": retry_count + 1, "error_message": None}
