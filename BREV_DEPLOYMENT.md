# AskVision Deployment on Brev.dev

## 🚀 **Quick Deployment (Your GPU Instance)**

### **Step 1: One-Command Deployment**

```bash
./deploy_brev.sh
```

### **Step 2: Manual Setup (if needed)**

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment
export NVIDIA_API_KEY="ed99e0cc-5fc0-4f9d-b3cc-c0dfba6ef53a"
export NVIDIA_MODEL="llama-3.3-nemotron-super-49b-v1.5"

# Test API access
python3 test_nvidia_api.py

# Start Jupyter
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

## 🎯 **Your Configuration**

✅ **API Key**: `ed99e0cc-5fc0-4f9d-b3cc-c0dfba6ef53a`  
✅ **Model**: `llama-3.3-nemotron-super-49b-v1.5`  
✅ **Platform**: Brev.dev GPU Instance  
✅ **Framework**: Existing Agent Structure

## 🏗️ **What You Have Ready**

### **Option 1: Use Existing Agent (Recommended)**

```bash
# Access Jupyter Lab
http://your-brev-url:8888

# Open notebook
code/agent_client.ipynb
```

### **Option 2: Use AskVision Agent**

```bash
# Test AskVision
python3 test_askvision_agent.py

# Use AskVision notebook
askvision_client.ipynb
```

### **Option 3: Use Flask Backend**

```bash
# Start backend
cd backend && python3 app.py

# Access API
http://your-brev-url:5001
```

## 🎉 **Hackathon Demo**

### **Demo 1: Existing Agent**

1. Open `code/agent_client.ipynb`
2. Change topic to: **"Amazon Echo Dot product reviews and pricing analysis"**
3. Run cells
4. Show intelligent multi-step reasoning!

### **Demo 2: AskVision Agent**

1. Run `python3 test_askvision_agent.py`
2. Show webpage analysis
3. Demonstrate accessibility features!

### **Demo 3: API Endpoints**

```bash
# Test health
curl http://your-brev-url:5001/health

# Test webpage analysis
curl -X POST http://your-brev-url:5001/process-and-ask \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.amazon.com/dp/B08N5WRWNW",
    "question": "What do the top 3 reviews say?"
  }'
```

## 🔧 **Environment Setup**

Your `variables.env` is configured with:

```bash
NVIDIA_API_KEY=ed99e0cc-5fc0-4f9d-b3cc-c0dfba6ef53a
NVIDIA_MODEL=llama-3.3-nemotron-super-49b-v1.5
FLASK_PORT=5001
FLASK_HOST=0.0.0.0
DEBUG=True
```

## 🎯 **Key Features Working**

✅ **NVIDIA AI Integration** - Your API key + Super 49B model  
✅ **Multi-step Reasoning** - Research → Extract → Answer  
✅ **Tool System** - Extensible webpage analysis tools  
✅ **Jupyter Interface** - Interactive notebooks  
✅ **LangGraph Workflow** - Stateful agent execution  
✅ **Accessibility Focus** - Screen reader friendly responses

## 🚀 **Deployment Commands**

```bash
# Quick start
./deploy_brev.sh

# Or step by step
pip install -r requirements.txt
python3 test_nvidia_api.py
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

## 📊 **Access Points**

- **Jupyter Lab**: `http://your-brev-url:8888`
- **Flask API**: `http://your-brev-url:5001`
- **Health Check**: `http://your-brev-url:5001/health`

## 🎉 **You're Ready!**

Your Brev.dev GPU instance is configured with:

- ✅ NVIDIA API key
- ✅ Super 49B model
- ✅ Complete agent framework
- ✅ Jupyter interface
- ✅ Flask backend

**Just run `./deploy_brev.sh` and start your hackathon demo!** 🚀
