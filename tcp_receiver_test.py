import socket

def start_server():
    HOST = '0.0.0.0'
    PORT = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    
    print(f"Server listening on Port {PORT} for ESP8266...")
    conn, addr = server_socket.accept()
    print(f"Connected to ESP8266 at {addr}")
    
    # Receive dummy audio packets
    while True:
        packet = conn.recv(4096)
        if not packet:
            break
        print(f"Received audio packet of size: {len(packet)} bytes")
        
    conn.close()

if __name__ == "__main__":
    start_server()
