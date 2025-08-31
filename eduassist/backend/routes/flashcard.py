from fastapi import APIRouter, HTTPException, Depends
from models.database import FlashcardRequest
from services.ai_service import ai_service
from services.supabase_service import supabase_service
from main import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/generate")
async def generate_flashcards(request: FlashcardRequest, current_user = Depends(get_current_user)):
    try:
        # Check if user is premium for more than 10 cards
        user_profile = await supabase_service.get_user_profile(current_user.id)
        if request.num_cards > 10 and not user_profile.get("is_premium", False):
            raise HTTPException(status_code=403, detail="Premium subscription required for more than 10 flashcards")
        
        # Generate flashcards using AI
        flashcards = await ai_service.generate_flashcards(request.topic, request.num_cards)
        
        # Save flashcard set to database
        flashcard_data = {
            "user_id": current_user.id,
            "topic": request.topic,
            "flashcards": flashcards,
            "created_at": datetime.now().isoformat()
        }
        
        saved_set = await supabase_service.save_flashcard_set(flashcard_data)
        
        return {
            "success": True,
            "flashcard_set": {
                "id": saved_set["id"] if saved_set else None,
                "topic": request.topic,
                "flashcards": flashcards
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/complete/{topic}")
async def complete_flashcard_session(topic: str, session_data: dict, current_user = Depends(get_current_user)):
    try:
        # Save progress
        progress_data = {
            "user_id": current_user.id,
            "topic": topic,
            "activity_type": "flashcard",
            "score": session_data.get("cards_reviewed", 0),
            "completed_at": datetime.now().isoformat()
        }
        
        await supabase_service.save_progress(progress_data)
        
        return {
            "success": True,
            "message": "Flashcard session completed",
            "cards_reviewed": session_data.get("cards_reviewed", 0)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))