from fastapi import APIRouter, HTTPException, Depends
from models.database import PaymentRequest
from services.payment_service import payment_service
from services.supabase_service import supabase_service
from main import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/initiate")
async def initiate_payment(request: PaymentRequest, current_user = Depends(get_current_user)):
    try:
        # Initiate payment with InstaSend
        payment_result = await payment_service.initiate_mpesa_payment(
            amount=request.amount,
            phone_number=request.phone_number,
            email=request.email
        )
        
        if payment_result["success"]:
            # Save payment record
            payment_data = {
                "user_id": current_user.id,
                "amount": request.amount,
                "currency": "KES",
                "status": "pending",
                "instasend_transaction_id": payment_result["data"].get("id", ""),
                "created_at": datetime.now().isoformat()
            }
            
            await supabase_service.save_payment(payment_data)
            
            return {
                "success": True,
                "payment_data": payment_result["data"],
                "message": "Payment initiated successfully"
            }
        else:
            raise HTTPException(status_code=400, detail=payment_result["message"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{transaction_id}")
async def check_payment_status(transaction_id: str, current_user = Depends(get_current_user)):
    try:
        # Check payment status with InstaSend
        status_result = await payment_service.check_payment_status(transaction_id)
        
        if status_result["success"]:
            payment_data = status_result["data"]
            
            # If payment is successful, update user to premium
            if payment_data.get("status") == "completed":
                await supabase_service.update_user_premium(current_user.id, True)
            
            return {
                "success": True,
                "payment_status": payment_data
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to check payment status")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/plans")
async def get_premium_plans():
    return {
        "success": True,
        "plans": [
            {
                "name": "Premium Monthly",
                "price": 500,  # KES
                "currency": "KES",
                "features": [
                    "Unlimited quiz questions",
                    "Unlimited flashcards",
                    "Advanced AI models",
                    "Progress analytics",
                    "Priority support"
                ],
                "duration": "1 month"
            },
            {
                "name": "Premium Yearly",
                "price": 5000,  # KES
                "currency": "KES",
                "features": [
                    "Unlimited quiz questions",
                    "Unlimited flashcards",
                    "Advanced AI models",
                    "Progress analytics",
                    "Priority support"
                ],
                "duration": "1 year",
                "discount": "17% off"
            }
        ]
    }