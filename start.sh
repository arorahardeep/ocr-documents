#!/bin/bash

echo "🚀 Starting OCR Document Processor..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Backend setup
echo "📦 Setting up backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Please create one with your OpenAI API key:"
    echo "   cp env.example .env"
    echo "   Then edit .env and add your OPENAI_API_KEY"
    echo ""
    echo "Press Enter to continue anyway..."
    read
fi

# Start backend server
echo "🚀 Starting backend server..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd ..

# Frontend setup
echo "📦 Setting up frontend..."
cd frontend

# Install Node.js dependencies
echo "📥 Installing Node.js dependencies..."
npm install

# Start frontend server
echo "🚀 Starting frontend server..."
npm start &
FRONTEND_PID=$!

cd ..

echo ""
echo "🎉 OCR Document Processor is starting up!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait
