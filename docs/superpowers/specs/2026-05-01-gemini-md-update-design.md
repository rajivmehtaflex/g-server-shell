# Spec: GEMINI.md Update for g-server-shell

Update the project's primary documentation (`GEMINI.md`) to reflect current capabilities, including Modal cloud deployment, environment configuration, and technical architecture.

## 1. Project Overview
- **Core Purpose:** Web-based remote terminal providing bash access via browser.
- **Tech Stack:** 
  - Backend: FastAPI, `pty`, `asyncio`.
  - Frontend: `xterm.js`, `FitAddon`.
  - Deployment: Local (Uvicorn) or Cloud (Modal).

## 2. Local Development
- **Setup:** Use `uv` for dependency management.
- **Command:** `uv sync` to install dependencies.
- **Execution:** `uv run uvicorn main:app --reload`.
- **Access:** Defaults to `http://127.0.0.1:8000`.

## 3. Modal Deployment
- **Purpose:** Persistent cloud hosting of the terminal.
- **Setup:** Requires `modal` CLI and account configuration (`modal setup`).
- **Command:** `modal deploy modal_app.py`.
- **Infrastructure:**
  - Debian slim base image.
  - Configurable CPU/Memory/GPU via `.env`.
  - 3-hour default timeout for long-running sessions.

## 4. Technical Architecture
### PTY-WebSocket Bridge
- Server uses `pty.fork()` to create a child process running `/bin/bash`.
- Parent process uses `asyncio.add_reader` to stream PTY output to WebSockets.
- Coalescing logic in `main.py` reduces frame overhead for high-throughput output.

### Terminal Resizing
- **Frontend:** `FitAddon` detects browser window changes.
- **Protocol:** Sends a JSON message `{ "type": "resize", "cols": N, "rows": M }` over WebSocket.
- **Backend:** Uses `fcntl.ioctl` with `termios.TIOCSWINSZ` to update the PTY window size, ensuring command-line interfaces (like `top` or `vim`) render correctly.

## 5. Configuration (`.env`)
The following environment variables are supported for Modal deployment:
- `MODAL_CPU`: Number of CPU cores (default: 2.0).
- `MODAL_MEMORY`: Memory in MB (default: 4096).
- `MODAL_TIMEOUT`: Function timeout in seconds (default: 10800).
- `MODAL_GPU_COUNT`: Number of GPUs to attach.
- `MODAL_GPU_MODEL`: Specific GPU model (e.g., "A10G").

## 6. Development Conventions
- Use `uv` for all dependency changes.
- Keep backend logic in `main.py` and deployment logic in `modal_app.py`.
- Ensure `static/index.html` remains the single-page entry point.
