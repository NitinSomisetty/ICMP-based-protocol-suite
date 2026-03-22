import socket
import struct
import time
import os
from utils import resolve_host

ICMP_ECHO_REQUEST = 8


def checksum(source):
    sum = 0
    count_to = (len(source) // 2) * 2
    count = 0
    #masking the checksum to 32 bits to prevent overflow, and then adding each 16-bit chunk of the source data to the sum.
    while count < count_to:
        this_val = source[count + 1] * 256 + source[count]
        sum = sum + this_val
        sum = sum & 0xffffffff
        count += 2

    if count_to < len(source):
        sum += source[len(source) - 1]
        sum = sum & 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)

    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer

#Field map of format bbHHh is: type, code, checksum, identifier, sequence.
# b = signed char, 1 byte, range -128 to 127
# B = unsigned char, 1 byte, range 0 to 255
# H = unsigned short, 2 bytes, range 0 to 65535

def create_packet(id):
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, id, 1)
    data = struct.pack("d", time.time())

    chksum = checksum(header + data)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0,
                         socket.htons(chksum), id, 1)

    return header + data


def ping(host, count=4):

    dest = resolve_host(host)

    output = f"\nPinging {host} [{dest}] with 32 bytes of data:\n\n"

    rtts = []

    for _ in range(count):

        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

        packet_id = os.getpid() & 0xFFFF
        packet = create_packet(packet_id)

        start = time.time()

        sock.sendto(packet, (dest, 1)) #ICMP doesn’t use ports
        sock.settimeout(2) 

        try:
            sock.recvfrom(1024)
            end = time.time()

            rtt = (end - start) * 1000
            rtts.append(rtt) #an array of round-trip times for each ping attempt, which will be used to calculate statistics later. 

            output += f"Reply from {dest}: time={round(rtt)}ms\n"

        except socket.timeout:  
            output += "Request timed out\n"

        sock.close()
    
    #stats
    sent = count
    received = len(rtts)
    lost = sent - received
    loss = (lost / sent) * 100

    if received > 0:
        minimum = min(rtts)
        maximum = max(rtts)
        avg = sum(rtts) / len(rtts)
    else:
        minimum = maximum = avg = 0

    output += f"\nPing statistics for {dest}:\n"
    output += f"    Packets: Sent = {sent}, Received = {received}, Lost = {lost} ({loss}% loss)\n"

    output += "\nApproximate round trip times in milli-seconds:\n"
    output += f"    Minimum = {round(minimum)}ms, Maximum = {round(maximum)}ms, Average = {round(avg)}ms\n"

    return output