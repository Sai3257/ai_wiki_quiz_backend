# 📡 API Usage Examples

## Base URL
```
http://127.0.0.1:8000
```

## 1. Get API Information

**Request:**
```bash
curl http://127.0.0.1:8000/
```

**Response:**
```json
{
  "message": "AI Wiki Quiz Generator API",
  "version": "1.0.0",
  "endpoints": {
    "generate_quiz": "POST /generate_quiz",
    "get_history": "GET /history",
    "get_quiz": "GET /quiz/{quiz_id}"
  }
}
```

---

## 2. Generate Quiz from Wikipedia

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/generate_quiz \
  -H "Content-Type: application/json" \
  -d "{\"wikipedia_url\": \"https://en.wikipedia.org/wiki/Artificial_intelligence\", \"num_questions\": 5}"
```

**PowerShell:**
```powershell
$body = @{
    wikipedia_url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    num_questions = 5
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/generate_quiz" -Method Post -Body $body -ContentType "application/json"
```

**Response:**
```json
{
  "id": 1,
  "wikipedia_url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
  "title": "Artificial intelligence",
  "summary": "Artificial intelligence (AI) is intelligence demonstrated by machines...",
  "questions": [
    {
      "question": "What is artificial intelligence?",
      "options": [
        "Intelligence by machines",
        "Human intelligence",
        "Natural intelligence",
        "None of the above"
      ],
      "correct_answer": "Intelligence by machines",
      "explanation": "AI is intelligence demonstrated by machines."
    }
  ],
  "created_at": "2024-01-01T12:00:00"
}
```

---

## 3. Get Quiz History

**Request:**
```bash
curl http://127.0.0.1:8000/history
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/history" -Method Get
```

**Response:**
```json
[
  {
    "id": 1,
    "wikipedia_url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "title": "Artificial intelligence",
    "created_at": "2024-01-01T12:00:00"
  },
  {
    "id": 2,
    "wikipedia_url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "title": "Python (programming language)",
    "created_at": "2024-01-01T12:05:00"
  }
]
```

---

## 4. Get Quiz by ID

**Request:**
```bash
curl http://127.0.0.1:8000/quiz/1
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/quiz/1" -Method Get
```

**Response:**
```json
{
  "id": 1,
  "wikipedia_url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
  "title": "Artificial intelligence",
  "summary": "Artificial intelligence (AI) is intelligence demonstrated by machines...",
  "questions": [
    {
      "question": "What is artificial intelligence?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option A",
      "explanation": "Explanation here..."
    }
  ],
  "created_at": "2024-01-01T12:00:00"
}
```

---

## 5. Delete Quiz

**Request:**
```bash
curl -X DELETE http://127.0.0.1:8000/quiz/1
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/quiz/1" -Method Delete
```

**Response:**
```json
{
  "message": "Quiz 1 deleted successfully"
}
```

---

## 🐍 Python Example

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Generate a quiz
response = requests.post(
    f"{BASE_URL}/generate_quiz",
    json={
        "wikipedia_url": "https://en.wikipedia.org/wiki/Machine_learning",
        "num_questions": 7
    }
)

quiz = response.json()
print(f"Quiz ID: {quiz['id']}")
print(f"Title: {quiz['title']}")
print(f"Questions: {len(quiz['questions'])}")

# Get history
history = requests.get(f"{BASE_URL}/history").json()
print(f"Total quizzes: {len(history)}")

# Get specific quiz
quiz_detail = requests.get(f"{BASE_URL}/quiz/{quiz['id']}").json()
print(f"Retrieved: {quiz_detail['title']}")
```

---

## 🌐 JavaScript/Fetch Example

```javascript
const BASE_URL = "http://127.0.0.1:8000";

// Generate a quiz
async function generateQuiz() {
  const response = await fetch(`${BASE_URL}/generate_quiz`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      wikipedia_url: "https://en.wikipedia.org/wiki/JavaScript",
      num_questions: 5,
    }),
  });
  
  const quiz = await response.json();
  console.log("Quiz ID:", quiz.id);
  console.log("Title:", quiz.title);
  return quiz;
}

// Get history
async function getHistory() {
  const response = await fetch(`${BASE_URL}/history`);
  const history = await response.json();
  console.log("Total quizzes:", history.length);
  return history;
}

// Get quiz by ID
async function getQuiz(id) {
  const response = await fetch(`${BASE_URL}/quiz/${id}`);
  const quiz = await response.json();
  console.log("Quiz:", quiz.title);
  return quiz;
}
```

---

## 📝 Request Parameters

### POST /generate_quiz

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| wikipedia_url | string | Yes | - | Valid Wikipedia article URL |
| num_questions | integer | No | 5 | Number of questions (5-10) |

### Validation Rules

- `wikipedia_url` must contain "wikipedia.org/wiki/"
- `num_questions` must be between 5 and 10
- URL must be accessible and contain valid content

---

## ⚠️ Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid Wikipedia URL. Must be a valid Wikipedia article URL."
}
```

### 404 Not Found
```json
{
  "detail": "Quiz with ID 999 not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Failed to generate quiz: [error message]"
}
```

---

## 🔍 Testing Tips

1. **Use Swagger UI:** Visit http://127.0.0.1:8000/docs for interactive testing
2. **Use ReDoc:** Visit http://127.0.0.1:8000/redoc for API documentation
3. **Use test_api.py:** Run `python test_api.py` for automated testing
4. **Use Postman:** Import the endpoints for visual testing

---

## 📚 Popular Wikipedia URLs for Testing

- Python: https://en.wikipedia.org/wiki/Python_(programming_language)
- AI: https://en.wikipedia.org/wiki/Artificial_intelligence
- Machine Learning: https://en.wikipedia.org/wiki/Machine_learning
- JavaScript: https://en.wikipedia.org/wiki/JavaScript
- React: https://en.wikipedia.org/wiki/React_(JavaScript_library)
- FastAPI: https://en.wikipedia.org/wiki/FastAPI
- Database: https://en.wikipedia.org/wiki/Database
- API: https://en.wikipedia.org/wiki/API
