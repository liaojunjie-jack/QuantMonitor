import sqlite3
import yaml
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any
from .data_fetcher import get_price_change

DB_PATH = "quant_monitor.db"

def init_db():
    """
    初始化数据库，创建告警表
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # 告警记录表
    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            target TEXT,
            symbol TEXT,
            message TEXT,
            current_value REAL,
            threshold REAL,
            time TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_alert(alert_info: Dict[str, Any]):
    """
    保存告警记录到数据库
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO alerts (type, target, symbol, message, current_value, threshold, time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        alert_info['type'],
        alert_info['target'],
        alert_info['symbol'],
        alert_info['message'],
        alert_info['current_change'],
        alert_info['threshold'],
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def get_alerts() -> List[Dict]:
    """
    获取历史告警记录
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql("SELECT * FROM alerts ORDER BY time DESC LIMIT 100", conn)
        conn.close()
        return df.to_dict('records')
    except Exception as e:
        print(f"获取告警记录失败: {e}")
        return []

def get_monitor_status() -> Dict:
    """
    获取当前监控状态
    """
    try:
        # 加载配置文件
        with open('config/config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 获取市场监控的状态
        targets = config['monitors']['market']['targets']
        status = {}
        for target in targets:
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
    except Exception as e:
        print(f"获取监控状态失败: {e}")
        return {}
