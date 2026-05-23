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

---

## 🚀 从零到一超详细配置&运行步骤
> 新手也可以直接跟着操作，每一步都有具体指引

### 🔹 步骤1：准备项目文件
1. 下载本项目的压缩包，右键解压到你电脑的任意目录，比如 `D:\quant-monitor`（**不要用中文路径**）

### 🔹 步骤2：安装Python环境（如果没装的话）
1. 打开Python官网：https://www.python.org/downloads/
2. 下载3.9以上的版本（比如3.11，不要用太低的版本）
3. 安装的时候，**一定要勾选左下角的「Add Python to PATH」**，然后点击安装即可

### 🔹 步骤3：安装项目依赖
1. 按下 `Win+R`，输入 `cmd`，回车打开命令提示符
2. 输入命令进入项目目录：
   ```cmd
   cd D:\quant-monitor
   ```
3. 执行依赖安装命令（如果下载慢，用清华源加速）：
   ```cmd
   # 普通安装
   pip install -r requirements.txt

   # 清华源加速安装
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```
4. 等待安装完成，没有报错就说明成功了

---

### 🔹 步骤4：配置你要监控的标的
1. 打开项目里的 `config` 文件夹，用记事本（或者VS Code）打开 `config.yaml` 文件
2. 找到 `monitors.market.targets` 这部分，这里是你要监控的股票/指数/加密货币，你可以修改、删除或者新增：
   ```yaml
   targets:
     # 例子1：监控上证指数，单日跌幅超过5%告警
     - symbol: 000001.SS
       name: 上证指数
       threshold: -5.0

     # 例子2：新增监控贵州茅台，单日跌幅超过7%告警
     - symbol: 600519  # A股可以直接写6位代码，也可以写600519.SS
       name: 贵州茅台
       threshold: -7.0

     # 例子3：新增监控英伟达，单日跌幅超过10%告警
     - symbol: NVDA
       name: 英伟达
       threshold: -10.0

     # 例子4：新增监控比特币，单日涨幅超过10%告警
     - symbol: BTC-USD
       name: 比特币
       threshold: 10.0
   ```
   ✅ 配置说明：
   - `symbol`：标的代码，A股写6位代码即可，美股写股票代码，加密货币写`BTC-USD`这种格式
   - `name`：你给这个标的起的名字，告警的时候会显示这个名字
   - `threshold`：告警阈值，**负数=监控跌幅**，**正数=监控涨幅**

---

### 🔹 步骤5：配置告警渠道（以企业微信为例，最常用）
1. 打开企业微信，进入你要接收告警的群聊
2. 点击群聊右上角的「...」，往下滑动找到「群机器人」
3. 点击「添加机器人」，输入机器人名字（比如`QuantMonitor告警`），点击「完成」
4. 复制生成的Webhook地址，比如：`https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxx`
5. 回到 `config.yaml`，找到 `alert.channels.wecom` 部分，修改配置：
   ```yaml
   wecom:
     enabled: true  # 把这里的false改成true，启用企业微信告警
     webhook: "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxx"  # 把你刚才复制的Webhook填在这里
   ```

---

### 🔹 步骤6：（可选）配置Bark iOS推送
如果你是iPhone用户，可以用Bark接收实时推送：
1. 在App Store下载 **Bark** 应用，打开它
2. 复制首页的设备Key，比如 `abc123xyz`
3. 回到 `config.yaml`，找到 `alert.channels.bark` 部分：
   ```yaml
   bark:
     enabled: true  # 改成true启用
     device_key: "abc123xyz"  # 把你的设备Key填在这里
   ```

---

### 🔹 步骤7：测试配置是否正常
1. 回到命令提示符，执行启动命令：
   ```cmd
   python app.py
   ```
2. 如果看到输出 `QuantMonitor 启动成功！`，说明你的配置没有问题，程序已经开始定时监控了
3. （可选测试）你可以临时把某个标的的阈值改得很大，比如把上证指数的阈值改成`0`，等待5分钟，看看能不能收到告警通知，测试告警是否正常

---

### 🔹 步骤8：启动可视化监控仪表盘
1. 打开一个**新的**命令提示符，还是进入项目目录：`cd D:\quant-monitor`
2. 执行仪表盘启动命令：
   ```cmd
   streamlit run dashboard.py
   ```
3. 执行完之后，会自动打开一个网页，你就可以看到所有监控标的的实时状态、历史告警记录了，网页地址是 `http://localhost:8501`

---

### 🔹 进阶：让程序后台自动运行
如果想要程序开机自动启动、后台运行不关闭：
1. Windows用户可以用「任务计划程序」，设置开机自动执行 `python app.py`
2. Mac/Linux用户可以用 `nohup python app.py &` 后台运行

---

## ❓ 常见问题
### 1. 支持哪些标的格式？
| 市场 | 格式示例 | 说明 |
|------|----------|------|
| A股 | `000001.SS` / `000001` | 支持带后缀或纯6位代码 |
| 美股 | `NVDA` / `TSLA` | 美股股票代码 |
| 加密货币 | `BTC-USD` / `ETH-USD` | Yahoo Finance支持的币种格式 |

### 2. 安装依赖的时候报错了怎么办？
- 检查你的Python版本是不是3.9以上
- 试试用管理员身份打开命令提示符，再执行安装命令
- 换用清华源安装，解决网络问题

### 3. 收不到告警怎么办？
- 检查配置里的`enabled`是不是改成了`true`
- 检查Webhook/设备Key是不是填对了，有没有空格
- 测试的时候把阈值改小，触发告警看看能不能收到

## 📁 项目结构
```
quant-monitor/
├── README.md               # 项目说明文档（就是你现在看的这个）
├── requirements.txt        # 依赖包列表
├── LICENSE                 # 许可证文件
├── config/
│   └── config.yaml         # 全局配置文件，所有配置都在这里改
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

## 📝 许可证
本项目采用 [MIT](LICENSE) 许可证，你可以自由使用、修改和分发该项目。
