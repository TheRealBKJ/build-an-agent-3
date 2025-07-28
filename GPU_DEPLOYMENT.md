# AskVision GPU Deployment Guide

## 🚀 Quick Start for GPU Instance

### Option 1: One-Command Deployment

```bash
./run_askvision.sh
```

### Option 2: Step-by-Step Deployment

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Set up environment
cp variables.env .env

# 3. Start backend
cd backend
python3 app.py &
cd ..

# 4. Start frontend
cd frontend
npm install
npm start &
cd ..
```

## 🔧 Configuration

### NVIDIA API Key Setup

1. Edit the `.env` file:

   ```bash
   nano .env
   ```

2. Add your NVIDIA API key:
   ```
   NVIDIA_API_KEY=your_api_key_here
   ```

### Port Configuration

- **Backend:** `http://localhost:5000`
- **Frontend:** `http://localhost:3000`
- **Access via:** Your GPU instance's public IP

## 🧪 Testing

### Test Backend API

```bash
# Health check
curl http://localhost:5000/health

# Test URL processing
curl -X POST http://localhost:5000/process-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.amazon.com/dp/B08N5WRWNW"}'
```

### Test Frontend

Open your browser to: `http://YOUR_GPU_IP:3000`

## 🎯 Hackathon Demo

### Demo Script

```bash
python3 demo_askvision.py
```

### Manual Demo Steps

1. **Paste Amazon URL:** `https://www.amazon.com/dp/B08N5WRWNW`
2. **Ask Questions:**
   - "What do the top 3 reviews say?"
   - "What's the total cost with shipping?"
   - "How many 5-star ratings are there?"

## 🔍 Troubleshooting

### Backend Issues

- **Import Error:** Make sure you're running from the project root
- **Port Issues:** Check if port 5000 is available
- **API Key:** Verify NVIDIA_API_KEY in .env

### Frontend Issues

- **Node Modules:** Run `npm install` in frontend directory
- **Port Issues:** Check if port 3000 is available
- **Proxy Errors:** Ensure backend is running on port 5000

### GPU Issues

- **Memory:** Monitor GPU memory usage
- **Model Loading:** Check NVIDIA API connectivity
- **Performance:** Adjust batch sizes if needed

## 📊 Monitoring

### Check Processes

```bash
# Check if processes are running
ps aux | grep python3
ps aux | grep npm

# Check ports
netstat -tlnp | grep :5000
netstat -tlnp | grep :3000
```

### Logs

```bash
# Backend logs
tail -f backend/app.log

# Frontend logs
tail -f frontend/npm-debug.log
```

## 🎉 Success Indicators

✅ **Backend Running:** `http://localhost:5000/health` returns `{"status": "healthy"}`

✅ **Frontend Running:** `http://localhost:3000` shows AskVision interface

✅ **Agent Working:** Can process URLs and answer questions

✅ **GPU Utilization:** NVIDIA GPU is being used for inference

## 🏁 Hackathon Ready!

Your AskVision deployment is ready for:

- ✅ URL processing
- ✅ Intelligent Q&A
- ✅ Voice input
- ✅ Beautiful UI
- ✅ Accessibility features

**Access your demo at:** `http://YOUR_GPU_IP:3000`
