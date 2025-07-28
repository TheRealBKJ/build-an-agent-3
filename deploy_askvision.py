#!/usr/bin/env python3
"""
Deployment script for AskVision on GPU instance
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Run a command and return the result"""
    print(f"🔄 Running: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(f"✅ Output: {result.stdout}")
        if result.stderr:
            print(f"⚠️  Warnings: {result.stderr}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Error output: {e.stderr}")
        return None

def setup_environment():
    """Set up the environment for AskVision"""
    print("🚀 Setting up AskVision environment...")
    
    # Install Python dependencies
    print("📦 Installing Python dependencies...")
    result = run_command("pip3 install -r requirements.txt")
    if not result:
        print("❌ Failed to install Python dependencies")
        return False
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        run_command("cp variables.env .env")
    
    return True

def start_backend():
    """Start the Flask backend"""
    print("🔧 Starting AskVision Backend...")
    
    # Change to backend directory and start
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return None
    
    # Start Flask server in background
    process = subprocess.Popen(
        ["python3", "app.py"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print("✅ Backend started on http://localhost:5000")
    return process

def setup_frontend():
    """Set up the React frontend"""
    print("🎨 Setting up AskVision Frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return None
    
    # Install Node.js dependencies
    print("📦 Installing Node.js dependencies...")
    result = run_command("npm install", cwd=frontend_dir)
    if not result:
        print("❌ Failed to install Node.js dependencies")
        return None
    
    # Start React development server
    print("🚀 Starting React development server...")
    process = subprocess.Popen(
        ["npm", "start"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print("✅ Frontend started on http://localhost:3000")
    return process

def main():
    """Main deployment function"""
    print("🌟 Deploying AskVision on GPU Instance")
    print("=" * 50)
    
    # Setup environment
    if not setup_environment():
        print("❌ Environment setup failed")
        return
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend")
        return
    
    # Wait for backend to start
    print("⏳ Waiting for backend to initialize...")
    time.sleep(5)
    
    # Start frontend
    frontend_process = setup_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend")
        backend_process.terminate()
        return
    
    print("\n🎉 AskVision is deployed and running!")
    print("📱 Frontend: http://localhost:3000")
    print("🔧 Backend:  http://localhost:5000")
    print("\n🔗 You can access the application through your GPU instance's public IP")
    print("💡 Make sure to configure your NVIDIA API key in the .env file")
    
    try:
        # Keep the processes running
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
        
        if backend_process:
            backend_process.terminate()
            print("✅ Backend stopped")
        
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend stopped")
        
        print("👋 AskVision stopped successfully")

if __name__ == "__main__":
    main() 