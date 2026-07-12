import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = input("Enter the server IP address: ")
port = int(input("Enter the server port: "))
client.connect((host, port))

prompt = client.recv(1024).decode('utf-8')
print(prompt, end='')
username = input()
client.send(username.encode('utf-8'))

def send_message():
    while True:
        message = input()
        if message.lower() == 'exit':
            client.send(b"exit")
            break
        client.send(message.encode('utf-8'))

def receive_message():
    while True:
        try:
            response = client.recv(1024).decode('utf-8')
            if not response:
                break
            print(response)
        except socket.error as e:
            print("Error receiving message:", e)
            break

thread = threading.Thread(target=receive_message, daemon=True)
thread.start()
send_message() 
