"""
Test script to demonstrate the AI Wiki Quiz Generator API
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def test_root():
    """Test root endpoint"""
    print("\n" + "="*60)
    print("Testing Root Endpoint: GET /")
    print("="*60)
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")


def test_generate_quiz():
    """Test quiz generation endpoint"""
    print("\n" + "="*60)
    print("Testing Quiz Generation: POST /generate_quiz")
    print("="*60)
    
    # Use a real Wikipedia URL for testing
    data = {
        "wikipedia_url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "num_questions": 5
    }
    
    print(f"Request Data:\n{json.dumps(data, indent=2)}")
    print("\nGenerating quiz... (this may take a few seconds)")
    
    response = requests.post(f"{BASE_URL}/generate_quiz", json=data)
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Quiz Generated Successfully!")
        print(f"Quiz ID: {result['id']}")
        print(f"Title: {result['title']}")
        print(f"Summary: {result['summary'][:150]}...")
        print(f"Number of Questions: {len(result['questions'])}")
        print(f"\nFirst Question:")
        print(f"  Q: {result['questions'][0]['question']}")
        print(f"  Options: {result['questions'][0]['options']}")
        print(f"  Answer: {result['questions'][0]['correct_answer']}")
        return result['id']
    else:
        print(f"❌ Error: {response.text}")
        return None


def test_get_history():
    """Test get history endpoint"""
    print("\n" + "="*60)
    print("Testing Quiz History: GET /history")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/history")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        history = response.json()
        print(f"\n✅ Found {len(history)} quiz(es) in history")
        for quiz in history:
            print(f"\n  Quiz ID: {quiz['id']}")
            print(f"  Title: {quiz['title']}")
            print(f"  URL: {quiz['wikipedia_url']}")
            print(f"  Created: {quiz['created_at']}")
    else:
        print(f"❌ Error: {response.text}")


def test_get_quiz_by_id(quiz_id):
    """Test get quiz by ID endpoint"""
    print("\n" + "="*60)
    print(f"Testing Get Quiz by ID: GET /quiz/{quiz_id}")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/quiz/{quiz_id}")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        quiz = response.json()
        print(f"\n✅ Quiz Retrieved Successfully!")
        print(f"Title: {quiz['title']}")
        print(f"Summary: {quiz['summary'][:150]}...")
        print(f"Questions: {len(quiz['questions'])}")
        
        print(f"\nAll Questions:")
        for i, q in enumerate(quiz['questions'], 1):
            print(f"\n  {i}. {q['question']}")
            for opt in q['options']:
                marker = "✓" if opt == q['correct_answer'] else " "
                print(f"     [{marker}] {opt}")
    else:
        print(f"❌ Error: {response.text}")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧠 AI Wiki Quiz Generator - API Test Suite")
    print("="*60)
    
    try:
        # Test 1: Root endpoint
        test_root()
        
        # Test 2: Get history (should be empty initially)
        test_get_history()
        
        # Test 3: Generate a quiz
        quiz_id = test_generate_quiz()
        
        # Test 4: Get history again (should have 1 quiz)
        test_get_history()
        
        # Test 5: Get quiz by ID
        if quiz_id:
            test_get_quiz_by_id(quiz_id)
        
        print("\n" + "="*60)
        print("✅ All tests completed!")
        print("="*60)
        print("\n📖 API Documentation: http://127.0.0.1:8000/docs")
        print("📖 ReDoc: http://127.0.0.1:8000/redoc")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API server.")
        print("Make sure the server is running with: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
