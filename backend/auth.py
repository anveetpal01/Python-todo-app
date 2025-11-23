# this file is security guard it has 2 main items
'''
1. Hashing: encrypt password
2. Token(JWT): create token
'''

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from pwdlib import PasswordHash
from typing import Optional
from dotenv import load_dotenv
import os
load_dotenv()

# Secret_key: ye wo chaabi hai jisse token sign hoga. real app mein ise environment variable me rakhte hai
SECRET_KEY = "5E65E38B64A55F2B21A7433DB7353"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# password hash
pwd_context = PasswordHash.recommended()

# 1. password verify
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 2. hash password during signup
def get_password_hash(password):
    return pwd_context.hash(password)

# 3. create token after success login
def create_access_token(data: dict, expires_delta: Optional[timedelta]=None):
    to_encode = data.copy()

    #set expiry time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    # generate token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt