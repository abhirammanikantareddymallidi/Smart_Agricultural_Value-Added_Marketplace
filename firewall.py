from scapy.all import *

blocked_ips = ["10.136.104.149","10.136.9.240","10.136.37.4"]
blocked_ports = [80]   # block HTTP

def firewall(packet):
    if packet.haslayer(IP):
        src_ip = packet[IP].src
        
        # Block IP
        if src_ip in blocked_ips:
            print(f"Blocked IP: {src_ip}")
            return
        
        # Block Port
        if packet.haslayer(TCP):
            if packet[TCP].dport in blocked_ports:
                print(f"Blocked Port: {packet[TCP].dport}")
                return
        
        print(f"Allowed: {src_ip}")

sniff(prn=firewall, store=0)