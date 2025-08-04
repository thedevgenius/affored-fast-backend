import pytz

TIMEZONE = pytz.timezone("Asia/Kolkata")

# Configuration for JWT tokens
SECRET_KEY = "52f5ff754a8cda946baaf933c01f89a622299f6a16d796f0f85ae232226b67bf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30  # 30 days
