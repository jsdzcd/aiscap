import streamlit as st
import pandas as pd
import os
from traffic_parser import TrafficParser
from ai_engine import AITrafficAnalyzer
import tempfile

st.set_page_config(page_title="AI Traffic Analyzer", page_icon="🛡️", layout="wide")

st.title("🛡️ AI 离线流量分析工具")
st.markdown("""
本工具支持上传 PCAP 文件，通过解析网络协议特征，并结合 AI 模型进行智能安全分析。
""")

# 侧边栏配置
st.sidebar.header("配置选项")
api_key = st.sidebar.text_input("API Key", type="password", help="输入您的 OpenAI 兼容 API Key")
base_url = st.sidebar.text_input("Base URL", value="https://api.openai.com/v1")
model_name = st.sidebar.selectbox("AI 模型", ["gpt-4.1-mini", "gpt-4.1-nano", "local-model"])

# 文件上传
uploaded_file = st.file_uploader("选择一个 PCAP 文件", type=["pcap", "pcapng"])

if uploaded_file is not None:
    # 保存上传的文件到临时目录
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pcap") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    st.success(f"文件已上传: {uploaded_file.name}")

    # 解析流量
    with st.spinner("正在解析流量包..."):
        try:
            parser = TrafficParser(tmp_path)
            df = parser.parse()
            summary = parser.get_summary(df)
            
            # 展示基础统计
            st.subheader("📊 流量统计摘要")
            col1, col2, col3 = st.columns(3)
            col1.metric("总数据包数", summary["total_packets"])
            col2.metric("源 IP 数量", summary["unique_src_ips"])
            col3.metric("目的 IP 数量", summary["unique_dst_ips"])

            # 展示数据表格
            st.subheader("🔍 数据包详情")
            st.dataframe(df[["id", "timestamp", "src_ip", "src_port", "dst_ip", "dst_port", "protocol_name", "length"]].head(100))

            # AI 分析按钮
            if st.button("🚀 开始 AI 智能分析"):
                if not api_key:
                    st.error("请先在侧边栏输入 API Key！")
                else:
                    analyzer = AITrafficAnalyzer(api_key=api_key, base_url=base_url)
                    with st.spinner("AI 正在深度分析中，请稍候..."):
                        report = analyzer.analyze(summary)
                        st.subheader("📝 AI 安全分析报告")
                        st.markdown(report)

        except Exception as e:
            st.error(f"解析出错: {e}")
        finally:
            # 清理临时文件
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
else:
    st.info("请上传 PCAP 文件以开始分析。")
    
    # 演示用例说明
    with st.expander("如何使用此工具？"):
        st.write("""
        1. 使用 Wireshark 或 tcpdump 抓取流量并保存为 `.pcap` 文件。
        2. 将文件上传到本页面。
        3. 在左侧配置您的 AI 模型信息。
        4. 点击“开始 AI 智能分析”获取报告。
        """)
