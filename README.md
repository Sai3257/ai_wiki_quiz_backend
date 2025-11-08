# AI Wiki Quiz Generator - Backend

A FastAPI backend that scrapes Wikipedia articles and generates quizzes using AI (LangChain + Gemini).

## 🚀 Quick Start

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Edit the `.env` file and add your Gemini API key:

```env
DATABASE_URL=sqlite:///./quiz_history.db
GEMINI_API_KEY=your_api_key_here
```

**Note:** If you don't have a Gemini API key, the system will use a fallback quiz generator.

### 5. Run the Server

```bash
uvicorn main:app --reload
```

The server will start at: **http://127.0.0.1:8000**

### 6. Access API Documentation

Open your browser and visit:
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## 📡 API Endpoints

### `POST /generate_quiz`
Generate a quiz from a Wikipedia URL.

**Request Body:**
```json
{
  "wikipedia_url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
  "num_questions": 5
}
```

**Response:**
```json
{
  "id": 1,
  "wikipedia_url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
  "title": "Python (programming language)",
  "summary": "Python is a high-level programming language...",
  "questions": [
    {
      "question": "What is Python?",
      "options": ["A snake", "A programming language", "A framework", "A database"],
      "correct_answer": "A programming language",
      "explanation": "Python is a high-level programming language."
    }
  ],
  "created_at": "2024-01-01T12:00:00"
}
```

### `GET /history`
Get all saved quiz summaries.

**Response:**
```json
[
  {
    "id": 1,
    "wikipedia_url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "title": "Python (programming language)",
    "created_at": "2024-01-01T12:00:00"
  }
]
```

### `GET /quiz/{quiz_id}`
Get full quiz details by ID.

**Response:** Same as `/generate_quiz`

### `DELETE /quiz/{quiz_id}`
Delete a quiz by ID.

## 🗄️ Database

- **Type:** SQLite (default)
- **File:** `quiz_history.db` (auto-created)
- **Switchable:** Can be changed to MySQL by updating `DATABASE_URL` in `.env`

## 🧩 Project Structure

```
backend/
├── main.py                    # FastAPI app with endpoints
├── database.py                # SQLAlchemy database setup
├── models.py                  # SQLAlchemy & Pydantic models
├── scraper.py                 # Wikipedia scraper
├── llm_quiz_generator.py      # AI quiz generator (Gemini + fallback)
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🔧 Technologies Used

- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation
- **BeautifulSoup4** - Web scraping
- **Google Gemini 2.5 Flash** - AI model for quiz generation (via direct API)

## 🌐 CORS Configuration

CORS is enabled for:
- `http://localhost:5173` (Vite/React)
- `http://localhost:3000` (Create React App)

## 📝 Notes

- The database file (`quiz_history.db`) is automatically created on first run
- If no Gemini API key is provided, a fallback generator creates simple quizzes
- All Wikipedia scraping respects rate limits and uses proper headers
- Content is limited to 5000 characters to avoid token limits

## 🐛 Troubleshooting

**Issue:** Module not found errors
- **Solution:** Make sure virtual environment is activated and dependencies are installed

**Issue:** Database errors
- **Solution:** Delete `quiz_history.db` and restart the server to recreate it

**Issue:** Wikipedia scraping fails
- **Solution:** Check internet connection and ensure URL is a valid Wikipedia article

## 📄 License

MIT License
