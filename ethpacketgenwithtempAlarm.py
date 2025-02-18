from scapy.all import Ether, IP, UDP, Raw, wrpcap

# Define the output PCAP filename
pcap_filename = "temperature_sensor_with_alarms.pcap"

# List to store packets
packets = []

# Generate packets for temperature values from 25.0°C to 42.0°C (step 0.5°C)
for temp in range(500, 840, 5):  # Multiply by 10 to handle decimal steps
    temperature = temp / 10  # Convert back to float format (e.g., 25.0, 25.5, ...)
    
    # Create an Ethernet frame
    eth = Ether(dst="ff:ff:ff:ff:ff:ff", src="00:1a:2b:3c:4d:5e", type=0x0800)

    # Create an IP packet
    ip = IP(src="192.168.1.100", dst="192.168.1.1")

    # Create a UDP packet
    udp = UDP(sport=8080, dport=8080)

    # Regular Temperature Sensor Message
    temp_message = f"TEMP={temperature:.1f} C"

    # Create the full temperature packet
    temp_packet = eth / ip / udp / Raw(load=temp_message)
    packets.append(temp_packet)

    # ** ALARM PACKET **
    if temperature % 5 == 0:  # Every 5°C (e.g., 25.0, 30.0, 35.0)
        alarm_message = f"ALARM: TEMP={temperature:.1f} C (HIGH TEMPERATURE)"
        alarm_packet = eth / ip / udp / Raw(load=alarm_message)
        packets.append(alarm_packet)

# Save all packets to a PCAP file
wrpcap(pcap_filename, packets)

print(f"PCAP file saved as {pcap_filename}")
