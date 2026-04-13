from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import pty
import subprocess
import asyncio

app = FastAPI()

@app.get("/")
async def get_index():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.websocket("/ws")
async def terminal_websocket(websocket: WebSocket):
    await websocket.accept()
    
    # Fork a child process attached to a pty
    (child_pid, fd) = pty.fork()

    if child_pid == 0:
        # Child process: replace with bash
        # Set some environment variables for terminal compatibility
        env = os.environ.copy()
        env["TERM"] = "xterm-256color"
        os.execvpe("/bin/bash", ["/bin/bash"], env)
    else:
        # Parent process: handle I/O
        loop = asyncio.get_event_loop()

        def read_from_pty():
            try:
                data = os.read(fd, 1024)
                if data:
                    asyncio.run_coroutine_threadsafe(
                        websocket.send_bytes(data), loop
                    )
            except (IOError, OSError):
                # Handle PTY closed
                pass

        loop.add_reader(fd, read_from_pty)

        try:
            while True:
                data = await websocket.receive_bytes()
                os.write(fd, data)
        except Exception:
            # Connection closed or error
            pass
        finally:
            loop.remove_reader(fd)
            os.close(fd)
            # Ensure child process is terminated
            try:
                os.kill(child_pid, 9)
            except OSError:
                pass
