import socket

def get_username(client_socket):
    try:
        client_socket.send(b"Enter your username: ")
        username = client_socket.recv(1024).decode("utf-8")
        return username
    except socket.error as e:
        print("Error receiving username:", e)
        return None

def handle_client(server, client_socket):
    username = get_username(client_socket)
    if not username:
        client_socket.close()
        return

    server.set_username(client_socket, username)

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            if message == b"exit":
                break
            text = message.decode("utf-8")
            print(f"{username}: {text}")
            server.broadcast(f"{username}: {text}".encode("utf-8"), client_socket)
        except socket.error as e:
            print("Error receiving message:", e)
            break
    server.remove_client(client_socket)
