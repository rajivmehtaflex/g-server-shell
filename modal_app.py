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
    scaledown_window=300
)
@modal.asgi_app()
def fastapi_app():
    # Import the app instance from main.py
    from main import app as fastapi_instance
    return fastapi_instance
