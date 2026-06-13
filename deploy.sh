#!/usr/bin/env bash
# Smart deployment script with GPU availability pre-check
# Usage: ./deploy.sh [--skip-check]

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
VENV_BIN="/Users/rajivmehtapy/Documents/Dev/g-server-shell/.venv/bin"
DEPLOY_CMD="$VENV_BIN/modal deploy modal_app.py"
CHECK_SCRIPT="$VENV_BIN/python check_gpu.py"

# Parse arguments
SKIP_CHECK=false
for arg in "$@"; do
    case $arg in
        --skip-check)
            SKIP_CHECK=true
            shift
            ;;
        *)
            echo "Unknown argument: $arg"
            echo "Usage: $0 [--skip-check]"
            exit 1
            ;;
    esac
done

echo "============================================================"
echo "🚀 Smart Deployment with GPU Pre-Check"
echo "============================================================"
echo ""

# Step 1: Check configuration
echo "📋 Step 1: Checking configuration..."
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found${NC}"
    exit 1
fi

GPU_MODEL=$(grep "^MODAL_GPU_MODEL=" .env | cut -d'=' -f2 | tr -d '"')
CPU=$(grep "^MODAL_CPU=" .env | cut -d'=' -f2)
MEMORY=$(grep "^MODAL_MEMORY=" .env | cut -d'=' -f2)

echo "   GPU Model: $GPU_MODEL"
echo "   CPU: $CPU cores"
echo "   Memory: $MEMORY MB"
echo ""

# Step 2: Skip or perform GPU check
if [ "$SKIP_CHECK" = true ]; then
    echo -e "${YELLOW}⚠️  Skipping GPU availability check (--skip-check flag used)${NC}"
    echo ""
else
    echo "🔍 Step 2: Checking GPU availability on Modal..."
    echo "   (This may take 2-3 minutes)"
    echo ""

    # Run the GPU check script
    if $CHECK_SCRIPT; then
        echo ""
        echo -e "${GREEN}✅ GPU availability check passed${NC}"
    else
        echo ""
        echo -e "${RED}❌ GPU availability check failed${NC}"
        echo ""
        echo "To proceed anyway, use:"
        echo "  $0 --skip-check"
        exit 1
    fi
    echo ""
fi

# Step 3: Deploy
echo "📦 Step 3: Deploying to Modal..."
echo ""

if $DEPLOY_CMD; then
    echo ""
    echo "============================================================"
    echo -e "${GREEN}🎉 Deployment successful!${NC}"
    echo "============================================================"
    echo ""
    echo "Next steps:"
    echo "  1. Check deployment status: modal app list"
    echo "  2. View logs: modal app logs g-gpu-proc"
    echo "  3. Access the terminal at the URL provided above"
else
    echo ""
    echo "============================================================"
    echo -e "${RED}❌ Deployment failed${NC}"
    echo "============================================================"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check deployment logs: modal app logs g-gpu-proc"
    echo "  2. Verify .env configuration"
    echo "  3. Try a different GPU model (T4, A10, A100)"
    exit 1
fi