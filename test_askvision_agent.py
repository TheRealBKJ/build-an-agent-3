#!/usr/bin/env python3
"""
Test script for AskVision Agent
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import requests
from askvision_agent import AskVisionState, graph

async def test_askvision():
    """Test the AskVision agent with a sample webpage"""
    
    print("🧪 Testing AskVision Agent...")
    
    # Test URL and question
    url = "https://www.amazon.com/dp/B08N5WRWNW"  # Echo Dot
    question = "What do the top 3 reviews say?"
    
    try:
        print(f"📡 Fetching webpage: {url}")
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        
        html_content = response.text
        print(f"✅ Fetched {len(html_content)} characters")
        
        # Create AskVision state
        state = AskVisionState(
            url=url,
            question=question,
            html_content=html_content
        )
        
        print("🤖 Running AskVision agent...")
        result = await graph.ainvoke(state)
        
        if result.answer:
            print(f"✅ AskVision Answer: {result.answer}")
        else:
            print("❌ No answer generated")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_askvision())
    sys.exit(0 if success else 1) 