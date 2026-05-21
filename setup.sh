#!/bin/bash

# ================================================
# NutriAI - Quick Setup Script for macOS/Linux
# ================================================

echo ""
echo "  ╔═══════════════════════════════════╗"
echo "  ║   NutriAI - Quick Setup Script    ║"
echo "  ║   AI Gym Nutrition Calculator     ║"
echo "  ╚═══════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed"
    echo "Please install Python 3.9+ using:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt-get install python3"
    exit 1
fi

echo "✓ Python found"
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi
echo "✓ Virtual environment created"

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
python -m pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "⚠️  Warning: Could not upgrade pip"
fi

# Install dependencies
echo ""
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"

# Train models
echo ""
echo "================================================"
echo "Training Machine Learning Models..."
echo "================================================"
python train_models.py
if [ $? -ne 0 ]; then
    echo "❌ Failed to train models"
    exit 1
fi
echo "✓ Models trained successfully"

# Check for .env file
echo ""
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your Google Gemini API key"
    echo "   1. Open .env in a text editor"
    echo "   2. Replace 'your_google_gemini_api_key_here' with your actual API key"
    echo "   3. Get API key from: https://ai.google.dev/"
fi

# Setup complete
echo ""
echo "================================================"
echo "✓ Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your Google Gemini API key"
echo "2. Run: python app.py"
echo "3. Open: http://localhost:5000"
echo ""
echo "To deactivate virtual environment later, type: deactivate"
echo ""
