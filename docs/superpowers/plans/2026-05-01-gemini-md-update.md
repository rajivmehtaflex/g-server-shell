# GEMINI.md Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `GEMINI.md` to provide a comprehensive guide for local development and Modal cloud deployment, including technical architecture and configuration details.

**Architecture:** Following the "Comprehensive Guide" approach, structuring the document into sections: Overview, Local Dev, Modal Deployment, Architecture, and Configuration.

**Tech Stack:** Markdown, FastAPI, Modal, xterm.js.

---

### Task 1: Draft the Updated GEMINI.md

**Files:**
- Modify: `GEMINI.md`

- [ ] **Step 1: Replace content with the new comprehensive guide**

Replace the entire content of `GEMINI.md` with:

```markdown
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
```

- [ ] **Step 2: Verify the file content**

Run: `cat GEMINI.md`
Expected: Content matches the draft above.

- [ ] **Step 3: Commit the update**

Run: `git add GEMINI.md && git commit -m "docs: update GEMINI.md with comprehensive guide and modal support"`
Expected: Commit successful.

---

### Task 2: Final Verification

- [ ] **Step 1: Check link and command validity**

Manually verify that the `modal` and `uv` commands mentioned in the docs are consistent with the project's `pyproject.toml` and existing scripts.

- [ ] **Step 2: Wrap up**

The task is documentation-only, so no functional tests are required beyond verification of content accuracy.
```bash
git status
```
