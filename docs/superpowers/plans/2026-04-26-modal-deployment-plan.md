# Deploy to Modal Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Configure and deploy the `g-server-shell` application as a persistent service on Modal using `uv` for dependency management.

**Architecture:** A new `modal_app.py` file will wrap the existing FastAPI application, configured with specific CPU and memory requirements and set to run as a persistent Modal service.

**Tech Stack:** Modal, FastAPI, uv.

---

### Task 1: Setup Modal Environment

**Files:**
- None (Environment setup)

- [ ] **Step 1: Install Modal**

Run: `uv pip install modal`

- [ ] **Step 2: Authenticate with Modal**

Run: `uv run modal setup`
*Follow the browser prompts to complete authentication.*

---

### Task 2: Create Modal Configuration

**Files:**
- Create: `modal_app.py`

- [ ] **Step 1: Create `modal_app.py`**

```python
import modal
import os

# Define the Modal application
app = modal.App("g-server-shell")

# Configure the image with necessary dependencies
image = modal.Image.debian_slim().pip_install("fastapi", "uvicorn")

# Define the persistent service
@app.function(
    image=image, 
    cpu=2.0, 
    memory=4096, 
    container_idle_timeout=300
)
@modal.asgi_app()
def fastapi_app():
    # Import the app instance from main.py
    from main import app as fastapi_instance
    return fastapi_instance
```

---

### Task 3: Test and Deploy

**Files:**
- Modify: `modal_app.py` (if needed)

- [ ] **Step 1: Test locally with `modal serve`**

Run: `uv run modal serve modal_app.py`
*Verify the app runs correctly at the provided local URL.*

- [ ] **Step 2: Deploy to Modal**

Run: `uv run modal deploy modal_app.py`
*Verify the deployment is successful and the app is active in your Modal dashboard.*

---

### Task 4: Commit Changes

- [ ] **Step 1: Commit the new configuration**

Run:
```bash
git add modal_app.py
git commit -m "chore: add modal deployment configuration"
```
