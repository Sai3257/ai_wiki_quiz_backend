from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import json
from typing import List
import os
import uvicorn

from database import get_db, init_db, Quiz
from models import QuizCreate, QuizResponse, QuizSummary, QuizGenerationRequest, QuestionSchema
from scraper import scrape_wikipedia, validate_wikipedia_url
from llm_quiz_generator import generate_quiz

# -----------------------------------------------------------
# Initialize FastAPI app
# -----------------------------------------------------------
app = FastAPI(
    title="AI Wiki Quiz Generator API",
    description="Generate quizzes from Wikipedia articles using AI",
    version="1.0.0"
)

# -----------------------------------------------------------
# Configure CORS for React frontend
# -----------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------
# Initialize database on startup
# -----------------------------------------------------------
@app.on_event("startup")
def startup_event():
    init_db()
    print("✅ Database initialized successfully")

# -----------------------------------------------------------
# Root endpoint
# -----------------------------------------------------------
@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "AI Wiki Quiz Generator API",
        "version": "1.0.0",
        "endpoints": {
            "generate_quiz": "POST /generate_quiz",
            "get_history": "GET /history",
            "get_quiz": "GET /quiz/{quiz_id}"
        }
    }

# -----------------------------------------------------------
# Generate quiz endpoint
# -----------------------------------------------------------
@app.post("/generate_quiz", response_model=QuizResponse)
def generate_quiz_endpoint(
    request: QuizGenerationRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a quiz from a Wikipedia URL.
    """
    try:
        # Validate URL
        if not validate_wikipedia_url(request.wikipedia_url):
            raise HTTPException(
                status_code=400,
                detail="Invalid Wikipedia URL. Must be a valid Wikipedia article URL."
            )

        # Scrape Wikipedia article
        try:
            article_data = scrape_wikipedia(request.wikipedia_url)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to scrape Wikipedia article: {str(e)}"
            )

        # Generate quiz using AI
        try:
            quiz_data = generate_quiz(
                content=article_data["content"],
                title=article_data["title"],
                num_questions=request.num_questions
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate quiz: {str(e)}"
            )

        # Save to database
        quiz_db = Quiz(
            url=request.wikipedia_url,
            title=article_data["title"],
            scraped_content=article_data["content"][:1000],
            full_quiz_data=json.dumps({
                "summary": quiz_data["summary"],
                "questions": quiz_data["questions"]
            })
        )

        db.add(quiz_db)
        db.commit()
        db.refresh(quiz_db)

        # Return response
        return QuizResponse(
            id=quiz_db.id,
            wikipedia_url=quiz_db.url,
            title=quiz_db.title,
            summary=quiz_data["summary"],
            questions=[QuestionSchema(**q) for q in quiz_data["questions"]],
            created_at=quiz_db.date_generated
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# -----------------------------------------------------------
# Get quiz history
# -----------------------------------------------------------
@app.get("/history", response_model=List[QuizSummary])
def get_quiz_history(db: Session = Depends(get_db)):
    """Get all saved quiz summaries (without full questions)."""
    try:
        quizzes = db.query(Quiz).order_by(Quiz.date_generated.desc()).all()
        return [
            QuizSummary(
                id=quiz.id,
                wikipedia_url=quiz.url,
                title=quiz.title,
                created_at=quiz.date_generated
            )
            for quiz in quizzes
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve quiz history: {str(e)}"
        )

# -----------------------------------------------------------
# Get quiz by ID
# -----------------------------------------------------------
@app.get("/quiz/{quiz_id}", response_model=QuizResponse)
def get_quiz_by_id(quiz_id: int, db: Session = Depends(get_db)):
    """Get full quiz details by ID."""
    try:
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise HTTPException(status_code=404, detail=f"Quiz with ID {quiz_id} not found")

        quiz_data = json.loads(quiz.full_quiz_data)
        return QuizResponse(
            id=quiz.id,
            wikipedia_url=quiz.url,
            title=quiz.title,
            summary=quiz_data.get("summary", ""),
            questions=[QuestionSchema(**q) for q in quiz_data.get("questions", [])],
            created_at=quiz.date_generated
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve quiz: {str(e)}"
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
