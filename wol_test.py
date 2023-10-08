import socket
import struct


def address2packet(address):
    # Trans input mac adress
    if len(address) == 17:
        separate = address[2]
        address = address.replace(separate, "")
    # Pass if omit separate
    elif len(address) == 12:
        pass
    # If format incorrect
    else:
        return True
    # Convert input mac adress string into bytes
    try:
        bytes_mac = bytes.fromhex("F" * 12 + address *16)
        return bytes_mac
    # If Mac address format incorrect
    except ValueError:
        return False


def packet_broadcasting(payload, broadcast_range='255.255.255.255', broadcast_protocol=9):
    # Broadcast socket
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
    ret = broadcast_socket.sendto(payload,(broadcast_range, broadcast_protocol))
    print(f'sent [{ret}]byte')
    broadcast_socket.close()




payload = address2packet("mac_address")
packet_broadcasting(payload)

