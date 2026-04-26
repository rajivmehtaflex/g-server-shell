# Project: g-server-shell

`g-server-shell` is a web-based remote terminal application. It allows users to interact with a bash shell running on the server directly from their browser, utilizing `xterm.js` for the frontend and a WebSocket-based FastAPI backend that interfaces with a pseudo-terminal (pty).

## Project Overview

- **Purpose:** Provide a web-based terminal interface for server shell access.
- **Backend:** Python with [FastAPI](https://fastapi.tiangolo.com/), using `pty` to bridge shell I/O with WebSockets.
- **Frontend:** HTML5 with [xterm.js](https://xtermjs.org/) for rendering the terminal emulator in the browser.
- **Dependencies:** 
    - `fastapi`
    - `uvicorn`

## Building and Running

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
   Open your browser to the address provided by `uvicorn` (usually `http://127.0.0.1:8000`).

## Development Conventions

- **Formatting:** Keep the backend code idiomatic Python.
- **Safety:** The current implementation provides direct shell access. Ensure appropriate authentication is implemented before exposing this service to any network.
- **Dependencies:** New dependencies should be added to `pyproject.toml` and managed via `uv`.
