import socket

def setup_server(host="0.0.0.0", port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"\n🚀 FINAL AI SERVER WITH MEMORY STARTED ON PORT {port}")
    return server_socket
