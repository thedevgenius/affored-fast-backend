from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Response, Depends, Request
from jose import JWTError, jwt
from app.core.config import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from app.core.database import get_db
from fastapi.responses import JSONResponse
from cachetools import TTLCache
from app.users.models import User 
from .schemas import SendOtp, UserCreate
from .utils import generate_otp, create_access_token, create_refresh_token 
from .service import create_user
from app.core.dependencies import get_current_user

router = APIRouter()
otp_cache = TTLCache(maxsize=100, ttl=300)  # Cache for OTPs with a TTL of 5 minutes
time_cache = TTLCache(maxsize=100, ttl=60)  # Cache for time-based data if needed

@router.post('/send-otp', name='Request OTP')
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


@router.post('/verify-otp', name='Verify OTP')
async def verify_otp(data: UserCreate, response: Response, db: Session = Depends(get_db)):
    """Verify the OTP sent to the user's phone number."""

    phone = data.phone
    otp = data.otp

    cached_otp = otp_cache.get(phone)
    if not cached_otp:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'success': False, 'message': "OTP expired"},
        )

    if cached_otp != otp:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'success': False, 'message': "Invalid OTP"},
        )

    user = await create_user(phone, db)

    del otp_cache[phone]

    access_token = create_access_token(data={"sub": phone})
    refresh_token = create_refresh_token(data={"sub": phone})

    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'success': True,
            'message': "OTP verified successfully",
            'data': {
                'user_id': str(user.id),
                'phone': user.phone,
                'access_token': access_token,
            }
        }
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
    )

    return response


@router.get("/refresh-token", name='Generate New Access Token')
async def refresh_token(request: Request):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phone = payload.get("sub")
        new_access = create_access_token({"sub": phone})
        return {"access_token": new_access}
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid refresh token")
    

@router.get("/profile")
async def get_profile(current_user: str = Depends(get_current_user)):
    return {"user": current_user}