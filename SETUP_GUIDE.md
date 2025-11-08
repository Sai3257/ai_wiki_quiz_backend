# 🚀 Quick Setup Guide - AI Wiki Quiz Generator Backend

## ✅ What's Been Created

The backend is fully set up with the following structure:

```
backend/
├── main.py                    # FastAPI app with all endpoints
├── database.py                # SQLAlchemy database configuration
├── models.py                  # Database models & Pydantic schemas
├── scraper.py                 # Wikipedia scraping functionality
├── llm_quiz_generator.py      # AI quiz generation (Gemini + fallback)
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
├── test_api.py               # API test script
├── .gitignore                # Git ignore rules
└── README.md                 # Detailed documentation
```

## 🎯 Quick Start (3 Steps)

### 1️⃣ Activate Virtual Environment

The virtual environment is already created. Just activate it:

```bash
cd backend
.\venv\Scripts\activate
```

### 2️⃣ Start the Server

```bash
uvicorn main:app --reload
```

The server will start at: **http://127.0.0.1:8000**

### 3️⃣ Test the API

Open your browser and visit:
- **Swagger UI:** http://127.0.0.1:8000/docs
- **Test Script:** Run `python test_api.py` in another terminal

## 📡 Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| POST | `/generate_quiz` | Generate quiz from Wikipedia URL |
| GET | `/history` | Get all saved quizzes |
| GET | `/quiz/{quiz_id}` | Get specific quiz by ID |
| DELETE | `/quiz/{quiz_id}` | Delete a quiz |

## 🧪 Test Results

✅ **All tests passed successfully!**

The test script demonstrated:
- ✅ Root endpoint working
- ✅ Quiz generation from Wikipedia (Python article)
- ✅ Database storage (SQLite)
- ✅ History retrieval
- ✅ Quiz retrieval by ID

**Sample Output:**
- Quiz ID: 1
- Title: Python (programming language)
- Questions: 5 generated
- Database: `quiz_history.db` created automatically

## 🔑 Optional: Add Gemini API Key

Currently using **fallback quiz generator** (rule-based).

To use **AI-powered quiz generation**:

1. Get a Gemini API key from: https://makersuite.google.com/app/apikey
2. Edit `.env` file:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```
3. Restart the server

## 🌐 CORS Configuration

CORS is pre-configured for React frontends:
- `http://localhost:5173` (Vite)
- `http://localhost:3000` (Create React App)

## 📦 Dependencies Installed

All dependencies are already installed in the virtual environment:
- ✅ FastAPI
- ✅ Uvicorn
- ✅ SQLAlchemy
- ✅ Pydantic
- ✅ BeautifulSoup4
- ✅ Requests
- ✅ Python-dotenv
- ✅ LangChain Core
- ✅ LangChain Google GenAI

## 🗄️ Database

- **Type:** SQLite
- **File:** `quiz_history.db` (auto-created)
- **Location:** `backend/quiz_history.db`
- **Switchable:** Can change to MySQL by updating `DATABASE_URL` in `.env`

## 📝 Next Steps

1. **Frontend Integration:** The backend is ready for React frontend integration
2. **API Key:** Add Gemini API key for AI-powered quizzes
3. **Customization:** Modify quiz generation logic in `llm_quiz_generator.py`
4. **Database:** Switch to MySQL/PostgreSQL for production

## 🐛 Troubleshooting

**Server not starting?**
- Make sure virtual environment is activated
- Check if port 8000 is available

**Database errors?**
- Delete `quiz_history.db` and restart server
- It will be recreated automatically

**Import errors?**
- Ensure all dependencies are installed: `pip install -r requirements.txt`

## 📚 Documentation

- **Full README:** See `README.md` for detailed documentation
- **API Docs:** http://127.0.0.1:8000/docs (when server is running)
- **Test Script:** Run `python test_api.py` to see all endpoints in action

---

**Status:** ✅ Backend is fully functional and tested!
