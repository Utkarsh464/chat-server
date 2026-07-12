<p align="center">
  <h1 align="center">Anonymous Chat Server</h1>
  <p align="center">
    <a href="https://www.python.org/downloads/">
      <img src="https://img.shields.io/badge/python-3.7%2B-blue" alt="Python 3.7+">
    </a>
    <a href="https://github.com/Utkarsh464/chat-server/blob/main/LICENSE">
      <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License">
    </a>
    <a href="https://github.com/Utkarsh464/chat-server">
      <img src="https://img.shields.io/github/stars/Utkarsh464/chat-server?style=social" alt="GitHub Stars">
    </a>
    <a href="https://github.com/Utkarsh464/chat-server/commits/main">
      <img src="https://img.shields.io/github/last-commit/Utkarsh464/chat-server" alt="Last Commit">
    </a>
  </p>
  <p align="center">
    A multi-threaded, real-time TCP chat server built with Python sockets.<br>
    Supports multiple concurrent clients, usernames, message broadcasting, and admin controls.
  </p>
</p>

---

## Features

- [x] **Multi-client support** — Handle unlimited simultaneous connections via threading
- [x] **Username identification** — Each client identifies with a unique name on join
- [x] **Real-time broadcasting** — Messages delivered to all connected clients instantly
- [x] **Server announcements** — Server operator can broadcast messages
- [x] **Graceful shutdown** — Server notifies all clients before stopping
- [x] **Anonymized connections** — Client IP addresses are never exposed
- [x] **Admin commands** — `/shutdown` and `/exit` controls from the server terminal
- [x] **Disconnect resilience** — Dropped clients are cleaned up without crashing the server

---

## Networking Architecture

```
                        ┌─────────────────────────────────────────────────┐
                        │                  SERVER (:9999)                  │
                        │                                                  │
                        │   ┌─────────────────────────────────────────┐   │
                        │   │         ChatServer Class                │   │
                        │   │  ┌─────────┐  ┌──────────┐  ┌───────┐  │   │
                        │   │  │ Accept  │  │Broadcast │  │Client │  │   │
                        │   │  │ Thread  │  │  Engine  │  │  Map  │  │   │
                        │   │  └────┬────┘  └────┬─────┘  └───┬───┘  │   │
                        │   └───────┼─────────────┼────────────┼──────┘   │
                        └───────────┼─────────────┼────────────┼──────────┘
                                    │             │            │
            ┌───────────────────────┼─────────────┼────────────┼───────────────────┐
            │              TCP Connection Pool     │            │                   │
            │                       │             │            │                   │
            │  ┌────────────────────┴──────┐  ┌───┴────────────┴──────┐            │
            │  │  Client Handler Thread 1  │  │  Client Handler Thd 2 │   ...      │
            │  │  ┌──────────────────────┐│  │  ┌──────────────────┐  │            │
            │  │  │ get_username()       ││  │  │ get_username()   │  │            │
            │  │  │ message loop         ││  │  │ message loop     │  │            │
            │  │  └──────────────────────┘│  │  └──────────────────┘  │            │
            │  └──────────────────────────┘  └────────────────────────┘            │
            └──────────────────────────────────────────────────────────────────────┘
                                    │                         │
                                    ▼                         ▼
                          ┌─────────────────┐     ┌─────────────────┐
                          │   Client A      │     │   Client B      │
                          │   (luffy)       │     │   (zoro)        │
                          │   :9999         │     │   :9999         │
                          └─────────────────┘     └─────────────────┘
```

### Data Flow

```
 Client A                    Server                         Client B
    │                          │                               │
    │──── SYN ───────────────► │                               │
    │◄─── SYN-ACK ──────────── │                               │
    │──── ACK ────────────────►│                               │
    │                          │                               │
    │──── "Enter your ───────► │                               │
    │     username:"           │                               │
    │◄─── "luffy" ──────────── │                               │
    │                          │── "luffy has joined." ──────► │
    │                          │                               │
    │──── "hello everyone" ──► │                               │
    │                          │── "luffy: hello everyone" ──► │
    │◄── "zoro: hey luffy" ─── │◄─── "zoro: hey luffy" ────── │
    │                          │                               │
    │──── FIN ────────────────►│                               │
    │                          │── "luffy has disconnected." ► │
```

---

## Project Structure

```
chat-server/
├── client/
│   └── client.py                # TCP chat client
├── server/
│   ├── __init__.py
│   ├── main.py                  # Server entry point
│   ├── chat_server.py           # ChatServer class
│   └── client_handler.py        # Per-client handling logic
├── screenshots/
│   ├── server_shutdown.png      # Server terminal demo
│   ├── luffy_client_chat.png    # Client A (luffy) demo
│   └── fresh_terminal.png       # Client B (zoro) terminal
├── .gitignore
├── LICENSE
└── README.md
```

---

## Installation

```bash
git clone https://github.com/Utkarsh464/chat-server.git
cd chat-server

# No external dependencies — pure Python standard library
```

Requires **Python 3.7+**.

---

## Usage

### 1. Start the server

```bash
cd server
python main.py
```

You will be prompted for a port number. The server displays its IP and waits for clients.

**Server commands:**
| Command | Effect |
|---------|--------|
| `text message` | Broadcasts `[Server]: <message>` to all clients |
| `shutdown` | Notifies all clients and stops the server |
| `exit` | Exits the admin input loop (server keeps running) |

### 2. Connect a client

```bash
cd client
python client.py
```

Enter the server IP and port, then choose a username. Type messages and press Enter to send.

**Client commands:**
| Command | Effect |
|---------|--------|
| `any text` | Sends message to all connected users |
| `exit` | Disconnects from server |

---

## Demo

### Server Terminal

```
Enter the port number for the chat server: 9999
Server IP: 192.168.29.176
Server is listening on port 9999...
A new client has connected.
luffy has joined.
A new client has connected.
zoro has joined.
zoro: hi ..anyone here?
luffy: hi zoro i was waiting for you
[Server]: focus on the fight guys
shutdown
Server shut down.
```

### Client (luffy) Terminal

```
Enter the server IP address: 192.168.29.176
Enter the server port: 9999
Enter your username: luffy
zoro: hi ..anyone here?
hi zoro i was waiting for you
[Server]: focus on the fight guys
[Server]: Server is shutting down.
```

> **Note:** An empty `server/__init__.py` has been added so the server package can be cleanly imported in a development context. It is not required for running the application.

---

## Code Quality

- **Robust broadcasting** — Disconnected clients are cleaned up during broadcast to prevent broken pipe errors
- **Thread-safe client tracking** — Client dictionary is safely iterated with `list()` copies
- **Daemon threads** — Background threads won't block process exit
- **Graceful shutdown** — All sockets are closed cleanly on server stop; `accept()` loop breaks on closed socket
- **PEP 8 compliant** — snake_case naming, proper spacing, organized imports

---

## Roadmap

- [ ] End-to-end encryption for private messaging
- [ ] SQLite-backed persistent chat history
- [ ] File sharing and image transfer
- [ ] Private messaging (`/msg <user> <message>`)
- [ ] Nickname changes and color-coded usernames
- [ ] Web-based client using WebSockets
- [ ] Rate limiting and anti-spam measures
- [ ] Docker containerization
- [ ] CI/CD pipeline with GitHub Actions

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3** | Core programming language |
| **Socket** | TCP/IP network communication |
| **Threading** | Concurrent client connection handling |
| **Git** | Version control and collaboration |

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

<p align="center">
  Built with Python &bull; Made for learning
</p>
