# network_socket.py - Sagnik's Contribution
import socket

def setup_tcp_server(host="0.0.0.0", port=5000):
    """TCP Server socket initialize karta hai aur listen mode me dalta hai."""
    print(f"🚀 Starting AI Voice Server on PORT {port}...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print("✅ Server bind successful. Waiting for ESP8266 connection...")
        return server_socket
    except Exception as e:
        print(f"❌ Socket Binding Error: {e}")
        return None

def accept_client(server_socket):
    """Client connection accept karta hai."""
    conn, addr = server_socket.accept()
    print(f"📡 ESP8266 CONNECTED from {addr}!")
    return conn, addr
