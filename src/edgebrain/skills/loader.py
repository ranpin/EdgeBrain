import os
import sys
import json
import importlib
from typing import Dict, Any, Callable
from loguru import logger

# 确保虚拟环境的 site-packages 在路径中
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    venv_site_packages = os.path.join(sys.prefix, 'lib', f'python{sys.version_info.major}.{sys.version_info.minor}', 'site-packages')
    if venv_site_packages not in sys.path:
        sys.path.insert(0, venv_site_packages)

class SkillLoader:
    """
    EdgeBrain 声明式技能加载器
    支持从 JSON 配置文件动态加载工具函数
    """
    def __init__(self, skills_dir: str = None):
        self.skills_dir = skills_dir or os.path.join(os.path.dirname(__file__))
        self.skills_registry: Dict[str, Dict[str, Any]] = {}
        self._scan_and_load()

    def _scan_and_load(self):
        """扫描目录下的所有 .json 技能配置文件并加载"""
        for filename in os.listdir(self.skills_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(self.skills_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        skill_config = json.load(f)
                        skill_id = skill_config.get('id')
                        if skill_id:
                            self.skills_registry[skill_id] = skill_config
                            logger.info(f"Skill loaded: {skill_id} - {skill_config.get('name')}")
                except Exception as e:
                    logger.error(f"Failed to load skill from {filepath}: {e}")

    def get_handler(self, skill_id: str) -> Callable:
        """
        根据 skill_id 获取对应的处理函数
        """
        config = self.skills_registry.get(skill_id)
        if not config:
            raise ValueError(f"Skill '{skill_id}' not found in registry.")
        
        module_path = config.get('handler_module')
        func_name = config.get('handler_function')
        
        if not module_path or not func_name:
            raise ValueError(f"Invalid configuration for skill '{skill_id}'.")
        
        try:
            module = importlib.import_module(module_path)
            handler = getattr(module, func_name)
            return handler
        except (ImportError, AttributeError) as e:
            logger.error(f"Failed to load handler for {skill_id}: {e}")
            raise e

    def execute(self, skill_id: str, **kwargs) -> Any:
        """执行指定的技能"""
        handler = self.get_handler(skill_id)
        return handler(**kwargs)
