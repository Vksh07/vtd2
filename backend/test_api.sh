#!/bin/bash
set -e
echo "Starting NeuroPrep backend..."
cd "$(dirname "$0")"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
