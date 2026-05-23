import requests
from typing import Dict, Any
from .base import BaseAlert

class WeComAlert(BaseAlert):
    """
    企业微信机器人告警渠道
    """
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.webhook = config.get('webhook', '')

    def send(self, alert_info: Dict[str, Any]) -> bool:
        """
        发送告警到企业微信
        """
        if not self.webhook:
            return False
        
        message = alert_info['message']
        data = {
            "msgtype": "text",
            "text": {
                "content": f"【QuantMonitor告警】{message}"
            }
        }
        
        try:
            response = requests.post(self.webhook, json=data, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"企业微信告警发送失败: {e}")
            return False
