from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: str
    email: str
    created_at: datetime
    is_premium: bool = False

class Quiz(BaseModel):
    id: Optional[str] = None
    user_id: str
    topic: str
    questions: List[dict]
    score: Optional[int] = None
    completed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

class Flashcard(BaseModel):
    id: Optional[str] = None
    user_id: str
    topic: str
    front: str
    back: str
    difficulty: Optional[str] = "medium"
    created_at: Optional[datetime] = None

class Progress(BaseModel):
    id: Optional[str] = None
    user_id: str
    topic: str
    activity_type: str  # 'quiz' or 'flashcard'
    score: Optional[int] = None
    completed_at: datetime

class Payment(BaseModel):
    id: Optional[str] = None
    user_id: str
    amount: float
    currency: str
    status: str
    instasend_transaction_id: str
    created_at: Optional[datetime] = None

class QuizRequest(BaseModel):
    topic: str
    num_questions: int = 5

class FlashcardRequest(BaseModel):
    topic: str
    num_cards: int = 10

class PaymentRequest(BaseModel):
    amount: float
    phone_number: str
    email: str