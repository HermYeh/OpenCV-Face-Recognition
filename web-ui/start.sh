#!/bin/bash

echo "🚀 Starting Face Recognition Web UI..."

# Function to kill background processes on exit
cleanup() {
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

# Set trap to cleanup on script exit
trap cleanup EXIT INT TERM

# Check if backend dependencies are installed
if [ ! -d "backend/venv" ]; then
    echo "📦 Setting up Python virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
else
    echo "✅ Backend environment already set up"
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
else
    echo "✅ Frontend dependencies already installed"
fi

# Start backend server
echo "🔧 Starting backend server on port 5000..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend server
echo "🎨 Starting frontend server on port 3000..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo "✨ Face Recognition Web UI is running!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for interrupt
wait