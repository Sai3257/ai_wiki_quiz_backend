from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional


# Pydantic Schemas
class QuestionSchema(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None
    difficulty: Optional[str] = "medium"  # easy, medium, hard

    class Config:
        from_attributes = True


class QuizCreate(BaseModel):
    wikipedia_url: str

    class Config:
        from_attributes = True


class QuizResponse(BaseModel):
    id: int
    wikipedia_url: str
    title: str
    summary: str
    questions: List[QuestionSchema]
    related_topics: Optional[List[str]] = []
    created_at: datetime

    class Config:
        from_attributes = True


class QuizSummary(BaseModel):
    id: int
    wikipedia_url: str
    title: str
    created_at: datetime

    class Config:
        from_attributes = True


class QuizGenerationRequest(BaseModel):
    wikipedia_url: str
    num_questions: int = Field(default=5, ge=5, le=10, description="Number of questions (5-10)")

    class Config:
        from_attributes = True
