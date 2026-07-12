# Anonymous Chat Server

A multi-threaded, real-time TCP chat system built with Python sockets. Supports multiple concurrent clients with usernames, message broadcasting, and server-side administration commands.

## Features

- **Multi-client support** — Handle multiple simultaneous connections via threading
- **Username-based identification** — Clients identify themselves on join
- **Real-time broadcasting** — Messages are delivered to all connected clients instantly
- **Server messaging** — Server operators can broadcast announcements
- **Graceful shutdown** — Server notifies all clients before shutting down
- **Anonymized connections** — Client IPs are never disclosed to other users

## Architecture

The project follows a modular client-server architecture:

```
                    ┌─────────────┐
                    │   Client A  │
                    │  (luffy)    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │             │
    ┌───────────────┤   Server    ├───────────────┐
    │               │             │               │
    │               └─────────────┘               │
    │                                             │
┌───▼───────┐                               ┌─────▼─────┐
│  Client B │                               │  Client C │
│  (zoro)   │                               │  (nami)   │
└───────────┘                               └───────────┘
```

### Server modules

| Module | Role |
|--------|------|
| `main.py` | Entry point — starts the server and admin input thread |
| `chat_server.py` | `ChatServer` class — socket setup, client management, broadcasting |
| `client_handler.py` | Username prompt and per-client message handling loop |

## Project Structure

```
anonymous/
├── client/
│   └── client.py          # TCP chat client
├── server/
│   ├── main.py            # Server entry point
│   ├── chat_server.py     # ChatServer class
│   └── client_handler.py  # Per-client handling logic
├── .gitignore
└── README.md
```

## Installation

```bash
# Clone the repository
git clone https://github.com/Utkarsh464/chat-server.git
cd chat-server

# No external dependencies — uses Python standard library only
```

Requires **Python 3.7+**.

## Usage

### Start the server

```bash
cd server
python main.py
```

You will be prompted to enter a port number. The server prints its IP and listens for clients.

**Server commands:**
- Type a message and press Enter — broadcasts `[Server]: <message>` to all clients
- Type `shutdown` — notifies all clients and shuts down the server
- Type `exit` — exits the admin input loop (server continues running)

### Start a client

```bash
cd client
python client.py
```

Enter the server IP and port when prompted, then choose a username. Messages are sent by typing and pressing Enter.

**Client commands:**
- Type `exit` to disconnect

### Demo

```
┌─ Server ───────────────────────────────────┐
│ Enter the port number: 9999                 │
│ Server IP: 192.168.1.10                     │
│ A new client has connected.                 │
│ luffy has joined.                           │
│ A new client has connected.                 │
│ zoro has joined.                            │
│ luffy: hey zoro                             │
│ zoro: hey luffy                             │
│ [Server]: focus on the fight guys           │
│ shutdown                                    │
│ Server shut down.                           │
└─────────────────────────────────────────────┘

┌─ Client (luffy) ───────────────────────────┐
│ Enter server IP: 192.168.1.10               │
│ Enter server port: 9999                     │
│ Enter your username: luffy                  │
│ zoro: hey luffy                             │
│ [Server]: focus on the fight guys           │
│ [Server]: Server is shutting down.          │
│ exit                                        │
└─────────────────────────────────────────────┘
```

## Code Quality Improvements

- **Robust broadcasting** — Disconnected clients are cleaned up during broadcast to prevent broken pipe errors
- **Thread-safe client tracking** — Client dictionary is safely iterated with `list()` copies
- **Daemon threads** — Background threads won't block process exit
- **Graceful shutdown** — All client sockets are closed cleanly on server stop

## Future Improvements

- End-to-end encryption for private messaging
- File sharing and image transfer over sockets
- Persistent chat history with SQLite
- Nickname change and color-coded usernames
- Private messaging (`/msg <user> <message>`)
- Web-based client using WebSockets
- Rate limiting and anti-spam measures

## Technologies Used

- **Python 3** — Core language
- **Socket** — TCP network communication
- **Threading** — Concurrent client handling
- **Git** — Version control

## License

This project is open source and available under the [MIT License](LICENSE).
