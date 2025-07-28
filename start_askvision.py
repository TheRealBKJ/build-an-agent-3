#!/usr/bin/env python3
"""
Startup script for AskVision
Runs both backend and frontend servers
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

def run_backend():
    """Run the Flask backend server"""
    print("🚀 Starting AskVision Backend...")
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return None
    
    try:
        # Install dependencies if needed
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        
        # Start Flask server
        process = subprocess.Popen(
            [sys.executable, "app.py"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("✅ Backend started on http://localhost:5000")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def run_frontend():
    """Run the React frontend"""
    print("🎨 Starting AskVision Frontend...")
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return None
    
    try:
        # Check if node_modules exists, if not install dependencies
        if not (frontend_dir / "node_modules").exists():
            print("📦 Installing frontend dependencies...")
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        
        # Start React development server
        process = subprocess.Popen(
            ["npm", "start"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("✅ Frontend started on http://localhost:3000")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def main():
    """Main startup function"""
    print("🌟 Starting AskVision - AI Accessibility Assistant")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found. Creating from variables.env...")
        if Path("variables.env").exists():
            subprocess.run(["cp", "variables.env", ".env"])
            print("✅ Created .env file from variables.env")
        else:
            print("❌ No variables.env file found. Please create a .env file with your NVIDIA_API_KEY")
            return
    
    # Start backend
    backend_process = run_backend()
    if not backend_process:
        print("❌ Failed to start backend. Exiting.")
        return
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend
    frontend_process = run_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend. Exiting.")
        backend_process.terminate()
        return
    
    print("\n🎉 AskVision is starting up!")
    print("📱 Frontend: http://localhost:3000")
    print("🔧 Backend:  http://localhost:5000")
    print("\nPress Ctrl+C to stop all servers")
    
    try:
        # Wait for processes
        while True:
            time.sleep(1)
            if backend_process.poll() is not None:
                print("❌ Backend process stopped unexpectedly")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend process stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Shutting down AskVision...")
        
        # Terminate processes
        if backend_process:
            backend_process.terminate()
            print("✅ Backend stopped")
        
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend stopped")
        
        print("👋 AskVision stopped successfully")

if __name__ == "__main__":
    main() 