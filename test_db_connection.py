"""
Test script to verify PostgreSQL database connection and setup
"""

import sys
from sqlalchemy import text
from database import engine, SessionLocal, init_db, Quiz
from datetime import datetime

def test_connection():
    """Test basic database connection"""
    print("=" * 60)
    print("🔍 Testing PostgreSQL Database Connection")
    print("=" * 60)
    
    try:
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print("✅ Database connection successful!")
            print(f"📊 PostgreSQL Version: {version[:50]}...")
            return True
    except Exception as e:
        print("❌ Database connection failed!")
        print(f"Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("  1. Make sure PostgreSQL is running")
        print("  2. Check your .env file has correct credentials")
        print("  3. Verify the database 'quizdb' exists")
        print("  4. Run: CREATE DATABASE quizdb; (in PostgreSQL)")
        return False

def test_table_creation():
    """Test table creation"""
    print("\n" + "=" * 60)
    print("🔨 Creating Database Tables")
    print("=" * 60)
    
    try:
        init_db()
        print("✅ Tables created successfully!")
        
        # Check if table exists
        with engine.connect() as connection:
            result = connection.execute(text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public' AND table_name = 'quizzes';"
            ))
            if result.fetchone():
                print("✅ 'quizzes' table verified in database")
            return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def test_crud_operations():
    """Test Create, Read operations"""
    print("\n" + "=" * 60)
    print("🧪 Testing CRUD Operations")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        # Create a test quiz
        test_quiz = Quiz(
            url="https://en.wikipedia.org/wiki/Python_(programming_language)",
            title="Python Programming Language Quiz",
            scraped_content="Python is a high-level programming language...",
            full_quiz_data='{"questions": [{"question": "What is Python?", "answer": "A programming language"}]}'
        )
        
        db.add(test_quiz)
        db.commit()
        db.refresh(test_quiz)
        
        print(f"✅ Created test quiz with ID: {test_quiz.id}")
        print(f"   Title: {test_quiz.title}")
        print(f"   Date: {test_quiz.date_generated}")
        
        # Read the quiz back
        retrieved_quiz = db.query(Quiz).filter(Quiz.id == test_quiz.id).first()
        if retrieved_quiz:
            print(f"✅ Successfully retrieved quiz: {retrieved_quiz.title}")
        
        # Count total quizzes
        total_quizzes = db.query(Quiz).count()
        print(f"📊 Total quizzes in database: {total_quizzes}")
        
        # Clean up test data
        db.delete(test_quiz)
        db.commit()
        print("✅ Test data cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ CRUD operations failed: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def main():
    """Run all tests"""
    print("\n🚀 Starting Database Tests...\n")
    
    # Test 1: Connection
    if not test_connection():
        print("\n❌ Cannot proceed without database connection")
        sys.exit(1)
    
    # Test 2: Table Creation
    if not test_table_creation():
        print("\n❌ Cannot proceed without tables")
        sys.exit(1)
    
    # Test 3: CRUD Operations
    if not test_crud_operations():
        print("\n❌ CRUD operations failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED! Database is ready to use!")
    print("=" * 60)
    print("\n✅ Your database setup is working correctly!")
    print("✅ You can now use it in your FastAPI application")

if __name__ == "__main__":
    main()
