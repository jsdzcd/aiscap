🛡️ AI 离线流量分析工具

这是一个基于 Python 和 Streamlit 构建的轻量级网络流量分析工具，结合了 Scapy 的强大解析能力与 AI 的智能分析逻辑。

🌟 核心功能

•
PCAP 解析：快速提取数据包的源/目的 IP、端口、协议及 Payload 摘要。

•
特征提取：自动生成流量统计摘要（如 Top 端口、协议分布）。

•
AI 智能分析：支持通过 OpenAI 兼容接口（如 GPT-4, Ollama 等）生成安全报告。

•
可视化界面：直观的 Web 界面，支持文件上传与实时结果展示。

🚀 快速开始

1. 环境准备

确保您的系统中已安装 Python 3.8+，然后安装依赖：

Bash


pip install scapy pandas streamlit openai



2. 运行工具

在项目目录下运行以下命令启动 Web 界面：

Bash


streamlit run app.py



启动后，浏览器会自动打开 http://localhost:8501 。

3. 使用步骤

1.
在侧边栏输入您的 API Key（如果使用本地模型如 Ollama，请修改 Base URL）。

2.
上传一个 .pcap 或 .pcapng 文件。

3.
点击 “🚀 开始 AI 智能分析” 按钮。

📂 项目结构

•
app.py: Streamlit Web 界面主程序。

•
traffic_parser.py: 负责流量包解析与特征提取。

•
ai_engine.py: 负责与 AI 模型交互。

•
generate_test_pcap.py: 用于生成测试样本的脚本。

🔒 隐私与安全

本工具在本地解析 PCAP 文件，仅将提取的摘要信息（不含完整数据包）发送至您配置的 AI 接口。若需完全离线，建议配合 Ollama 使用本地大模型。

