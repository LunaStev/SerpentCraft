import socket
import struct
import json

def send_packet(sock, data):
    packet_length = len(data)
    packed_length = struct.pack('>i', packet_length)
    sock.sendall(packed_length + data)

def read_varint(sock):
    num = 0
    for i in range(5):
        byte = sock.recv(1)
        num |= (byte[0] & 0x7F) << 7*i
        if not byte[0] & 0x80:
            break
    return num

def handle_client(client_socket):
    packet_length = read_varint(client_socket)
    packet_id = read_varint(client_socket)
    
    if packet_id == 0x00:  # Handshake packet
        protocol_version = read_varint(client_socket)
        server_address = ''
        byte = client_socket.recv(1)
        while byte != b'\x00':
            server_address += byte.decode('utf-8')
            byte = client_socket.recv(1)
        server_port = struct.unpack('>H', client_socket.recv(2))[0]
        next_state = read_varint(client_socket)

        if next_state == 1:  # Status request
            packet_length = read_varint(client_socket)
            packet_id = read_varint(client_socket)
            
            if packet_id == 0x00:  # Request
                response = {
                    "version": {
                        "name": "1.20.1",
                        "protocol": 763  # TODO: Replace with the correct protocol number for 1.20.1
                    },
                    "players": {
                        "max": 100,
                        "online": 5,
                        "sample": []
                    },
                    "description": {
                        "text": "SerpentCraft Server"
                    }
                }
                send_packet(client_socket, b'\x00' + json.dumps(response).encode('utf-8'))

    client_socket.close()

def start_server(host='0.0.0.0', port=25565):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"SerpentCraft server started on {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            handle_client(client_socket)
    except KeyboardInterrupt:
        print("SerpentCraft server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
