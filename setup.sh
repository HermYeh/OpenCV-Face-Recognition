#!/bin/bash

echo "🚀 Setting up Face Recognition Web UI..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update -y

# Install Python3 and pip if not already installed
echo "🐍 Installing Python3 and pip..."
sudo apt-get install -y python3 python3-pip

# Install system dependencies for OpenCV
echo "📷 Installing OpenCV system dependencies..."
sudo apt-get install -y libopencv-dev python3-opencv
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install -y libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev
sudo apt-get install -y libgtk-3-dev libpng-dev libjpeg-dev libopenexr-dev
sudo apt-get install -y libtiff-dev libwebp-dev

# Install Python dependencies
echo "📋 Installing Python dependencies..."
pip3 install -r requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p trainer
mkdir -p dataset
mkdir -p static/css
mkdir -p static/js
mkdir -p templates

# Make the script executable
chmod +x setup.sh

echo "✅ Setup complete!"
echo ""
echo "To start the Face Recognition Web UI:"
echo "   python3 app.py"
echo ""
echo "Then open your browser and go to:"
echo "   http://localhost:5000"
echo ""
echo "🎯 Features:"
echo "   • Real-time face detection"
echo "   • Face recognition with confidence scores"
echo "   • Beautiful web interface"
echo "   • Live camera feed"
echo "   • Recognition history"
echo "   • System statistics"
echo ""