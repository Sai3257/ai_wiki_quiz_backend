"""
Script to view database structure and data
"""

from sqlalchemy import inspect, text
from database import engine, SessionLocal, Quiz
from datetime import datetime

def view_database_structure():
    """View all tables and their columns"""
    print("=" * 60)
    print("📊 DATABASE STRUCTURE")
    print("=" * 60)
    
    inspector = inspect(engine)
    
    # Get all table names
    tables = inspector.get_table_names()
    print(f"\n✅ Total Tables: {len(tables)}")
    
    for table_name in tables:
        print(f"\n📋 Table: {table_name}")
        print("-" * 60)
        
        # Get columns for each table
        columns = inspector.get_columns(table_name)
        for col in columns:
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            print(f"  • {col['name']:20} {str(col['type']):20} {nullable}")

def view_all_quizzes():
    """View all quiz records in the database"""
    print("\n" + "=" * 60)
    print("📚 ALL QUIZ RECORDS")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        quizzes = db.query(Quiz).all()
        
        if not quizzes:
            print("\n⚠️  No quizzes found in database (empty table)")
        else:
            print(f"\n✅ Total Quizzes: {len(quizzes)}\n")
            
            for quiz in quizzes:
                print(f"{'─' * 60}")
                print(f"ID:              {quiz.id}")
                print(f"Title:           {quiz.title}")
                print(f"URL:             {quiz.url}")
                print(f"Date Generated:  {quiz.date_generated}")
                print(f"Scraped Content: {quiz.scraped_content[:100] if quiz.scraped_content else 'None'}...")
                print(f"Quiz Data:       {quiz.full_quiz_data[:100]}...")
                print()
                
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

def add_sample_quiz():
    """Add a sample quiz to test"""
    print("\n" + "=" * 60)
    print("➕ ADDING SAMPLE QUIZ")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        sample_quiz = Quiz(
            url="https://en.wikipedia.org/wiki/Artificial_intelligence",
            title="Artificial Intelligence Quiz",
            scraped_content="Artificial intelligence (AI) is intelligence demonstrated by machines...",
            full_quiz_data='{"questions": [{"q": "What is AI?", "options": ["A", "B", "C", "D"], "answer": "A"}]}'
        )
        
        db.add(sample_quiz)
        db.commit()
        db.refresh(sample_quiz)
        
        print(f"✅ Sample quiz added with ID: {sample_quiz.id}")
        
    except Exception as e:
        print(f"❌ Error adding sample quiz: {e}")
        db.rollback()
    finally:
        db.close()

def get_database_stats():
    """Get database statistics"""
    print("\n" + "=" * 60)
    print("📈 DATABASE STATISTICS")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        total_quizzes = db.query(Quiz).count()
        
        print(f"\n✅ Total Quizzes: {total_quizzes}")
        
        if total_quizzes > 0:
            latest_quiz = db.query(Quiz).order_by(Quiz.date_generated.desc()).first()
            oldest_quiz = db.query(Quiz).order_by(Quiz.date_generated.asc()).first()
            
            print(f"📅 Latest Quiz: {latest_quiz.title} ({latest_quiz.date_generated})")
            print(f"📅 Oldest Quiz: {oldest_quiz.title} ({oldest_quiz.date_generated})")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

def main():
    """Main function to run all checks"""
    print("\n🔍 DATABASE INSPECTION TOOL")
    print("=" * 60)
    
    # 1. View database structure
    view_database_structure()
    
    # 2. View all quizzes
    view_all_quizzes()
    
    # 3. Get statistics
    get_database_stats()
    
    # 4. Ask if user wants to add sample data
    print("\n" + "=" * 60)
    print("💡 TIP: Run this script anytime to view your database!")
    print("=" * 60)

if __name__ == "__main__":
    main()
