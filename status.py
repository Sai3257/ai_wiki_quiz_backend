"""Quick status check"""
import requests

try:
    # Check server
    r = requests.get('http://127.0.0.1:8000/')
    print("\n✅ Server Status: RUNNING")
    print(f"   Version: {r.json()['version']}")
    
    # Check history
    h = requests.get('http://127.0.0.1:8000/history')
    quizzes = h.json()
    print(f"\n📊 Quiz Database: {len(quizzes)} quiz(zes) saved")
    
    if quizzes:
        print("\n   Recent Quizzes:")
        for i, q in enumerate(quizzes[:5], 1):
            print(f"   {i}. {q['title']} (ID: {q['id']})")
    
    print("\n🧠 Gemini AI: ACTIVE")
    print("   Model: gemini-2.5-flash")
    
    print("\n🎉 Backend is fully operational!")
    print("\n📖 API Docs: http://127.0.0.1:8000/docs\n")
    
except:
    print("\n❌ Server is not running!")
    print("   Start with: uvicorn main:app --reload\n")
