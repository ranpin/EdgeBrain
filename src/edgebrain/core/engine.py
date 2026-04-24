import os
from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.types import interrupt
from loguru import logger

from .state import AgentState
from .config import settings
from .rag_node import RAGNode
from .vlm_node import VLMNode
from .screen_awareness_node import ScreenAwarenessNode
from .self_healing_node import SelfHealingNode
from ..skills.loader import SkillLoader
from ..security.gateway import SecurityGateway

class EdgeBrainEngine:
    def __init__(self):
        self.skill_loader = SkillLoader()
        self.security_gateway = SecurityGateway()
        self.rag_node = RAGNode(data_dir=os.path.join(settings.project_root, "data", "knowledge_base"))
        self.vlm_node = VLMNode()
        self.screen_node = ScreenAwarenessNode()
        self.healing_node = SelfHealingNode()
        self.graph = self._build_graph()
        logger.info("EdgeBrain Engine initialized with RAG, VLM and Declarative Skills.")

    def _plan_node(self, state: AgentState) -> dict:
        """规划节点：分析意图并决定下一步动作"""
        logger.info("Planning node executed.")
        last_msg = state['messages'][-1]['content'].lower()
        next_action = "respond"
        target_skill = None
        
        # 技能执行意图
        if "系统" in last_msg or "status" in last_msg or "cpu" in last_msg:
            next_action = "execute"
            target_skill = "sys_info_v1"
        # RAG 检索意图
        elif any(kw in last_msg for kw in ["核心组件", "架构", "说明", "是什么", "how to", "what is"]):
            next_action = "retrieve"
            
        return {"reasoning_steps": [f"Intent analyzed: {next_action}"], "next_action": next_action, "target_skill": target_skill}

    def _retrieve_node(self, state: AgentState) -> dict:
        """检索节点：执行 RAG 查询"""
        logger.info("Retrieval node executed.")
        query = state['messages'][-1]['content']
        docs = self.rag_node.query(query)
        return {"retrieved_docs": docs}

    def _execute_node(self, state: AgentState) -> dict:
        """执行节点：调用技能并经过安全网关"""
        logger.info("Execution node started.")
        skill_id = state.get('target_skill')
        if not skill_id:
            return {"error_message": "No target skill specified."}

        # 安全检查
        check_result = self.security_gateway.check_permission(skill_id, "EXECUTE")
        if not check_result.get("allowed", False):
            reason = check_result.get("reason", "Unknown restriction")
            logger.warning(f"HITL required: {reason}")
            # 触发中断，等待用户确认
            user_input = interrupt(value={"question": f"安全网关拦截：{reason}\n是否继续执行？(yes/no)", "skill_id": skill_id})
            if user_input and user_input.lower() == "yes":
                logger.info("User approved the action.")
            else:
                logger.info("User rejected the action.")
                return {"error_message": "Action cancelled by user.", "requires_approval": False}

        try:
            result = self.skill_loader.execute(skill_id)
            logger.info(f"Skill {skill_id} executed successfully: {result}")
            return {"tool_results": [result], "requires_approval": False}
        except Exception as e:
            logger.error(f"Skill execution failed: {e}")
            return {"error_message": str(e)}

    def _vlm_node(self, state: AgentState) -> dict:
        """视觉节点：分析图像内容"""
        logger.info("VLM node executed.")
        return self.vlm_node.analyze(state)

    def _screen_awareness_node(self, state: AgentState) -> dict:
        """屏幕感知节点：截图并分析 UI"""
        logger.info("Screen Awareness node executed.")
        return self.screen_node.execute(state)

    def _respond_node(self, state: AgentState) -> dict:
        """响应节点：生成最终回复"""
        logger.info("Response node executed.")
        response_text = "Task processed by EdgeBrain 3.0 Pro."
        if state.get('tool_results'):
            response_text = f"Execution Result: {state['tool_results']}"
        elif state.get('retrieved_docs'):
            response_text = f"RAG Context: {state['retrieved_docs']}"
        
        return {"messages": [{"role": "assistant", "content": response_text}]}

    def _self_healing_node(self, state: AgentState) -> dict:
        """自愈节点：分析错误并尝试修复"""
        logger.info("Self-healing node executed.")
        return self.healing_node.analyze_and_repair(state)

    def _route_logic(self, state: AgentState) -> Literal["retrieve", "execute", "respond", "vlm", "screen", "self_heal"]:
        """路由逻辑"""
        # 优先处理错误状态，触发自愈
        if state.get("error_message"):
            return "self_heal"

        # 优先处理多模态输入
        if state.get("image_path"):
            return "vlm"
        
        # 检查屏幕感知意图
        last_msg = state['messages'][-1]['content'].lower()
        if any(kw in last_msg for kw in ["屏幕", "截图", "分析当前界面", "screen", "screenshot"]):
            return "screen"
        
        next_action = state.get('next_action', 'respond')
        logger.info(f"Routing decision: {next_action}")
        if next_action == "execute":
            return "execute"
        elif next_action == "retrieve":
            return "retrieve"
        return "respond"

    def _build_graph(self) -> StateGraph:
        """构建 LangGraph 状态机"""
        workflow = StateGraph(AgentState)
        
        workflow.add_node("plan", self._plan_node)
        workflow.add_node("retrieve", self._retrieve_node)
        workflow.add_node("execute", self._execute_node)
        workflow.add_node("vlm", self._vlm_node)
        workflow.add_node("screen", self._screen_awareness_node)
        workflow.add_node("self_heal", self._self_healing_node)
        workflow.add_node("respond", self._respond_node)
        
        workflow.set_entry_point("plan")
        workflow.add_conditional_edges("plan", self._route_logic)
        workflow.add_edge("retrieve", "respond")
        workflow.add_edge("execute", "respond")
        workflow.add_edge("vlm", "respond")
        workflow.add_edge("screen", "respond")
        workflow.add_edge("self_heal", "plan")  # 自愈后重新规划
        
        return workflow.compile()

    def run(self, input_data: dict):
        """运行引擎"""
        return self.graph.invoke(input_data)
