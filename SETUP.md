# AskVision Setup Guide

This guide will help you set up and run the AskVision AI Accessibility Assistant for the hackathon.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Run the automated startup script
python start_askvision.py
```

### Option 2: Manual Setup

Follow the steps below to set up each component manually.

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **Node.js 16+** installed
3. **NVIDIA API Key** for Nemotron 3.3

## 🔧 Backend Setup

1. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**

   ```bash
   # Copy the template
   cp variables.env .env

   # Edit .env and add your NVIDIA API key
   # NVIDIA_API_KEY=your_api_key_here
   ```

3. **Start the Flask backend:**

   ```bash
   cd backend
   python app.py
   ```

   The backend will run on `http://localhost:5000`

## 🎨 Frontend Setup

1. **Install Node.js dependencies:**

   ```bash
   cd frontend
   npm install
   ```

2. **Start the React development server:**

   ```bash
   npm start
   ```

   The frontend will run on `http://localhost:3000`

## 🧪 Testing

### Test the Agent

```bash
python test_askvision.py
```

### Run the Demo

```bash
python demo_askvision.py
```

## 🎯 Hackathon Demo Flow

1. **Start the application:**

   ```bash
   python start_askvision.py
   ```

2. **Open your browser to:** `http://localhost:3000`

3. **Demo the features:**

   - Paste an Amazon URL (e.g., `https://www.amazon.com/dp/B08N5WRWNW`)
   - Ask questions like:
     - "What do the top 3 reviews say?"
     - "What's the total cost with shipping?"
     - "How many 5-star ratings are there?"

4. **Try voice input** using the microphone button

## 🏗️ Architecture Overview

```
AskVision/
├── backend/                 # Flask API server
│   └── app.py              # Main Flask application
├── agent/                  # LangChain agent logic
│   ├── __init__.py
│   └── section_author_agent.py  # Core agent implementation
├── frontend/               # React UI
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   └── components/     # React components
│   └── package.json        # Node.js dependencies
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## 🔍 Key Features

### Backend (Flask + LangChain)

- **URL Processing:** Fetches and parses webpages
- **Content Structuring:** Extracts reviews, pricing, product info
- **Intelligent Q&A:** Uses Nemotron 3.3 for reasoning
- **REST API:** Clean endpoints for frontend integration

### Frontend (React)

- **Modern UI:** Beautiful, accessible interface
- **Voice Input:** Speech recognition for hands-free use
- **Real-time Updates:** Live conversation history
- **Responsive Design:** Works on all devices

### Agent (LangChain + NVIDIA)

- **Section Author Pattern:** Intelligent content analysis
- **Multi-step Reasoning:** Research → Extract → Answer
- **Accessibility Focus:** Screen reader friendly responses
- **NVIDIA Integration:** Nemotron 3.3 for advanced NLP

## 🐛 Troubleshooting

### Backend Issues

- **Import errors:** Make sure all dependencies are installed
- **API key issues:** Verify your NVIDIA API key in `.env`
- **Port conflicts:** Change port in `backend/app.py`

### Frontend Issues

- **Node modules:** Run `npm install` in frontend directory
- **Proxy errors:** Check that backend is running on port 5000
- **Voice input:** Ensure browser supports SpeechRecognition API

### Agent Issues

- **Model loading:** Check NVIDIA API key and network connection
- **Parsing errors:** Some websites may block scraping
- **Memory issues:** Large pages may need optimization

## 🎁 NVIDIA Integration

The project uses NVIDIA's Nemotron 3.3 model for:

- **Natural Language Understanding:** Parse user questions
- **Content Summarization:** Extract key information
- **Reasoning:** Multi-step problem solving
- **Accessibility:** Generate screen reader friendly responses

## 🏁 Hackathon Deliverables

✅ **MVP Demo Ready:**

- Paste Amazon URL
- Ask 3 questions
- Get intelligent answers
- Voice input support
- Beautiful UI

✅ **Technical Features:**

- Flask backend with CORS
- React frontend with voice input
- LangChain agent architecture
- NVIDIA AI integration
- Web scraping with BeautifulSoup

✅ **Accessibility Focus:**

- Screen reader compatible
- Voice input/output
- High contrast support
- Keyboard navigation

## 🚀 Next Steps

1. **Test with different websites** beyond Amazon
2. **Add more voice features** (TTS output)
3. **Implement caching** for better performance
4. **Add user accounts** for conversation history
5. **Deploy to cloud** for production use

## 📞 Support

For hackathon support:

- **Caleb Calderon** - Frontend & Design
- **Joseph Akintunde** - Backend & Agent Logic
- **Chioma Ibe** - Testing & Documentation

---

**AskVision** - Making the web accessible through AI! 🌟
