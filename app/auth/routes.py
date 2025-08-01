from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from cachetools import TTLCache
from .schemas import SendOtp
from .utils import generate_otp

router = APIRouter()
otp_cache = TTLCache(maxsize=100, ttl=300)  # Cache for OTPs with a TTL of 5 minutes
time_cache = TTLCache(maxsize=100, ttl=60)  # Cache for time-based data if needed

@router.post('/send-otp')
async def send_otp(data: SendOtp):
    """Send OTP to the user's phone number."""

    phone = data.phone
    if not phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number is required"
        )
    
    # Check if the user has requested an OTP in the last 60 seconds
    if phone in time_cache:
        last_request_time = time_cache.get(phone)
        if last_request_time and (datetime.now() - last_request_time).total_seconds() < 60:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please wait before requesting another OTP."
            )
        
    # Generate and cache the OTP
    otp = generate_otp()
    otp_cache[phone] = otp
    time_cache[phone] = datetime.now()
    print(f"OTP for {phone}: {otp}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "OTP sent successfully"
        }
    )