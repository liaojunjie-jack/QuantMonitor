import streamlit as st
import pandas as pd
from core.storage import get_alerts, get_monitor_status

# 页面配置
st.set_page_config(
    page_title="QuantMonitor 监控仪表盘",
    page_icon="📈",
    layout="wide"
)

st.title("📈 QuantMonitor 量化金融监控仪表盘")
st.caption("实时监控市场异动与风险指标，助你把握投资机会")

# 刷新按钮
if st.button("🔄 刷新数据"):
    st.rerun()

# 实时市场状态
st.header("市场监控状态")
status = get_monitor_status()
if status:
    # 转换为DataFrame
    df = pd.DataFrame.from_dict(status, orient='index')
    df['状态'] = df['alert_triggered'].apply(lambda x: "⚠️ 告警" if x else "✅ 正常")
    df['涨跌幅(%)'] = df['change']
    df['阈值(%)'] = df['threshold']
    
    # 重命名列
    display_df = df[['name', '涨跌幅(%)', '阈值(%)', '状态']].rename(columns={'name': '标的名称'})
    st.dataframe(display_df, use_container_width=True)
else:
    st.info("暂无监控数据")

# 历史告警
st.header("历史告警记录")
alerts = get_alerts()
if alerts:
    alerts_df = pd.DataFrame(alerts)
    alerts_df['时间'] = alerts_df['time']
    alerts_df['标的'] = alerts_df['target']
    alerts_df['告警信息'] = alerts_df['message']
    
    display_alerts = alerts_df[['时间', '标的', '告警信息']]
    st.dataframe(display_alerts, use_container_width=True)
else:
    st.info("暂无告警记录")

# 页脚
st.divider()
st.caption("QuantMonitor - 开源量化金融实时监测工具")
