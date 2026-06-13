#!/usr/bin/env python3
"""
GPU availability checker using Modal shell command.
Simpler approach that doesn't require @app.function decorator.
"""

import os
import subprocess
import sys
import time
from dotenv import load_dotenv

load_dotenv()


def check_gpu_availability_simple(gpu_model: str, timeout: int = 300) -> bool:
    """
    Check if a specific GPU model is available on Modal using shell command.

    Args:
        gpu_model: GPU model to check (e.g., "L4", "T4", "H100")
        timeout: Maximum wait time in seconds (default: 300)

    Returns:
        True if GPU is available, False otherwise
    """
    print(f"🔍 Checking {gpu_model} GPU availability on Modal...")
    print("-" * 60)

    modal_bin = "/Users/rajivmehtapy/Documents/Dev/g-server-shell/.venv/bin/modal"

    # Run a simple GPU test using modal shell
    cmd = [
        modal_bin, "shell",
        "--gpu", gpu_model,
        "bash", "-c",
        "nvidia-smi --query-gpu=name --format=csv,noheader 2>&1 || echo 'GPU not found'"
    ]

    print(f"⏱️  Attempting to allocate {gpu_model} GPU...")
    print(f"   (This may take 1-3 minutes if GPU is available)")
    print(f"   Timeout set to {timeout} seconds\n")

    start_time = time.time()
    elapsed = 0.0

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        elapsed = time.time() - start_time

        print(f"\n⏱️  Allocation time: {elapsed:.1f} seconds")

        # Check if GPU was detected
        if "NVIDIA" in result.stdout or "NVIDIA" in result.stderr:
            # Extract GPU name
            for line in result.stdout.split('\n') + result.stderr.split('\n'):
                if "NVIDIA" in line and "not found" not in line.lower():
                    print(f"📊 Result: ✅ GPU available: {line.strip()}")
                    print("-" * 60)
                    print(f"🎉 {gpu_model} GPU is available for deployment!")
                    return True

        print(f"📊 Result: ❌ GPU not available")
        print(f"   Output: {result.stdout[:200]}")
        print(f"   Error: {result.stderr[:200]}")
        print("-" * 60)
        print(f"❌ {gpu_model} GPU allocation failed")
        return False

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        print(f"\n⏱️  Time elapsed: {elapsed:.1f} seconds")
        print("-" * 60)
        print(f"❌ TIMEOUT: {gpu_model} GPU not available within {timeout} seconds")
        print(f"💡 Suggestion: Try a different GPU model (T4, A10, A100)")
        return False
    except Exception as e:
        print(f"\n❌ Error during GPU check: {str(e)}")
        return False


def suggest_alternative_gpus(failed_gpu: str) -> list[str]:
    """Suggest alternative GPU models based on availability tiers."""
    # Ordered by typical availability (fastest to slowest)
    alternatives = {
        "B200": ["H100", "H200", "L40S", "A100", "A10", "L4", "T4"],
        "H200": ["H100", "L40S", "A100", "A10", "L4", "T4"],
        "H100": ["L40S", "A100", "A10", "L4", "T4"],
        "L40S": ["A100", "A10", "L4", "T4"],
        "A100": ["A10", "L4", "T4"],
        "A10": ["L4", "T4"],
        "L4": ["T4", "A10"],
        "T4": ["A10", "L4", "A100"],
    }

    return alternatives.get(failed_gpu, ["T4", "A10", "L4"])


def main():
    """Main entry point."""
    gpu_model = os.getenv("MODAL_GPU_MODEL", "L4").strip('"')

    if not gpu_model:
        print("❌ No GPU model configured. Set MODAL_GPU_MODEL in .env")
        sys.exit(1)

    print("=" * 60)
    print("🚀 Modal GPU Availability Checker")
    print("=" * 60)
    print()

    # Check GPU availability
    is_available = check_gpu_availability_simple(gpu_model)

    if not is_available:
        print()
        print("💡 Alternatives to try:")
        alternatives = suggest_alternative_gpus(gpu_model)
        for i, alt in enumerate(alternatives[:3], 1):
            print(f"   {i}. {alt} GPU")

        print()
        print("📝 To use an alternative GPU, update your .env:")
        print(f"   MODAL_GPU_MODEL=\"{alternatives[0]}\"")

        sys.exit(1)

    print()
    print("✅ Pre-check passed! Proceeding with deployment...")
    print()


if __name__ == "__main__":
    main()