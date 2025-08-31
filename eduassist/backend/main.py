from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv
from routes import auth, quiz, flashcard, progress, payment
from services.supabase_service import supabase_client

load_dotenv()

app = FastAPI(title="EduAssist API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        # Verify token with Supabase
        response = supabase_client.auth.get_user(credentials.credentials)
        if response.user:
            return response.user
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(quiz.router, prefix="/quiz", tags=["quiz"])
app.include_router(flashcard.router, prefix="/flashcard", tags=["flashcard"])
app.include_router(progress.router, prefix="/progress", tags=["progress"])
app.include_router(payment.router, prefix="/payment", tags=["payment"])

@app.get("/")
async def root():
    return {"message": "EduAssist API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))