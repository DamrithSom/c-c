import socket
import threading

all_connections = []
all_address = []

def create_socket(host='', port=9999):
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    print(f"Listening on port {port}...")
    return s

def accept_connections(s):
    def accept_loop():
        while True:
            conn, addr = s.accept()
            conn.setblocking(1)
            all_connections.append(conn)
            all_address.append(addr)
            print(f"New connection: {addr}")
    thread = threading.Thread(target=accept_loop, daemon=True)
    thread.start()

def get_clients():
    clients = []
    for i, addr in enumerate(all_address):
        clients.append({'id': i, 'ip': addr[0], 'port': addr[1]})
    return clients

def send_command_to_client(client_id, command):
    try:
        conn = all_connections[client_id]
        conn.send(str.encode(command))
        response = conn.recv(20480).decode()
        return response
    except Exception as e:
        return f"Error: {e}"
