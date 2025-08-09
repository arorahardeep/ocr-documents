#!/usr/bin/env python3
"""
Test script to verify OCR Document Processor setup
"""

import sys
import importlib
import subprocess
import os

def test_python_version():
    """Test Python version"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python 3.9+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def test_dependencies():
    """Test if required packages can be imported"""
    print("\n📦 Testing Python dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'openai',
        'fitz',  # PyMuPDF
        'PIL',   # Pillow
        'pydantic',
        'aiofiles'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r backend/requirements.txt")
        return False
    
    return True

def test_node_npm():
    """Test if Node.js and npm are available"""
    print("\n📦 Testing Node.js and npm...")
    
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()}")
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        return False
    
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm {result.stdout.strip()}")
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found")
        return False
    
    return True

def test_backend_config():
    """Test backend configuration"""
    print("\n⚙️  Testing backend configuration...")
    
    # Check if backend directory exists
    if not os.path.exists('backend'):
        print("❌ Backend directory not found")
        return False
    
    # Check if main.py exists
    if not os.path.exists('backend/main.py'):
        print("❌ backend/main.py not found")
        return False
    
    # Check if requirements.txt exists
    if not os.path.exists('backend/requirements.txt'):
        print("❌ backend/requirements.txt not found")
        return False
    
    # Check if .env file exists
    if not os.path.exists('backend/.env'):
        print("⚠️  backend/.env not found (you'll need to create this)")
        print("   Copy backend/env.example to backend/.env and add your OpenAI API key")
    else:
        print("✅ backend/.env found")
    
    print("✅ Backend files found")
    return True

def test_frontend_config():
    """Test frontend configuration"""
    print("\n⚙️  Testing frontend configuration...")
    
    # Check if frontend directory exists
    if not os.path.exists('frontend'):
        print("❌ Frontend directory not found")
        return False
    
    # Check if package.json exists
    if not os.path.exists('frontend/package.json'):
        print("❌ frontend/package.json not found")
        return False
    
    # Check if src directory exists
    if not os.path.exists('frontend/src'):
        print("❌ frontend/src directory not found")
        return False
    
    print("✅ Frontend files found")
    return True

def main():
    """Run all tests"""
    print("🧪 OCR Document Processor Setup Test")
    print("=" * 40)
    
    tests = [
        test_python_version,
        test_dependencies,
        test_node_npm,
        test_backend_config,
        test_frontend_config
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 To start the application:")
        print("   - On macOS/Linux: ./start.sh")
        print("   - On Windows: start.bat")
        print("   - Or manually:")
        print("     cd backend && uvicorn main:app --reload --port 8000")
        print("     cd frontend && npm start")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
