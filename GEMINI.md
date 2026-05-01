# Project: g-server-shell

`g-server-shell` is a web-based remote terminal application. It provides a bash shell interface directly in your browser, supporting both local execution and persistent cloud deployment via Modal.

## Project Overview

- **Purpose:** Secure, browser-based shell access for remote server management.
- **Backend:** FastAPI (Python) using `pty` to bridge shell I/O with WebSockets.
- **Frontend:** HTML5 with [xterm.js](https://xtermjs.org/) and `FitAddon` for a responsive terminal experience.
- **Deployment:** Supports local execution and [Modal](https://modal.com) cloud deployment.

## Getting Started (Local)

This project uses `uv` for dependency management.

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Run the server:**
   ```bash
   uv run uvicorn main:app --reload
   ```

3. **Access the terminal:**
   Open `http://127.0.0.1:8000` in your browser.

## Modal Deployment

Deploy your terminal to the cloud for persistent access.

1. **Setup Modal:**
   Install the Modal CLI and authenticate:
   ```bash
   pip install modal
   modal setup
   ```

2. **Deploy:**
   ```bash
   modal deploy modal_app.py
   ```

3. **Cloud Infrastructure:**
   - Base Image: Debian Slim with `curl`.
   - Default Resources: 2.0 CPU, 4GB Memory.
   - Session Timeout: 3 hours (configurable).

## Technical Architecture

### PTY-WebSocket Bridge
The backend uses `pty.fork()` to create a child process running `/bin/bash`. The parent process manages an asynchronous I/O loop:
- **PTY to WebSocket:** Reads from the PTY file descriptor and streams data to the client. Coalescing logic is used to group small chunks and reduce frame overhead.
- **WebSocket to PTY:** Receives input from the client and writes it directly to the PTY.

### Terminal Resizing
Responsive resizing is handled via a JSON protocol:
1. The frontend `FitAddon` detects window size changes.
2. A message `{ "type": "resize", "cols": N, "rows": M }` is sent via WebSocket.
3. The backend uses `fcntl.ioctl` with `termios.TIOCSWINSZ` to update the PTY window size, ensuring CLI tools like `vim` or `htop` render correctly.

## Configuration (.env)

Customize your Modal deployment using a `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `MODAL_CPU` | Number of CPU cores | 2.0 |
| `MODAL_MEMORY` | Memory in MB | 4096 |
| `MODAL_TIMEOUT` | Function timeout (seconds) | 10800 |
| `MODAL_GPU_COUNT` | Number of GPUs to attach | 0 |
| `MODAL_GPU_MODEL` | GPU model (e.g., "A10G") | "" |

## Development Conventions

- **Dependencies:** Add new dependencies via `uv`.
- **Files:**
  - `main.py`: Core FastAPI and PTY logic.
  - `modal_app.py`: Modal-specific configuration and deployment.
  - `static/index.html`: Frontend terminal implementation.
- **Safety:** Ensure appropriate authentication is added before exposing the service to public networks.
