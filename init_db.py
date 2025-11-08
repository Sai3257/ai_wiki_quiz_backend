"""
Database initialization script
Run this script to create all database tables
"""

from database import Base, engine, init_db

if __name__ == "__main__":
    print("Initializing database tables...")
    try:
        init_db()
        print("✅ Database tables created successfully!")
        print("Tables created:")
        print("  - quizzes")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        print("\nMake sure:")
        print("  1. PostgreSQL is running")
        print("  2. .env file exists with correct credentials")
        print("  3. Database 'quizdb' exists (or create it first)")
