#!/bin/bash

echo "🔧 Testing Face Recognition Backend API..."

cd backend

# Setup virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "📦 Setting up Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo "🚀 Starting backend server..."
python app.py