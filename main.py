import socket
import threading
import time

class ProtocolManager:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.tcp_server_socket = None
        self.udp_server_socket = None

    # TCP Server
    def start_tcp_server(self):
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.bind((self.host, self.port))
        self.tcp_server_socket.listen(5)
        print(f"TCP Server started on {self.host}:{self.port}")

        while True:
            client_socket, addr = self.tcp_server_socket.accept()
            print(f"TCP Client connected: {addr}")
            client_thread = threading.Thread(target=self.handle_tcp_client, args=(client_socket, addr))
            client_thread.start()

    def handle_tcp_client(self, client_socket, addr):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"TCP Received from {addr}: {data.decode()}")
                client_socket.send(f"TCP Echo: {data.decode()}".encode())
        except Exception as e:
            print(f"TCP Error: {e}")
        finally:
            client_socket.close()
            print(f"TCP Client disconnected: {addr}")

    # UDP Server
    def start_udp_server(self):
        self.udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_server_socket.bind((self.host, self.port))
        print(f"UDP Server started on {self.host}:{self.port}")

        while True:
            data, addr = self.udp_server_socket.recvfrom(1024)
            print(f"UDP Received from {addr}: {data.decode()}")
            self.udp_server_socket.sendto(f"UDP Echo: {data.decode()}".encode(), addr)

    # TCP Client
    def tcp_client(self, message):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((self.host, self.port))
            client_socket.send(message.encode())
            response = client_socket.recv(1024).decode()
            print(f"TCP Server response: {response}")
        except Exception as e:
            print(f"TCP Client error: {e}")
        finally:
            client_socket.close()

    # UDP Client
    def udp_client(self, message):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            client_socket.sendto(message.encode(), (self.host, self.port))
            response, _ = client_socket.recvfrom(1024)
            print(f"UDP Server response: {response.decode()}")
        except Exception as e:
            print(f"UDP Client error: {e}")
        finally:
            client_socket.close()

def main():
    # Initialize protocol manager
    pm = ProtocolManager()

    # Start TCP and UDP servers in separate threads
    tcp_thread = threading.Thread(target=pm.start_tcp_server)
    udp_thread = threading.Thread(target=pm.start_udp_server)
    
    tcp_thread.daemon = True
    udp_thread.daemon = True
    
    tcp_thread.start()
    udp_thread.start()
    
    # Wait for servers to start
    time.sleep(1)

    # Test clients
    try:
        print("\nTesting TCP Client...")
        pm.tcp_client("Hello, TCP Server!")
        
        print("\nTesting UDP Client...")
        pm.udp_client("Hello, UDP Server!")
        
        # Keep the main thread running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        if pm.tcp_server_socket:
            pm.tcp_server_socket.close()
        if pm.udp_server_socket:
            pm.udp_server_socket.close()

if __name__ == "__main__":
    main()