import pandas as pd
from scapy.all import rdpcap, IP, TCP, UDP, Raw
import os

class TrafficParser:
    def __init__(self, pcap_path):
        self.pcap_path = pcap_path
        self.packets = []

    def parse(self):
        """解析 PCAP 文件并提取数据包信息"""
        if not os.path.exists(self.pcap_path):
            raise FileNotFoundError(f"File not found: {self.pcap_path}")
        
        scapy_packets = rdpcap(self.pcap_path)
        parsed_data = []

        for i, pkt in enumerate(scapy_packets):
            if IP in pkt:
                info = {
                    "id": i,
                    "timestamp": float(pkt.time),
                    "src_ip": pkt[IP].src,
                    "dst_ip": pkt[IP].dst,
                    "proto": pkt[IP].proto,
                    "length": len(pkt),
                }

                # 提取端口和负载
                if TCP in pkt:
                    info["src_port"] = pkt[TCP].sport
                    info["dst_port"] = pkt[TCP].dport
                    info["protocol_name"] = "TCP"
                elif UDP in pkt:
                    info["src_port"] = pkt[UDP].sport
                    info["dst_port"] = pkt[UDP].dport
                    info["protocol_name"] = "UDP"
                else:
                    info["src_port"] = None
                    info["dst_port"] = None
                    info["protocol_name"] = "IP"

                # 提取原始载荷摘要
                if Raw in pkt:
                    payload = pkt[Raw].load
                    # 仅保留前 128 字节以供 AI 分析，避免 Token 过长
                    info["payload_hex"] = payload.hex()[:256]
                    info["payload_ascii"] = "".join([chr(b) if 32 <= b <= 126 else "." for b in payload[:128]])
                else:
                    info["payload_hex"] = ""
                    info["payload_ascii"] = ""

                parsed_data.append(info)
        
        self.packets = parsed_data
        return pd.DataFrame(parsed_data)

    def get_summary(self, df):
        """生成流量摘要以供 AI 分析"""
        if df.empty:
            return "No IP traffic found."
        
        summary = {
            "total_packets": len(df),
            "unique_src_ips": df["src_ip"].nunique(),
            "unique_dst_ips": df["dst_ip"].nunique(),
            "protocols": df["protocol_name"].value_counts().to_dict(),
            "top_dst_ports": df["dst_port"].value_counts().head(5).to_dict(),
            "sample_payloads": df[df["payload_ascii"] != ""]["payload_ascii"].head(5).tolist()
        }
        return summary
