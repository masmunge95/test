import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_ANON_KEY")

supabase_client: Client = create_client(url, key)

class SupabaseService:
    def __init__(self):
        self.client = supabase_client
    
    async def create_user_profile(self, user_id: str, email: str):
        try:
            result = self.client.table("users").insert({
                "id": user_id,
                "email": email,
                "is_premium": False
            }).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating user profile: {e}")
            return None
    
    async def get_user_profile(self, user_id: str):
        try:
            result = self.client.table("users").select("*").eq("id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return None
    
    async def save_quiz(self, quiz_data: dict):
        try:
            result = self.client.table("quizzes").insert(quiz_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error saving quiz: {e}")
            return None
    
    async def save_flashcard_set(self, flashcard_data: dict):
        try:
            result = self.client.table("flashcard_sets").insert(flashcard_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error saving flashcard set: {e}")
            return None
    
    async def save_progress(self, progress_data: dict):
        try:
            result = self.client.table("progress").insert(progress_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error saving progress: {e}")
            return None
    
    async def get_user_progress(self, user_id: str):
        try:
            result = self.client.table("progress").select("*").eq("user_id", user_id).order("completed_at", desc=True).execute()
            return result.data
        except Exception as e:
            print(f"Error getting user progress: {e}")
            return []
    
    async def save_payment(self, payment_data: dict):
        try:
            result = self.client.table("payments").insert(payment_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error saving payment: {e}")
            return None
    
    async def update_user_premium(self, user_id: str, is_premium: bool):
        try:
            result = self.client.table("users").update({"is_premium": is_premium}).eq("id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error updating user premium status: {e}")
            return None

supabase_service = SupabaseService()