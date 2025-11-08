"""
List available Gemini models
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    print("\n" + "="*60)
    print("📋 Available Gemini Models:")
    print("="*60)
    
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"\n✅ {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description[:100]}...")
    
    print("\n" + "="*60)
else:
    print("❌ GEMINI_API_KEY not set!")
