# 📈 QuantMonitor - 量化金融实时监测系统

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Last Commit](https://img.shields.io/github/last-commit/your-username/quant-monitor)

一个开源的量化金融实时监测工具，帮助量化投资者实时掌握市场异动、风险指标与策略运行状态，不错过任何关键信号。

## ✨ 功能特性
- 🌍 **全市场覆盖**：支持A股、美股、外汇、加密货币等多类资产，统一监控入口
- 📊 **多维度监控**：
  - ✅ **市场异动监控**：实时检测价格涨跌幅、成交量异常波动
  - 🔄 **风险指标监控**：支持波动率、VaR、最大回撤等风险指标实时跟踪（开发中）
  - 🎯 **策略运行监控**：实盘策略净值、持仓、绩效指标全链路监测（开发中）
- 🚨 **多渠道告警**：支持企业微信、飞书、Bark、邮件等多种告警推送方式
- 📈 **可视化仪表盘**：轻量级Web监控面板，直观查看监控状态与历史告警
- ⚙️ **灵活配置**：自定义监控标的、阈值、告警规则，满足个性化需求
- 🧩 **模块化设计**：易于扩展新的监控类型、告警渠道，支持按需定制

## 🚀 快速开始

### 环境要求
- Python 3.9+
- pip 20.0+

### 1. 克隆仓库
```bash
git clone https://github.com/your-username/quant-monitor.git
cd quant-monitor
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置监控规则
修改 `config/config.yaml`，根据你的需求配置监控与告警：
```yaml
# 监控配置
monitors:
  market:
    enabled: true
    interval: 300  # 检查间隔，单位：秒
    targets:
      - symbol: 000001.SS
        name: 上证指数
        threshold: -5.0  # 负数=跌幅阈值，正数=涨幅阈值

# 告警配置
alert:
  enabled: true
  channels:
    wecom:
      enabled: true
      webhook: "你的企业微信机器人Webhook"
    bark:
      enabled: true
      device_key: "你的Bark设备Key"
```

### 4. 启动服务
```bash
# 启动后台监控服务
python app.py

# 启动可视化监控仪表盘
streamlit run dashboard.py
```

## ❓ 常见问题

### 1. 如何创建企业微信机器人？
1. 打开企业微信，进入目标群聊
2. 点击群聊右上角「...」→ 找到「群机器人」
3. 点击「添加机器人」，完成创建后即可获取Webhook地址

### 2. 如何获取Bark的设备Key？
1. 在App Store下载 **Bark** 应用
2. 打开Bark，首页即可看到你的设备Key，复制填入配置即可

### 3. 支持哪些标的格式？
| 市场 | 格式示例 | 说明 |
|------|----------|------|
| A股 | `000001.SS` / `000001` | 支持带后缀或纯6位代码 |
| 美股 | `NVDA` / `TSLA` | 美股股票代码 |
| 加密货币 | `BTC-USD` / `ETH-USD` | Yahoo Finance支持的币种格式 |

### 4. 如何自定义告警阈值？
在配置文件的`targets`中，`threshold`字段：
- 填写负数：监控跌幅，例如`-5.0`表示单日跌幅超过5%告警
- 填写正数：监控涨幅，例如`3.0`表示单日涨幅超过3%告警

## 📁 项目结构
```
quant-monitor/
├── README.md               # 项目说明文档
├── requirements.txt        # 依赖包列表
├── LICENSE                 # 许可证文件
├── config/
│   └── config.yaml         # 全局配置文件
├── core/
│   ├── data_fetcher.py     # 多市场数据获取模块
│   ├── storage.py          # 本地数据存储模块
│   ├── monitors/           # 监控器模块
│   │   ├── base.py         # 监控器抽象基类
│   │   └── market_monitor.py # 市场异动监控实现
│   └── alert/              # 告警渠道模块
│       ├── base.py         # 告警渠道抽象基类
│       ├── wecom_alert.py  # 企业微信告警实现
│       └── bark_alert.py   # Bark推送告警实现
├── app.py                  # 监控服务启动入口
└── dashboard.py            # 可视化监控仪表盘
```

## 🛠️ 扩展开发

### 添加新的监控类型
1. 在 `core/monitors/` 下创建新的监控文件，继承 `BaseMonitor`
2. 实现 `check()`（检查逻辑）和 `get_status()`（状态获取）方法
3. 在 `app.py` 中加载新的监控器即可

### 添加新的告警渠道
1. 在 `core/alert/` 下创建新的告警文件，继承 `BaseAlert`
2. 实现 `send()` 方法，完成告警推送逻辑
3. 在配置文件中添加对应的配置项即可

## 🤝 贡献
欢迎提交 Issue 和 Pull Request 来完善这个项目！
- 报告Bug或提出新功能建议
- 提交代码改进
- 完善文档

## 📝 许可证
本项目采用 [MIT](LICENSE) 许可证，你可以自由使用、修改和分发该项目。
