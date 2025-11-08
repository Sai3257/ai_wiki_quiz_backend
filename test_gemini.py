"""
Test script to verify Gemini API integration
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def test_gemini_quiz_generation():
    """Test quiz generation with Gemini API"""
    print("\n" + "="*70)
    print("🧠 Testing AI-Powered Quiz Generation with Gemini API")
    print("="*70)
    
    # Use a Wikipedia article about AI
    data = {
        "wikipedia_url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "num_questions": 6
    }
    
    print(f"\n📝 Request:")
    print(f"   URL: {data['wikipedia_url']}")
    print(f"   Questions: {data['num_questions']}")
    print("\n⏳ Generating quiz with Gemini AI... (this may take 10-20 seconds)")
    
    try:
        response = requests.post(f"{BASE_URL}/generate_quiz", json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n" + "="*70)
            print("✅ SUCCESS! Quiz Generated with Gemini AI")
            print("="*70)
            
            print(f"\n📊 Quiz Details:")
            print(f"   Quiz ID: {result['id']}")
            print(f"   Title: {result['title']}")
            print(f"   Created: {result['created_at']}")
            
            print(f"\n📝 Summary:")
            print(f"   {result['summary']}")
            
            print(f"\n❓ Generated {len(result['questions'])} Questions:\n")
            
            for i, q in enumerate(result['questions'], 1):
                print(f"   {i}. {q['question']}")
                print(f"      Options:")
                for j, opt in enumerate(q['options'], 1):
                    marker = "✓" if opt == q['correct_answer'] else " "
                    print(f"         [{marker}] {chr(64+j)}. {opt}")
                print(f"      💡 Explanation: {q.get('explanation', 'N/A')}")
                print()
            
            print("="*70)
            print("🎉 Gemini API is working perfectly!")
            print("="*70)
            
            # Check if it's using fallback or real AI
            if "Information from paragraph" in result['questions'][0]['question']:
                print("\n⚠️  WARNING: Still using fallback generator!")
                print("   Please check your GEMINI_API_KEY in .env file")
            else:
                print("\n✨ Using AI-powered quiz generation!")
            
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"   {response.text}")
            
    except requests.exceptions.Timeout:
        print("\n⏱️  Request timed out. Gemini API might be slow or unavailable.")
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to server. Make sure it's running!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


def check_api_status():
    """Check if API is running"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ API Server is running")
            return True
    except:
        print("❌ API Server is not running!")
        print("   Start it with: uvicorn main:app --reload")
        return False


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🔍 Checking API Status...")
    print("="*70)
    
    if check_api_status():
        test_gemini_quiz_generation()
    
    print("\n" + "="*70)
    print("📖 View API Documentation: http://127.0.0.1:8000/docs")
    print("="*70 + "\n")
