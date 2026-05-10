from scapy.all import wrpcap, IP, TCP, Raw
import os

def generate_test_pcap(filename):
    packets = []
    
    # 模拟一个 HTTP GET 请求
    pkt1 = IP(src="192.168.1.10", dst="93.184.216.34") / \
           TCP(sport=12345, dport=80, flags="S")
    packets.append(pkt1)
    
    pkt2 = IP(src="192.168.1.10", dst="93.184.216.34") / \
           TCP(sport=12345, dport=80, flags="A") / \
           Raw(load="GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
    packets.append(pkt2)

    # 模拟一个可疑的端口扫描行为
    for port in range(100, 105):
        pkt = IP(src="10.0.0.5", dst="192.168.1.1") / \
              TCP(sport=54321, dport=port, flags="S")
        packets.append(pkt)

    wrpcap(filename, packets)
    print(f"Generated test PCAP: {filename}")

if __name__ == "__main__":
    generate_test_pcap("/home/ubuntu/traffic_ai_tool/test_traffic.pcap")
