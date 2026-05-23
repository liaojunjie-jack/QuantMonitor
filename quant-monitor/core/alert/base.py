from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAlert(ABC):
    """
    告警渠道基类，所有告警渠道需要继承并实现抽象方法
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def send(self, alert_info: Dict[str, Any]) -> bool:
        """
        发送告警信息
        """
        pass
