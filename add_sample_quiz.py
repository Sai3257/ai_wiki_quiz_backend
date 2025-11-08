"""
Add sample quiz data to test the database
"""

from database import SessionLocal, Quiz
import json

def add_sample_quizzes():
    """Add sample quiz records"""
    db = SessionLocal()
    
    try:
        # Sample Quiz 1
        quiz1 = Quiz(
            url="https://en.wikipedia.org/wiki/Python_(programming_language)",
            title="Python Programming Quiz",
            scraped_content="Python is a high-level, interpreted programming language...",
            full_quiz_data=json.dumps({
                "questions": [
                    {
                        "question": "What is Python?",
                        "options": ["A programming language", "A snake", "A framework", "A database"],
                        "correct_answer": "A programming language"
                    },
                    {
                        "question": "Who created Python?",
                        "options": ["Guido van Rossum", "James Gosling", "Bjarne Stroustrup", "Dennis Ritchie"],
                        "correct_answer": "Guido van Rossum"
                    }
                ]
            })
        )
        
        # Sample Quiz 2
        quiz2 = Quiz(
            url="https://en.wikipedia.org/wiki/Artificial_intelligence",
            title="Artificial Intelligence Quiz",
            scraped_content="Artificial intelligence (AI) is intelligence demonstrated by machines...",
            full_quiz_data=json.dumps({
                "questions": [
                    {
                        "question": "What does AI stand for?",
                        "options": ["Artificial Intelligence", "Automated Integration", "Advanced Interface", "None"],
                        "correct_answer": "Artificial Intelligence"
                    }
                ]
            })
        )
        
        db.add(quiz1)
        db.add(quiz2)
        db.commit()
        
        print("✅ Sample quizzes added successfully!")
        print(f"   - Quiz 1: {quiz1.title} (ID: {quiz1.id})")
        print(f"   - Quiz 2: {quiz2.title} (ID: {quiz2.id})")
        
        # Show all quizzes
        all_quizzes = db.query(Quiz).all()
        print(f"\n📊 Total quizzes in database: {len(all_quizzes)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("➕ Adding sample quiz data...\n")
    add_sample_quizzes()
    print("\n💡 Run 'python view_database.py' to see all data!")
