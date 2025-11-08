"""
Check if environment variables are loaded correctly
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("\n" + "="*60)
print("🔍 Environment Variables Check")
print("="*60)

# Check if .env file exists
env_file = ".env"
if os.path.exists(env_file):
    print(f"✅ .env file exists")
else:
    print(f"❌ .env file not found!")

# Check DATABASE_URL
db_url = os.getenv("DATABASE_URL")
if db_url:
    print(f"✅ DATABASE_URL: {db_url}")
else:
    print(f"⚠️  DATABASE_URL not set")

# Check GEMINI_API_KEY (masked for security)
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    if len(api_key) > 10:
        masked = api_key[:8] + "..." + api_key[-4:]
        print(f"✅ GEMINI_API_KEY: {masked} (length: {len(api_key)})")
    else:
        print(f"⚠️  GEMINI_API_KEY is too short: {len(api_key)} characters")
else:
    print(f"❌ GEMINI_API_KEY not set or empty!")

# Check Google GenAI availability
try:
    import google.generativeai as genai
    print(f"✅ Google GenerativeAI is installed")
except ImportError as e:
    print(f"❌ Google GenerativeAI not available: {e}")

print("="*60)

# Test if we can initialize Gemini
if api_key and len(api_key) > 10:
    print("\n🧪 Testing Gemini API connection...")
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Try a simple test
        response = model.generate_content("Say 'Hello' if you can read this.")
        print(f"✅ Gemini API is working!")
        print(f"   Response: {response.text[:100]}")
        
    except Exception as e:
        print(f"❌ Error connecting to Gemini API:")
        print(f"   {str(e)}")
else:
    print("\n⚠️  Cannot test Gemini API - API key not properly set")

print("="*60 + "\n")
