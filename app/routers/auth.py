from fastapi import APIRouter

router = APIRouter()

@router.get("/send-otp")
async def send_otp():
    return {"message": "OTP send endpoint"}