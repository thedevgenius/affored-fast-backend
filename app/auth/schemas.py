from pydantic import BaseModel, Field

class SendOtp(BaseModel):
    phone: str = Field(..., description="Phone number to send OTP to")

class UserCreate(BaseModel):
    phone: str
    otp: str