import yfinance as yf
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

def is_a_stock(symbol: str) -> bool:
    """
    判断是否是A股标的
    """
    return symbol.endswith('.SS') or symbol.endswith('.SZ') or (symbol.isdigit() and len(symbol) == 6)

def get_price_change(symbol: str) -> float:
    """
    获取标的单日涨跌幅
    """
    try:
        if is_a_stock(symbol):
            # A股数据，使用AkShare获取
            if len(symbol) == 6:
                # 补全市场后缀
                if symbol.startswith('6') or symbol.startswith('5') or symbol.startswith('9'):
                    symbol = f"{symbol}.SS"
                else:
                    symbol = f"{symbol}.SZ"
            
            # 获取日线数据
            df = ak.stock_zh_a_daily(symbol=symbol, adjust="hfq")
        else:
            # 海外标的，使用Yahoo Finance获取
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="2d")
        
        if len(df) < 2:
            return 0.0
        
        # 计算单日涨跌幅
        prev_close = df['close'].iloc[-2]
        current_close = df['close'].iloc[-1]
        change = (current_close - prev_close) / prev_close * 100
        
        return round(change, 2)
    except Exception as e:
        print(f"获取 {symbol} 数据失败: {e}")
        return 0.0
