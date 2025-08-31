import os
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class InstaSendService:
    def __init__(self):
        self.api_key = os.getenv("INSTASEND_API_KEY")
        self.api_token = os.getenv("INSTASEND_API_TOKEN")
        self.base_url = "https://sandbox.intasend.com/api/v1"  # Use sandbox for testing
        self.headers = {
            "Content-Type": "application/json",
            "X-IntaSend-Public-API-Key": self.api_key,
        }
    
    async def initiate_mpesa_payment(self, amount: float, phone_number: str, email: str) -> Dict:
        """Initiate M-Pesa payment via InstaSend"""
        try:
            payload = {
                "public_key": self.api_key,
                "amount": amount,
                "currency": "KES",
                "phone_number": phone_number,
                "email": email,
                "api_ref": f"EDU_{phone_number}_{int(amount*100)}",
                "method": "M-PESA"
            }
            
            response = requests.post(
                f"{self.base_url}/payment/mpesa-stk-push/",
                json=payload,
                headers=self.headers
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "message": "Payment initiated successfully"
                }
            else:
                return {
                    "success": False,
                    "error": response.json(),
                    "message": "Failed to initiate payment"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Payment service error"
            }
    
    async def check_payment_status(self, transaction_id: str) -> Dict:
        """Check payment status"""
        try:
            response = requests.get(
                f"{self.base_url}/payment/status/{transaction_id}/",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to check payment status"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

payment_service = InstaSendService()