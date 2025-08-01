from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from cachetools import TTLCache
from app.schemas.user import UserCreate, SendOtp
from app.utils.user import generate_otp
from app.database import get_db 
from app.models.user import User  # Assuming you have a User model defined
from app.utils.auth import create_access_token, create_refresh_token, SECRET_KEY, ALGORITHM
from app.dependencies.auth import get_current_user

router = APIRouter()
otp_cache = TTLCache(maxsize=1000, ttl=300)  # 5 mins TTL

@router.post("/send-otp")
async def send_otp(data: SendOtp):
    """Send OTP to the user's phone number."""

    phone = data.phone
    otp = generate_otp()
    otp_cache[phone] = otp  # Store OTP in cache
    print(f"OTP for {phone}: {otp}")  # Simulate sending OTP
    return {
        'success': True,
        'message': f"OTP sent to {phone}",
    }


@router.post("/verify-otp")
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

    db_user = db.query(User).filter_by(phone=phone).first()
    if not db_user:
        db_user = User(phone=phone)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    del otp_cache[phone]

    access_token = create_access_token(data={"sub": phone})
    refresh_token = create_refresh_token(data={"sub": phone})
    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'success': True,
            'message': "OTP verified successfully",
            'data': {
                'user_id': str(db_user.id),
                'phone': db_user.phone,
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


@router.get("/refresh-token")
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