from fastapi import APIRouter
import redis
from cachetools import TTLCache
from app.schemas.user import UserCreate, SendOtp
from app.utils.user import generate_otp

router = APIRouter()

# r = redis.Redis(host='localhost', port=6379, decode_responses=True)

otp_cache = TTLCache(maxsize=1000, ttl=300)  # 5 mins TTL

@router.post("/send-otp")
async def send_otp( data: SendOtp):
    """Send OTP to the user's phone number.
    Args:
        send_otp (SendOtp): The phone number to which the OTP will be sent.
    Returns:
        dict: A message indicating that the OTP has been sent.
    """
    phone = data.phone
    otp = generate_otp()
    otp_cache[phone] = otp  # Store OTP in cache
    # r.setex(f"otp:{phone}", 300, otp)  # Store OTP for 5 minutes
    print(f"OTP for {phone}: {otp}")  # Simulate sending OTP
    return {
        'success': True,
        'message': f"OTP sent to {phone}",
    }
