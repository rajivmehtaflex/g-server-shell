# g-server-shell

> **GPU-powered web-based remote terminal with smart deployment and GPU availability pre-check**

A web-based terminal application that provides a full bash shell interface in your browser, with support for GPU acceleration and intelligent deployment to Modal cloud infrastructure.

## 🚀 Features

- **Web-based Terminal**: Full bash shell in your browser using xterm.js
- **WebSocket PTY Bridge**: Real-time bidirectional communication
- **GPU Support**: Deploy with L4, A10, T4, A100, H100, H200, or B200 GPUs
- **Smart Deployment**: Automatic GPU availability pre-check before deployment
- **Optimized Bundle**: 88% smaller deployment (32KB vs 276KB)
- **Fast Deploy**: Sub-minute cold starts with optimized image and mount filtering
- **Auto-resize**: Responsive terminal resizing support
- **Configuration**: Flexible resource configuration via environment variables

## 📋 Prerequisites

- Python >= 3.12
- [uv](https://github.com/astral-sh/uv) package manager
- [Modal](https://modal.com/) account and CLI

## 🔧 Installation

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/rajivmehtaflex/g-server-shell.git
cd g-server-shell
uv sync
```

### 2. Configure Modal (First Time)

```bash
.venv/bin/modal setup
```

### 3. Configure Deployment (`.env`)

```bash
# Auth handled by ~/.modal.toml (modal setup)
AUTH_TOKEN=your_auth_token_here

# Resource Configuration
MODAL_CPU=8.0                # CPU cores (default: 2.0)
MODAL_MEMORY=16384           # Memory in MB (default: 4096)
MODAL_TIMEOUT=21600          # Timeout in seconds (default: 10800)
MODAL_GPU_COUNT=1            # Number of GPUs (default: 0)
MODAL_GPU_MODEL="A10"        # GPU model: T4, L4, A10, A100, H100, H200, B200
```

## 🎯 Quick Start

### Option 1: Smart Deployment (Recommended)

Uses automatic GPU availability pre-check to ensure deployment succeeds:

```bash
./deploy.sh
```

**What happens:**
1. ✅ Validates configuration
2. 🔍 Checks GPU availability (2-3 min)
3. 📦 Deploys only if GPU is found
4. 💡 Suggests alternatives if unavailable

### Option 2: Skip Pre-Check

If you know the GPU is available:

```bash
./deploy.sh --skip-check
```

### Option 3: Manual Deployment

```bash
.venv/bin/modal deploy modal_app.py
```

## 🔍 GPU Availability Check

Check if a GPU is available before deploying:

```bash
.venv/bin/python check_gpu.py
```

**Output:**
```
============================================================
🚀 Modal GPU Availability Checker
============================================================

🔍 Checking A10 GPU availability on Modal...
------------------------------------------------------------
⏱️  Attempting to allocate A10 GPU...
⏱️  Allocation time: 127.3 seconds
📊 Result: ✅ GPU available: NVIDIA A10G
------------------------------------------------------------
🎉 A10 GPU is available for deployment!
```

## 🏃 Local Development

Run the terminal locally without GPU:

```bash
uv run uvicorn main:app --reload
```

Access at: `http://127.0.0.1:8000`

## 🌐 Accessing Deployed Terminal

After deployment, access your terminal at:

```
https://<workspace>--g-gpu-proc-fastapi-app.modal.run
```

The URL will be displayed in the deployment output.

## 💻 Usage

### Verify GPU Access

Open the terminal URL and run:

```bash
nvidia-smi
```

Expected output:
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.xx.xx    Driver Version: 535.xx.xx    CUDA Version: 12.2   |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  NVIDIA A10G          On   | 00000000:00:04.0 Off |                    0 |
| N/A   34C    P8    20W / 300W |      3MiB /  24000MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
```

### Run Inference

```bash
# Example with a model
pip install torch
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

## ⚡ Optimizations

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Bundle Size** | 276 KB | 32 KB | 88% reduction |
| **Deploy Time (A10)** | N/A | 3.5s | Ultra-fast |
| **Cold Start (L4)** | 3-5 min | 2-4 min | ~1-2 min faster |
| **Mount Upload** | 5-10s | 2-3s | ~5s faster |

## 🎮 GPU Options

| GPU | VRAM | Availability | Deploy Time | Price/Hour | Best For |
|-----|------|--------------|-------------|------------|----------|
| **T4** | 16 GB | ⭐⭐⭐⭐⭐ | 30-60s | $0.59 | Light inference |
| **L4** | 24 GB | ⭐⭐⭐ | 1-3 min | $0.80 | Mid-tier inference |
| **A10** | 24 GB | ⭐⭐⭐ | 1-2 min | $1.10 | Balanced performance |
| **L40S** | 48 GB | ⭐⭐ | 2-5 min | $1.95 | High-end inference |
| **A100** | 40/80 GB | ⭐⭐ | 2-4 min | $2.50/3.00 | Large models |
| **H100** | 80 GB | ⭐ | 3-10 min | $3.95 | Training |
| **B200** | — | ⭐ | 5-15 min | $6.25 | Cutting-edge |

## 📁 Project Structure

```
g-server-shell/
├── main.py              # FastAPI application (PTY-WebSocket bridge)
├── modal_app.py         # Modal deployment configuration
├── check_gpu.py         # GPU availability checker
├── deploy.sh            # Smart deployment script
├── .env                 # Configuration (create from .env.example)
├── .env.example         # Configuration template
├── .gitignore           # Git ignore rules
├── pyproject.toml       # Python dependencies
├── uv.lock              # Dependency lock file
├── README.md            # This file
├── GPU_PRECHECK.md      # GPU pre-check documentation
└── static/
    └── index.html       # Frontend (xterm.js terminal)
```

## 🛠️ Architecture

### PTY-WebSocket Bridge (`main.py`)

1. `pty.fork()` creates child process running `/bin/bash`
2. Parent uses `asyncio` to monitor PTY file descriptor
3. PTY output → WebSocket (binary, coalesced)
4. WebSocket input → PTY (keystrokes)
5. Text JSON messages handle terminal resize

### Frontend (`static/index.html`)

- xterm.js with dark theme
- FitAddon for responsive resizing
- Binary WebSocket mode for efficiency

### Modal Deployment (`modal_app.py`)

- Debian Slim base image with dependencies
- Local project mounted to `/root`
- Configurable CPU, memory, GPU, timeout via `.env`
- Mount filtering for minimal bundle size

## 🔧 Configuration Reference

### Environment Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MODAL_CPU` | float | 2.0 | CPU cores |
| `MODAL_MEMORY` | int | 4096 | Memory in MB |
| `MODAL_TIMEOUT` | int | 10800 | Function timeout (seconds) |
| `MODAL_GPU_COUNT` | int | 0 | Number of GPUs |
| `MODAL_GPU_MODEL` | string | "" | GPU model (T4, L4, A10, A100, H100, H200, B200) |
| `AUTH_TOKEN` | string | — | Authentication token |

### Recommended Configurations

| Use Case | CPU | RAM | GPU | Timeout |
|----------|-----|-----|-----|---------|
| **Inference** | 8.0 | 16384 | A10 | 21600 (6h) |
| **Training** | 16.0 | 65536 | H100 | 43200 (12h) |
| **Testing** | 4.0 | 8192 | T4 | 3600 (1h) |

## 📊 Monitoring

### Check Deployment Status

```bash
modal app list
```

### View Logs

```bash
modal app logs g-gpu-proc
```

### Stop Deployment

```bash
modal app stop g-gpu-proc --yes
```

## 🐛 Troubleshooting

### GPU Allocation Timeout

**Symptom:** Deployment stuck in "initializing" or timeout after 5+ minutes

**Solution:**
```bash
# Check GPU availability first
.venv/bin/python check_gpu.py

# If unavailable, try a different GPU
sed -i '' 's/MODAL_GPU_MODEL="L4"/MODAL_GPU_MODEL="T4"/' .env
./deploy.sh
```

### WebSocket Disconnect

**Symptom:** Terminal disconnects frequently

**Solution:**
- Check logs: `modal app logs g-gpu-proc`
- Verify timeout is sufficient (increase `MODAL_TIMEOUT`)
- Check network stability

### Deployment Fails

**Symptom:** Deployment error after GPU check passes

**Solution:**
```bash
# Check logs for specific error
modal app logs g-gpu-proc

# Verify .env configuration
cat .env

# Try skipping pre-check
./deploy.sh --skip-check
```

## 📚 Additional Documentation

- [GPU Pre-Check Documentation](GPU_PRECHECK.md) - Detailed GPU availability workflow
- [GEMINI.md](GEMINI.md) - Original project overview
- [QWEN.md](QWEN.md) - Alternative project documentation

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- [Modal](https://modal.com/) - Cloud infrastructure platform
- [xterm.js](https://xtermjs.org/) - Terminal emulator library
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [uv](https://github.com/astral-sh/uv) - Python package manager

## 📞 Support

- Issues: [GitHub Issues](https://github.com/rajivmehtaflex/g-server-shell/issues)
- Documentation: [Modal Docs](https://modal.com/docs)
- Community: [Modal Discord](https://modal.com/discord)

---

**Deployed with A10 GPU in 3.5 seconds ⚡**