import os
import threading
from chat_server import ChatServer

port = int(input("Enter the port number for the chat server: "))
try:
    server = ChatServer(port)
    server.start()
except OSError as e:
    print("Error binding to port:", e)
    exit(1)

def server_input():
    while True:
        msg = input()
        if msg.lower() == 'shutdown':
            server.broadcast_all("[Server]: Server is shutting down.".encode("utf-8"))
            server.stop()
            os._exit(0)
        elif msg.lower() == 'exit':
            break
        server.broadcast_all(f"[Server]: {msg}".encode("utf-8"))

thread = threading.Thread(target=server_input, daemon=True)
thread.start()
