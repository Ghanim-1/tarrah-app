#!/bin/bash

# طرّة Business Management System - Startup Script
# Run this file to start the application: bash run_tarrah.sh

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║          طرّة (Tarrah) Business Management System         ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is not installed"
    echo ""
    echo "Please install Python 3.7 or higher:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-venv"
    echo ""
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "ℹ Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "ℹ Checking dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Start the application
echo "═════════════════════════════════════════════════════════════"
echo ""
echo "✓ Starting طرّة application..."
echo ""
echo "📱 Open your browser and go to: http://localhost:5000"
echo ""
echo "🔑 Default login:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "📲 Mobile Access:"
echo "   Find your IP: ifconfig | grep inet"
echo "   Then on phone: http://YOUR-IP:5000"
echo ""
echo "🛑 To stop: Press Ctrl+C"
echo ""
echo "═════════════════════════════════════════════════════════════"
echo ""

# Run the application
python app.py
