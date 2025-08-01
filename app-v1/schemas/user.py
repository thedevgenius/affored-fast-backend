from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    phone: str
    otp: str

class SendOtp(BaseModel):
    phone: str = Field(..., description="Phone number to send OTP to")