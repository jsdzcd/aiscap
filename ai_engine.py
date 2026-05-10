import os
from openai import OpenAI
import json

class AITrafficAnalyzer:
    def __init__(self, api_key=None, base_url=None):
        # 默认使用环境变量或用户提供的配置
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "your-api-key")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def analyze(self, summary_data):
        """发送流量摘要给 AI 进行分析"""
        prompt = f"""
        你是一个专业的网络安全专家。请分析以下网络流量摘要，并提供你的见解：
        
        流量摘要信息：
        {json.dumps(summary_data, indent=2)}
        
        请从以下几个方面进行分析：
        1. **流量概览**：简述流量的主要特征。
        2. **潜在风险**：是否有可疑的端口扫描、异常协议或频繁的连接行为？
        3. **载荷分析**：根据提供的样本载荷（Payload），判断是否存在明文敏感信息或恶意指令。
        4. **改进建议**：针对发现的问题提出安全防护建议。
        
        请使用 Markdown 格式输出分析报告。
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini", # 默认使用高效模型
                messages=[
                    {"role": "system", "content": "你是一个资深网络安全分析师，擅长从数据包特征中发现潜在威胁。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI 分析失败: {str(e)}\n\n请检查您的 API Key 或网络连接。"

    def analyze_single_packet(self, packet_info):
        """对单个可疑数据包进行深度分析"""
        prompt = f"""
        请分析以下特定数据包的详细信息：
        {json.dumps(packet_info, indent=2)}
        
        这个数据包是否表现出恶意特征？如果是协议握手或常规通信，请解释其目的。
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "你是一个协议分析专家。"},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"分析失败: {str(e)}"
