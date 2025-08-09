@echo off
echo 🚀 Starting OCR Document Processor...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm is not installed. Please install npm first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Backend setup
echo 📦 Setting up backend...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo 🔧 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo 📥 Installing Python dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  No .env file found. Please create one with your OpenAI API key:
    echo    copy env.example .env
    echo    Then edit .env and add your OPENAI_API_KEY
    echo.
    pause
)

REM Start backend server
echo 🚀 Starting backend server...
start "Backend Server" cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"

cd ..

REM Frontend setup
echo 📦 Setting up frontend...
cd frontend

REM Install Node.js dependencies
echo 📥 Installing Node.js dependencies...
npm install

REM Start frontend server
echo 🚀 Starting frontend server...
start "Frontend Server" cmd /k "npm start"

cd ..

echo.
echo 🎉 OCR Document Processor is starting up!
echo.
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo Both servers are now running in separate windows.
echo Close those windows to stop the servers.
pause
