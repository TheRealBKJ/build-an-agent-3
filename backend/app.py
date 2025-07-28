from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import json
import asyncio

# Add the parent directory to the path so we can import the agent module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from askvision_agent import AskVisionState, graph

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "AskVision Backend"})

@app.route('/process-url', methods=['POST'])
def process_url():
    """Process a URL and extract structured content"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        # Fetch and parse the webpage
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract basic structured content
        structured_content = {
            'url': url,
            'title': soup.find('title').get_text().strip() if soup.find('title') else '',
            'sections': {
                'reviews': {'review_count': 0, 'review_items': []},
                'pricing': {'price': ''},
                'product_info': {'name': '', 'description': ''},
                'navigation': {'menu_items': []},
                'content': {'headings': [], 'paragraphs': []}
            },
            'metadata': {
                'total_sections': 5,
                'has_reviews': True,
                'has_pricing': True,
                'has_product_info': True
            }
        }
        
        return jsonify({
            "success": True,
            "url": url,
            "structured_content": structured_content
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ask-question', methods=['POST'])
def ask_question():
    """Ask a question about the processed webpage"""
    try:
        data = request.get_json()
        question = data.get('question')
        structured_content = data.get('structured_content')
        
        if not question or not structured_content:
            return jsonify({"error": "Question and structured_content are required"}), 400
        
        # For now, return a simple answer since we need to fetch the actual HTML
        answer = f"AskVision is analyzing your question: '{question}'. This would use the full AskVision agent to provide an intelligent answer."
        
        return jsonify({
            "success": True,
            "question": question,
            "answer": answer
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/process-and-ask', methods=['POST'])
def process_and_ask():
    """Process a URL and answer a question in one step using AskVision agent"""
    try:
        data = request.get_json()
        url = data.get('url')
        question = data.get('question')
        
        if not url or not question:
            return jsonify({"error": "URL and question are required"}), 400
        
        # Fetch and parse the webpage
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        
        html_content = response.text
        
        # Use the AskVision agent
        async def run_askvision():
            state = AskVisionState(
                url=url,
                question=question,
                html_content=html_content
            )
            result = await graph.ainvoke(state)
            return result
        
        # Run the async function
        result = asyncio.run(run_askvision())
        
        answer = result.answer if result.answer else "AskVision couldn't generate an answer for this question."
        
        return jsonify({
            "success": True,
            "url": url,
            "question": question,
            "answer": answer
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))  # Changed from 5000 to 5001
    app.run(host='0.0.0.0', port=port, debug=True) 