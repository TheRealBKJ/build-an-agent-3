#!/usr/bin/env python3
"""
Demo script for AskVision hackathon deliverables
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.section_author_agent import SectionAuthorAgent
from bs4 import BeautifulSoup
import requests
import time

def demo_askvision():
    """Demo the AskVision capabilities"""
    
    print("🎯 AskVision Hackathon Demo")
    print("=" * 50)
    print("This demo showcases AskVision's ability to:")
    print("1. Parse Amazon product pages")
    print("2. Answer intelligent questions")
    print("3. Provide accessibility-focused responses")
    print("=" * 50)
    
    # Initialize agent
    agent = SectionAuthorAgent()
    
    # Demo URLs (Amazon product pages)
    demo_urls = [
        "https://www.amazon.com/dp/B08N5WRWNW",  # Echo Dot
        "https://www.amazon.com/dp/B07FZ8S74R",  # Fire TV Stick
        "https://www.amazon.com/dp/B08C7KG5LP"   # Ring Video Doorbell
    ]
    
    # Demo questions (from hackathon requirements)
    demo_questions = [
        "What do the top 3 reviews say?",
        "What's the total cost with shipping?",
        "How many 5-star ratings are there?",
        "What are the main product features?"
    ]
    
    for i, url in enumerate(demo_urls, 1):
        print(f"\n📦 Demo {i}: Processing Amazon product page")
        print(f"URL: {url}")
        
        try:
            # Fetch and parse the page
            print("📡 Fetching webpage...")
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            print("✅ Page parsed successfully")
            
            # Process and structure content
            print("🔍 Extracting structured content...")
            structured_content = agent.parse_and_structure(soup)
            structured_content['url'] = url
            
            print(f"📊 Found {len(structured_content['sections'])} content sections")
            
            # Answer demo questions
            print("\n🤔 Answering demo questions:")
            for j, question in enumerate(demo_questions, 1):
                print(f"\nQuestion {j}: {question}")
                print("-" * 40)
                
                try:
                    answer = agent.answer_question(question, structured_content)
                    print(f"AskVision: {answer}")
                except Exception as e:
                    print(f"Error: {e}")
                
                time.sleep(1)  # Brief pause between questions
            
            print(f"\n✅ Demo {i} completed successfully!")
            
        except Exception as e:
            print(f"❌ Demo {i} failed: {e}")
        
        if i < len(demo_urls):
            print("\n" + "="*50)
            print("Press Enter to continue to next demo...")
            input()
    
    print("\n🎉 All demos completed!")
    print("\nKey Features Demonstrated:")
    print("✅ Intelligent webpage parsing")
    print("✅ Natural language question understanding")
    print("✅ Accessibility-focused responses")
    print("✅ Multi-step reasoning with Nemotron 3.3")
    print("✅ Real-world Amazon product page handling")

if __name__ == "__main__":
    demo_askvision() 