# AskVision - AI Accessibility Assistant

Welcome to **AskVision**, an intelligent AI overlay assistant that helps blind or visually impaired users interact more intelligently with websites. Traditional screen readers read everything linearly, but they don't understand context, structure, or user intent. AskVision is a smarter semantic layer that lets users ask natural language questions and get concise, meaningful answers.

## 🧠 Architecture Overview

AskVision uses a **Section Author Agent** architecture to:

1. **Parse and structure** any webpage's raw HTML (e.g., Amazon product pages)
2. **Build a semantic tree** of sections (reviews, pricing, headers)
3. **Intelligently identify** what part of the page contains the answer to user queries
4. **Run reasoning and summarization** via Nemotron 3.3
5. **Return friendly responses** (TTS or screenreader-compatible)

## 🎯 Example Use Case

User opens Amazon, activates AskVision, and asks:

> "What do the top 3 reviews say?"

AskVision responds:

> "Most reviewers loved the product quality, but one mentioned delayed shipping. Overall sentiment is highly positive."

## 🏗️ Project Structure

```
askvision/
├── frontend/          # React overlay interface
├── backend/           # Flask server with agent logic
├── agent/             # LangChain Section Author agent
├── .env              # NVIDIA_API_KEY and config
└── README.md         # This file
```

## 🚀 Quick Start

1. **Setup Environment**

   ```bash
   pip install -r requirements.txt
   cp variables.env .env
   # Add your NVIDIA_API_KEY to .env
   ```

2. **Start Backend**

   ```bash
   cd backend
   python app.py
   ```

3. **Start Frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```

## 🎁 NVIDIA Integration

- **Nemotron 3.3** for natural language understanding, summarization, and reasoning
- **NeMo** for multi-step orchestration and tool planning
- **TTS integration** for voice responses back to the user

## 👥 Team

- **Caleb Calderon** (Calebc4554) – frontend, design, overlay logic
- **Joseph Akintunde** – backend, agent orchestration, parsing logic
- **Chioma Ibe** – research or testing support

## 🏁 Hackathon Deliverables

MVP demo featuring:

- Paste Amazon URL
- Ask 3 questions (e.g., "Top review?", "Total cost with shipping?", "How many 5-stars?")
- Agent answers aloud or in text

This is a real AI assistant, not a simple scraper. We're pushing accessibility forward by letting blind users ask for what they want and get intelligent, conversational responses from any website.
