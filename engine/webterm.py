"""A real terminal in the browser: bridge a PTY-backed shell to the web UI over
a WebSocket. Stdlib only (pty/termios/select + a minimal WebSocket codec).

Protocol
--------
Client -> server: JSON text frames
    {"t":"data","d":"ls -la\n"}          keystrokes / input
    {"t":"resize","cols":120,"rows":30}  window size
Server -> client: binary frames carrying raw PTY output (ANSI and all), which
    xterm.js renders directly.

Security: the shell runs as the user who started the server, and the server
binds to localhost only — this is a single-user local training workstation, by
design. Set CAIC_NO_TERMINAL=1 to disable the feature entirely.
"""
from __future__ import annotations

import base64
import fcntl
import hashlib
import json
import os
import pty
import select
import signal
import struct
import termios

from . import paths

_WS_GUID = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
disabled = os.environ.get("CAIC_NO_TERMINAL") == "1"


def is_upgrade(handler) -> bool:
    return (handler.headers.get("Upgrade", "").lower() == "websocket"
            and "upgrade" in handler.headers.get("Connection", "").lower())


def _handshake(handler) -> bool:
    key = handler.headers.get("Sec-WebSocket-Key")
    if not key:
        return False
    accept = base64.b64encode(hashlib.sha1(key.encode() + _WS_GUID).digest()).decode()
    resp = ("HTTP/1.1 101 Switching Protocols\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Accept: {accept}\r\n\r\n")
    handler.connection.sendall(resp.encode())
    return True


def _recv_exact(sock, n: int) -> bytes:
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("socket closed")
        buf += chunk
    return buf


def _read_frame(sock):
    """Return (opcode, payload) or raise ConnectionError on close."""
    b = _recv_exact(sock, 2)
    opcode = b[0] & 0x0F
    masked = b[1] & 0x80
    length = b[1] & 0x7F
    if length == 126:
        length = struct.unpack(">H", _recv_exact(sock, 2))[0]
    elif length == 127:
        length = struct.unpack(">Q", _recv_exact(sock, 8))[0]
    mask = _recv_exact(sock, 4) if masked else b"\x00\x00\x00\x00"
    data = bytearray(_recv_exact(sock, length))
    if masked:
        for i in range(length):
            data[i] ^= mask[i % 4]
    return opcode, bytes(data)


def _send_frame(sock, payload: bytes, opcode: int = 0x2) -> None:
    header = bytearray([0x80 | opcode])
    n = len(payload)
    if n < 126:
        header.append(n)
    elif n < 65536:
        header.append(126); header += struct.pack(">H", n)
    else:
        header.append(127); header += struct.pack(">Q", n)
    sock.sendall(bytes(header) + payload)


def _set_winsize(fd: int, rows: int, cols: int) -> None:
    try:
        fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))
    except OSError:
        pass


def handle(handler) -> None:
    """Entry point from webapp.do_GET for /ws/terminal."""
    if disabled:
        handler.connection.sendall(b"HTTP/1.1 403 Forbidden\r\n\r\nterminal disabled")
        return
    if not _handshake(handler):
        return
    sock = handler.connection
    handler.close_connection = True

    shell = os.environ.get("SHELL") or "/bin/bash"
    pid, master = pty.fork()
    if pid == 0:  # child: become the shell, rooted in the lab folder
        try:
            os.chdir(str(paths.ROOT))
        except OSError:
            pass
        os.environ["TERM"] = "xterm-256color"
        os.environ.setdefault("PS1", r"\[\e[35m\]caic\[\e[0m\]:\[\e[36m\]\w\[\e[0m\]$ ")
        os.execvp(shell, [shell])
        os._exit(1)

    # parent: bridge master <-> websocket
    try:
        while True:
            r, _, _ = select.select([master, sock], [], [], 60)
            if master in r:
                try:
                    out = os.read(master, 65536)
                except OSError:
                    break
                if not out:
                    break
                _send_frame(sock, out, opcode=0x2)
            if sock in r:
                try:
                    opcode, payload = _read_frame(sock)
                except (ConnectionError, OSError):
                    break
                if opcode == 0x8:          # close
                    break
                if opcode == 0x9:          # ping -> pong
                    _send_frame(sock, payload, opcode=0xA)
                    continue
                if opcode not in (0x1, 0x2):
                    continue
                try:
                    msg = json.loads(payload.decode("utf-8", "replace"))
                except json.JSONDecodeError:
                    continue
                if msg.get("t") == "data":
                    os.write(master, msg.get("d", "").encode("utf-8"))
                elif msg.get("t") == "resize":
                    _set_winsize(master, int(msg.get("rows", 24)), int(msg.get("cols", 80)))
    finally:
        try:
            os.close(master)
        except OSError:
            pass
        try:
            os.kill(pid, signal.SIGKILL)
            os.waitpid(pid, 0)
        except OSError:
            pass
