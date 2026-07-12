import socket
import threading
from client_handler import handle_client

class ChatServer:
    def __init__(self, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.clients = {}
        self.server.bind(('0.0.0.0', port))
        self.server.listen(5)
        hostname = socket.gethostname()
        self.ip = socket.gethostbyname(hostname)

    def start(self):
        print(f"Server IP: {self.ip}")
        print(f"Server is listening on port {self.port}...")
        accept_thread = threading.Thread(target=self._accept_connections)
        accept_thread.start()

    def _accept_connections(self):
        while True:
            client_socket, addr = self.server.accept()
            self.clients[client_socket] = None
            print("A new client has connected.")
            thread = threading.Thread(target=handle_client, args=(self, client_socket))
            thread.start()

    def set_username(self, client_socket, username):
        self.clients[client_socket] = username
        print(f"{username} has joined.")

    def remove_client(self, client_socket):
        if client_socket in self.clients:
            username = self.clients[client_socket]
            del self.clients[client_socket]
            client_socket.close()
            if username:
                print(f"{username} has disconnected.")
            else:
                print("A client has disconnected.")

    def broadcast(self, message, sender_socket):
        for client in list(self.clients):
            if client != sender_socket:
                try:
                    client.send(message)
                except socket.error:
                    self.remove_client(client)

    def broadcast_all(self, message):
        for client in list(self.clients):
            try:
                client.send(message)
            except socket.error:
                self.remove_client(client)

    def stop(self):
        for client in list(self.clients):
            client.close()
        self.clients.clear()
        self.server.close()
        print("Server shut down.")
