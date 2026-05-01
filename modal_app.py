import modal
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Define the Modal application
app = modal.App("g-server-shell")

# Configure the image with necessary dependencies and mount the code
image = (
    modal.Image.debian_slim()
    .apt_install("curl")
    .pip_install("fastapi", "uvicorn", "python-dotenv")
    .add_local_dir(".", remote_path="/root")
)

# Parse resource parameters
cpu = float(os.getenv("MODAL_CPU", "2.0"))
memory = int(os.getenv("MODAL_MEMORY", "4096"))
gpu_count = int(os.getenv("MODAL_GPU_COUNT", "0"))
gpu_model = os.getenv("MODAL_GPU_MODEL", "")
timeout = int(os.getenv("MODAL_TIMEOUT", "10800"))

# Handle GPU configuration
gpu_config = None
if gpu_count > 0:
    if gpu_model:
        gpu_config = f"{gpu_model}:{gpu_count}"
    else:
        gpu_config = str(gpu_count)

# Define the persistent service
@app.function(
    image=image, 
    cpu=cpu, 
    memory=memory, 
    gpu=gpu_config,
    scaledown_window=300,
    timeout=timeout
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
