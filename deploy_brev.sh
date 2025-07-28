#!/bin/bash

echo "🚀 Deploying AskVision on Brev.dev GPU Instance..."

# Set environment variables
export NVIDIA_API_KEY="ed99e0cc-5fc0-4f9d-b3cc-c0dfba6ef53a"
export NVIDIA_MODEL="llama-3.3-nemotron-super-49b-v1.5"

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Jupyter if not already installed
pip install jupyter lab

# Copy environment file
echo "🔧 Setting up environment..."
cp variables.env .env

# Test the agent
echo "🧪 Testing AskVision agent..."
python3 test_askvision_agent.py

# Start Jupyter Lab
echo "🎯 Starting Jupyter Lab..."
echo "📊 Access your agent at: http://localhost:8888"
echo "🔗 Use the existing agent: code/agent_client.ipynb"
echo "🔗 Or use AskVision: askvision_client.ipynb"

jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root 