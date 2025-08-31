from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from services.supabase_service import supabase_service, supabase_client

router = APIRouter()

class SignUpRequest(BaseModel):
    email: str
    password: str

class SignInRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
async def sign_up(request: SignUpRequest):
    try:
        # Create user with Supabase Auth
        auth_response = supabase_client.auth.sign_up({
            "email": request.email,
            "password": request.password
        })
        
        if auth_response.user:
            # Create user profile
            profile = await supabase_service.create_user_profile(
                auth_response.user.id, 
                request.email
            )
            
            return {
                "success": True,
                "user": auth_response.user,
                "session": auth_response.session,
                "message": "User created successfully"
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to create user")
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/signin")
async def sign_in(request: SignInRequest):
    try:
        auth_response = supabase_client.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        
        if auth_response.user and auth_response.session:
            return {
                "success": True,
                "user": auth_response.user,
                "session": auth_response.session,
                "access_token": auth_response.session.access_token
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
            
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/signout")
async def sign_out():
    try:
        supabase_client.auth.sign_out()
        return {"success": True, "message": "Signed out successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))