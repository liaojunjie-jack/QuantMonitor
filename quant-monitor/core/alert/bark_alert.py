import requests
from typing import Dict, Any
from .base import BaseAlert

class BarkAlert(BaseAlert):
    """
    Bark iOS推送告警渠道
    """
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.device_key = config.get('device_key', '')

    def send(self, alert_info: Dict[str, Any]) -> bool:
        """
        发送告警到Bark
        """
        if not self.device_key:
            return False
        
        message = alert_info['message']
        url = f"https://api.day.app/{self.device_key}/QuantMonitor/{message}"
        
        try:
            response = requests.get(url, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Bark告警发送失败: {e}")
            return False
