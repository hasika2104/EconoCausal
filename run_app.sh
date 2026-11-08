#!/usr/bin/env bash
# EconoCausal — Multi-tier Web Application Runner
# Launches FastAPI backend on port 8000 and React Vite frontend on port 5173

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# Ensure root directory is on PYTHONPATH for all python sub-processes and uvicorn reloads
export PYTHONPATH="$DIR:${PYTHONPATH:-}"

PYTHON_BIN=".venv/bin/python"
if [ ! -f "$PYTHON_BIN" ]; then
    PYTHON_BIN="python3"
fi

echo "================================================================="
echo "   📈 Starting EconoCausal — Causal AI & Pricing Web App"
echo "================================================================="
echo "Working directory: $DIR"
echo "Python binary:     $PYTHON_BIN"

# Start FastAPI backend in the background
echo "1. Starting FastAPI backend on http://127.0.0.1:8000..."
"$PYTHON_BIN" -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!

cleanup() {
    echo ""
    echo "Stopping EconoCausal servers (Backend PID: $BACKEND_PID)..."
    kill "$BACKEND_PID" 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

# Wait for backend to be ready
sleep 2

# Start Vite frontend
echo "2. Starting React Vite frontend on http://localhost:5173..."
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
