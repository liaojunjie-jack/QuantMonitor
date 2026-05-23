from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseMonitor(ABC):
    """
    监控器基类，所有监控器需要继承并实现抽象方法
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = self.__class__.__name__

    @abstractmethod
    def check(self) -> list:
        """
        执行监控检查，返回告警信息列表
        """
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """
        获取当前监控状态，用于可视化展示
        """
        pass
