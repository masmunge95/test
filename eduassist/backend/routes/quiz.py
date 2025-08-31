from fastapi import APIRouter, HTTPException, Depends
from models.database import QuizRequest, Quiz
from services.ai_service import ai_service
from services.supabase_service import supabase_service
from main import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/generate")
async def generate_quiz(request: QuizRequest, current_user = Depends(get_current_user)):
    try:
        # Check if user is premium for more than 5 questions
        user_profile = await supabase_service.get_user_profile(current_user.id)
        if request.num_questions > 5 and not user_profile.get("is_premium", False):
            raise HTTPException(status_code=403, detail="Premium subscription required for more than 5 questions")
        
        # Generate quiz using AI
        questions = await ai_service.generate_quiz(request.topic, request.num_questions)
        
        # Save quiz to database
        quiz_data = {
            "user_id": current_user.id,
            "topic": request.topic,
            "questions": questions,
            "created_at": datetime.now().isoformat()
        }
        
        saved_quiz = await supabase_service.save_quiz(quiz_data)
        
        return {
            "success": True,
            "quiz": {
                "id": saved_quiz["id"] if saved_quiz else None,
                "topic": request.topic,
                "questions": questions
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit/{quiz_id}")
async def submit_quiz(quiz_id: str, answers: dict, current_user = Depends(get_current_user)):
    try:
        # Calculate score
        user_answers = answers.get("answers", [])
        
        # Get quiz from database to check correct answers
        # For now, we'll simulate scoring
        total_questions = len(user_answers)
        correct_answers = sum(1 for i, answer in enumerate(user_answers) if answer == 0)  # Assuming first option is always correct for demo
        score = int((correct_answers / total_questions) * 100) if total_questions > 0 else 0
        
        # Save progress
        progress_data = {
            "user_id": current_user.id,
            "topic": answers.get("topic", "Unknown"),
            "activity_type": "quiz",
            "score": score,
            "completed_at": datetime.now().isoformat()
        }
        
        await supabase_service.save_progress(progress_data)
        
        return {
            "success": True,
            "score": score,
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "percentage": score
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))