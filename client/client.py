import socket
import threading


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = input("Enter the server IP address: ")
    port = int(input("Enter the server port: "))
    client.connect((host, port))

    prompt = client.recv(1024).decode("utf-8")
    print(prompt, end="")
    username = input()
    client.send(username.encode("utf-8"))

    def send_message():
        while True:
            try:
                message = input()
                if message.lower() == "exit":
                    client.send(b"exit")
                    break
                client.send(message.encode("utf-8"))
            except OSError:
                break

    def receive_message():
        while True:
            try:
                response = client.recv(1024).decode("utf-8")
                if not response:
                    break
                print(response)
            except OSError:
                break

    thread = threading.Thread(target=receive_message, daemon=True)
    thread.start()
    send_message()


if __name__ == "__main__":
    main()
