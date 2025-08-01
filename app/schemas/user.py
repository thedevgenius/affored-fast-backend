from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    phone: str
    otp: int

class SendOtp(BaseModel):
    phone: str = Field(..., description="Phone number to send OTP to")