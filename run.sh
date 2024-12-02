#!/bin/bash
source .venv/bin/activate
export HOST=147.182.169.165
export PORT=80
python3 app.py

sleep 3
exec ./run.sh