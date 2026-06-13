# GPU Pre-Check Deployment Workflow

## Overview

This deployment system includes a **GPU availability pre-check** to prevent wasting time deploying when GPUs are unavailable. The workflow:

1. **Check GPU availability** (2-3 min) → Only proceed if GPU is found
2. **Deploy** (3-5 min) → Full deployment with confirmed resources

## Files Added

| File | Purpose |
|------|---------|
| `check_gpu.py` | Tests GPU availability on Modal before deployment |
| `deploy.sh` | Smart deployment script that runs pre-check automatically |

## How It Works

### check_gpu.py

```python
# Checks if GPU is available by allocating a test container
python check_gpu.py
```

**Features:**
- Tests actual GPU allocation (not just API availability)
- Measures allocation time
- Suggests alternative GPUs if unavailable
- Returns exit code 1 if GPU check fails

### deploy.sh

```bash
# Smart deployment with pre-check
./deploy.sh

# Skip pre-check (for emergencies)
./deploy.sh --skip-check
```

**Workflow:**
1. ✅ Validates `.env` configuration
2. 🔍 Runs `check_gpu.py` (unless `--skip-check`)
3. 📦 Deploys to Modal only if GPU is available
4. 📊 Provides clear status messages

## Usage Examples

### Normal Deployment (With Pre-Check)

```bash
cd /Users/rajivmehtapy/Documents/Dev/g-server-shell
./deploy.sh
```

**Output:**
```
============================================================
🚀 Smart Deployment with GPU Pre-Check
============================================================

📋 Step 1: Checking configuration...
   GPU Model: L4
   CPU: 8.0 cores
   Memory: 16384 MB

🔍 Step 2: Checking GPU availability on Modal...
   (This may take 2-3 minutes)

============================================================
🚀 Modal GPU Availability Checker
============================================================

🔍 Checking L4 GPU availability on Modal...
------------------------------------------------------------
⏱️  Attempting to allocate L4 GPU...
   (This may take 1-3 minutes if GPU is available)
   Timeout set to 300 seconds

⏱️  Allocation time: 127.3 seconds
📊 Result: ✅ GPU available: NVIDIA L4
------------------------------------------------------------
🎉 L4 GPU is available for deployment!

✅ GPU availability check passed

📦 Step 3: Deploying to Modal...

✓ Created objects.
...
✓ App deployed in 30.869s! 🎉
```

### Skip Pre-Check (If GPU is Known to be Available)

```bash
./deploy.sh --skip-check
```

### Check GPU Availability Only

```bash
/Users/rajivmehtapy/Documents/Dev/g-server-shell/.venv/bin/python check_gpu.py
```

## Benefits

| Before | After |
|--------|-------|
| Build image → Wait 10 min → **GPU unavailable** → Fail | Check GPU (2 min) → **Skip if unavailable** → Save 8 min |
| No feedback on why deployment fails | Clear GPU unavailability message |
| Try different GPUs manually | Automatic alternative suggestions |
| Wasted compute time | Smart pre-decision making |

## Configuration

The script reads from `.env`:

```bash
MODAL_GPU_MODEL="L4"     # GPU to check
MODAL_CPU=8.0            # CPU cores (for display only)
MODAL_MEMORY=16384       # RAM in MB (for display only)
```

## GPU Availability Tiers

| GPU | Typical Availability | Check Time | Recommended Use |
|-----|---------------------|------------|-----------------|
| **T4** | ⭐⭐⭐⭐⭐ | 30-60s | Inference, light training |
| **L4** | ⭐⭐⭐ | 1-3 min | Inference (24GB VRAM) |
| **A10** | ⭐⭐⭐ | 1-2 min | Mid-tier workloads |
| **L40S** | ⭐⭐ | 2-5 min | High-end inference |
| **H100** | ⭐ | 3-10 min | Large training |
| **B200** | ⭐ | 5-15 min | Cutting-edge |

## Error Handling

### GPU Unavailable

If GPU check fails, you'll see:

```
❌ TIMEOUT: L4 GPU not available within 300 seconds
💡 Suggestion: Try a different GPU model (T4, A10, A100)

💡 Alternatives to try:
   1. T4 GPU
   2. A10 GPU
   3. L4 GPU

📝 To use an alternative GPU, update your .env:
   MODAL_GPU_MODEL="T4"
```

### Deployment Fails After Check

If deployment fails after GPU check:

```bash
# Check logs
modal app logs g-gpu-proc

# Check status
modal app list
```

## Integration with Existing Workflow

This adds **no breaking changes** to your existing deployment:

| Old Way | New Way |
|---------|---------|
| `modal deploy modal_app.py` | `./deploy.sh` (adds pre-check) |
| Manual GPU testing | Automatic GPU availability check |
| Wait for deployment to fail | Fail fast if GPU unavailable |

## Troubleshooting

### "No such file or directory: check_gpu.py"

```bash
cd /Users/rajivmehtapy/Documents/Dev/g-server-shell
./deploy.sh
```

### "Permission denied: deploy.sh"

```bash
chmod +x deploy.sh
```

### Check Timeout Too Short

Edit `check_gpu.py`:

```python
# Default timeout is 300 seconds (5 min)
is_available = check_gpu_availability(gpu_model, timeout=600)  # 10 min
```

### Pre-Check Passes but Deployment Fails

This means GPU was available but another issue occurred:

1. Check `.env` configuration
2. Check deployment logs: `modal app logs g-gpu-proc`
3. Try `--skip-check` to bypass pre-check

## Cost Savings

**Scenario:** L4 GPU unavailable, you try deployment

| Approach | Time Wasted | Cost |
|----------|-------------|------|
| **Without pre-check** | ~10 min | Build + attempt = wasted |
| **With pre-check** | ~2 min | GPU check only = minimal |

**Annual savings (assuming 50 failed deployments/year):**
- Time saved: ~400 minutes (~6.7 hours)
- Less frustration and faster iteration