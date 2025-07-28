#!/usr/bin/env python3
"""
Test NVIDIA API key and model access
"""

import os
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA

# Load environment variables
load_dotenv("variables.env")

def test_nvidia_api():
    """Test NVIDIA API access"""
    
    print("🧪 Testing NVIDIA API access...")
    
    # Set API key
    api_key = "ed99e0cc-5fc0-4f9d-b3cc-c0dfba6ef53a"
    model_name = "llama-3.3-nemotron-super-49b-v1.5"
    
    try:
        # Initialize the model
        llm = ChatNVIDIA(
            model=model_name,
            temperature=0,
            api_key=api_key
        )
        
        print(f"✅ Successfully initialized model: {model_name}")
        
        # Test a simple query
        response = llm.invoke("Hello! Can you confirm you're working?")
        
        print(f"✅ Model response: {response.content[:100]}...")
        print("🎉 NVIDIA API is working correctly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing NVIDIA API: {e}")
        return False

if __name__ == "__main__":
    success = test_nvidia_api()
    exit(0 if success else 1) 