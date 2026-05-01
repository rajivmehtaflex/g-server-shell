# Modal Deployment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deploy the `g-server-shell` application to Modal with robust pathing.

**Architecture:** Update `modal_app.py` to use `workdir="/root"` and ensure static files are correctly served by the FastAPI backend running in the Modal container.

**Tech Stack:** Modal, FastAPI, uv.

---

### Task 1: Update Modal Configuration

**Files:**
- Modify: `modal_app.py`

- [ ] **Step 1: Update `modal_app.py` with robust configuration**

```python
import modal
import os
import sys

# Define the Modal application
app = modal.App("g-server-shell")

# Configure the image with necessary dependencies and mount the code
image = (
    modal.Image.debian_slim()
    .apt_install("curl")
    .pip_install("fastapi", "uvicorn")
    .add_local_dir(".", remote_path="/root")
)

# Define the persistent service
@app.function(
    image=image, 
    cpu=2.0, 
    memory=4096, 
    container_idle_timeout=300,
    timeout=10800
)
@modal.asgi_app()
def fastapi_app():
    # Ensure current directory is in path so 'main' can be imported
    sys.path.append("/root")
    # Set the working directory to /root so FileResponse("static/index.html") works
    os.chdir("/root")
    # Import the app instance from main.py
    from main import app as fastapi_instance
    return fastapi_instance
```

- [ ] **Step 2: Verify the file content**

Run: `cat modal_app.py`

---

### Task 2: Local Verification

**Files:**
- None

- [ ] **Step 1: Run `modal serve` to test locally**

Run: `uv run modal serve modal_app.py`
*Note: This will output a local URL. The agent should check if the process starts successfully and if there are any immediate errors.*

- [ ] **Step 2: (Manual/Visual) Verify functionality**
*Since I cannot interact with the browser, I will look for "Runner: ready" or similar success logs.*

---

### Task 3: Deployment

**Files:**
- None

- [ ] **Step 1: Run `modal deploy`**

Run: `uv run modal deploy modal_app.py`
Expected: Successful deployment message with a public URL.

- [ ] **Step 2: Capture and report the URL**

---

### Task 4: Commit Changes

- [ ] **Step 1: Commit the updated configuration**

Run:
```bash
git add modal_app.py
git commit -m "feat: robust modal deployment configuration"
```
