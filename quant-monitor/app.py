import yaml
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from core.monitors.market_monitor import MarketMonitor
from core.alert.wecom_alert import WeComAlert
from core.alert.bark_alert import BarkAlert
from core.storage import init_db, save_alert

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_config():
    """
    加载配置文件
    """
    with open('config/config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def init_components(config):
    """
    初始化监控器和告警渠道
    """
    # 初始化监控器
    monitors = []
    
    # 加载市场监控器
    market_config = config['monitors']['market']
    if market_config['enabled']:
        monitors.append(MarketMonitor(market_config))
        logger.info(f"已加载市场监控器，共 {len(market_config['targets'])} 个监控标的")
    
    # 初始化告警渠道
    alerts = []
    alert_config = config['alert']
    if alert_config['enabled']:
        # 企业微信告警
        wecom_config = alert_config['channels'].get('wecom', {})
        if wecom_config.get('enabled', False):
            alerts.append(WeComAlert(wecom_config))
            logger.info("已加载企业微信告警渠道")
        
        # Bark告警
        bark_config = alert_config['channels'].get('bark', {})
        if bark_config.get('enabled', False):
            alerts.append(BarkAlert(bark_config))
            logger.info("已加载Bark告警渠道")
    
    return monitors, alerts

def check_task(monitors, alerts):
    """
    定时执行的监控检查任务
    """
    logger.info("开始执行监控检查...")
    for monitor in monitors:
        try:
            alerts_info = monitor.check()
            for alert_info in alerts_info:
                logger.warning(f"触发告警: {alert_info['message']}")
                # 保存告警记录
                save_alert(alert_info)
                # 发送告警到所有启用的渠道
                for alert in alerts:
                    alert.send(alert_info)
        except Exception as e:
            logger.error(f"监控器 {monitor.name} 执行失败: {e}", exc_info=True)

def main():
    config = load_config()
    init_db()
    monitors, alerts = init_components(config)
    
    if not monitors:
        logger.error("没有启用任何监控器，程序退出")
        return
    
    # 初始化定时任务
    scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    interval = config['monitors']['market']['interval']
    scheduler.add_job(
        check_task, 
        'interval', 
        seconds=interval, 
        args=[monitors, alerts],
        id='monitor_check'
    )
    
    logger.info(f"QuantMonitor 启动成功！")
    logger.info(f"检查间隔: {interval}秒")
    logger.info(f"已加载 {len(monitors)} 个监控器，{len(alerts)} 个告警渠道")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("QuantMonitor 已停止")

if __name__ == '__main__':
    main()
