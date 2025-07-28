#!/bin/bash

echo "🌟 Starting AskVision on GPU Instance"
echo "======================================"

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp variables.env .env
fi

# Start backend
echo "🔧 Starting AskVision Backend..."
cd backend
python3 app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 5

# Start frontend
echo "🎨 Starting AskVision Frontend..."
cd frontend
npm install
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "🎉 AskVision is running!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:5000"
echo ""
echo "🔗 Access via your GPU instance's public IP"
echo "💡 Configure NVIDIA_API_KEY in .env for full functionality"
echo ""
echo "Press Ctrl+C to stop"

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID 