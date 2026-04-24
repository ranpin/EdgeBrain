import psutil
import platform
from loguru import logger

def get_system_metrics() -> dict:
    """
    获取系统基础运行指标
    Returns:
        dict: 包含 CPU、内存、操作系统信息的字典
    """
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        os_info = {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine()
        }
        
        metrics = {
            "cpu_usage_percent": cpu_percent,
            "memory_total_gb": round(memory.total / (1024**3), 2),
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "memory_usage_percent": memory.percent,
            "os_info": os_info
        }
        
        logger.info(f"System metrics collected: CPU={cpu_percent}%, Mem={memory.percent}%")
        return metrics
    except Exception as e:
        logger.error(f"Failed to collect system metrics: {e}")
        return {"error": str(e)}
