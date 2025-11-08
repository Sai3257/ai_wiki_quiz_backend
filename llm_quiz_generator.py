import os
import json
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

# Try to import Google GenAI directly
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


def generate_quiz_with_gemini(content: str, title: str, num_questions: int = 5) -> Dict:
    """
    Generate quiz using Google Gemini AI model.
    
    Args:
        content: Wikipedia article content
        title: Article title
        num_questions: Number of questions to generate (5-10)
        
    Returns:
        Dictionary containing 'summary' and 'questions'
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or not GENAI_AVAILABLE:
        return generate_fallback_quiz(content, title, num_questions)
    
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize model (using gemini-2.5-flash - stable and fast)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Create prompt for quiz generation
        prompt = f"""You are an expert quiz generator. Based on the following Wikipedia article, create a quiz with exactly {num_questions} multiple-choice questions.

Article Title: {title}

Article Content:
{content[:4000]}

Generate a JSON response with the following structure:
{{
    "summary": "A concise 2-3 sentence summary of the article",
    "questions": [
        {{
            "question": "The question text",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "The correct option text (must match one of the options exactly)",
            "explanation": "Brief explanation of why this is correct"
        }}
    ]
}}

Requirements:
- Generate exactly {num_questions} questions
- Each question must have exactly 4 options
- Questions should cover different aspects of the article
- Make questions challenging but fair
- Ensure correct_answer matches one of the options exactly
- Provide clear explanations

Return ONLY the JSON, no additional text."""
        
        # Generate quiz
        response = model.generate_content(prompt)
        response_text = response.text
        
        # Extract JSON from response (handle markdown code blocks)
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        quiz_data = json.loads(response_text)
        
        # Validate structure
        if "summary" not in quiz_data or "questions" not in quiz_data:
            raise ValueError("Invalid quiz structure from AI")
        
        return quiz_data
        
    except Exception as e:
        print(f"Error using Gemini API: {str(e)}")
        return generate_fallback_quiz(content, title, num_questions)


def generate_fallback_quiz(content: str, title: str, num_questions: int = 5) -> Dict:
    """
    Fallback quiz generator when Gemini API is not available.
    Creates a simple rule-based quiz from the content.
    
    Args:
        content: Wikipedia article content
        title: Article title
        num_questions: Number of questions to generate
        
    Returns:
        Dictionary containing 'summary' and 'questions'
    """
    # Generate simple summary (first 2 sentences)
    sentences = content.split('.')
    summary = '. '.join(sentences[:2]).strip() + '.'
    
    # Generate simple questions based on content
    questions = []
    
    # Extract some key facts from content
    paragraphs = content.split('\n\n')
    
    for i in range(min(num_questions, len(paragraphs))):
        if i < len(paragraphs) and len(paragraphs[i]) > 100:
            # Create a simple question from the paragraph
            para = paragraphs[i][:200]
            
            questions.append({
                "question": f"What is mentioned about {title} in the article?",
                "options": [
                    f"Information from paragraph {i+1}",
                    "This is not mentioned in the article",
                    "The article discusses something else",
                    "None of the above"
                ],
                "correct_answer": f"Information from paragraph {i+1}",
                "explanation": f"This information is found in the article content about {title}."
            })
    
    # If we don't have enough questions, add generic ones
    while len(questions) < num_questions:
        questions.append({
            "question": f"What is the main topic of this article?",
            "options": [
                title,
                "Something else",
                "Not specified",
                "Multiple topics"
            ],
            "correct_answer": title,
            "explanation": f"The article is about {title}."
        })
    
    return {
        "summary": summary if summary else f"This article is about {title}.",
        "questions": questions[:num_questions]
    }


def generate_quiz(content: str, title: str, num_questions: int = 5) -> Dict:
    """
    Main function to generate quiz. Tries Gemini first, falls back if needed.
    
    Args:
        content: Wikipedia article content
        title: Article title
        num_questions: Number of questions to generate (5-10)
        
    Returns:
        Dictionary containing 'summary' and 'questions'
    """
    return generate_quiz_with_gemini(content, title, num_questions)
