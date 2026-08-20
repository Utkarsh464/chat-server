# Anonymous Chat Server

<div align="center">

[![Python 3.7+](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![Build & Run](https://img.shields.io/badge/build%20%26%20run-python%203.7%2B-brightgreen)](<>)
[![Tests](https://img.shields.io/badge/tests-none%20yet-lightgrey)](<>)
[![Status](https://img.shields.io/badge/status-learning%20project-yellow)](<>)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Utkarsh464/chat-server?style=social)](<>)
[![Last Commit](https://img.shields.io/github/last-commit/Utkarsh464/chat-server)](<>)

</div>

A multi-threaded TCP chat server built from scratch with Python's standard library. Supports concurrent clients, named message broadcasting, and a server-side input loop for broadcasting messages and shutting down the server.

---

## Background — What I Set Out to Learn

I built this to understand TCP networking and concurrency below the abstraction layer of web frameworks: the sockets API (`bind`, `listen`, `accept`, `send`, `recv`, and the TCP state machine), thread-per-connection design with shared mutable state, and the GIL's real-world impact on I/O-bound workloads.
---

## Architecture

The server uses a **thread-per-client** model. One acceptor thread blocks on `socket.accept()` and spawns a `ClientHandler` thread per connection. Each handler runs an independent receive loop; messages fan out through a shared `clients` dict (username → socket).

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
                            │    Client A     │     │    Client B     │
                            │   (ephemeral)   │     │   (ephemeral)   │
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
    │◄─── "Alice" ──────────── │                               │
    │                          │── "Alice has joined." ──────► │
    │                          │                               │
    │──── "hello everyone" ──► │                               │
    │                          │── "Alice: hello everyone" ──► │
    │◄── "Bob: hey Alice" ──── │◄─── "Bob: hey Alice" ─────── │
    │                          │                               │
    │──── FIN ────────────────►│                               │
    │                          │── "Alice has disconnected." ► │
```

### Design Decisions

**Non-daemon threads, terminated via `os._exit()`** — Handler and acceptor threads are created without `daemon=True`, so the process stays alive as long as `accept()` blocks or any client handler is running. Shutdown therefore relies on `os._exit(0)` in `main.py`, which kills every thread immediately — no join tracking. In-flight `send()` calls may be interrupted without recovery.
**Safe dict iteration with `list()` copy** — The broadcast loop iterates over `list(self.clients)` rather than the dict directly. Without this intermediate copy, a mid-broadcast disconnect that removes an entry from `clients` raises `RuntimeError: dictionary changed size during iteration`.
**`os._exit()` for shutdown** — `sys.exit()` raises `SystemExit`, which a bare `except:` anywhere in the thread pool would catch and suppress. `os._exit()` terminates the process immediately, file descriptors and all. A cooperative `threading.Event`-based approach would be cleaner but was deferred.
**Binding to `0.0.0.0`** — The server listens on all interfaces so LAN clients connect without configuration. A production deployment would bind to a specific interface; for a learning project, `0.0.0.0` is the pragmatic default.
**Cleanup on disconnect** — When `recv()` returns empty bytes (FIN from peer), the handler removes its entry from `clients` and broadcasts a disconnect notification. The socket is closed via `socket.close()` to release the fd.
---

## Problems Encountered

**Broken pipe during broadcast** — Writing to a socket whose peer has already sent FIN raises `BrokenPipeError` (SIGPIPE on UNIX). The broadcast loop now catches `OSError` (parent class of both `BrokenPipeError` and `ConnectionResetError`) per-client, removes the dead entry, and continues. Without this, one abrupt disconnect crashed the entire server.
**Stale client entries after handler crash** — Cleanup depends on `remove_client()` being reached after the receive loop exits normally. There is no `try/finally`: if `recv()` or `broadcast()` raises anything other than `socket.error`, the handler exits without removing its entry and later broadcasts fail silently on that socket. Known limitation — the handler could be hardened with a `try/finally`.
**Blocking `accept()` on shutdown** — After the shutdown command, the acceptor thread blocks on `accept()` forever. The fix: close the server socket so `accept()` raises `OSError`, which the loop interprets as the signal to exit.
---

## What I'd Do Differently

- **Test suite** — Zero tests. A `pytest` suite with loopback socket tests would make refactoring safe.
- **Structured logging** — Replace `print` with `logging` (INFO for joins, DEBUG for raw bytes, ERROR for failures).
- **Package with `pyproject.toml`** — Define entry points so `pip install -e .` works.
- **Cooperative shutdown** — Use `threading.Event` to drain work before exit instead of daemon-thread semantics.
- **Rate limiting** — No back-pressure mechanism; a malicious client could flood the broadcast loop.

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
├── .gitignore
├── LICENSE
└── README.md
```

---

## Installation & Usage

```bash
git clone https://github.com/Utkarsh464/chat-server.git && cd chat-server
```

No external dependencies — pure Python standard library (3.7+).

### Server

```bash
cd server && python main.py
```

The server operator types commands in the terminal — there are no roles or privileges; the input loop runs in the main thread and directly controls the server.

| Command        | Effect                                          |
| -------------- | ----------------------------------------------- |
| `text message` | Broadcasts `[Server]: <message>` to all clients |
| `shutdown`     | Notifies all clients and stops the server       |
| `exit`         | Exits the input loop (server keeps running)     |

### Client

```bash
cd client && python client.py
```

| Command    | Effect                               |
| ---------- | ------------------------------------ |
| `any text` | Sends message to all connected users |
| `exit`     | Disconnects from server              |

---

## Demo

### Server Terminal

```
Enter the port number for the chat server: 9999
Server IP: &lt;server-ip&gt;
Server is listening on port 9999...
A new client has connected.
Alice has joined.
A new client has connected.
Bob has joined.
Bob: hi ..anyone here?
Alice: hey Bob! I was waiting for you
[Server]: focus on the fight guys
shutdown
Server shut down.
```

### Client (Alice) Terminal

```
Enter the server IP address: &lt;server-ip&gt;
Enter the server port: 9999
Enter your username: Alice
Bob: hi ..anyone here?
hey Bob! I was waiting for you
[Server]: focus on the fight guys
[Server]: Server is shutting down.
```

---

## Roadmap

- End-to-end encryption for private messaging
- SQLite-backed persistent chat history
- File sharing and image transfer
- Private messaging (`/msg <user> <message>`)
- Nickname changes and color-coded usernames
- Web-based client using WebSockets
- Rate limiting and anti-spam measures
- Docker containerization
- CI/CD pipeline with GitHub Actions

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Known Limitations

- No real authentication — usernames are free-text selection, not verified identity.
- Plaintext TCP (no TLS) — all traffic is unencrypted.
- No message framing — the TCP stream can split or merge messages across reads.
- Shared client state is not protected by a lock — race conditions under concurrent load.
- Usernames can be spoofed via newline injection.
