#!/bin/bash
cd "$(dirname "$0")"
echo "Installing dependencies..."
pip3 install flask markdown --quiet
echo ""
echo "Starting Dr Neal Aggarwal site at http://localhost:5000"
echo "Press Ctrl+C to stop."
echo ""
open "http://localhost:5001"
python3 app.py
