from scapy.all import rdpcap, UDP
import re

# Define the input PCAP filename
pcap_filename = "temperature_sensor_with_alarms.pcap"

# Read packets from the PCAP file
packets = rdpcap(pcap_filename)

# Lists to store extracted data
temperature_readings = []
alarms = []

# Regular expressions for temperature and alarm messages
temp_pattern = re.compile(r"TEMP=(-?\d+\.\d+) C")
alarm_pattern = re.compile(r"ALARM: TEMP=(-?\d+\.\d+) C")

# Loop through packets and extract relevant data
for packet in packets:
    if packet.haslayer(UDP) and packet.haslayer("Raw"):
        payload = packet["Raw"].load.decode(errors="ignore")  # Extract payload
        
        # Extract temperature values
        temp_match = temp_pattern.search(payload)
        if temp_match:
            temperature_readings.append(float(temp_match.group(1)))
        
        # Extract alarms
        alarm_match = alarm_pattern.search(payload)
        if alarm_match:
            alarms.append(float(alarm_match.group(1)))

# Display extracted temperature readings
print("\n🌡️ Temperature Readings:")
print("-" * 30)
for temp in temperature_readings:
    print(f"Temperature: {temp:.1f}°C")

# Display extracted alarms
print("\n🚨 Alarm Messages:")
print("-" * 30)
for alarm in alarms:
    print(f"ALARM TRIGGERED at {alarm:.1f}°C")

print("\n✅ Extraction complete!")
