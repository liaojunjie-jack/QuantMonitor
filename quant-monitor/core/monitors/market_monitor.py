from typing import Dict, Any, List
from .base import BaseMonitor
from ...data_fetcher import get_price_change

class MarketMonitor(BaseMonitor):
    """
    市场异动监控器，监控标的价格涨跌幅是否超过阈值
    """
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.targets: List[Dict] = config.get('targets', [])
        self.interval = config.get('interval', 300)

    def check(self) -> List[Dict]:
        """
        执行市场监控检查，返回触发的告警列表
        """
        alerts = []
        for target in self.targets:
            symbol = target['symbol']
            name = target['name']
            threshold = target['threshold']
            
            # 获取当前涨跌幅
            change = get_price_change(symbol)
            
            # 判断是否触发告警
            if threshold < 0:
                # 跌幅监控
                if change <= threshold:
                    alerts.append({
                        'type': 'market_alert',
                        'target': name,
                        'symbol': symbol,
                        'current_change': change,
                        'threshold': threshold,
                        'message': f"[{name}] 单日跌幅达到{change:.2f}%，超过阈值{threshold:.2f}%"
                    })
            else:
                # 涨幅监控
                if change >= threshold:
                    alerts.append({
                        'type': 'market_alert',
                        'target': name,
                        'symbol': symbol,
                        'current_change': change,
                        'threshold': threshold,
                        'message': f"[{name}] 单日涨幅达到{change:.2f}%，超过阈值{threshold:.2f}%"
                    })
        
        return alerts

    def get_status(self) -> Dict[str, Any]:
        """
        获取当前所有监控标的的状态
        """
        status = {}
        for target in self.targets:
            symbol = target['symbol']
            name = target['name']
            change = get_price_change(symbol)
            threshold = target['threshold']
            
            if threshold < 0:
                alert_triggered = change <= threshold
            else:
                alert_triggered = change >= threshold
            
            status[symbol] = {
                'name': name,
                'change': change,
                'threshold': threshold,
                'alert_triggered': alert_triggered
            }
        return status
