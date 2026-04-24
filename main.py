from src.edgebrain.core.engine import EdgeBrainEngine
from loguru import logger

def main():
    logger.info("Starting EdgeBrain 3.0 Pro Integration Test...")
    
    # 初始化引擎
    engine = EdgeBrainEngine()
    
    # 测试用例 1: 触发系统信息查询技能 (带安全拦截)
    test_input_1 = {
        "messages": [{"role": "user", "content": "Check system status"}],
        "reasoning_steps": [],
        "tool_calls": [],
        "tool_results": [],
        "retrieved_docs": [],
        "context_summary": None,
        "visual_input": None,
        "current_node": "start",
        "error_message": None,
        "requires_approval": False,
        "approval_status": None,
        "next_action": None,
        "target_skill": None
    }
    
    logger.info("--- Test Case 1: System Info Skill ---")
    try:
        result_1 = engine.run(test_input_1)
        logger.success(f"Result: {result_1}")
    except Exception as e:
        logger.error(f"Test Case 1 Failed: {e}")

    # 测试用例 2: 普通对话 (直接响应)
    test_input_2 = {
        "messages": [{"role": "user", "content": "Hello EdgeBrain"}],
        "reasoning_steps": [],
        "tool_calls": [],
        "tool_results": [],
        "retrieved_docs": [],
        "context_summary": None,
        "visual_input": None,
        "current_node": "start",
        "error_message": None,
        "requires_approval": False,
        "approval_status": None,
        "next_action": None,
        "target_skill": None
    }

    logger.info("--- Test Case 2: General Chat ---")
    try:
        result_2 = engine.run(test_input_2)
        logger.success(f"Result: {result_2}")
    except Exception as e:
        logger.error(f"Test Case 2 Failed: {e}")

    # 测试用例 3: RAG 知识查询
    test_input_3 = {
        "messages": [{"role": "user", "content": "EdgeBrain 的核心组件有哪些？"}],
        "reasoning_steps": [],
        "tool_calls": [],
        "tool_results": [],
        "retrieved_docs": [],
        "context_summary": None,
        "visual_input": None,
        "current_node": "start",
        "error_message": None,
        "requires_approval": False,
        "approval_status": None,
        "next_action": None,
        "target_skill": None
    }

    logger.info("--- Test Case 3: RAG Knowledge Query ---")
    try:
        result_3 = engine.run(test_input_3)
        logger.success(f"Result: {result_3}")
    except Exception as e:
        logger.error(f"Test Case 3 Failed: {e}")

if __name__ == "__main__":
    main()
