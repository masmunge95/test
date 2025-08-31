from fastapi import APIRouter, HTTPException, Depends
from services.supabase_service import supabase_service
from main import get_current_user

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_data(current_user = Depends(get_current_user)):
    try:
        # Get user progress
        progress_data = await supabase_service.get_user_progress(current_user.id)
        
        # Calculate statistics
        total_quizzes = len([p for p in progress_data if p["activity_type"] == "quiz"])
        total_flashcard_sessions = len([p for p in progress_data if p["activity_type"] == "flashcard"])
        
        quiz_scores = [p["score"] for p in progress_data if p["activity_type"] == "quiz" and p["score"]]
        average_quiz_score = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0
        
        # Get unique topics studied
        topics_studied = list(set([p["topic"] for p in progress_data]))
        
        # Recent activity (last 10)
        recent_activity = progress_data[:10]
        
        return {
            "success": True,
            "dashboard": {
                "total_quizzes": total_quizzes,
                "total_flashcard_sessions": total_flashcard_sessions,
                "average_quiz_score": round(average_quiz_score, 1),
                "topics_studied": len(topics_studied),
                "recent_activity": recent_activity,
                "topics_list": topics_studied
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_progress_history(current_user = Depends(get_current_user)):
    try:
        progress_data = await supabase_service.get_user_progress(current_user.id)
        
        return {
            "success": True,
            "history": progress_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))