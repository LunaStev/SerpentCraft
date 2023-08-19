import socket

def start_server(host='0.0.0.0', port=25565):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"SerpentCraft server started on {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            # 여기서 실제 클라이언트 처리 로직을 구현해야 합니다.
            client_socket.close()
    except KeyboardInterrupt:
        print("SerpentCraft server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
