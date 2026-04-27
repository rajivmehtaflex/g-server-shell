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
    scaledown_window=300,
    timeout=10800
)
@modal.asgi_app()
def fastapi_app():
    # Ensure current directory is in path so 'main' can be imported
    sys.path.append("/root")
    # Import the app instance from main.py
    from main import app as fastapi_instance
    return fastapi_instance

