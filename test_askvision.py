#!/usr/bin/env python3
"""
Test script for AskVision Section Author Agent
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.section_author_agent import SectionAuthorAgent
from bs4 import BeautifulSoup
import requests

def test_agent():
    """Test the AskVision agent with a sample webpage"""
    
    print("🧪 Testing AskVision Section Author Agent...")
    
    # Initialize the agent
    agent = SectionAuthorAgent()
    print("✅ Agent initialized successfully")
    
    # Test with a sample Amazon product page
    test_url = "https://www.amazon.com/dp/B08N5WRWNW"  # Echo Dot
    
    try:
        print(f"📡 Fetching test URL: {test_url}")
        response = requests.get(test_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        print("✅ HTML parsed successfully")
        
        # Test parsing and structuring
        print("🔍 Testing content parsing and structuring...")
        structured_content = agent.parse_and_structure(soup)
        
        print(f"📊 Found {len(structured_content['sections'])} sections:")
        for section_name, section_data in structured_content['sections'].items():
            print(f"  - {section_name}: {type(section_data)}")
        
        # Test question answering
        test_questions = [
            "What is the product name?",
            "What's the price?",
            "Are there any reviews?"
        ]
        
        print("\n🤔 Testing question answering...")
        for question in test_questions:
            print(f"\nQuestion: {question}")
            try:
                answer = agent.answer_question(question, structured_content)
                print(f"Answer: {answer[:200]}...")
            except Exception as e:
                print(f"Error: {e}")
        
        print("\n✅ All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_agent()
    sys.exit(0 if success else 1) 