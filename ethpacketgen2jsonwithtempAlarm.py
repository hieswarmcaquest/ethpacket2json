import json
import re
from scapy.all import rdpcap, UDP, IP, Ether
from decimal import Decimal

# Define the input PCAP filename
pcap_filename = "temperature_sensor_with_alarms.pcap"

# Read packets from the PCAP file
packets = rdpcap(pcap_filename)

# Lists to store extracted data
extracted_data = []

# Regular expressions for temperature and alarm messages
temp_pattern = re.compile(r"TEMP=(-?\d+\.\d+) C")
alarm_pattern = re.compile(r"ALARM: TEMP=(-?\d+\.\d+) C")

# Function to convert unsupported types to JSON-serializable types
def convert_to_serializable(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # Convert EDecimal to float
    return obj

# Loop through packets and extract relevant data
for packet in packets:
    if packet.haslayer(UDP) and packet.haslayer("Raw"):
        payload = packet["Raw"].load.decode(errors="ignore")  # Extract payload

        # Extract temperature values
        temp_match = temp_pattern.search(payload)
        temperature = float(temp_match.group(1)) if temp_match else None

        # Extract alarms
        alarm_match = alarm_pattern.search(payload)
        alarm_triggered = bool(alarm_match)

        # Extract Ethernet & IP details
        packet_info = {
            "timestamp": float(packet.time),  # Convert to standard float
            "eth": {
                "src_mac": str(packet[Ether].src) if packet.haslayer(Ether) else None,
                "dst_mac": str(packet[Ether].dst) if packet.haslayer(Ether) else None
            },
            "ip": {
                "src_ip": str(packet[IP].src) if packet.haslayer(IP) else None,
                "dst_ip": str(packet[IP].dst) if packet.haslayer(IP) else None,
                "protocol": int(packet[IP].proto) if packet.haslayer(IP) else None,
                "ttl": int(packet[IP].ttl) if packet.haslayer(IP) else None,
                "packet_length": int(len(packet)) if packet.haslayer(IP) else None
            },
            "udp": {
                "src_port": int(packet[UDP].sport) if packet.haslayer(UDP) else None,
                "dst_port": int(packet[UDP].dport) if packet.haslayer(UDP) else None
            },
            "sensor_data": {
                "temperature": temperature,
                "alarm_triggered": alarm_triggered
            }
        }
        
        extracted_data.append(packet_info)

# Save extracted data to a JSON file (for Elasticsearch ingestion)
json_filename = "extracted_sensor_data.json"
with open(json_filename, "w") as json_file:
    json.dump(extracted_data, json_file, indent=4, default=convert_to_serializable)

# Print confirmation
print(f"\n✅ Extraction complete! Data saved to {json_filename}")
